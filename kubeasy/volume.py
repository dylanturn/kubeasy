from __future__ import annotations
from imports import k8s
from cdk8s import Chart
from typing import Mapping


from kubeasy.utils.resource import Renderable


class Volume(Renderable):
  def __init__(self, name: str, labels: Mapping[str, str]):
    self.name = name
    self.labels = labels

  def render(self, chart: Chart) -> k8s.PersistentVolumeClaim:
    object_meta = k8s.ObjectMeta(labels=self.labels)
    persistent_volume_claim_spec = k8s.PersistentVolumeClaimSpec(volume_name=self.name)
    return k8s.PersistentVolumeClaim(chart, name=self.name, metadata=object_meta, spec=persistent_volume_claim_spec)
