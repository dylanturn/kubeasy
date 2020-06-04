#!/usr/bin/env python

import kubeasy

name = "hello-k8s"
namespace = "default"
image = "paulbouwer/hello-kubernetes"
release = "1.7"
environment = "stg"
replicas = 2

easy_chart = kubeasy.EasyChart(name=name, namespace=namespace, environment=environment, release=release)
easy_chart.add_container("main_container", image, release)
easy_chart.add_service("test_service")
print(easy_chart.render())
