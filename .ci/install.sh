#!/usr/bin/env bash

set -e
set -x

TARGET_DIR=${TARGET_DIR:-"wrappers/python"}

cd "${TARGET_DIR}"

pip3 install dist/*.whl