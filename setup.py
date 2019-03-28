import os
import io
from setuptools import setup, find_packages

# This file is  based on:
#   https://github.com/ines/wasabi/blob/master/setup.py


def setup_package():
    package_name = "openpipe"
    root = os.path.abspath(os.path.dirname(__file__))

    # Read in package meta from about.py
    about_path = os.path.join(root, package_name, "about.py")
    print("PATH is", about_path)
    with io.open(about_path, encoding="utf8") as f:
        about = {}
        exec(f.read(), about)

    # Get readme
    readme_path = os.path.join(root, "README.md")
    with io.open(readme_path, encoding="utf8") as f:
        readme = f.read()

    # Add meta packages
    namespace_packages = ["openpipe", "openpipe/actions"]
    all_packages = find_packages()
    all_packages.extend(namespace_packages)

    setup(
        name=package_name,
        description=about["__summary__"],
        long_description=readme,
        long_description_content_type="text/markdown",
        author=about["__author__"],
        author_email=about["__email__"],
        url=about["__uri__"],
        version=about["__version__"],
        license=about["__license__"],
        packages=all_packages,
        zip_safe=True,
        entry_points={"console_scripts": ["openpipe = openpipe.cli.__main__:main"]},
    )


if __name__ == "__main__":
    setup_package()
