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
    try:
        parsed_resp = json.loads(MessageToJson(response))
    except Exception as err:
        raise Exception(f"can not convert from json to dict\nError: {err}")
    return parsed_resp


def get_campaign_by_id(cmp_id: str):
    cmp = list(filter(
        lambda campaign: campaign['Id'] == cmp_id,
        get_all_campaigns()['Campaigns']
    ))
    return cmp


if __name__ == "__main__":
    a = get_campaign_by_id('7d132d2ac7c34b7ca787db703c9b8ee2')
    print(a)