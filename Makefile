GIT_COMMIT=$(shell git rev-parse --verify HEAD)
PROJECT_NAME=pod_discovery
SERVICE_DEFN_DIR=./$(PROJECT_NAME)/services/definitions
SERVICE_STUB_DIR=./$(PROJECT_NAME)/services/stubs
SERVICE_SERVER_DIR=./$(PROJECT_NAME)/services/server
SERVICE_SERVER_NAME="pod_discovery_server.py"
SERVICE_CLIENT_DIR=./$(PROJECT_NAME)/client_example
SERVICE_CLIENT_NAME="pod_discovery_client.py"


.PHONY: build
build:
	docker build \
    --build-arg GIT_COMMIT=${GIT_COMMIT} \
    -t $(PROJECT_NAME):latest \
    -t $(PROJECT_NAME):${GIT_COMMIT} \
    .

.PHONY: down
down:
	docker-compose down

.PHONY: install
install:
	pip install -r requirements/dev.txt

.PHONY: lint
lint:
	pre-commit run pylint --all-files

.PHONY: protogen
protogen:
	python -m grpc.tools.protoc \
				 -I=$(SERVICE_DEFN_DIR) \
				 --python_out=$(SERVICE_STUB_DIR) \
				 --grpc_python_out=$(SERVICE_STUB_DIR) \
				 $(SERVICE_DEFN_DIR)/pod_discovery.proto $(SERVICE_DEFN_DIR)/health.proto

# Usage: make run-text-api ARGS="check_health"
# 			 make run-text-api ARGS="get_item 1"
.PHONY: run-text-api
run-text-api:
	python -m $(PROJECT_NAME).apis.text $(ARGS)

.PHONY: run-http-api
run-http-api:
	gunicorn -b 0.0.0.0:4000 $(PROJECT_NAME).apis.http.wsgi:app

.PHONY: run-grpc-api
run-grpc-api:
	python $(SERVICE_SERVER_DIR)/$(SERVICE_SERVER_NAME)

.PHONY: run-grpc-client
run-grpc-client:
	python $(SERVICE_CLIENT_DIR)/$(SERVICE_CLIENT_NAME)

.PHONY: up
up:
	docker-compose up -d
