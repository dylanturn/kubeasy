from __future__ import annotations

from typing import List

from imports import k8s

from kubeasy.utils.networking.container_port import ContainerPort


class ServicePort(object):

  def __init__(self, container_port: ContainerPort):
    self.name = container_port.name
    self.protocol = container_port.protocol
    self.port = container_port.port

  def render(self) -> k8s.ServicePort:
    cont_port_int_string = k8s.IntOrString.from_number(self.port)
    return k8s.ServicePort(name=self.name,
                           port=self.port,
                           protocol=self.protocol,
                           target_port=cont_port_int_string)

  @staticmethod
  def render_port_list(port_list: List[ServicePort]) -> List[k8s.ServicePort]:
    ports = []
    for port_index in range(0, len(port_list)):
      ports.append(port_list[port_index].render())
    return ports
