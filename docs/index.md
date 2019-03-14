# An Open Data Integration Framework


## A human friendly data-oriented language:

*hello.yaml*
```yaml
start:
    - insert:
        name: John Doe
        age: 80
    - print:
    - print: Hello $name$ your age is $age - 41$
```

## A simple command line tool:
*openpipe run hello.yaml*
```
{'name': 'John Doe', 'age': 80}
Hello John Doe your age is 39
```
