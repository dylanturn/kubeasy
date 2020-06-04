from __future__ import annotations
from imports import k8s
from cdk8s import Chart


from kubeasy.utils.resource import Renderable


class Volume(Renderable):
  def __init__(self, name: str):
    pass
