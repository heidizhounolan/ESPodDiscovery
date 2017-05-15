# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""The Python implementation of the gRPC route guide server."""

import grpc
import time
from concurrent import futures

import pod_discovery_pb2
import pod_discovery_pb2_grpc
import pod_discovery_resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def get_pod(pod_db, pod_name):
  """Returns pod details of a given pod_name or None."""
  for pod in pod_db:
    if pod.pod_name == pod_name:
      return pod
  return None

class PodDiscoveryServicer(pod_discovery_pb2_grpc.PodDiscoveryServicer):
  """Provides methods that implement functionality of route guide server."""

  def __init__(self):
    self.db = pod_discovery_resources.read_pod_discovery_database()

  def GetPod(self, request, context):
    pod = get_pod(self.db, request)
    if pod is None:
      return pod_discovery_pb2.Pod(name="", location=request)
    else:
      return pod

  def ListPods(self, request, context):
    for pod in self.db:
        yield pod

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pod_discovery_pb2_grpc.add_PodDiscoveryServicer_to_server(
      PodDiscoveryServicer(), server)
  server.add_insecure_port('[::]:51051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
