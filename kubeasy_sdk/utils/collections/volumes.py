from __future__ import annotations

from imports import k8s
from cdk8s import Chart
from kubeasy_sdk.volume import Volume


class Volumes(list):
    def add_volume(self, volume: Volume) -> Volumes:
        self.append(volume)
        return self

    def get_volume(self, index) -> Volume:
        return self[index]

    def render(self, chart: Chart) -> list[k8s.Volume]:
        volumes = []
        for volume_index in range(0, len(self)):
            volumes.append(self.get_volume(volume_index).render(chart))
        return volumes
