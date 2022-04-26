from API.Auth import Auth
from API.Wallet import Wallet
from API.Verify import Verify
import pytest
import settings
from GRPC.ChangeBalance.change_balance import changeBalance
from time import sleep
from Database.db import get_db_client
from API.GmailApi import GmailApi


@pytest.fixture(scope='session')
def db_connection():
    if settings.db_connection_string:
        return get_db_client()
    else:
        assert False, 'db_connection_string is not set'


@pytest.fixture()
def register():
    def inner(email, password, *args):
        print(f"Register by: {email} with password: {password}")
        response = Auth(email, password).register()
        Verify().verify_email(response['token'], '000000')
        return response
    return inner


@pytest.fixture
def auth():
    def get_tokens(email, password, specific_case=False):
        auth_data = Auth(email, password).authenticate(specific_case)
        print(f"Log in by: {email}")
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


@pytest.fixture(scope='session', autouse=True)
def clear_emailbox():
    gmail_api = GmailApi()
    gmail_api.generateCreds()
    gmail_api.generateService()
    gmail_api._deleteParsedMessage()


def pytest_configure(config):

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
        "markers", "swap: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "auth: mark1 test to run only on named environment"
    )
    config.addinivalue_line(
        "markers", "candels: mark1 test to run only on named environment"
    )

def pytest_bdd_before_scenario(request, feature, scenario):
    print(f'\n\nStarted new scenario:{scenario.name}\nFeature: {feature.name}\n')
    if scenario.name in ['Make a swap', 'Make a deposit by simplex', 'Make a transfer by phone', 'Make a internalWithdrawal',
        'Make a transfer by address', 'Transfer(waiting for user)', 'Internal withdrawal', 'Success withdrawal or transfer && deposit']:
        assets_for_update = []
        if scenario.name in ['Transfer(waiting for user)', 'Internal withdrawal', 'Success withdrawal or transfer && deposit']:
            token = Auth(
                settings.template_tests_email,
                settings.template_tests_password
            ).authenticate()['token']
            client_Id = settings.template_tests_client_id
        else:
            token = Auth(
                settings.me_tests_email,
                settings.me_tests_password
            ).authenticate()['token']
            client_Id = settings.me_tests_client_id

        balances = Wallet().balances(token)
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
                        print(f"assets_for_update: {assets_for_update}")
                    elif item['balance'] > settings.balance_asssets[item['assetId']]:
                        correct_amount = (item['balance'] - settings.balance_asssets[item['assetId']] ) * -1
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
            print(f"item[1]: {item[1]}\titem[0]: {item[0]}")
            bl_change_result = changeBalance(
                client_Id,
                item[1],
                f'SP-{client_Id}',
                item[0]
            )
            assert bl_change_result != None, 'Ошибка при пополнении баланса'

def pytest_bdd_after_scenario(request, feature, scenario):
    sleep(10)

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args) :
    print(f'Step: {step} of scenario: {scenario.name} PASSED')

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step: {step} of scenario: {scenario.name} FAILED\nException: {exception}')

