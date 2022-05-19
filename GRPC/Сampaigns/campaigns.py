import json

from GRPC.Сampaigns import ICampaignManager_pb2 as cmp_pb2
from GRPC.Сampaigns import ICampaignManager_pb2_grpc as cmp_grpc
import grpc
from GRPC.UsefulImport import empty_pb2
from google.protobuf.json_format import MessageToJson


def get_all_campaigns():
    try:
        channel = grpc.insecure_channel("bonuscampaign.spot-services.svc.cluster.local:80")
    except Exception as err:
        raise ConnectionError(f"Can not make channel to bonuscampaign\n{err}")
    try:
        client = cmp_grpc.CampaignManagerStub(channel)
    except Exception as err:
        raise SystemError(f"Can not make client to CampaignManagerStub\n{err}")
    try:
        empty = empty_pb2.Empty()
    except Exception as err:
        raise Exception(f"Can not make empty data for request\n{err}")
    try:
        response = client.GetAllCampaigns(empty)
    except Exception as err:
        raise Exception(f"can not send request\n{err}")
    return MessageToJson(response)


def get_client_context(client_id: str) -> str:
    try:
        channel = grpc.insecure_channel("bonuscampaign.spot-services.svc.cluster.local:80")
    except Exception as err:
        raise ConnectionError(f"Can not make channel to bonuscampaign\n{err}")
    try:
        client = cmp_grpc.CampaignManagerStub(channel)
    except Exception as err:
        raise SystemError(f"Can not make client to CampaignManagerStub\n{err}")
    try:
        request = cmp_pb2.GetContextsByClientRequest(
            ClientId=client_id,
            Skip=0,
            Take=100
        )
    except Exception as err:
        raise Exception(f"Can not make request for get context of client.\nError:{err}")
    try:
        response = client.GetContextsByClient(request)
    except Exception as err:
        raise Exception(f"can not send request\n{err}")
    return MessageToJson(response)


if __name__ == "__main__":
    a = get_client_context('f4967266ac824455b311302f85a828fc')
    b = (
        cmp_id['CampaignId']
        for cmp_id in json.loads(a)['Contexts']
    )
    assert '99a2d5e0edeb4998ac5b6025e82c826b' in b
    for item in b:
        print(item)