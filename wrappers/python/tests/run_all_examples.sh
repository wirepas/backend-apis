#!/usr/bin/env bash

set -e

cd examples/
for f in ./*.py
do
    echo "running ${f}"
    python ${f};

done
