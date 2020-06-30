from __future__ import annotations

from typing import Mapping

from imports import k8s
from cdk8s import Chart

from kubeasy_sdk.utils.collections.container_ports import ContainerPorts
from kubeasy_sdk.utils.request_limits import ContainerResources
from kubeasy_sdk.utils.security import SecurityContext
from kubeasy_sdk.utils.networking.container_port import ContainerPort
from kubeasy_sdk.utils.resource import Rendered


class Container(Rendered):

  def __init__(self, name: str, image: str, tag: str):
    self.name = name
    self.image = image
    self.image_pull_policy = "Always"
    self.image_pull_secret = None
    self.tag = tag
    self.ports = ContainerPorts()
    self.security_context = SecurityContext()
    self.resource_requirements = ContainerResources()

    self.command = []
    self.env_variables = {}

    self.liveness_probe_path = None
    self.liveness_probe_port = None
    self.readiness_probe_path = None
    self.readiness_probe_port = None

    self.volume_mounts = []

    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)


  # Container Command
  def set_command(self, command: list) -> Container:
    self.command = command
    return self

  # Environment Variables

  def set_env_variables(self, variables: dict[str]) -> Container:
    self.env_variables = variables
    return self

  def add_env_variable(self, key: str, value: str) -> Container:
    self.env_variables[key] = value
    return self

  # === Volume Stuff ===
  def mount_volume(self, name, mount_path, read_only=False) -> Container:
    self.volume_mounts.append(k8s.VolumeMount(name=name, mount_path=mount_path, read_only=read_only))
    return self

  # === Security ===

  def set_security_context(self, security_context: SecurityContext) -> Container:
    self.security_context = security_context
    return self

  # === Resource Limits and Requests ===
  def set_resource_limit(self, resource_name: str, resource_quantity):
    self.resource_requirements.add_limit(resource_name, resource_quantity)

  def set_resource_request(self, resource_name: str, resource_quantity):
    self.resource_requirements.add_request(resource_name, resource_quantity)

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

  def render_k8s_resource(self, chart: Chart) -> k8s.Container:

    if self.liveness_probe_path is not None and self.liveness_probe_port is not None:
      liveness_probe = k8s.Probe(http_get=k8s.HttpGetAction(port=self.liveness_probe_port,
                                                            path=self.liveness_probe_path))
    else:
      liveness_probe = None

    if self.readiness_probe_port is not None and self.readiness_probe_port is not None:
      readiness_probe = k8s.Probe(http_get=k8s.HttpGetAction(port=self.readiness_probe_port,
                                                            path=self.readiness_probe_path))
    else:
      readiness_probe = None

    return k8s.Container(name=self.name,
                         image=f"{self.image}:{self.tag}",
                         ports=self.ports.render(),
                         security_context=self.security_context.render(),
                         resources=self.resource_requirements.render(),
                         volume_mounts=self.volume_mounts,
                         command=self.command,
                         liveness_probe=liveness_probe,
                         readiness_probe=readiness_probe)
