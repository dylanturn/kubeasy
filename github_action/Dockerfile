# Container image that runs your code
FROM python:3.8.5-alpine3.12

ARG KUBEASY_VERSION
ARG KUBECTL_VERSION=1.19.0

# Install CURL and PIPENV
RUN apk add curl &&\
    pip3 install pipenv

# Install Kubernetes Pre-reqs
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v$KUBECTL_VERSION/bin/linux/amd64/kubectl &&\
    chmod +x ./kubectl &&\
    mv ./kubectl /usr/local/bin/kubectl

# Upgrade pip and install Kubeasy
RUN pip install --upgrade pip &&\
    pip install kubeasy-py==$KUBEASY_VERSION

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]