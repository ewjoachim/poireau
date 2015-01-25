import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="poireau",
    version="0.2.0",
    author="Joachim Jablon",
    author_email="ewjoachim@gmail.com",
    description="A choir files management website.",
    license="BSD",
    keywords="choir django",
    packages=find_packages(exclude="research"),
    long_description=read('README.md'),
    install_requires=[
        "Django==1.7.3",
        "django-bootstrap3==5.0.3",
        "django-extensions==1.4.9",
        "django-debug-toolbar==1.2.2",
        "sh==1.11",
        "pytz==2014.10",
    ],
)
