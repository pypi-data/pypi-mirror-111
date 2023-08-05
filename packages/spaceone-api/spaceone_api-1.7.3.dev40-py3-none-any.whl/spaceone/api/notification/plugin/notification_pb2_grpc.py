# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from spaceone.api.notification.plugin import notification_pb2 as spaceone_dot_api_dot_notification_dot_plugin_dot_notification__pb2


class NotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.dispatch = channel.unary_unary(
                '/spaceone.api.notification.plugin.Notification/dispatch',
                request_serializer=spaceone_dot_api_dot_notification_dot_plugin_dot_notification__pb2.PluginDispatchRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class NotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def dispatch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'dispatch': grpc.unary_unary_rpc_method_handler(
                    servicer.dispatch,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_plugin_dot_notification__pb2.PluginDispatchRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.notification.plugin.Notification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Notification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def dispatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.plugin.Notification/dispatch',
            spaceone_dot_api_dot_notification_dot_plugin_dot_notification__pb2.PluginDispatchRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
