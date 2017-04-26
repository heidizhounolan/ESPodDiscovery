import logging
import grpc
from pod_discovery.services.stubs import pods_pb2
from pod_discovery.services.implementations.database import (
        connection as db, models)

log = logging.getLogger(__name__)


class PodMasterServicer(pods_pb2.PodMasterServicer):
    """Implements PodMaster protobuf service interface."""

    def GetPod(self, request, context):
        """Retrieve a pod from the database.

        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        pod = db.query(models.Pod).get(request.id)

        if pod:
            pod_pb = pods_pb2.Pod(**pod.to_dict())
            return pods_pb2.GetPodResponse(pod=pod_pb)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Pod with id %s not found' % request.id)
            return pods_pb2.GetPodResponse()
