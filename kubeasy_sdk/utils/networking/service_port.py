from __future__ import annotations

from typing import List

from cdk8s import Chart

from imports import k8s

from kubeasy_sdk.utils.networking.container_port import ContainerPort
from kubeasy_sdk.utils.resource import Rendered


class ServicePort(Rendered):

  def __init__(self, container_port: ContainerPort):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

    self.service_name = None
    self.name = container_port.name
    self.protocol = container_port.protocol
    self.port = container_port.port

  def set_service_name(self, service_name: str) -> ServicePort:
    self.service_name = service_name
    return self
  
  def render_k8s_resource(self, chart: Chart) -> k8s.ServicePort:
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
