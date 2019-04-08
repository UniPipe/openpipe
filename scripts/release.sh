#!/bin/sh
set -e
rm -rf dist
/usr/bin/python setup.py sdist bdist_wheel
twine upload dist/*
