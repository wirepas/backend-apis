#!/usr/bin/env bash

set -e

./.ci/install-devtools.sh

pip3 install -r dev-requirements.txt
