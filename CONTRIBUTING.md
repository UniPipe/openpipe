# Contributing to openpipe

Thank you for considering contributing to this project. It is much appreciated. Read this guide carefully to avoid unnecessary work and disappointment for anyone involved.

## Filling bug reports

1. Test your issue with openpipe from the github master version:

```bash
pip install --user --upgrade https://github.com/Openpipe/openpipe/archive/master.zip
openpipe run your_test_pipeline.yaml
```

## Development contributions

Setting up your environment is pretty straight forward:

1. Fork the repository
2. `git clone` this repository to your machine
3. `cd` to where you've cloned the repository
4. Apply your improvements
5. Execute: `tox` to run the tests
6. Submit a pull request
