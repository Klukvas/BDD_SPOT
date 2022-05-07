import traceback
import grpc
from GRPC.Kyc import IKycStatusService_pb2 as kyc_pb2, \
    IKycStatusService_pb2_grpc as kyc_grpc


def set_kys_allowed(client_id: str) -> None or str:
    try:
        channel = grpc.insecure_channel("kyc.spot-services.svc.cluster.local:80")
        try:
            client = kyc_grpc.KycStatusServiceStub(channel)
        except Exception as err:
            raise Exception(f"Can not make client for set kyc status.\nError: {err}")
        request = kyc_pb2.SetOperationStatusRequest(
            ClientId=client_id,
            Agent="AutoTest",
            Comment="Auto_Test_Comm",
            DepositStatus=2,
            TradeStatus=2,
            WithdrawalStatus=2
        )
    except Exception as err:
        raise Exception(f"Can not make request for set kyc status.\nError:{err}")
    try:
        response = client.SetKycStatuses(request)
        try:
            result = response.IsSuccess
            return result
        except Exception as err:
            raise Exception(f"Can not get result of setting kyc status with error: {err}")
    except Exception as err:
        raise Exception(f"Can not process request for set kyc status.\nError: {err}")


if __name__ == '__main__':
    set_kys_allowed('1cb010347bf94bcca71d6cce4456106b')