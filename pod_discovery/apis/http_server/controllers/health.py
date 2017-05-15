"""Flask blueprint for /health endpoint.

Exposes the blueprint as a module-level variable named `health`.
"""
import json
from flask import Blueprint
from healthcheck import HealthCheck
from ripozo.adapters import JSONAPIAdapter
from ripozo.exceptions import RestException

from pod_discovery.apis.http_server.services import health_conn
from pod_discovery.services.server import grpc
from pod_discovery.services.stubs import health_pb2

# pylint: disable=invalid-name
health = Blueprint('health', __name__)


def _grpc_available():
    """Checks that the http client is connected and that the grpc server
    is available.

    Returns:
        A tuple of (bool, str or dict) where bool indicates whether the check
            passed, and the str or dict provides extra context about the check
    """
    try:
        resp = health_conn.stub.Check(health_pb2.HealthCheckRequest())
        check_passed = resp.status == health_pb2.HealthCheckResponse.SERVING
        return check_passed, 'grpc server OK'
    except grpc._channel._Rendezvous as exc:  # pylint: disable=protected-access
        return False, {'code': str(exc.code())}
    except RestException as exc:
        response, _, _ = JSONAPIAdapter.format_exception(exc)
        return False, json.loads(response)


_health_check = HealthCheck(health, '/health')
_health_check.add_check(_grpc_available)
