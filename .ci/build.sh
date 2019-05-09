#!/usr/bin/env bash

set -e
set -x

TARGET_DIR=${TARGET_DIR:-"wrappers/python"}

cd "${TARGET_DIR}"

./utils/compile_protos.sh
./utils/generate_wheel.sh
