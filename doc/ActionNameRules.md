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
