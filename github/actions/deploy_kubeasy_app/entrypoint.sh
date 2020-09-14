#!/bin/sh -l

KUBEASY_VERSION=$1
DEPLOYMENT_FILE=$2
BASE64_KUBE_CONFIG=$3

cd kubeasy

# Download and setup Kubeasy
curl -L https://github.com/dylanturn/kubeasy/archive/v${KUBEASY_VERSION}.tar.gz --output kubeasy-${KUBEASY_VERSION}.tar.gz

# Extract the tar into the current dir
tar -xvf kubeasy-${KUBEASY_VERSION}.tar.gz --strip 1

# Install the pre-reqs
pipenv install

# Write out the kubeconfig to some place the kubectl binary will know to look.
echo ${BASE64_KUBE_CONFIG} | base64 -d > ./kubeconfig

# Generate and deploy the manifest
pipenv run python3 ./${DEPLOYMENT_FILE} | kubectl apply --kubeconfig ./kubeconfig -f -