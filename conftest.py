from API import Auth, Wallet
import pytest
import settings
from ChangeBalance.change_balance import changeBalance
from time import sleep

@pytest.fixture
def auth():
    token = Auth(settings.email, settings.password, 1).authenticate()
    assert type(token) == list
    return token[0]



def pytest_bdd_before_scenario(request, feature, scenario):
    if scenario.name == 'Make a swap':
        assets_for_update = []
        token = Auth(settings.email, settings.password, 1).authenticate()
        balances = Wallet(1).balances(token[0])
        for item in balances:
            if item['assetId'] in settings.balance_asssets.keys():
                if item['balance'] < settings.balance_asssets[item['assetId']]:
                    assets_for_update.append(
                        [
                            item['assetId'],
                            balances[item['assetId']]
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
    if scenario.name == 'Make a swap':
        sleep(10)