#!/usr/bin/env python

"""RESTful, JSON-API compliant wrapper around pod_discovery' services.

Interfaces with grpc stubs which in turn interface with core service logic.
"""
import grpc
from flask import Flask, Response
from ripozo.adapters import JSONAPIAdapter
from ripozo.exceptions import RestException
from pod_discovery.apis.http.controllers.main import main
from pod_discovery.apis.http.controllers.health import health
from pod_discovery.apis.http.controllers.pods import pods
from pod_discovery.apis.http.services import health_conn, pods_conn
from pod_discovery.apis.http.exceptions import (
    InternalServerException, NotFoundException)


def create_app(object_name):
    """A flask application factory for pod_discovery.
    Args:
        object_name: the python path of the config object,
                     e.g. pod_discovery.apis.http.settings.DevelopmentConfig
    """
    app = Flask(__name__)

    app.config.from_object(object_name)

    # initialize connection to grpc services
    health_conn.start()
    pods_conn.start()

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(health)
    app.register_blueprint(pods)

    # pylint: disable=unused-variable
    @app.errorhandler(Exception)
    def all_exception_handler(exc):
        """Default, JSON-API compliant exception handler."""
        # pylint: disable=redefined-variable-type
        if isinstance(exc, RestException):
            rest_exc = exc
        elif (isinstance(exc, grpc._channel._Rendezvous)  # pylint: disable=protected-access
              and exc.code() == grpc.StatusCode.NOT_FOUND):
            rest_exc = NotFoundException(message=exc.details())
        else:
            rest_exc = InternalServerException(message=str(exc))

        response, content_type, status_code = \
            JSONAPIAdapter.format_exception(rest_exc)

        return Response(response=response,
                        content_type=content_type,
                        status=status_code)

    return app
