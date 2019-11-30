#!/bin/sh
set -e
rm -rf dist
/usr/bin/python3 setup.py sdist bdist_wheel
twine upload dist/*
