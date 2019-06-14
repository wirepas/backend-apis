#!/usr/bin/env bash

./.ci/install-devtools.sh

pip3 install -r dev-requirements.txt
pip3 install -r wrappers/python/requirements.txt
