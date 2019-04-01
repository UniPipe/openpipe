# Data Pipeline Language

## Introduction
---------------
This page describes the syntax and core concepts of the *data pipeline language*, an human friendly data-oriented language that can be used to describe data transformation workflows for both structured and unstructured data. DPL does not replace technology specific languages (e.g. SQL), instead it  provides an higher level computable language capable of integrating data from diverse formats, sources and technology.

## Prerequisites
DPL is entirely based on the [YAML] format. The knowledge of YAML is fundamental for the proper understanding of the material in this document. While in general the data processing operations will be described using markup language, when calculations and transformations are needed, a good understanding of [Python's Standard Data Types and Operations][python_std_types] is required.

## Concepts

### Pipeline
DPL follows the data pipeline design pattern: a set of data processing elements connected in series, where the output of one element is the input of the next one.
In DPL the elements are referred as **actions**, and a sequence of actions is referred as a ***segment***. A pipeline document is a single YAML document that contains one or more segments.

#### Segments
A segment must be represented by a dictionary, where the key is the segment name and the value is a sequence of actions.

!!! Warning "_segment name "
    Segment names started with "_" will not be loaded. They can be used to store configuration to be referenced with YAML anchors. The `_libraries` segment name has a special purpose explained later on this document.

#### Actions
An action must be represented by a dictionary, where the key is an action name and the value contains the action config, config may be of any of the YAML supported data types.

#### Example

> pipeline.yaml
    ```yaml
    # This is the 'start' segment
    start:
        # Call the "print" action with the config string Hello World!
        - print: Hello World!
    ```

> Output:
    ```
    Hello World!
    ```

!!! Important "The start segment"
    Runnable pipelines must contain a segment named ***start*** . The first operation in that segment will receive a single input item with openpipe run arguments.

#### Multiple Segments
A single pipeline may need to produce distinct outputs from the same input data, in order to support this some actions can send data to other segments.

### Integrated Development Environment
At this time there is no specialized IDE for pipeline editing, any general purpose IDE with a good support for YAML is suitable.

## Workflow Execution

### Document Loading
The command line tool `openpipe` is the software that reads a pipeline document file, loads it into the execution engine and activates the workflow.

### Action Modules
The execution engine loads the action modules associated with  action names, and creates action instances for every action defined in the pipeline. Action modules can provide a wide range of action types: collection, filtering, exporting, etc.

You can get the list of available actions with:
```sh
openpipe help
```

You can get the help for an action with:
```
openpipe help «action»
```

### Data Items
In DPL any kind of workflow managed data is referred as an _item_, in openpipe _items_ are stored in memory and transmitted as Python object references, as such, items can be of any data type or class available with Python.

### Data Flow

Action instances should be observed as independent processing units, the following items will be available to them:

- Input Item: the input data provided to the action
- Config Item: the config data that is based on the user provided config
- Output Item: output data produced by the action execution
- Tag Item: the tag

!!! Information "Output -> Input"
    As a general rule the output item of a action will be the input item of the next action in the same segment, with the exception of the `send to` action that can deliver items to the first action of other segments.

!!! Information "Last Action Output Items"
    Output items from the last action in a segment will be silently discarded.


### Dynamic Configuration

Action configuration items provided in the pipeline document, can include dynamic components. When an action is executed due to the reception of an input item, it's configuration is updated to reflect any changes in the input. This feature provides the ability to embed python expressions and action input data on it's configuration.

Before invoking the action input handling, any config text found between consecutive dollar signs ($) will be evaluated as a python expression and replaced with it's result. If you need to have '$' in your string, you will need to escape it using \\$ .

During expression evaluation, the "_" symbol is a reference to the full input item. When the input item is a dict, it's keys values will be mapped to variable names so that you can refer to them easily by providing $key$.

!!! Important
    Several actions use a default configuration of `$_$` which means the full input item will be used as the configuration item. It is the case of the `print` and `assert` actions.


Examples:
> calc.yaml
    ```yaml
    start:
        - print: 2 + 1 = $2 + 1$    # Print a sum result
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
        - print: $_$    # Print the full  input item
    ```

> input_field.yaml
    ```yaml
    start:
        - insert:
            animal: Elephant
            size: big
        - print: The $animal$ is $size$. # Print some fields
    ```


> Output:
    ```
    The Elephant is big.
    ```

### Data Tagging

One of the challenges of using independent pipeline actions with a strict input/output pattern is the need to correlate/aggregate outputs from different actions. Openpipe addresses this with the support for data tagging. Items flowing through a pipeline can be tagged, a tag is a piece of information that will be transmitted with every item as it is sent to the _after tagging actions in the pipeline.

Let's assume as example that we want to produce the count of 'a' letters from a list of files:
```yaml
start:
    - iterate: [/etc/passwd, /etc/group]
    - read from file: $_$
    # The read from file outputs only the file content, we can't refer to
    # the file name anymore
    - print: The number of 'a's in file is $ _.count(b'a') $
```
In order to persist the file name, we need to tag it before the the _read from file_ action.  After being tagged, we can refer to it with the special reference `$_tag$` :
```yaml
start:
    - iterate: [/etc/passwd, /etc/group]
    - tag: $_$ # The filename is tagged, tag is available on every next action
    - read from file: $_$
    # We can now use $_tag_
    - print: The number of 'a's in file $_tag$ is $ _.count(b'a') $
```

When more than two items need to be tagged, a dictionary based tag needs to be used, every tag will be merged into the tag dict.

```yaml
    # do some action
    tag: { animal_type: $_$ }   # Tag it as animal type
    # do some other action
    tag: { animal_size: $_$ }   # Tag it as animal size
    # We can now use $_tag['animal_type']$ and $_tag['animal_size']$
```


## Action Libraries

A pipeline may contain a special segment named `_libraries`. This segment must contain a list of local directories or urls for libraries containing additional actions.

## Copyright and License

© 2019 CCS Group International

This document is distributed under the [Creative Commons Attribution 4.0 International License].

[YAML]: http://yaml.org/spec/1.1/
[python_std_types]: https://docs.python.org/3/library/stdtypes.html
[openpipe tool]: /OpenpipeTool

[Creative Commons Attribution 4.0 International License]: https://creativecommons.org/licenses/by/4.0/
