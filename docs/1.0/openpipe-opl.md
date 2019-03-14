 Most trivial data processing operations do not require the knowledge of any specific programming language. However when calculations and transformations are needed, a good understanding of  [Python's Standard Data Types and Operations][python_std_types] is required.

for this case you can use the `duplicate` plugin which will deliver a copy of all received items into the first step of one or more other segments.

The `test` plugin can be used to send input data to other segments depending on a conditional expression.


## Plugins

Plugins provide the data processing logic to is applied when some input is received. Every step in a pipeline is associated with a `plugin`. Plugins can provide a wide range of operation types: collection, filtering, exporting, etc. When a pipeline is run, a plugin instance is created for each step. A minimal set of plugins are available from the standard library, additional plugins can be provided using external libraries.


## Input, Output and Configuration Items

One of the great challenges of integrating data from different sources is data type diversity. OPL inputs, outputs and configurations are Python objects, in OPL we refer to them using the general term `item`. Input and output items can be of any object type available on Python while configuration items are restricted to those types representable on YAML.

The most common item types are: strings, integer numbers, float numbers, lists and dictionaries.


## Item parts
Some item types can be divided into indexable parts:

- strings - Parts can be extracted (but not changed) using [slices]
- lists - Parts can be read/changed using an integer positional index or [slices]
- dictionaries- Parts can be read/changed using index `keys`

### Item parts examples

```python
"look"[1]                                   # 'o'
"look"[2:4]                                 # 'ok'
["this", "is", "a", "list"][3]              # 'list'
{ "name": "John", "weight": 130}['name']    # 'John'
```

# Plugin Input/Output Polymorphism
OPL plugins can be polymorphic, meaning the same plugin may be able to handle different types of input and configuration item and apply different logic based on those types.

# Dynamic Configuration
Dynamic configuration allows you to provide dynamic/input driven based configuration for most plugins. A plugin configuration item can use Python expressions, those expressions can refer to the input item.

In OPL any text between consecutive dollar signs ($) will be treated as a Python expression. When the input item is a dictionary, it's keys will be available as variables that can be used in the expression. The "_" variable is a special variable that refers to the entire input item content.

### Dynamic Configuration Examples

``` yaml
start:
    - print: $_$                    # Print the entire input item
...
    - print: $name$                 # Print the input item ['name']
...
    - print: $2 * 10$               # Print 20
...
    - print: $price * unit_count$   # item['price'] * item ['unit_count']
```

!!!NOTE
    If you need to include a regular _"$"_ symbol as part of your configuration text, it needs to be escaped using double signs "$$" .

!!!danger "WARNING"
    Dynamic items are evaluated every time an input item is received, they should be used with caution as they allow to introduce arbitrary code and performance overhead.

## Duplicate
When dealing with complex data and/or processes it may be needed to apply conditional and/or distinct logic to the same input item. In this case the special plugin `copy to segment` must be used. It maintains the regular flow by delivering the input item to the next step, but it also delivers input items copies to the first step of every segment listed.

### Duplicate Examples

```yaml
start:
    - copy to segment: # Sends the start input item to the email_report and statistics segments
        - email_report
        - statistics
    - copy to segment: # send the start item to the selected_red_shoes segment
        - selected_red_shoes
email_report:
    ...
statistics:
    ...
selected_red_shoes:
    - select: $color is 'red'$
    ...
```

!!!NOTE
    When using `copy to segment`, the pipeline developer **must not** make any assumption about the order/concurrency of delivery and execution. The use of multiple segments is implicitly associated with a concurrency capability in the process.

## Plugin Libraries

A pipeline may contain a special segment named `libraries`. This segment must contain a list of local directories or urls for libraries containing additional plugins.

#### Plugin Libraries Examples

```yaml
libraries:
    - ~/Projects/openpipe-plugins/influxdb
```
