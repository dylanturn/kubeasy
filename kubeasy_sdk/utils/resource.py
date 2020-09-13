from cdk8s import Chart

#################################################################################################################
# TODO: There should be some plugin framework that makes it easy for users to define default and required configs
#################################################################################################################

###########################
# TODO: Make this a plugin!
###########################
# Configuration defaults will be read here
def __load_default_configuration__(self, **kwargs):
  #print(f"Load default configs for class: {self.__class__.__name__}")
  #print(f"Instance KWARGS: {kwargs}")

  # Load the defaults for containers
  if self.__class__.__name__ == 'Container':
    self.set_resource_request("cpu", "100m")
    self.set_resource_request("memory", "128Mi")
    self.set_resource_limit("cpu", "200m")
    self.set_resource_limit("memory", "256Mi")

###########################
# TODO: Make this a plugin!
###########################
# Configuration required by admins will be read here
def __load_enforced_configuration__(self):
  #print(f"Load enforced configs for class: {self.__class__.__name__}")

  if self.__class__.__name__ == 'Deployment':
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/environment"] = self.environment
    self.match_labels["app.kubernetes.io/name"] = self.name
    self.match_labels["app.kubernetes.io/environment"] = self.environment

  if self.__class__.__name__ == 'Service':
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/deployment"] = self.deployment.name
    self.labels["app.kubernetes.io/environment"] = self.environment
    self.selector = self.deployment.match_labels

###########################
# TODO: Make this a plugin!
###########################
# Perform any runtime validations we might have
def __validate_resource__(self):
  #print(f"Perform validations for class: {self.__class__.__name__}")
  pass


class Rendered(object):

  # Tries to make the process easier on users by loading defaults so they have less to worry about.
  def __init__(self, **kwargs):
    __load_default_configuration__(self, **kwargs)

  # Render the resource after having performed config enforcement and validation
  def render(self, chart: Chart = None):
    __load_enforced_configuration__(self)
    __validate_resource__(self)
    return self.render_k8s_resource(chart)

  # This is what needs to be overridden in each implementation.
  def render_k8s_resource(self, chart: Chart):
    pass