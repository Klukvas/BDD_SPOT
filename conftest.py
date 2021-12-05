from API import Auth, Wallet
import pytest
import settings
from ChangeBalance.change_balance import changeBalance
from time import sleep

@pytest.fixture
def auth():
    def get_tokens(email, password):
        token = Auth(email, password).authenticate()
        assert type(token) == list
        return token[0]
    return get_tokens



def pytest_bdd_before_scenario(request, feature, scenario):
    print(f'\n\nStarted new scenario:{scenario.name}\nFeature: {feature.name}\n')
    if scenario.name in ['Make a swap with fixed True', 'Make a swap with fixed False', 'Make a transfer by phone', 
        'Make a transfer by address', 'Transfer(waiting for user)', 'Internal withdrawal']:
        print('call upd balance')
        assets_for_update = []
        if scenario.name in ['Transfer(waiting for user)', 'Internal withdrawal']:
            token = Auth(settings.template_email, settings.password).authenticate()
            client_Id = settings.template_clientId
        else:
            token = Auth(settings.email, settings.password).authenticate()                    
            client_Id = settings.client_Id

        balances = Wallet().balances(token[0])
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
            assert bl_change_result != None, 'Ошибка при пополнении баланса'

def pytest_bdd_after_scenario(request, feature, scenario):
    sleep(10)

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args) :
    print(f'Step: {step} of scenario: {scenario.name} PASSED')

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step: {step} of scenario: {scenario.name} FAILED\nException: {exception}')

