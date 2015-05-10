import os
from setuptools import setup, find_packages

NAME = "poireau"

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'version.txt')) as version_file:
    VERSION = version_file.read().strip()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as readme_file:
    REQUIREMENTS = [line for line in readme_file.readlines() if line and not line.startswith(NAME)]

setup(
    name=NAME,
    version=VERSION,
    author="Joachim Jablon",
    author_email="ewjoachim@gmail.com",
    description="A choir files management website.",
    license="MIT",
    keywords="choir django",
    packages=find_packages(exclude="research"),
    long_description=README,
    install_requires=REQUIREMENTS,
)
