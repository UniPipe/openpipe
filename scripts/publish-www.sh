#!/bin/sh
set -eu
python -m openpipe.cli run docs/1.0/generate_actions_doc.yaml
mkdocs gh-deploy
