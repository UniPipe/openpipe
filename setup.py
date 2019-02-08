from setuptools import setup, find_packages

namespace_packages = ['openpipe', 'openpipe/plugins']
all_packages = find_packages()
all_packages.extend(namespace_packages)


setup(
    name="openpipe",
    packages=all_packages,
    entry_points={
        'console_scripts': [
            'openpipe = openpipe.__main__:main'
        ]
    }
)
