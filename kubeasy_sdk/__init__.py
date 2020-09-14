from __future__ import annotations

import yaml
import json

from cdk8s import App, Chart
from constructs import Construct
from kubeasy_sdk.utils.collections.chart_resource_collection import ChartResourceCollection
from kubeasy_sdk.utils.resource import Rendered
from kubeasy_sdk.deployment import Deployment
from kubeasy_sdk.container import Container
from kubeasy_sdk.service import Service, ServicePort, ServiceType
from kubeasy_sdk.ingress import Ingress, IngressPath
from kubeasy_sdk.volume import Volume, ConfigMap, EmptyDir
from typing import Mapping


class EasyChart(object):
  def __init__(self, name: str, namespace: str, environment: str, release: str):
    self.name = name
    self.namespace = namespace
    self.environment = environment
    self.release = release

    self.deployment = Deployment(name=self.name,
                                 namespace=self.namespace,
                                 environment=self.environment)

    self.service_collection = ChartResourceCollection()
    self.ingress_collection = ChartResourceCollection()

  def add_init_container(self, name: str, image: str, tag: str) -> Container:
    new_init_container = Container(name, image, tag)
    self.deployment.add_init_container(new_init_container)
    return new_init_container

  def add_container(self, name: str, image: str, tag: str) -> Container:
    new_container = Container(name, image, tag)
    self.deployment.add_container(new_container)
    return new_container

  def include_volume(self, name: str, labels: Mapping[str, str]) -> Volume:
    new_volume = Volume(name, labels)
    self.deployment.include_volume(new_volume)
    return new_volume

  def include_config_map(self, name: str, config_name: str) -> ConfigMap:
    new_config_map = ConfigMap(name=name, config_name=config_name)
    self.deployment.include_volume(volume=new_config_map)
    return new_config_map

  def add_empty_dir(self, name: str, size_limit: str, use_memory: bool = False) -> EmptyDir:
    new_empty_dir = EmptyDir(name=name, size_limit=size_limit, use_memory=use_memory)
    self.deployment.include_volume(volume=new_empty_dir)
    return new_empty_dir

  def add_service(self, service_name) -> Service:
    new_service = Service(name=service_name, deployment=self.deployment)
    self.service_collection.add_resource(new_service)
    return new_service

  def add_ingress(self, name: str, tls: bool = False, labels: dict = None) -> Ingress:
    new_ingress = Ingress(name, tls, labels)
    self.ingress_collection.add_resource(new_ingress)
    return new_ingress

  def render(self) -> list:
    app = App()
    combined_resource_collection = ChartResourceCollection.combine([self.service_collection, self.ingress_collection])

    chart_json = self.__EasyChart(app, self.deployment, combined_resource_collection).to_json()

    yaml_manifest = ""
    for manifest in chart_json:
      yaml_manifest += f"---\n{yaml.dump(yaml.load(json.dumps(manifest), Loader=yaml.FullLoader))}"
    return yaml_manifest

  class __EasyChart(Chart):
    def __init__(self, scope: Construct, chart_deployment: Deployment, chart_resources: ChartResourceCollection):
      super().__init__(scope, chart_deployment.name)
      self.name = chart_deployment.name
      self.scope = scope
      chart_deployment.render(self)
      chart_resources.render(self)