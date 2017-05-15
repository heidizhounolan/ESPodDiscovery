"""Module that setups grpc service connectors.

Connectors are used throughout pod_discovery.apis.http."""
from pod_discovery.services.stubs import health_pb2, pods_pb2
from pod_discovery.services import GrpcServiceConnector

# pylint: disable=invalid-name
health_conn = GrpcServiceConnector(health_pb2.HealthStub)
pods_conn = GrpcServiceConnector(pods_pb2.PodMasterStub)
