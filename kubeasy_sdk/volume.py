from __future__ import annotations
from imports import k8s
from cdk8s import Chart
from typing import Mapping


from kubeasy_sdk.utils.resource import Rendered


class Volume(Rendered):
  def __init__(self, name: str, labels: Mapping[str, str] = None):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

    self.name = name
    self.labels = labels

  def render_k8s_resource(self, chart: Chart) -> k8s.Volume:
    pass


class EmptyDir(Volume):
  def __init__(self, name: str, size_limit: str, use_memory: bool):
    super().__init__(name)
    self.use_memory = use_memory
    self.size_limit = size_limit
    self.medium_map = {False: None, True: 'memory'}

  def render_k8s_resource(self, chart: Chart) -> k8s.Volume:
    volume_size = k8s.Quantity.from_string(self.size_limit)
    volume_source = k8s.EmptyDirVolumeSource(size_limit=volume_size, medium=self.medium_map[self.use_memory])
    return k8s.Volume(name=self.name, empty_dir=volume_source)


class ConfigMap(Volume):
  def __init__(self, name: str, config_name: str):
    super().__init__(name)
    self.config_name = config_name

  def render_k8s_resource(self, chart: Chart) -> k8s.Volume:
    volume_source = k8s.ConfigMapVolumeSource(name=self.config_name)
    return k8s.Volume(name=self.name, config_map=volume_source)
