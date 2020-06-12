from __future__ import annotations
from imports import k8s
from cdk8s import Chart

from kubeasy.utils.resource import Renderable


class IngressPath(Renderable):
  def __init__(self, service_name: str, backend_port: int, path: str = None):
    self.name = service_name
    self.port = backend_port
    self.path = path

  def render(self, chart: Chart) -> k8s.HttpIngressPath:
    ingress_backend = k8s.IngressBackend(service_name=self.name, service_port=k8s.IntOrString.from_number(self.port))
    return k8s.HttpIngressPath(backend=ingress_backend, path=self.path)


class Ingress(Renderable):

  def __init__(self, name: str, tls: bool, labels: dict = None):
    self.name = name
    self.tls = tls
    self.labels = labels
    self.rules = []
    self.__load_default_configuration__()

  # Configuration defaults will be read here
  def __load_default_configuration__(self):
    pass # TODO: This thing

  # Configuration required by admins will be read here
  def __load_enforced_configuration(self):
    pass # TODO: This thing

  def set_labels(self, labels: dict) -> Ingress:
    self.labels = labels
    return self

  def add_labels(self, key: str, value: str) -> Ingress:
    self.labels[key] = value
    return self

  def __create_object_meta(self):
    return k8s.ObjectMeta(labels=self.labels)

  def __create_ingress_tls(self, tls_hosts=[]):
    if self.tls:
      return k8s.IngressTls(hosts=tls_hosts, secret_name=None)  # TODO: Figure out the secret business
    else:
      return None

  def add_rule(self, host: str, ingress_path: IngressPath):
    self.rules.append({"host": host, "path": ingress_path})

  def render(self, chart: Chart) -> k8s.Ingress:
    self.__load_enforced_configuration()
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls()

    ingress_rules = []

    for rule in self.rules:
      print(rule)
      ingress_rules.append(k8s.IngressRule(host=rule["host"], http=rule.render(chart)))
      k8s.HttpIngressPath()
      k8s.HttpIngressRuleValue(paths=ingress_rules)

    ingress_spec = k8s.IngressSpec(rules=ingress_rules, tls=ingress_tls)
    return k8s.Ingress(chart, "ingress", metadata=ingress_meta, spec=ingress_spec)


class SimpleIngress(Ingress):

  def __init__(self, name: str, tls: bool, service_name: str, service_port: int, labels: dict = None):
    super().__init__(name, tls, labels)

    self.name = service_name
    self.port = service_port

  def render(self, chart: Chart) -> k8s.Ingress:
    self.__load_enforced_configuration()
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls([self.name])
    ingress_backend = k8s.IngressBackend(service_name=self.name, service_port=k8s.IntOrString.from_number(self.port))
    ingress_spec = k8s.IngressSpec(backend=ingress_backend, tls=ingress_tls)
    return k8s.Ingress(chart, "ingress", metadata=ingress_meta, spec=ingress_spec)
