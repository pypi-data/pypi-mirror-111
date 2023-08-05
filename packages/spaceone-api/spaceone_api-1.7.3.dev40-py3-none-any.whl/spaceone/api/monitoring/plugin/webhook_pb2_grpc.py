# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from spaceone.api.monitoring.plugin import webhook_pb2 as spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2


class WebhookStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.init = channel.unary_unary(
                '/spaceone.api.monitoring.plugin.Webhook/init',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookInitRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginInfo.FromString,
                )
        self.verify = channel.unary_unary(
                '/spaceone.api.monitoring.plugin.Webhook/verify',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginVerifyRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class WebhookServicer(object):
    """Missing associated documentation comment in .proto file."""

    def init(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WebhookServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'init': grpc.unary_unary_rpc_method_handler(
                    servicer.init,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookInitRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginInfo.SerializeToString,
            ),
            'verify': grpc.unary_unary_rpc_method_handler(
                    servicer.verify,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginVerifyRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.monitoring.plugin.Webhook', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Webhook(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def init(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.plugin.Webhook/init',
            spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookInitRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def verify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.plugin.Webhook/verify',
            spaceone_dot_api_dot_monitoring_dot_plugin_dot_webhook__pb2.WebhookPluginVerifyRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
