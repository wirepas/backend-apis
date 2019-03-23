#!/usr/bin/env bash

cd examples/
for f in ./*.py
do
    echo "running ${f}"
    python ${f};

done;
