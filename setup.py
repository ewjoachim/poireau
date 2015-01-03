import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="poireau",
    version="0.1.0",
    author="Joachim Jablon",
    author_email="ewjoachim@gmail.com",
    description="A choir files management website.",
    license="BSD",
    keywords="choir django",
    packages=find_packages(exclude="research"),
    long_description=read('README.md'),
    requirements=["Django==1.7.1"],
)
