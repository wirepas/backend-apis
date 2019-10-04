#!/usr/bin/env bash

set -e

TARGET_DIR=${TARGET_DIR:-"wrappers/python"}

cd "${TARGET_DIR}"

pip3 install dist/*.whl
pip3 install -r tests/requirements.txt
