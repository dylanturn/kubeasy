from __future__ import annotations
from imports import k8s
from cdk8s import Chart

from kubeasy.deployment import Deployment
from kubeasy.utils.networking import ServiceType, ServicePort
from kubeasy.utils.collections.service_ports import ServicePorts
from kubeasy.utils.resource import Renderable


class Service(Renderable):
  def __init__(self, name: str, deployment: Deployment):
    self.name = name
    self.deployment = deployment

    self.environment = deployment.environment
    self.namespace = deployment.namespace
    self.labels = {}
    self.selector = {}
    self.service_type = ServiceType.CLUSTERIP
    self.ports = ServicePorts()
    self.__load_default_configuration__()

  # Configuration defaults will be read here
  def __load_default_configuration__(self):
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/deployment"] = self.deployment.name

    self.labels["app.kubernetes.io/environment"] = self.environment

    self.selector = self.deployment.match_labels

  # Configuration required by admins will be read here
  def __load_enforced_configuration(self):
    pass

  def set_type(self, service_type:  ServiceType) -> Service:
    self.service_type = service_type
    return self

  def add_port(self, service_port: ServicePort) -> Service:
    self.ports.add_port(service_port)
    return self

  # Service Labels

  def set_labels(self, labels: dict[str]) -> Service:
    self.labels = labels
    return self

  def add_label(self, key: str, value: str) -> Service:
    self.labels[key] = value
    return self

  # Service Selectors

  def set_selectors(self, selectors: dict[str]) -> Service:
    self.selector = selectors
    return self

  def add_selector(self, selector_key: str, selector_value: str) -> Service:
    self.selector[selector_key] = selector_value
    return self

  def render(self, chart: Chart) -> k8s.Service:
    self.__load_enforced_configuration()
    svc_spec = k8s.ServiceSpec(type=self.service_type.k8s_name(), ports=self.ports.render(), selector=self.selector)
    return k8s.Service(chart, 'service', spec=svc_spec)
