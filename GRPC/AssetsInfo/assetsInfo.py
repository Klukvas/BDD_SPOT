import traceback
import grpc

from GRPC.AssetsInfo import IAssetsDictionaryService_pb2 as asset_pb2, \
    IAssetsDictionaryService_pb2_grpc as asset_grpc


def get_asset_by_id(assetId, broker='jetwallet'):
    channel = grpc.insecure_channel("assets-dictionary.spot-services.svc.cluster.local:80")
    client = asset_grpc.AssetsDictionaryServiceStub(channel)

    try:
        request = asset_pb2.AssetIdentity(
            BrokerId=broker,
            Symbol=assetId
        )
    except Exception as err:
        print(f"Error with creating request: {err}\nassetId: {assetId}, broker: {broker}")
        return None

    try:
        response = client.GetAssetById(request)
    except Exception as err:
        print(f"Error with getting response: {err}\nassetId: {assetId}, broker: {broker}")
        return None
    return response


def update_asset(grpc_object, min_max_object):
    channel = grpc.insecure_channel("assets-dictionary.spot-services.svc.cluster.local:80")
    client = asset_grpc.AssetsDictionaryServiceStub(channel)

    try:
        request = asset_pb2.Asset(
            DepositBlockchains=grpc_object.DepositBlockchains if grpc_object.DepositBlockchains else [],
            WithdrawalBlockchains=grpc_object.WithdrawalBlockchains if grpc_object.WithdrawalBlockchains else [],
            BrokerId=grpc_object.BrokerId if grpc_object.BrokerId else '',
            Symbol=grpc_object.Symbol if grpc_object.BrokerId else '',
            Description=grpc_object.Description if grpc_object.BrokerId else '',
            Accuracy=grpc_object.Accuracy if grpc_object.BrokerId else 0,
            IsEnabled=grpc_object.IsEnabled if grpc_object.BrokerId else False,
            MatchingEngineId=grpc_object.MatchingEngineId if grpc_object.BrokerId else '',
            KycRequiredForDeposit=grpc_object.KycRequiredForDeposit if grpc_object.BrokerId else False,
            KycRequiredForWithdrawal=grpc_object.KycRequiredForWithdrawal if grpc_object.BrokerId else False,
            IconUrl=grpc_object.IconUrl if grpc_object.BrokerId else '',
            PrefixSymbol=grpc_object.PrefixSymbol if grpc_object.BrokerId else '',
            IsMainNet=grpc_object.IsMainNet if grpc_object.BrokerId else False,
            CanBeBaseAsset=grpc_object.CanBeBaseAsset if grpc_object.BrokerId else False,
            ShortDescription=grpc_object.ShortDescription if grpc_object.BrokerId else '',
            Type=grpc_object.Type if grpc_object.BrokerId else '',
            KycRequiredForTrade=grpc_object.KycRequiredForTrade if grpc_object.BrokerId else False,
            HideInTerminal=grpc_object.HideInTerminal if grpc_object.BrokerId else False,
            MinTradeValue=min_max_object['MinTradeValue'] if min_max_object['MinTradeValue'] else '',
            MaxTradeValue=min_max_object['MaxTradeValue'] if min_max_object['MaxTradeValue'] else ''
        )
    except Exception:
        traceback.print_exc()
        print(f"Error with creating request for upd asset")
        return None

    try:
        response = client.UpdateAsset(request)
    except Exception:
        traceback.print_exc()
        print(f"Error with getting response with upd asset")
        return None
    return response

    """
    {
    {
    "DepositBlockchains": [
      "fireblocks-btc-test"
    ],
    "WithdrawalBlockchains": [
      "fireblocks-btc-test"
    ],
    "BrokerId": "jetwallet",
    "Symbol": "BTC",
    "Description": "Bitcoin",
    "Accuracy": 8,
    "IsEnabled": true,
    "MatchingEngineId": "jetwallet::BTC",
    "KycRequiredForDeposit": false,
    "KycRequiredForWithdrawal": false,
    "IconUrl": "",
    "PrefixSymbol": "",
    "IsMainNet": false,
    "CanBeBaseAsset": true,
    "ShortDescription": "",
    "Type": "Crypto",
    "KycRequiredForTrade": false,
    "HideInTerminal": true,
    "MinTradeValue": {
      "lo": "120",
      "hi": 0,
      "signScale": 2
    },
    "MaxTradeValue": {
      "lo": "220",
      "hi": 0,
      "signScale": 2
    }
  }
}
    """


if __name__ == "__main__":
    get_asset_by_id('BTC')
