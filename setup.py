import setuptools
import os
from requirementslib import Lockfile

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    install_requires = Lockfile.load("Pipfile.lock").as_requirements()
)