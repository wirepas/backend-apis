#!/usr/bin/env bash

set -e

TARGET_DIR=${TARGET_DIR:-"wrappers/python"}

cd "${TARGET_DIR}"

./utils/pull_protos.sh
./utils/compile_protos.sh
./utils/generate_wheel.sh
twine check dist/*
