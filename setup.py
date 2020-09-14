import setuptools
import toml
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_install_requirements():
    try:
        # read my pipfile
        with open ('Pipfile', 'r') as fh:
            pipfile = fh.read()
        # parse the toml
        pipfile_toml = toml.loads(pipfile)
    except FileNotFoundError:
        return []    # if the package's key isn't there then just return an empty
    # list
    try:
        required_packages = pipfile_toml['packages'].items()
    except KeyError:
        return []

    # If a version/range is specified in the Pipfile honor it
    # otherwise just list the package
    return ["{0}{1}".format(pkg,ver) if ver != "*"
        else pkg for pkg,ver in required_packages]

setuptools.setup(
    name="kubeasy-py",
    version=os.getenv('KUBEASY_VERSION', "v0.0.0"),
    author="Dylan Turnbull",
    author_email="dylanturn@gmail.com",
    description="Kubernetes made easy!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanturn/kubeasy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires = get_install_requirements()
)