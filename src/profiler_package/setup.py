
from distutils.core import setup
from setuptools import find_packages

setup(
    name="nvim_trace",
    author="Matthis Ehrhardt",
    author_email="ehrhardt.matthis@gmail.com",
    description="Webscraper for local server",
    version="0.1",
    packages=find_packages(),
    package_data={
        "": ['config/*.yml']
    },
    include_package_data=True,
    install_requires=[]
)

