
import grpc
from ChangeBalance.ISpotChangeBalanceService_pb2_grpc import SpotChangeBalanceServiceStub as ChangeBalanceStub
from ChangeBalance.ISpotChangeBalanceService_pb2 import ManualChangeBalanceGrpcRequest
from random import randint

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
