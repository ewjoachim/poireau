import os
from setuptools import setup, find_packages
from pip import download, req

NAME = "poireau"

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'version.txt')) as version_file:
    VERSION = version_file.read().strip()

REQUIREMENTS = [
    requirement.req.__str__()
    for requirement in req.parse_requirements("requirements.txt", session=download.PipSession())
]

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
