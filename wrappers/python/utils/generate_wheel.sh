#!/usr/bin/env bash
# Wirepas Oy

echo "generating the wheel"

rm -fr build || true
rm -fr dist || true

py3clean . || true
python3 setup.py clean --all
python3 setup.py sdist bdist_wheel
