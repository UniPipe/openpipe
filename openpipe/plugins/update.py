"""
# update

## Purpose
Update parts of input item

## Trigger
    - Input item is received

## Example 1
```yaml
start:
    - insert:   # Select from a list of dictionaries
        - bad word
        - good word
    - update:
        where: $ 'bad' in _ $
        set: "very good word"
    - print:
```

## Example 2
```yaml
start:
    - insert:   # Select from a list of dictionaries
        - { name: "Rose", gender: female, age: 17}
        - { name: "Bob", gender: male, age: 75 }
    - update:
        where: $ age < 18 $
        set:
            discount: 0.20  # Teens get a 20% discount
        else:
            discount: 0.10  # Everyone else gets 10%
    - pprint
```
"""
from openpipe.engine import PluginRuntime


class Plugin(PluginRuntime):
    """
        def on_input(self, item):

            # config becomes a merged dictionary with values from config replacing those from default_config
            # https://stackoverflow.com/a/26853961
            new_item = item.copy()
            new_item.update(self.config)

            self.put(new_item)
    """
    def on_start(self, config):
        if not isinstance(config, dict) or 'set' not in config:
            raise ValueError("The update plugin config must have a 'set' key ")

    # Output the configuration item
    def on_input(self, item):
        new_item = item
        where = self.config.get('where', True)
        if where is True:
            if isinstance(self.config['set'], dict):
                for key, value in self.config['set'].items():
                    new_item[key] = value
            else:
                new_item = self.config['set']
        if where is False and 'else' in self.config:
            if isinstance(self.config['else'], dict):
                for key, value in self.config['else'].items():
                    new_item[key] = value
            else:
                new_item = self.config['else']
        self.put(new_item)
