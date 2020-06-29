from __future__ import annotations

from cdk8s import Chart

from imports import k8s
from kubeasy_sdk.utils.resource import Rendered


class ContainerPort(Rendered):
  def __init__(self, name: str, port: int, protocol: str = None):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

    self.name = name
    self.protocol = protocol.upper()
    self.port = port

  def render_k8s_resource(self, chart: Chart) -> k8s.ContainerPort:
    return k8s.ContainerPort(name=self.name, protocol=self.protocol, container_port=self.port)
