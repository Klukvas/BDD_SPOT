# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import ISpotChangeBalanceService_pb2 as ISpotChangeBalanceService__pb2


class SpotChangeBalanceServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BlockchainDeposit = channel.unary_unary(
                '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainDeposit',
                request_serializer=ISpotChangeBalanceService__pb2.BlockchainDepositGrpcRequest.SerializeToString,
                response_deserializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
                )
        self.BlockchainFeeApply = channel.unary_unary(
                '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainFeeApply',
                request_serializer=ISpotChangeBalanceService__pb2.BlockchainFeeApplyGrpcRequest.SerializeToString,
                response_deserializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
                )
        self.BlockchainWithdrawal = channel.unary_unary(
                '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainWithdrawal',
                request_serializer=ISpotChangeBalanceService__pb2.BlockchainWithdrawalGrpcRequest.SerializeToString,
                response_deserializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
                )
        self.ManualChangeBalance = channel.unary_unary(
                '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/ManualChangeBalance',
                request_serializer=ISpotChangeBalanceService__pb2.ManualChangeBalanceGrpcRequest.SerializeToString,
                response_deserializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
                )
        self.PciDssDeposit = channel.unary_unary(
                '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/PciDssDeposit',
                request_serializer=ISpotChangeBalanceService__pb2.PciDssDepositGrpcRequest.SerializeToString,
                response_deserializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
                )


class SpotChangeBalanceServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def BlockchainDeposit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BlockchainFeeApply(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BlockchainWithdrawal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ManualChangeBalance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PciDssDeposit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SpotChangeBalanceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BlockchainDeposit': grpc.unary_unary_rpc_method_handler(
                    servicer.BlockchainDeposit,
                    request_deserializer=ISpotChangeBalanceService__pb2.BlockchainDepositGrpcRequest.FromString,
                    response_serializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.SerializeToString,
            ),
            'BlockchainFeeApply': grpc.unary_unary_rpc_method_handler(
                    servicer.BlockchainFeeApply,
                    request_deserializer=ISpotChangeBalanceService__pb2.BlockchainFeeApplyGrpcRequest.FromString,
                    response_serializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.SerializeToString,
            ),
            'BlockchainWithdrawal': grpc.unary_unary_rpc_method_handler(
                    servicer.BlockchainWithdrawal,
                    request_deserializer=ISpotChangeBalanceService__pb2.BlockchainWithdrawalGrpcRequest.FromString,
                    response_serializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.SerializeToString,
            ),
            'ManualChangeBalance': grpc.unary_unary_rpc_method_handler(
                    servicer.ManualChangeBalance,
                    request_deserializer=ISpotChangeBalanceService__pb2.ManualChangeBalanceGrpcRequest.FromString,
                    response_serializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.SerializeToString,
            ),
            'PciDssDeposit': grpc.unary_unary_rpc_method_handler(
                    servicer.PciDssDeposit,
                    request_deserializer=ISpotChangeBalanceService__pb2.PciDssDepositGrpcRequest.FromString,
                    response_serializer=ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SpotChangeBalanceService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def BlockchainDeposit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainDeposit',
            ISpotChangeBalanceService__pb2.BlockchainDepositGrpcRequest.SerializeToString,
            ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BlockchainFeeApply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainFeeApply',
            ISpotChangeBalanceService__pb2.BlockchainFeeApplyGrpcRequest.SerializeToString,
            ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BlockchainWithdrawal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/BlockchainWithdrawal',
            ISpotChangeBalanceService__pb2.BlockchainWithdrawalGrpcRequest.SerializeToString,
            ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ManualChangeBalance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/ManualChangeBalance',
            ISpotChangeBalanceService__pb2.ManualChangeBalanceGrpcRequest.SerializeToString,
            ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PciDssDeposit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service.ChangeBalanceGateway.Grpc.SpotChangeBalanceService/PciDssDeposit',
            ISpotChangeBalanceService__pb2.PciDssDepositGrpcRequest.SerializeToString,
            ISpotChangeBalanceService__pb2.ChangeBalanceGrpcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
