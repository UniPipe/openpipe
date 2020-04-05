# Openpipe Tool

## Introduction
The `openpipe` tool is a command line utility which runs on Linux, Mac and Windows and can be used to collect, transform and analyse data from multiple sources.

In order to use openpipe, you must either adapt existing pipeline examples, or create your own data pipelines, in any case it is strongly recommended that you read the [DPL language documentation] .

[Openpipe Language]: /OpenpipeLanguage

## Requirements
In order to use openpipe you must have Python 3 with pip installed. If you are using Windows and need help use the [Windows Python 3] install guide, if you are using Linux follow the appropriate instructions for your Linux distribution.

[Windows Python 3]: /Windows_Python_3_Install

# Install
Open a command line prompt/terminal and install the openpipe package:
```sh
pip install --user --upgrade openpipe
```

Getting Started
------------------------------------------------------
Using your preferred text editor, create a file named `pipeline.yaml` with the following content:

```yaml
# This is a simple example that pretty prints the content of a remote JSON file
start:
    - read from url: https://api.exchangeratesapi.io/latest
    - pprint:
```

Then just run the pipeline using:

```bash
openpipe run pipeline.yaml
```

------
To get a list of the action actions available in the standard library, run:
```bash
openpipe help
```
To get the help/example for a specific action, run:
```bash
openpipe help action name
```

Example:
```bash
openpipe help print
```

## Extra Actions Libraries

Openpipe supports additional actions libraries, you can check for available libraries with:
```sh
openpipe list-actions-lib
```

Install the required library with:

```sh
openpipe install-actions-lib «library_name»
```

Action libraries are maintained on GitHub repositories under the [openpipe-extra-actions] organization.

[openpipe-extra-actions]: https://github.com/openpipe-extra-actions/
[DPL language documentation]: /1.0/language