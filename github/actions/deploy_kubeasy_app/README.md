# Kubeasy Deployment Action

Kubeasy Deployment

## Inputs

### `kubeasy_version`
**Required** The version of Kubeasy that should be used.

### `deployment_file`
**Required** The python file that contains the Kubeasy deployment.

### `base64_kube_config`
**Required** The base64 encoded contents of a .kube/config file.

## Outputs
None, for now you just go look.

## Example usage

uses: actions/hello-world-docker-action@v1
with:
  who-to-greet: 'Mona the Octocat'

