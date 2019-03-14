# The OpenPipe Language

## Introduction

This manual describes the syntax and core concepts of the OpenPipe Language, an human friendly data-oriented language that can be used to describe data transformation processes for both structured and unstructured data. It does not intend to be a replacement for domain/technology specific languages like SQL, instead it seeks to provide an higher level «but computable» language capable of integrating data using diverse formats, sources and technology.

## Data Pipeline Document
OPL follows a data pipeline approach: a set of data processing elements are connected in series, where the output of one element is the input of the next one.

### Prerequisites
OPL is entirely based on the [YAML] format. The knowledge of YAML is fundamental for the proper understanding of the material in this document.

In OPL these elements are referred as **steps**, and a sequence of operations is referred as a ***segment***, a data pipeline is a single YAML document that contains one or more segments.

### Segments
A segment must be represented by a dictionary, where the key is the segment name and the value is a sequence of operations.

### Steps
A step is represented by a dictionary, where the key is an action name, and the value is the action parameter, which may be of any of the YAML supported data types.

### Example

> pipeline.yaml
    ```yaml
    # This is the 'start' segment
    start:
        # Call the "print" action with the Hello World! parameter.
        - print: Hello World!
    ```

> Output:
    ```
    Hello World!
    ```

!!! Important "The start segment"
    Runnable pipelines must contain a segment named ***start*** . The first operation in that segment will receive a single input item with the system clock time.

### Multiple Segments

In complex pipelines it may be needed to produce distinct outputs from the same input data, in order to support this, an action may deliver data tot he first step of other segments.

## OPL Execution Engine


!!!NOTE "Out of Scope"
    - OPL does not set any specific data transmission media for communication between plugins. The data transfer is an implementation aspect of the OPL execution tool.
    - A future OPL tool implementation may leverage concurrent and parallel capabilities by associating multiple instances of a plugin with a single step.

## Conclusion

After reading this document you should be familiar with the fundamental concepts required to write a data pipeline, you can now explore the language by installing and using the [openpipe tool].

## Copyright and License

(C) 2019, João Pinto

This document is distributed under the [Creative Commons Attribution 4.0 International License].

[YAML]: http://yaml.org/spec/1.1/
[python_std_types]: https://docs.python.org/3/library/stdtypes.html
[Data Pipeline]: https://en.wikipedia.org/wiki/Pipeline_(computing)
[business process]: https://en.wikipedia.org/wiki/Business_process
[slices]: https://developers.google.com/edu/python/strings#string-slices
[openpipe tool]: /OpenPipeTool

[Creative Commons Attribution 4.0 International License]: https://creativecommons.org/licenses/by/4.0/

YAML supports both "vertical" and "horizontal" arrangement of items, the same example using the horizontal layout:

```yaml
hello_world: [ { print: "Hello World!" } ]
```
