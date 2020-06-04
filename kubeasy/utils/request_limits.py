from __future__ import annotations
from imports import k8s


class ContainerResources(object):

  def __init__(self):
    self.requests = {}
    self.limits = {}
    self.__read_defaults__()

  def __read_defaults__(self):
    self.add_request("cpu", "100m")
    self.add_request("memory", "128Mi")

    self.add_limit("cpu", "200m")
    self.add_limit("memory", "256Mi")

  def add_request(self, resource_name: str, resource_quantity) -> ContainerResources:
    if (type(resource_quantity) is int) or (type(resource_quantity) is float):
      self.requests[resource_name] = k8s.Quantity.from_number(resource_quantity)
    elif type(resource_quantity) is str:
      self.requests[resource_name] = k8s.Quantity.from_string(resource_quantity)

    else:
      raise Exception("uhoh, this isn't a string, int, or float!")
    return self

  def set_requests(self, requests: dict) -> ContainerResources:
    for request_key, request_value in requests:
      self.add_request(request_key, request_value)
    return self

  def add_limit(self, resource_name: str, resource_quantity) -> ContainerResources:

    if (type(resource_quantity) is int) or (type(resource_quantity) is float):
      self.limits[resource_name] = k8s.Quantity.from_number(resource_quantity)
    elif type(resource_quantity) is str:
      self.limits[resource_name] = k8s.Quantity.from_string(resource_quantity)
    else:
      raise Exception("uhoh, this isn't a string, int, or float!")
    return self

  def set_limits(self, limits: dict) -> ContainerResources:
    for limit_key, limit_value in limits:
      self.add_limit(limit_key, limit_value)
    return self

  def render(self) -> k8s.ResourceRequirements:
    return k8s.ResourceRequirements(requests=self.requests, limits=self.limits)
