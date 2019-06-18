#!/usr/bin/env bash
set -e

ROOT_DIR=$(pwd)
TARGET_DIR=${TARGET_DIR:-"wrappers/python"}
cd "${TARGET_DIR}"

set -a
GH_RELEASE_PYTHON_VERSION=$(< wirepas_messaging/__init__.py  \
                     awk '/__version__/{print $NF}' | \
                     tr -d "\"")

GH_RELEASE_CANDIDATE="false"
GH_RELEASE_DRAFT="false"
GH_RELEASE_NAME="\"Release ${GH_RELEASE_PYTHON_VERSION}\""
GH_RELEASE_BODY="\"Please see attached CHANGELOG.md\""
set +a

if [[ ${GH_RELEASE_PYTHON_VERSION} =~ "rc" ]]
then
    echo "Release candidate"
    GH_RELEASE_CANDIDATE="true"
    GH_RELEASE_DRAFT="false"
    GH_RELEASE_NAME="\"Release candidate ${GH_RELEASE_PYTHON_VERSION}\""

elif [[ ${GH_RELEASE_PYTHON_VERSION} =~ "dev" ]]
then
    echo "Development version"
    GH_RELEASE_DRAFT="true"
    GH_RELEASE_NAME="\"Development version ${GH_RELEASE_PYTHON_VERSION}\""
fi

echo "version=${GH_RELEASE_PYTHON_VERSION},name=${GH_RELEASE_NAME}, body=${GH_RELEASE_BODY}, draft=${GH_RELEASE_DRAFT}, rc=${GH_RELEASE_CANDIDATE}"

cd "${ROOT_DIR}"
env | grep "GH_" > releases.env