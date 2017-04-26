"""Flask blueprint for /pods* endpoint.

Exposes the blueprint as a module-level variable named `main`.
"""
from flask import Blueprint
from flask_ripozo import FlaskDispatcher
from ripozo import restmixins
from ripozo.manager_base import BaseManager
from ripozo.adapters import JSONAPIAdapter
from ripozo.resources.fields.common import StringField, IntegerField
from pod_discovery.services.stubs import pods_pb2
from pod_discovery.apis.http.services import pods_conn

# pylint: disable=invalid-name
pods = Blueprint('pods', __name__)


class PodManager(BaseManager):
    """Manager that interops between ripozo and grpc.

    Provides convience functions primarily for basic CRUD.
    """
    fields = ('id', 'name',)
    field_validators = [
        IntegerField('id', required=True),
        StringField('name', required=True),
    ]

    def create(self, values, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, lookup_keys, *args, **kwargs):
        raise NotImplementedError()

    def retrieve(self, lookup_keys, *args, **kwargs):
        """Retrieve a single pod and nothing more as a dictionary.

        Args:
            lookup_keys (dict): Taken from url_params on flask request. Used to
                lookup a pod and its associated values.

        Returns:
            dict or None: Properties of the retrieved pod or None if no
                such pod found.
        """
        resp = pods_conn.stub.GetPod(
            pods_pb2.GetPodRequest(id=lookup_keys['id']))
        pod = resp.pod

        if pod:
            return dict(id=pod.id, name=pod.name)

    def retrieve_list(self, filters, *args, **kwargs):
        raise NotImplementedError()

    def update(self, lookup_keys, updates, *args, **kwargs):
        raise NotImplementedError()


class PodResource(restmixins.Retrieve):
    """Standard ripozo resource that can be used by ripozo adapters. Handles
    requests and constructs resources to return as a request.
    """
    manager = PodManager()
    pks = 'id',
    resource_name = 'pods'


# register resources and valid response types
_dispatcher = FlaskDispatcher(pods)
_dispatcher.register_adapters(JSONAPIAdapter)
_dispatcher.register_resources(PodResource)
