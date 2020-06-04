from __future__ import annotations
from imports import k8s


class SecurityContext(object):
  def __init__(self, capabilities: dict = None, read_only_root_fs: bool = True, run_as_uid: int = 1000, run_as_gid: int = 1000, run_as_root: bool = False):

    self.capabilities = capabilities
    self.read_only_root_fs = read_only_root_fs
    self.run_as_uid = run_as_uid
    self.run_as_gid = run_as_gid
    self.run_as_non_root = run_as_root
    self.__read_defaults__()

  def __read_defaults__(self):
    pass

  def set_capabilities(self, capabilities: dict = None) -> SecurityContext:
    if capabilities is None:
      self.capabilities = k8s.Capabilities(drop=["ALL"])
    return self

  def set_ro_root_fs(self, read_only_root_fs: bool = True) -> SecurityContext:
    self.read_only_root_fs = read_only_root_fs
    return self

  def set_run_as_uid(self, run_as_uid: int = 1000) -> SecurityContext:
    self.run_as_uid = run_as_uid
    return self

  def set_run_as_gid(self, run_as_gid: int = 1000) -> SecurityContext:
    self.run_as_gid = run_as_gid
    return self

  def set_run_as_root(self, run_as_root: bool = False) -> SecurityContext:
    self.run_as_non_root = not run_as_root
    return self

  def render(self) -> k8s.SecurityContext:
    return k8s.SecurityContext(capabilities=self.capabilities,
                               privileged=False,
                               read_only_root_filesystem=self.read_only_root_fs,
                               run_as_group=self.run_as_gid,
                               run_as_user=self.run_as_uid,
                               run_as_non_root=self.run_as_non_root)
