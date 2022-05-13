from API.Auth import Auth
from API.Wallet import Wallet
from API.Verify import Verify
from API.GmailApi import GmailApi
from API.OpenVPN import OpenVPN
from API.WalletHistory import WalletHistory

import pytest
import settings
from GRPC.ChangeBalance.change_balance import changeBalance
from time import sleep
from Database.db import get_db_client
from datetime import datetime
from Logger import Logger

log = Logger().custom_logger()


@pytest.fixture()
def find_record_in_op():
    def inner(token: str, search_by: dict, asset: str = '', time_compare: int = 6000, research_count=10, sleep_for=10):
        # search_by: {"operationId": '123', "operationType": 4, "status": 0}
        # time_compare: difference btw date in history and today - in seconds
        wh_obj = WalletHistory()
        filtered_data = []
        for _ in range(research_count):
            if asset:
                response = wh_obj.operations_history(token, asset)['response']
            else:
                response = wh_obj.operations_history(token)['response']
            assert 'data' in response.keys(), \
                f"Expected that 'data' key will be in response. But response is: {response}"
            today = datetime.utcnow()
            filtered_data = [
                record for record in response['data'] if all(
                    [
                        record[filter_name] == filter_value,
                        (today - datetime.strptime(record['timeStamp'], "%Y-%m-%dT%H:%M:%S.%f")).seconds < time_compare
                    ]
                    for filter_name, filter_value in search_by.items()
                )
            ]
            if filtered_data:
                log.info(f"Filtered data by params: {search_by} was found")
                break
            sleep(sleep_for)
        return filtered_data

    return inner


@pytest.fixture(scope='session')
def db_connection():
    if settings.db_connection_string:
        return get_db_client()
    else:
        raise ConnectionError('db_connection_string is not set')


@pytest.fixture(scope='session')
def openvpn_client():
    return OpenVPN()


@pytest.fixture()
def register():
    def inner(email, password, *args):
        log.info(f"Register by: {email} with password: {password}")
        response = Auth(email, password).register()['response']['data']
        Verify().verify_email(response['token'], '000000')
        return response

    return inner


@pytest.fixture
def auth():
    def get_tokens(email, password, specific_case=False):
        auth_data = Auth(email, password).authenticate(specific_case)
        log.info(f"Log in by: {email}")
        return auth_data

    return get_tokens


@pytest.fixture
def create_temporary_template():
    def inner(body, name):
        with open(f"{name}.html", 'w+') as f:
            f.writelines(body)
            f.flush()
            f.seek(0)
            data = f.read()
        return data

    return inner


def clear_emailbox():
    log.info(f"Start clearning email box")
    gmail_api = GmailApi()
    gmail_api.generateCreds()
    gmail_api.generateService()
    gmail_api._deleteParsedMessage()


def change_balance_by_scenario():
    assets_for_update = []
    token = Auth(
        settings.base_user_data_email,
        settings.base_user_data_password
    ).authenticate()['response']['data']['token']
    client_Id = settings.base_user_data_client_id
    log.info(f"Check balance for user: {settings.base_user_data_email}")
    balances = Wallet().balances(token)['response']['data']['balances']
    assets_not_in_balance = [
        asset
        for asset in settings.balance_asssets.keys()
        if asset not in [
            asset['assetId']
            for asset in balances
            if asset['assetId'] in settings.balance_asssets.keys()
        ]
    ]
    if len(assets_not_in_balance):
        for item in assets_not_in_balance:
            assets_for_update.append(
                [
                    item,
                    settings.balance_asssets[item]
                ]
            )
    if len(balances):
        for item in balances:
            if item['assetId'] in settings.balance_asssets.keys():
                if item['balance'] < settings.balance_asssets[item['assetId']]:
                    correct_amount = settings.balance_asssets[item['assetId']] - item['balance']
                    if correct_amount > 0.0001:
                        assets_for_update.append(
                            [
                                item['assetId'],
                                correct_amount
                            ]
                        )
                elif item['balance'] > settings.balance_asssets[item['assetId']]:
                    correct_amount = (item['balance'] - settings.balance_asssets[item['assetId']]) * -1
                    if correct_amount * -1 > 0.0001:
                        assets_for_update.append(
                            [
                                item['assetId'],
                                correct_amount
                            ]
                        )
    else:
        for item in settings.balance_asssets.items():
            assets_for_update.append(
                item[0],
                item[1]
            )
    for item in assets_for_update:
        bl_change_result = changeBalance(
            client_Id,
            item[1],
            f'SP-{client_Id}',
            item[0]
        )
        assert bl_change_result, 'Ошибка при пополнении баланса'


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "autoinvest: mark test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "signalr: mark test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "email_test: mark test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "test: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "emails: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "transfer: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "circle_all: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "circle_cards: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "simplex: asd"
    )
    config.addinivalue_line(
        "markers", "circle_bank_accounts: mark1 test to run only on named environment"
    )

    config.addinivalue_line(
        "markers", "campaign: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "swap: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "auth: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "candels: mark1 test to run only on named environment"
    )


def pytest_bdd_before_scenario(request, feature, scenario):
    log.info(f'Started new scenario:{scenario.name}\nFeature: {feature.name}')
    if feature.name == 'Emails receive':
        clear_emailbox()
    if scenario.name in settings.scenarios_with_balance_change:
        change_balance_by_scenario()


def pytest_bdd_after_scenario(request, feature, scenario):
    sleep(2)


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    log.info(f'Step: {step} of scenario: {scenario.name} PASSED')


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    log.error(f'Step: {step} of scenario: {scenario.name} FAILED\nException: {exception}')
