# Data Pipeline Language

## Introduction

This page describes the syntax and core concepts of the *data pipeline language*, an human friendly data-oriented language that can be used to describe data transformation workflows for both structured and unstructured data. DPL does not replace technology specific languages (e.g. SQL), instead it  provides an higher level computable language capable of integrating data from diverse formats, sources and technology.

## Prerequisites
DPL is entirely based on the [YAML] format. The knowledge of YAML is fundamental for the proper understanding of the material in this document. While in general the data processing operations will be described using markup language, when calculations and transformations are needed, a good understanding of [Python's Standard Data Types and Operations][python_std_types] is required.

## Concepts

### Pipeline
DPL follows the data pipeline design pattern: a set of data processing elements are connected in series, where the output of one element is the input of the next one.
In DPL the elements are referred as **steps**, and a sequence of steps is referred as a ***segment***. A pipeline document is a single YAML document that contains one or more segments.

#### Segments
A segment must be represented by a dictionary, where the key is the segment name and the value is a sequence of steps.

####  Steps

A step must be represented by a dictionary, where the key is an action name and the value contains the action parameters, parameters may be of any of the YAML supported data types.

#### Example

> pipeline.yaml
    ```yaml
    # This is the 'start' segment
    start:
        # Call the "print" action with the string parameter Hello World!
        - print: Hello World!
    ```

> Output:
    ```
    Hello World!
    ```

!!! Important "The start segment"
    Runnable pipelines must contain a segment named ***start*** . The first operation in that segment will receive a single input item with the system clock time.

#### Multiple Segments
A single pipeline may need to produce distinct outputs from the same input data, in order to support this some actions allow to send data to other segments.

### Integrated Development Environment
At this time there is no specialized IDE for pipeline editing, any general purpose IDE with a good support for YAML is suitable.

## Workflow Execution

The command line tool `openpipe` is the software that reads pipeline documents and starts the corresponding workflow.

### Action Plugins
After the pipeline document is loaded, openpipe associates each workflow step with a plugin instance, the plugin to be used will be determined by the action name and action parameters.  Plugins can provide a wide range of action types: collection, filtering, exporting, etc.

You can get the list of available plugins with:
```sh
openpipe help
```

You can get the help for a plugin with:
```
openpipe help «plugin_name»
```

OpenPipe action plugins may be polymorphic, meaning the same plugin may be able to handle different input and configuration types.

### Data Items
In DPL any kind of workflow managed data is referred as an _item_, in openpipe _items_ are stored in memory and transmitted as Python object references, as such, items can be of any data type or class available with Python.

### Data Flow

Action plugins should be observed as independent processing units, the following items will be available to them:

- Config Item: action parameters for the step «provided in the pipeline document»
- Input Item: input data provided for the action execution
- Output Item: output data produced by the action execution

!!! Information "Output -> Input"
    As a general rule the output item of a step will be the input item of the next step in the same segment, with the exception of the `test` and `duplicate` actions that can deliver items to the first step of other segments.

!!! Information "Last Step Output Items"
    Output items from the last step in a segment will be silently discarded.

### Dynamic Configuration

The configuration provided to steps may include dynamic components, this feature provides the ability to inject python expressions and data driven configuration.

Before invoking an action, any text in the action parameters found between consecutive dollar signs ($) will be evaluated as a python expression and replaced with it's result. If you need to have $ on your strings, you will need to escape them using \\$ .

You can inject input data in your configuration by using the special dict "_" in your python code. When evaluating dynamic configuration expressions, _ is a referenced o the input item.

Dynamic configuration allows you to provide python code/input data based configuration for most plugins. A plugin configuration item can use Python expressions, those expressions can refer to the input item.

In OPL any text between consecutive dollar signs ($) will be treated as a Python expression. When the input item is a dictionary, it's keys will be available as variables that can be used in the expression. The "_" variable is a special variable that refers to the entire input item content.

Examples:
> calc.yaml
    ```yaml
    start:
        - print: 2 + 1 = $2 + 1$
    ```

> Output:
    ```
    2 + 1 = 3
    ```

> input_item.yaml
    ```yaml
    start:
        - insert:
            place: zoo
        - print: $_$   # Print the input item
    ```

> input_field.yaml
    ```yaml
    start:
        - insert:
            animal: Elephant
            size: big
        - print: The $animal$ is $size$.
    ```


> Output:
    ```
    The Elephant is big.
    ```

## Plugin Libraries

!!! Warning

    The plugin API is not stable yet, the provided plugins are likely to break with openpipe upgrades.


A pipeline may contain a special segment named `libraries`. This segment must contain a list of local directories or urls for libraries containing additional plugins.

## Copyright and License

(C) 2019, João Pinto <lamego.pinto@gmail.com>

This document is distributed under the [Creative Commons Attribution 4.0 International License].

[YAML]: http://yaml.org/spec/1.1/
[python_std_types]: https://docs.python.org/3/library/stdtypes.html
[openpipe tool]: /OpenPipeTool

[Creative Commons Attribution 4.0 International License]: https://creativecommons.org/licenses/by/4.0/
