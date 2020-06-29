from __future__ import annotations
from imports import k8s
from cdk8s import Chart

import jmespath

from kubeasy_sdk.utils.networking.service_port import ServicePort
from kubeasy_sdk.utils.resource import Rendered


class IngressPath(Rendered):
  def __init__(self, service_name: str, backend_port: int, path: str = None):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

    self.name = service_name
    self.port = backend_port
    self.path = path

  def render_k8s_resource(self, chart: Chart) -> k8s.HttpIngressPath:
    ingress_backend = k8s.IngressBackend(service_name=self.name, service_port=k8s.IntOrString.from_number(self.port))
    return k8s.HttpIngressPath(backend=ingress_backend, path=self.path)


class Ingress(Rendered):
  def __init__(self, name: str, tls: bool, labels: dict = None):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

    self.name = name
    self.tls = tls
    self.labels = labels
    self.annotations = {}
    self.rules = []
    self.service_ports = []

  def set_labels(self, labels: dict) -> Ingress:
    self.labels = labels
    return self

  def add_labels(self, key: str, value: str) -> Ingress:
    self.labels[key] = value
    return self

  def annotate(self, key: str, value: str) -> Ingress:
    self.annotations[key] = value
    return self

  def __create_object_meta(self):
    return k8s.ObjectMeta(name=self.name, labels=self.labels, annotations=self.annotations)

  def __create_ingress_tls(self, tls_hosts: list = []):
    if self.tls:
      return k8s.IngressTls(hosts=tls_hosts, secret_name=None)  # TODO: Figure out the secret business
    else:
      return None

  def add_rule(self, host: str, backend_port: ServicePort, path: str = None):
    self.rules.append({"host": host, "path": path, "port": backend_port})

  def render_k8s_resource(self, chart: Chart) -> k8s.Ingress:
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls()

    host_list = jmespath.search("rules[].host", {"rules": self.rules})

    ingress_rules = []
    for host in host_list:
      backend_list = jmespath.search(f"rules[?host == '{host}'].port", {"rules": self.rules})

      for backend in backend_list:
        ingress_backend = k8s.IngressBackend(service_name=backend.service_name, service_port=k8s.IntOrString.from_number(backend.port))
        backend_paths = jmespath.search(f"rules[?host == '{host}'].path", {"rules": self.rules})

        http_ingress_paths = []
        if len(backend_paths) > 0:
          for path in backend_paths:
            http_ingress_paths.append(k8s.HttpIngressPath(backend=ingress_backend, path=path))
        else:
          http_ingress_paths.append(k8s.HttpIngressPath(backend=ingress_backend))

        ingress_rules.append(k8s.IngressRule(host=host, http=k8s.HttpIngressRuleValue(paths=http_ingress_paths)))

    ingress_spec = k8s.IngressSpec(rules=ingress_rules, tls=ingress_tls)
    return k8s.Ingress(scope=chart, name=self.name, metadata=ingress_meta, spec=ingress_spec)


class SimpleIngress(Ingress):

  def __init__(self, name: str, tls: bool, service_name: str, service_port: int, labels: dict = None):
    super().__init__(name, tls, labels)
    self.name = service_name
    self.port = service_port

  def render_k8s_resource(self, chart: Chart) -> k8s.Ingress:
    ingress_meta = self.__create_object_meta()
    ingress_tls = self.__create_ingress_tls([self.name])
    ingress_backend = k8s.IngressBackend(service_name=self.name, service_port=k8s.IntOrString.from_number(self.port))
    ingress_spec = k8s.IngressSpec(backend=ingress_backend, tls=ingress_tls)
    return k8s.Ingress(scop=chart, name=self.name, metadata=ingress_meta, spec=ingress_spec)
