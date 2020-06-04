from __future__ import annotations
from imports import k8s
from cdk8s import Chart

from kubeasy.service import Service
from kubeasy.utils.networking import ServicePort
from kubeasy.utils.resource import Renderable


class Ingress(Renderable):

  def __init__(self, name: str, tls: bool, labels: dict = None):
    self.name = name
    self.tls = tls
    self.labels = labels

    self.__load_default_configuration__()

  # Configuration defaults will be read here
  def __load_default_configuration__(self):
    pass

  # Configuration required by admins will be read here
  def __load_enforced_configuration(self):
    pass

  def set_labels(self, labels: dict) -> Ingress:
    self.labels = labels
    return self

  def add_labels(self, key: str, value: str) -> Ingress:
    self.labels[key] = value
    return self

  def __create_object_meta(self):
    return k8s.ObjectMeta(labels=self.labels)

  def __create_ingress_tls(self, tls_hosts):
    if self.tls:
      return k8s.IngressTLS(hosts=tls_hosts, secret_name=None) # TODO: Figure out the secret business
    else:
      return None

  def render(self, chart: Chart) -> k8s.Ingress:
    pass


class SimpleIngress(Ingress):
  def __init__(self, name: str, tls: bool, service_name: str, service_port: ServicePort, labels: dict = None):
    super().__init__(name, tls, labels)
    self.service_name = service_name
    self.service_port = service_port.render()

  def render(self, chart: Chart) -> k8s.Ingress:
    self.__load_enforced_configuration()
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls([self.service_name])
    ingress_backend = k8s.IngressBackend(service_name=self.service_name, service_port=self.service_port)
    return k8s.Ingress(chart, "ingress", metadata=ingress_meta, spec=k8s.IngressSpec(backend=ingress_backend, tls=ingress_tls))


class FanOutIngress(Ingress):
  def __init__(self, name: str, hosts: list[str], tls: bool, service: Service):
    super().__init__(name, hosts, tls, service)
    self.rules = {}

  def add_rule(self, host: str, paths: list):
    self.rules[host] = paths

  def render(self, chart: Chart) -> k8s.Ingress:
    self.__load_enforced_configuration()
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls()

    http_rule_values = k8s.HTTPIngressRuleValue()
    k8s.HTTPIngressPath()

    ingress_rules = k8s.IngressRule(host="self", http=http_rule_values)

    return k8s.Ingress(chart, "ingress", metadata=ingress_meta, spec=k8s.IngressSpec(rules=ingress_rules, tls=ingress_tls))


class VirtualHostIngress(Ingress):
  def render(self, chart: Chart) -> k8s.Ingress:
    pass
