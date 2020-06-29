from __future__ import annotations

from typing import List

from imports import k8s
from kubeasy_sdk.utils.networking.service_port import ServicePort


class ServicePorts(List[k8s.ServicePort]):

  def add_port(self, service_port: ServicePort) -> ServicePort:
    self.append(service_port)
    return service_port

  def get_port(self, index) -> ServicePort:
    return self[index]

  def render(self) -> List[k8s.ServicePort]:
    ports = []
    for port_index in range(0, len(self)):
      ports.append(self.get_port(port_index).render())
    return ports
