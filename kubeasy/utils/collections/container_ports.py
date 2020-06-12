from __future__ import annotations

from typing import Mapping, Dict
from imports import k8s

from kubeasy.utils.networking.container_port import ContainerPort


class ContainerPorts(object):

  def __init__(self):
    self.ports = {}

  def add_port(self, name: str, port: int, protocol: str = "tcp") -> ContainerPort:
    container_port = ContainerPort(name=name, protocol=protocol, port=port)
    self.ports[name] = container_port
    return container_port

  def get_port(self, name: str) -> int:
    return self.ports[name].port

  def render(self) -> list[k8s.ContainerPort]:
    container_ports = []
    for port_name in self.ports:
      container_ports.append(k8s.ContainerPort(name=port_name, container_port=self.get_port(port_name)))
    return container_ports
