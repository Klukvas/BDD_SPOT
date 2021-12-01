from API import Auth, Wallet
import pytest
import settings
from ChangeBalance.change_balance import changeBalance
from time import sleep

@pytest.fixture
def auth():
    def get_tokens(email, password):
        token = Auth(email, password, 1).authenticate()
        assert type(token) == list
        return token[0]
    return get_tokens



def pytest_bdd_before_scenario(request, feature, scenario):
    print(f'\n\nStarted new scenario:{scenario.name}\nFeature: {feature.name}\n')
    if scenario.name in ['Make a swap with fixed True', 'Make a swap with fixed False', 'Make a transfer by phone', 'Make a transfer by address']:
        print('call upd balance')
        assets_for_update = []
        token = Auth(settings.email, settings.password, 1).authenticate()
        balances = Wallet(1).balances(token[0])
        for item in balances:
            if item['assetId'] in settings.balance_asssets.keys():
                if item['balance'] < settings.balance_asssets[item['assetId']]:
                    correct_amount = settings.balance_asssets[item['assetId']] - item['balance'] 
                    assets_for_update.append(
                        [
                            item['assetId'],
                            correct_amount
                        ]
                    )
                elif item['balance'] > settings.balance_asssets[item['assetId']]:
                    correct_amount = (item['balance'] - settings.balance_asssets[item['assetId']] ) * -1
                    assets_for_update.append(
                        [
                            item['assetId'],
                            correct_amount
                        ]
                    )
        for item in assets_for_update:
                bl_change_result = changeBalance(
                    settings.client_Id,
                    item[1],
                    f'SP-{settings.client_Id}',
                    item[0]
                )
                assert bl_change_result != None, 'Ошибка при пополнении баланса'

def pytest_bdd_after_scenario(request, feature, scenario):
    sleep(10)

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args) :
    print(f'Step: {step} of scenario: {scenario.name} PASSED')

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step: {step} of scenario: {scenario} FAILED\nException: {exception}')

