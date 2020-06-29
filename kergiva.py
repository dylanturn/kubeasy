#!/usr/bin/env python

import kubeasy_sdk

# ==== CHART PARAMETERS ====
# These could be supplied in a number of ways.

name = "kergiva-org-web"
namespace = "kergiva"
image = "docker.pkg.github.com/rationalhealthcare/kgweb/kgweb"
release = "latest"
environment = "dev"
replicas = 1
external_container_port = 80
ingress_host = "kergiva.app"


# ==== DEPLOYMENT ====
# Creates the deployment that will manage the charts containers.
kergiva_web_chart = kubeasy_sdk.EasyChart(name=name, namespace=namespace, environment=environment, release=release)

nginx_config = kergiva_web_chart.include_config_map("nginx-config", "site-configmap")
site_config = kergiva_web_chart.include_config_map("site-config", "site-configmap")
cache_volume = kergiva_web_chart.add_empty_dir("cache-volume", "512Mb")
run_volume = kergiva_web_chart.add_empty_dir("run-volume", "512Mb")


# ==== CONTAINER ====
# Add an init container to the deployment to set the credentials for the nginx configs.
chart_init_container = kergiva_web_chart.add_init_container("install", "busybox", "latest")
chart_init_container.set_command(["sh", "-c", "mkdir -p /var/cache/nginx && chown 1000:1000 /var/cache/nginx"])
chart_init_container.mount_volume(cache_volume.name, "/var/cache")


# ==== CONTAINER ====
# Add the container to the deployment.
chart_container = kergiva_web_chart.add_container(name, image, release)

# Add environment variables NGINX needs so it knows which port to listen on.
chart_container.add_env_variable("NGINX_PORT", str(external_container_port))

# Add the volume mounts the container needs so it can write cache files and read it's config
chart_container.mount_volume(site_config.name, "/etc/nginx/conf.d/", read_only=True)
chart_container.mount_volume(cache_volume.name, "/var/cache")
chart_container.mount_volume(run_volume.name, "/var/run")

# Open any ports the container needs.
chart_container_external_port = chart_container.add_port("external", external_container_port)


# ==== SERVICE ====
# Add a service to the deployment to enable communication from other deployments or services
chart_service = kergiva_web_chart.add_service("kergiva-external-service")

# Attach service ports to the charts service.
chart_service_external_port = chart_service.add_port(kubeasy_sdk.ServicePort(chart_container_external_port))


# ==== INGRESS ====
# Add an Ingress that can be attached to service ports for communication external to the cluster.
example_ingress = kergiva_web_chart.add_ingress(ingress_host)

# Add the annotations that we need for things like lets encrypt certs
example_ingress.annotate("kubernetes.io/ingress.class","nginx")
example_ingress.annotate("cert-manager.io/cluster-issuer", "letsencrypt-prod")

# Attach an ingress rule to the external service port to enable communications from outside the cluster.
example_ingress.add_rule(ingress_host, chart_service_external_port)

# Render the chart into a Kubernetes manifest
print(kergiva_web_chart.render())