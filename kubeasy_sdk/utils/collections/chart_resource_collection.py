from __future__ import annotations

from typing import List
from kubeasy_sdk.utils.resource import Rendered
from cdk8s import Chart


class ChartResourceCollection(list):

  @staticmethod
  def combine(cls: List[ChartResourceCollection]) -> ChartResourceCollection:
    resource_collection = ChartResourceCollection()
    for collection in cls:
      for resource in collection:
        resource_collection.add_resource(resource)
    return resource_collection

  def add_resource(self, resource: Rendered) -> ChartResourceCollection:
    self.append(resource)
    return self

  def get_resource(self, index) -> Rendered:
    return self[index]

  def render(self, chart: Chart):
    for resource_index in range(0, len(self)):
      self.get_resource(resource_index).render(chart)
