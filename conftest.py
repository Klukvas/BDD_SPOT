from API import Wallet, Auth
import pytest

import settings

import grpc
from ChangeBalance.ISpotChangeBalanceService_pb2_grpc import SpotChangeBalanceServiceStub as ChangeBalanceStub
from ChangeBalance.ISpotChangeBalanceService_pb2 import ManualChangeBalanceGrpcRequest
from random import randint
import json
from requests_pkcs12 import get, post

def changeBalance(clientId, amount, walletId, asset, BrokerId='jetwallet') -> None or str:
    try:
        channel = grpc.insecure_channel("change-balance-gateways.spot-services.svc.cluster.local:80")
        client = ChangeBalanceStub(channel)
        transactionId = randint(10**5, 10**25)
        request = ManualChangeBalanceGrpcRequest(
            TransactionId = f"{transactionId}",
            ClientId      = f"{clientId}",
            WalletId      = f"{walletId}",
            Amount        = amount,
            AssetSymbol   = f"{asset}",
            Comment       =  "BaseTests",
            BrokerId      =  f"{BrokerId}",
            Officer       = "BaseTests",
            Agent         =  {
                "ApplicationName": "BaseTests",
                "ApplicationEnvInfo": "BaseTests"
            }

        )
    except Exception as err:
        print(f'Can not make request object')
    try:
        response = client.ManualChangeBalance(request)
        try:
            result = response.Result
            return result
        except Exception as err:
            print(f'Error with parse response in changeBalance function.\n{err}')
            return None
    except Exception as err:
        print(f'Error with sending request in changeBalance function.\n{err}')
        return None


@pytest.fixture(scope="session", autouse=True)
def upd_balance(): 
    for item in settings.balance_asssets.items():
        bl_change_result = changeBalance(
            settings.client_Id,
            item[1],
            f'SP-{settings.client_Id}',
            item[0]
        )
        assert bl_change_result != None, 'Ошибка при пополнении баланса'

if __name__ == '__main__':
    changeBalance(
        'e66866aa8012430aa0d3302565333779',
        0.2,
        f'SP-e66866aa8012430aa0d3302565333779',
        'BNB'
    )