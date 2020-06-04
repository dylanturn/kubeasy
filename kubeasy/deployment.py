from __future__ import annotations
from imports import k8s
from cdk8s import Chart

from kubeasy.utils.collections.chart_resource_collection import ChartResourceCollection

from kubeasy.container import Container
from kubeasy.utils.collections.containers import Containers
from kubeasy.volume import Volume
from kubeasy.utils.security import SecurityContext


class Deployment(object):

  def render(self, chart: Chart) -> Deployment:
    # Create the metadata and label selectors for the deployment
    object_meta = k8s.ObjectMeta(labels=self.labels)
    label_selector = k8s.LabelSelector(match_labels=self.match_labels)

    # Generate the podspec templates for the deployment
    podspec = k8s.PodSpec(containers=self.containers.render(chart))
    podspec_template = k8s.PodTemplateSpec(metadata=object_meta, spec=podspec)

    # Use the podspec to create the deployment spec before finally returning the completed K8s Deployment.
    deployment_spec = k8s.DeploymentSpec(replicas=self.replicas, selector=label_selector, template=podspec_template)
    k8s.Deployment(chart, 'deployment', spec=deployment_spec)
    return self

  def __init__(self, name: str, namespace: str, environment: str, replicas: int = 1):
    self.name = name
    self.namespace = namespace
    self.environment = environment
    self.replicas = replicas

    self.labels = {}
    self.match_labels = {}

    self.image_pull_policy = None
    self.image_pull_secret = None

    self.pod_fs_gid = None

    self.init_containers = Containers()
    self.containers = Containers()
    self.volumes = ChartResourceCollection()

    # Security Context
    self.security_context = SecurityContext()

    # This is where certain provided values might be overridden.
    self.__read_defaults__()

  def __read_defaults__(self):
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/environment"] = self.environment

    self.match_labels["app.kubernetes.io/deployment"] = self.name
    self.match_labels["app.kubernetes.io/environment"] = self.environment

  def set_replicas(self, replicas: int) -> Deployment:
    self.replicas = replicas
    return self

  # Deployment Labels

  def set_labels(self, labels: dict[str]) -> Deployment:
    self.labels = labels
    return self

  def add_label(self, key: str, value: str) -> Deployment:
    self.labels[key] = value
    return self

  # Deployment Match Labels

  def set_match_labels(self, match_labels: dict[str]) -> Deployment:
    self.match_labels = match_labels
    return self

  def add_match_label(self, key: str, value: str) -> Deployment:
    self.match_labels[key] = value
    return self

  # === Security Settings ===

  # Image Policies

  def set_image_pull_policy(self, pull_policy: str) -> Deployment:
    self.image_pull_policy = pull_policy
    return self

  def set_image_pull_secret(self, pull_secret: str) -> Deployment:
    self.image_pull_secret = pull_secret
    return self

  def set_pod_fs_gid(self, pod_fs_gid: int) -> Deployment:
    self.pod_fs_gid = pod_fs_gid
    return self

  # Containers

  def add_container(self, container: Container) -> Container:
    self.containers.add_container(container)
    return container

  # Init Containers

  def add_init_container(self, container: Container) -> Container:
    self.init_containers.add_container(container)
    return container

  # Volume Mounts

  def add_volume_mount(self, volume: Volume) -> Volume:
    self.volumes.add_resource(volume)
    return volume
