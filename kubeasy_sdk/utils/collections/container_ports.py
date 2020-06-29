from __future__ import annotations
from imports import k8s
from kubeasy_sdk.utils.networking.container_port import ContainerPort


class ContainerPorts(dict):

  def add_port(self, name: str, port: int, protocol: str = "tcp") -> ContainerPort:
    container_port = ContainerPort(name=name, protocol=protocol, port=port)
    self[name] = container_port
    return container_port

  def get_port(self, name: str) -> ContainerPort:
    return self[name]

  def render(self, **kwargs) -> list[k8s.ContainerPort]:
    container_ports = []
    for port_name in self:
      container_ports.append(self.get_port(name=port_name).render())
    return container_ports
