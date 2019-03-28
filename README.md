# Openpipe: A human friendly data-oriented integration toolkit

Over the years while performing different roles within Information Technology, a significant part of my effort was devoted to data collection/analysis/transformation automation. I have lost the track to the number of sheets, shell and python scripts whose main purpose was to parse/filter/transform data.

Openpipe is and attempt to offer those automation capabilities in a more human-friendly and highly
reusable format.

To get a better understanding how openpipe can be used, take a look at https://www.openpipe.org/ .

[![PyPi](https://img.shields.io/pypi/v/openpipe.svg?style=flat-square)](https://pypi.python.org/pypi/openpipe)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

This python library provides the following packages:

- openpipe.cli: the command line interface
- openpipe.client: client modules for pipeline document loading/validation
- openpipe.pipeline: the pipeline manager and runtime for the 'local' pipeline engine
- openpipe.actions: the action modules to be used by pipeline runtime


[Openpipe tool]: https://www.openpipe.org/OpenpipeTool
[PyPA Code of Conduct]: https://www.pypa.io/en/latest/code-of-conduct/
