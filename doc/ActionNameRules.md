# Action Name Guidelines

## Action Name Syntax
This document servers as a guideline for selecting action names.

Action names must contain only ASCII letters and spaces.

1. The first word must be a `«verb»`
2. If it uses more than word, the last word must be an `«object»`

## Action Names to python modules mappings

The max allowed package depth is 2, if an action name contains more than 3 words, the module name is built concatenaning all the remaning words with '_'

```python
def action2module(action_name):
    action_words = action_name.split(' ', 2)
    package_name = action_words[:-1]
    module_name = action_words[-1].replace(' ', '_')
    return "openpipe.plugins." + ('.'.join(package_name + [module_name]))
```
