
import traceback
import grpc
from random import randint
# from new_change_balance.Change_Balance__pb2_grpc import SpotChangeBalanceServiceStub as ChangeBalanceStub
# from new_change_balance.Change_Balance__pb2 import ManualChangeBalanceGrpcRequest
# from new_change_balance.Helper_pb2_grpc import GrpcHelperServiceStub
# from new_change_balance.Helper_pb2 import Data_String

from GRPC.ChangeBalance import ChangeBalance_pb2 as ch_bal_pb2, \
    ChangeBalance_pb2_grpc as ch_bal_grpc
from GRPC.Helper import Helper_pb2 as help_pb, \
    Helper_pb2_grpc as help_grpc
# from ChangeBalance.new import (
#     Helper_pb2_grpc as help_grpc,
#     ChangeBalance_pb2 as ch_bal_pb2,
#     ChangeBalance_pb2_grpc as ch_bal_grpc,
#     Helper_pb2 as help_pb
# )

from GRPC.Helper import helper

def changeBalance(clientId, amount, walletId, asset, BrokerId='jetwallet') -> None or str:
    decimal_amount = helper.string_to_decimal(amount)
    if not decimal_amount:
        return None
    else:
        try:
            channel = grpc.insecure_channel("change-balance-gateways.spot-services.svc.cluster.local:80")
            try:
                client = ch_bal_grpc.SpotChangeBalanceServiceStub(channel)
            except Exception:
                traceback.print_exc()
                return None
            transactionId = randint(10**5, 10**25)
            print(decimal_amount)
            request = ch_bal_pb2.ManualChangeBalanceGrpcRequest(
                TransactionId = f"{transactionId}",
                ClientId      = f"{clientId}",
                WalletId      = f"{walletId}",
                Amount        = decimal_amount,
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
            print(f'Can not make request object\nErr: {err}')
            return None
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
if __name__ == '__main__':
    r = changeBalance("217eff37bb0249efa5ffdd239ef12f70", 1.022, "SP-217eff37bb0249efa5ffdd239ef12f70", "LTC")
    print(f"Resp: {r}")
# def get_amount(amount):
#     channel = grpc.insecure_channel("change-balance-gateways.spot-services.svc.cluster.local:80")
#     client = GrpcHelperServiceStub(channel)
#     decimal_amount = {}
#     try:
#         request = Data_String(
#             Value = str(amount)
#         )
#     except Exception as err:
#         print(f"Err with creating request\nErr: {err}")
#         return None
#     try:
#         response = client.StringToDecimal(request)
        
#         if response.Value.lo:
#             decimal_amount['lo'] = str(response.Value.lo)
#         else:
#             decimal_amount['lo'] = "0"

#         if response.Value.hi:
#             decimal_amount['hi'] = response.Value.hi
#         else:
#             decimal_amount['hi'] = 0
        
#         if response.Value.signScale:
#             decimal_amount['signScale'] = response.Value.signScale
#         else:
#             decimal_amount['signScale'] = 0
#         print(decimal_amount)
#     except Exception as err:
#         print(f"Err with sending request\nErr: {err}")
#         return None


# def changeBalance(clientId, amount, walletId, asset, BrokerId='jetwallet') -> None or str:
#     decimal_amount = get_amount(amount)
#     if not decimal_amount:
#         return None
#     else:
#         try:
#             channel = grpc.insecure_channel("change-balance-gateways.spot-services.svc.cluster.local:80")
#             client = ChangeBalanceStub(channel)
#             transactionId = randint(10**5, 10**25)
#             request = ManualChangeBalanceGrpcRequest(
#                 TransactionId = f"{transactionId}",
#                 ClientId      = f"{clientId}",
#                 WalletId      = f"{walletId}",
#                 Amount        = decimal_amount,
#                 AssetSymbol   = f"{asset}",
#                 Comment       =  "BaseTests",
#                 BrokerId      =  f"{BrokerId}",
#                 Officer       = "BaseTests",
#                 Agent         =  {
#                     "ApplicationName": "BaseTests",
#                     "ApplicationEnvInfo": "BaseTests"
#                 }

#             )
#         except Exception as err:
#             print(f'Can not make request object')
#             return None
#         try:
#             response = client.ManualChangeBalance(request)
#             try:
#                 result = response.Result
#                 return result
#             except Exception as err:
#                 print(f'Error with parse response in changeBalance function.\n{err}')
#                 return None
#         except Exception as err:
#             print(f'Error with sending request in changeBalance function.\n{err}')
#             return None

