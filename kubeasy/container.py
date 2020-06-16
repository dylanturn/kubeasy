from __future__ import annotations

from typing import List, Mapping

from imports import k8s
from cdk8s import Chart

from kubeasy.utils.collections.container_ports import ContainerPorts
from kubeasy.utils.request_limits import ContainerResources
from kubeasy.utils.security import SecurityContext
from kubeasy.utils.networking.container_port import ContainerPort
from kubeasy.utils.resource import Renderable


class Container(Renderable):
  def __init__(self, name: str, image: str, tag: str):
    self.name = name
    self.image = image
    self.image_pull_policy = "Always"
    self.image_pull_secret = None
    self.tag = tag
    self.ports = ContainerPorts()
    self.security_context = SecurityContext()
    self.resource_requirements = ContainerResources()

    self.env_variables = {}

    self.liveness_probe_path = None
    self.liveness_probe_port = None
    self.readiness_probe_path = None
    self.readiness_probe_port = None

    self.volume_mounts = {}

    self.__load_default_configuration__()

  # Configuration defaults will be read here
  def __load_default_configuration__(self):
    pass

  # Configuration required by admins will be read here
  def __load_enforced_configuration(self):
    pass

  # Environment Variables

  def set_env_variables(self, variables: dict[str]) -> Container:
    self.env_variables = variables
    return self

  def add_env_variable(self, key: str, value: str) -> Container:
    self.env_variables[key] = value
    return self

  # === Security ===

  def set_resource_requirements(self, resource_requirements: ContainerResources) -> Container:
    self.resource_requirements = resource_requirements
    return self

  def set_security_context(self, security_context: SecurityContext) -> Container:
    self.security_context = security_context
    return self

  # === Networking ===

  def add_port(self, name: str, port: int) -> ContainerPort:
    return self.ports.add_port(name=name, port=port)

  def add_ports(self, ports: Mapping[str, int]) -> ContainerPorts:
    for port_name in ports:
      self.ports.add_port(name=port_name, port=ports[port_name])
    return self.ports

  # === Liveness and Readiness ===

  def set_liveness_probe(self, path: str, port: int) -> Container:
    self.liveness_probe_path = path
    self.liveness_probe_port = port
    return self

  def set_readiness_probe(self, path: str, port: int) -> Container:
    self.readiness_probe_path = path
    self.readiness_probe_port = port
    return self

  def render(self, chart: Chart) -> k8s.Container:
    self.__load_enforced_configuration()
    return k8s.Container(name=self.name,
                         image=f"{self.image}:{self.tag}",
                         ports=self.ports.render(),
                         security_context=self.security_context.render(),
                         resources=self.resource_requirements.render())
