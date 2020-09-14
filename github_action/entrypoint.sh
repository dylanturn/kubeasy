#!/bin/sh -l

DEPLOYMENT_FILE=$2
BASE64_KUBE_CONFIG=$3

# Write out the kubeconfig to some place the kubectl binary will know to look.
echo ${BASE64_KUBE_CONFIG} | base64 -d > ./kubeconfig

# Generate and deploy the manifest
python3 ${DEPLOYMENT_FILE} | kubectl apply --kubeconfig ./kubeconfig -f -