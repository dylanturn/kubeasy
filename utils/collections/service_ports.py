from __future__ import annotations

from imports import k8s
from kubeasy.service import ServicePort


class ServicePorts(list):

  def add_port(self, service_port: ServicePort) -> ServicePorts:
    self.append(service_port)
    return self

  def add_new_port(self, port: int, name: str = None, target: int = None, protocol: str = None) -> ServicePorts:
    self.add_port(ServicePort(port=port, name=name, target=target, protocol=protocol))
    return self

  def get_port(self, index) -> ServicePort:
    return self[index]

  def render(self) -> list[k8s.ServicePort]:
    ports = []
    for port_index in range(0, len(self)):
      ports.append(self.get_port(port_index).render())
    return ports
