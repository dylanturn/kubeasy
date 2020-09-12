#!/usr/bin/env python

import kubeasy_sdk

# ==== CHART PARAMETERS ====
# These could be supplied in a number of ways.

name = "hello-k8s"
namespace = "default"
image = "paulbouwer/hello-kubernetes"
release = "1.7"
environment = "stg"
replicas = 2
internal_container_port = 8080
external_container_port = 8081


# ==== DEPLOYMENT ====
# Creates the deployment that will manage the charts containers.
easy_chart = kubeasy.EasyChart(name=name, namespace=namespace, environment=environment, release=release)


# ==== CONTAINER ====
# Add the container to the deployment.
chart_container = easy_chart.add_container(name, image, release)

# Open any ports the container needs.
chart_container_internal_port = chart_container.add_port("internal", internal_container_port)
chart_container_external_port = chart_container.add_port("external", external_container_port)


# ==== SERVICE ====
# Add a service to the deployment to enable communication from other deployments or services
chart_service = easy_chart.add_service("test-service")

# Attach service ports to the charts service.
chart_service_internal_port = chart_service.add_port(kubeasy.ServicePort(chart_container_internal_port))
chart_service_external_port = chart_service.add_port(kubeasy.ServicePort(chart_container_external_port))


# ==== INGRESS ====
# Add an Ingress that can be attached to service ports for communication external to the cluster.
example_ingress = easy_chart.add_ingress("example")

# Attach an ingress rule to the external service port to enable communications from outside the cluster.
example_ingress.add_rule("example.com", chart_service_external_port)
example_ingress.add_rule("whoop.com", chart_service_external_port, "/there/it/is")

# Render the chart into a Kubernetes manifest
print(easy_chart.render())
