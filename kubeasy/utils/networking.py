from imports import k8s
from enum import Enum


class ContainerPort(object):
  def __init__(self, name: str = None, protocol: str = None, port: int = None):
    self.name = name
    self.protocol = protocol
    self.port = port

  def create_service(self):
    pass

  def render(self):
    return k8s.ContainerPort(name=self.name, protocol=self.protocol, container_port=self.port)


class ServiceType(Enum):
  CLUSTERIP = "ClusterIP"
  LOADBALANCER = "LoadBalancer"
  NODEPORT = "NodePort"

  def k8s_name(self) -> str:
    return '{0}'.format(self.value)


class ServicePort(object):
  def __init__(self, port: int, name: str = None, target: k8s.IntOrString = None, protocol: str = "tcp"):
    self.name = name
    self.protocol = protocol
    self.port = port
    self.target = target

  def render(self):
    return k8s.ServicePort(port=self.port, name=self.name, protocol=self.protocol, target_port=self.target)
