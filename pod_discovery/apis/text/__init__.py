"""Module with text client for pod_discovery's grpc server."""

from google.protobuf import text_format
from pod_discovery.services.stubs import health_pb2, pods_pb2
from pod_discovery.services import GrpcServiceConnector


class TextClient(object):
    """A text client for pod_discovery's grpc server."""
    def __init__(self):
        self.health_conn = GrpcServiceConnector(health_pb2.HealthStub)
        self.pods_master_conn = GrpcServiceConnector(pods_pb2.PodMasterStub)

        self.health_conn.start()
        self.pods_master_conn.start()

    def check_health(self):
        """Checks that the text client is connected and that the grpc server
        is available.

        Raises:
            grpc._channel._Rendezvous: When grpc server is down

        Returns:
            str: True or False depending on connection state
        """
        res = self.health_conn.stub.Check(health_pb2.HealthCheckRequest())
        return str(res.status == health_pb2.HealthCheckResponse.SERVING)

    def get_pod(self, pod_id):
        """Retrieve a pod.

        Args:
            pod_id (int): id of pod to retrieve

        Raises:
            grpc._channel._Rendezvous: When grpc server is down

        Returns:
            str: True or False depending on connection state
        """
        req = pods_pb2.GetPodRequest(id=pod_id)
        res = self.pods_master_conn.stub.GetPod(req)
        return text_format.MessageToString(res)
