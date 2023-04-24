from setuptools import setup
from setuptools import find_packages

setup(
    name='MPLRemoteGraphicsView',  # package name
    version='0.0.1',  # package version
    description='A matplotlib mutiprocessing plot lib',  # package description
    packages=find_packages(),
    package_dir={"MPLRemoteGraphicsView": "MPLRemoteGraphicsView"},
    license="MIT",
    author_email="moebius.ever@outlook.com",
    zip_safe=False,
)
