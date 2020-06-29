
from cdk8s import Chart


class Rendered(object):

  def __init__(self, **kwargs):
    self.__load_default_configuration__(**kwargs)

  # Configuration defaults will be read here
  def __load_default_configuration__(self, **kwargs):
    print("Load default configs")
    print(self.__class__)

  # Configuration required by admins will be read here
  def __load_enforced_configuration__(self):
    print("Load enforced configs")
    print(self.__class__)

  # Perform any runtime validations we might have
  def __validate_resource__(self):
    print("Perform validations")
    print(self.__class__)

  # Render the resource after having performed config enforcement and validation
  def render(self, chart: Chart = None):
    self.__load_enforced_configuration__()
    self.__validate_resource__()
    return self.render_k8s_resource(chart)

  def render_k8s_resource(self, chart: Chart):
    pass