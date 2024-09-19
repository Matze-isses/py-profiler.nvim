from distutils.core import setup
from setuptools import find_packages

setup(
    name="nvim_trace",
    author="Matthis Ehrhardt",
    author_email="ehrhardt.matthis@gmail.com",
    description="Tracer module connecting to the neovim lua api!",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[]
)

