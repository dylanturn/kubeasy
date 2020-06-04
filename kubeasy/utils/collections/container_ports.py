from __future__ import annotations

from imports import k8s
from kubeasy.utils.networking import ContainerPort


class ContainerPorts(list):
  def add_port(self, container_port: ContainerPort) -> ContainerPort:
    self.append(container_port)
    return self

  def get_container_port(self, index) -> ContainerPort:
    return self[index]

  def render(self) -> list[k8s.ContainerPort]:
    container_ports = []
    for container_port_index in range(0, len(self)):
      container_ports.append(self.get_container_port(container_port_index).render())
    return container_ports
