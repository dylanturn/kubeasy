from __future__ import annotations
from imports import k8s


class ContainerPort(object):
  def __init__(self, name: str = None, protocol: str = None, port: int = None):
    self.name = name
    self.protocol = protocol
    self.port = port

  def create_service(self):
    pass

  def render(self):
    return k8s.ContainerPort(name=self.name, protocol=self.protocol, container_port=self.port)
