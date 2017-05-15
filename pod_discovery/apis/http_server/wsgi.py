"""WSGI config for pod_discovery.apis.http.

Exposes the WSGI callable as a module-level variable named `app`.
"""
import os
from pod_discovery.apis.http_server import create_app

# pylint: disable=invalid-name
env = os.environ.get('ENV', 'development')
app = create_app('pod_discovery.apis.http.settings.%sConfig' % env.capitalize())


if __name__ == '__main__':
    app.run()
