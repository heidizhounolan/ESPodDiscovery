FROM python:3.5

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

# Add dockerize, which will add a command we can use to wait for
# dependent containers to finish setup (instead of just startup)
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.1.0/dockerize-linux-amd64-v0.1.0.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.1.0.tar.gz

RUN mkdir /opt/pod_discovery/
WORKDIR /opt/pod_discovery/

ARG GIT_COMMIT
ENV GIT_COMMIT $GIT_COMMIT

# Docker caches packages so that this line is only re-run
# when requirements change
RUN mkdir /opt/pod_discovery/requirements
ADD ./requirements/*.txt /opt/pod_discovery/requirements/
RUN pip install -r requirements/dev.txt

COPY . /opt/pod_discovery

# Server and clients are run from same container
# so rely on docker compose to determine command
CMD []
