from __future__ import annotations
from imports import k8s
from cdk8s import Chart

from kubeasy_sdk.container import Container
from kubeasy_sdk.utils.collections.containers import Containers
from kubeasy_sdk.utils.resource import Rendered
from kubeasy_sdk.volume import Volume
from kubeasy_sdk.utils.collections.volumes import Volumes
from kubeasy_sdk.utils.security import SecurityContext


class Deployment(Rendered):

  def __init__(self, name: str, namespace: str, environment: str, replicas: int = 1):
    func_locals = dict(locals())
    del func_locals['self']
    super().__init__(**func_locals)

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
    self.volumes = Volumes()

    # Security Context
    self.security_context = SecurityContext()

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

  def include_volume(self, volume: Volume) -> Volume:
    self.volumes.add_volume(volume)
    return volume

  def render_k8s_resource(self, chart: Chart) -> Deployment:

    # Create the metadata and label selectors for the deployment
    object_meta = k8s.ObjectMeta(labels=self.labels)
    label_selector = k8s.LabelSelector(match_labels=self.match_labels)

    # Generate the podspec templates for the deployment
    podspec = k8s.PodSpec(init_containers=self.init_containers.render(chart),
                          containers=self.containers.render(chart),
                          volumes=self.volumes.render(chart))

    podspec_template = k8s.PodTemplateSpec(metadata=object_meta,
                                           spec=podspec)

    # Use the podspec to create the deployment spec before finally returning the completed K8s Deployment.
    deployment_spec = k8s.DeploymentSpec(replicas=self.replicas, selector=label_selector, template=podspec_template)
    k8s.Deployment(chart, 'deployment', metadata=k8s.ObjectMeta(name=self.name), spec=deployment_spec)
    return self
