"""
    Wirepas Messaging
    =================
    Installation script

    Copyright Wirepas Ltd 2019 licensed under Apache 2.0

    Please see License file for full text.
"""

import os
import re
import glob

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_file = "README.md"
license_file = "LICENSE"
requirements_file = "requirements.txt"

with open(readme_file) as f:
    long_description = f.read()


def custom_scheme():
    def custom_version(version):
        tag = str(version.tag)
        if version.exact:
            return tag

        # split on rc and compute a pre-release tag for the next patch
        tag_components = tag.rsplit("rc")
        major, minor, patch = tag_components[0].split(".")
        patch = int(patch) + 1
        distance = version.distance
        tag = f"{major}.{minor}.{patch}.dev{distance}"

        return tag

    return {
        "root": "../..",
        "version_scheme": custom_version,
        "local_scheme": "no-local-version",
        "write_to": "wrappers/python/version.py",
        "fallback_version": str(fallback_version["version"]),
    }


def get_list_files(root, flist=None):
    if flist is None:
        flist = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            flist.append(os.path.join(path, name))
    print("FLIST", flist)
    return flist


def get_absolute_path(*args):
    """ Transform relative pathnames into absolute pathnames """
    return os.path.join(here, *args)


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


about = {}
with open(get_absolute_path("./wirepas_messaging/__about__.py")) as f:
    exec(f.read(), about)

fallback_version = {}
try:
    with open(get_absolute_path("./version.py")) as f:
        exec(f.read(), fallback_version)
except FileNotFoundError:
    fallback_version["version"] = "0.1.0"


setup(
    name=about["__pkg_name__"],
    use_scm_version=custom_scheme,
    setup_requires=["setuptools_scm"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    classifiers=about["__classifiers__"],
    keywords=about["__keywords__"],
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=get_requirements(requirements_file),
    extras_require={"examples": ["websocket-client==0.48.0", "PyYAML==5.1.2"]},
    data_files=[
        (
            "./wirepas_messaging-extras/package",
            [readme_file, license_file, requirements_file, "setup.py"],
        ),
        (
            "./wirepas_messaging-extras/protos/wnt",
            glob.glob(get_absolute_path("wirepas_messaging/wnt/*.proto")),
        ),
        (
            "./wirepas_messaging-extras/protos/gateway",
            glob.glob(get_absolute_path("wirepas_messaging/gateway/*.proto")),
        ),
        (
            "./wirepas_messaging-extras/protos/wpe",
            glob.glob(get_absolute_path("wirepas_messaging/wpe/*.proto")),
        ),
        (
            "./wirepas_messaging-extras/protos/nanopb",
            glob.glob(get_absolute_path("wirepas_messaging/nanopb/*.proto")),
        ),
        (
            "./wirepas_messaging-extras/protos/google",
            glob.glob(get_absolute_path("wirepas_messaging/google/protobuf/*.proto")),
        ),
        (
            "./wirepas_messaging-extras/examples/wnt",
            glob.glob(get_absolute_path("examples/wnt/*.py")),
        ),
        (
            "./wirepas_messaging-extras/examples/wnt/",
            [get_absolute_path("examples/wnt/README.md")],
        ),
        (
            "./wirepas_messaging-extras/examples/wnt/assets",
            glob.glob(get_absolute_path("examples/wnt/assets/*")),
        ),
    ],
)
