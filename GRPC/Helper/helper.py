
import grpc
from GRPC.Helper import Helper_pb2 as help_pb, \
    Helper_pb2_grpc as help_grpc

def string_to_decimal(amount):
    channel = grpc.insecure_channel("change-balance-gateways.spot-services.svc.cluster.local:80")
    client = help_grpc.GrpcHelperServiceStub(channel)
    decimal_amount = {}
    value=str(amount)
    value2=value.replace(',', '.')
    amount = float(value2)
    
    try:
        request = help_pb.Data_String(
            Value = str(amount)
        )
    except Exception as err:
        print(f"Err with creating request\nErr: {err}")
        return None
    try:
        response = client.StringToDecimal(request)
        
        if response.Value.lo:
            decimal_amount["lo"] = int(response.Value.lo)
        else:
            decimal_amount["lo"] = 0

        if response.Value.hi:
            decimal_amount["hi"] = response.Value.hi
        else:
            decimal_amount["hi"] = 0
        
        if response.Value.signScale:
            decimal_amount['signScale'] = response.Value.signScale
        else:
            decimal_amount['signScale'] = 0
        return decimal_amount
    except Exception as err:
        print(f"Err with sending request\namount: {amount}\nrequest:{request}\nErr: {err}")
        return None

