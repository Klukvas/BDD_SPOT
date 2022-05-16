import json

from GRPC.PersonalData import IPersonalDataServiceGrpc_pb2 as pd_pb2
from GRPC.PersonalData import IPersonalDataServiceGrpc_pb2_grpc as pd_grpc
import grpc
from google.protobuf.json_format import MessageToJson


def change_personal_data(client_id, Country):
    try:
        channel = grpc.insecure_channel("personaldata.spot-services.svc.cluster.local:80")
    except Exception as err:
        raise ConnectionError(f"Can not make channel to personaldata\n{err}")
    try:
        client = pd_grpc.PersonalDataServiceGrpcStub(channel)
    except Exception as err:
        raise SystemError(f"Can not make client to CampaignManagerStub\n{err}")
    try:
        request = pd_pb2.UpdatePersonalDataGrpcContract(
            Id=client_id,
            FirstName="Hello",
            LastName="Hello",
            Sex=0,
            DateOfBirth={
                "value":1200,
                "scale":0,
                "kind":0
            },
            CountryOfResidence=Country,
            CountryOfCitizenship=Country,
            City="Hello",
            PostalCode="Hello",
            Phone="Hello",
            AuditLog = {
                "TraderId": "3193daae-2b21-476a-a242-ba7ca7b739ea",
                "Ip": "Hello",
                "ServiceName": "Hello",
                "ProcessId": "2723eb46-601c-4421-9274-839e57606130",
                "Context":"Hello"
            },
            Address= "Hello",
            USCitizen= True

        )
    except Exception as err:
        raise Exception(f"Can not make request for update personal data.\nError:{err}")


    try:
        response = client.Update(request)
        try:
            result = response.Ok
            return result
        except Exception as err:
            raise Exception(f"Can not get result of setting kyc status with error: {err}")
    except Exception as err:
        raise Exception(f"Can not process request for set kyc status.\nError: {err}")



if __name__ == "__main__":
    a = change_personal_data('e34a179c41244965b959207acb7d78d0', 'asd')
    print(a)