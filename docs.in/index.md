# An Open Source Data Integration Toolkit

## A human friendly data-oriented language

*hello.yaml*
```yaml
start:
    - insert:
        name: John Doe
        age: 80
    - print:
    - print: Hello $name$ your age is $age - 41$
```
To learn more about the language, check the [language documentation].


## A simple command line tool
*openpipe run hello.yaml*
```
{'name': 'John Doe', 'age': 80}
Hello John Doe your age is 39
```
To learn more about the tool, check the [tool documentation].


[language documentation]: /1.0/language
[tool documentation]: /1.0/language
