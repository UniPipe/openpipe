# Action Name Guidelines

## Action Name Syntax
This document servers as a guideline for selecting action names.

Action names must contain only ASCII letters and spaces.

1. The first word must be a `«verb»`
2. The last would must be a `noun` or a `verb`

## Action Name to python module mapping

If more than one word is used, all the words except the last are taken as directories in the path to the module.

The last word is the module name, it gets an`"_"` appended to avoid module namespace collisions with other action names that may be under the same path.

Example:

```python
import openpipe.actions.insert_.py              # "insert" action
import openpipe.actions.insert.using.tag_.py    # "insert using tag" action
```

```python
def action2module(action_name):
    action_words = action_name.split(' ')
    package_name = action_words[:-1]
    if not '_' in package_name:
        module_name = action_words[-1] + "_"
    return "openpipe.actions." + ('.'.join(package_name + [module_name]))
```


read from archive... (.tar, .zip)
write to archive... (.tar, .zip)


read from... file/url
    auto_decoding based on mime type (gz/bz2/xv/text/json/yaml/xml)

write to... file/url
    auto_encoding based on mime type (gz/bz2/xv/text/json/yaml/xml)

transform from csv ... into dict
transform into csv ... from dict

transform from regex assign
transform from regex groups

update from string replace:
    "" :  [red: blue, big: small]
    "key_name1" : [red: blue, big: small]

update from regex replace:
    "" : [source_regex: target_string]

update from mapping:
    "x": [ "source_key_value": "target_key_value" ]

update from matching:
    "": [ "*abc*": "target_key_value" ]

update from regex matching:
    "": [ ".*abc*": "target_key_value" ]

update into date:
    timestamp: "%Y %M"

update from date:
    timestamp: "%Y %M"

