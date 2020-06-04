from __future__ import annotations

from imports import k8s
from cdk8s import Chart
from kubeasy.container import Container


class Containers(list):
  def add_container(self, container: Container) -> Containers:
    self.append(container)
    return self

  def add_new_container(self, name: str, image: str, tag: str, ports: list[int]) -> Containers:
    self.append(Container(name, image, tag).set_ports(ports))
    return self

  def get_container(self, index) -> Container:
    return self[index]

  def render(self, chart: Chart) -> list[k8s.Container]:
    containers = []
    for container_index in range(0, len(self)):
      containers.append(self.get_container(container_index).render(chart))
    return containers
