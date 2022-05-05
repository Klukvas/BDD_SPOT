import ICampaignManager_pb2 as cmp_pb2
import ICampaignManager_pb2_grpc as cmp_grpc
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


def get_referrer_campaign():
    all_campaigns = get_all_campaigns()
    for campaign in all_campaigns['Campaigns']:
        if campaign['Status'] == "Active":
            for criteria in  campaign['CriteriaList']:
                if 'HasReferrer' in criteria['Parameters'].keys() and \
                        criteria['Parameters']['HasReferrer']:
                    return campaign
        continue


if __name__ == "__main__":
    a = get_all_campaigns()
    json_obj = MessageToJson(a)

    # print(a)
    print(type(json_obj))
