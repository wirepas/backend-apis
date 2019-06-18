"""
    Wirepas Messaging
    =================
    Installation script

    Wirepas Oy licensed under Apache 2.0

    Please see License file for full text.
"""
import codecs
import os
import re
import glob

from setuptools import setup, find_packages
from wirepas_messaging import __title__
from wirepas_messaging import __version__

with open("README.rst") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()


def setup_filter(flist, rules=None):

    if rules is None:
        rules = ["private", ".out"]

    for f in flist:
        for rule in rules:
            if rule in f:
                flist.pop(flist.index(f))
    return flist


def get_list_files(root, flist=None):
    if flist is None:
        flist = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            flist.append(os.path.join(path, name))
    return flist


def get_absolute_path(*args):
    """ Transform relative pathnames into absolute pathnames """
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, *args)


def get_requirements(*args):
    """ Get requirements requirements.txt """
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


setup(
    name=__title__,
    version=__version__,
    description="Wirepas messaging utilities",
    long_description=long_description,
    author="Wirepas Oy",
    author_email="opensource@wirepas.com",
    url="https://github.com/wirepas/backend-apis/tree/master/wrappers/python",
    license="Apache-2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
    keywords="wirepas connectivity iot mesh",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=get_requirements("requirements.txt"),
    data_files=[
        (
            "./wirepas_messaging-extras/package",
            ["LICENSE", "README.rst", "requirements.txt", "setup.py"],
        )
    ],
)
