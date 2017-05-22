# ESPodDiscovery
Service to retrieve POD information from Datamodel, json/yaml files, consul/etcd.

## Table of Contents


## Description

### Pros

#### gRPC server

#### Language agnostic stubs

#### How to run pod discovery service locally
##### Setup Python virtual environment
$ python -m pip install virtualenv 

$ virtualenv venv 

$ source venv/bin/activate 

$ python -m pip install --upgrade pip

$ python -m pip install grpcio-tools

##### build pod discovery service
$ make install
$ make protogen

##### run service locally
$ make run-grpc-api

##### run test client
$ make run-grpc-client

#### How to run pod discovery service docker container locally
##### build pod discovery service docker image
$ make build

##### run docker container locally
$ docker run -p 51051:51051 pod_discovery:latest

##### run test client
$ make run-grpc-client

##### kill the docker container
$ docker ps | grep pod_discovery
$ docker kill <container-id>

