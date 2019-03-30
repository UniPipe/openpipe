import hashlib
import os
import zipfile
import urllib.request
from glob import glob
from shutil import rmtree, copytree
from os.path import expanduser, join, exists
from urllib.parse import urlparse
from wasabi import Printer
from tempfile import TemporaryDirectory
import pip._internal.req as pip_req
from pip._internal import main as pip_main
from pip._internal.utils.misc import get_installed_distributions


def download_and_cache(url, is_upgrade=False, auto_install=False):
    msg = Printer()
    parsed_url = urlparse(url)
    if parsed_url.netloc == "github.com":
        url += "/archive/master.zip"
    cache_dir = join(expanduser("~"), ".openpipe", "libraries_cache")
    if not exists(cache_dir):
        os.makedirs(cache_dir, 0o700)
    libname_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    cached_lib_name = join(cache_dir, libname_hash)
    if exists(cached_lib_name):
        if is_upgrade:
            rmtree(cached_lib_name)
    if not exists(cached_lib_name):
        zip_file_name = cached_lib_name + ".zip"
        try:
            os.unlink(zip_file_name)
        except FileNotFoundError:
            pass
        with msg.loading("Downloading... " + url):
            try:
                urllib.request.urlretrieve(url, zip_file_name)
            except:  # NOQA: E722, we really don't care about the error details
                print()
                msg.warn("WARNING: Unable to retrieve remote library")
                return None
        msg.good("Successfully downloaded ", url)
        with TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(zip_file_name) as zf:
                zf.extractall(tmpdirname)
                req_pattern = join(tmpdirname, "*", "requirements.txt")
                req_files = glob(req_pattern)
                if len(req_files) == 1:
                    check_requirements(req_files[0], auto_install)
                    copytree(tmpdirname, cached_lib_name)
        msg.good("Installed")

    actions_dir = glob(join(cached_lib_name, "*"))
    if len(actions_dir) == 1 and not actions_dir[0].endswith("openpipe"):
        cached_lib_name = actions_dir[0]

    return cached_lib_name


def check_requirements(requirements_filename, auto_install):
    installed_packages = [
        package.project_name for package in get_installed_distributions()
    ]
    missing_packages = []
    for item in pip_req.parse_requirements(
        requirements_filename, session="somesession"
    ):
        if isinstance(item, pip_req.InstallRequirement):
            if item.name not in installed_packages:
                missing_packages.append(item.name)
    if missing_packages:
        print("The plugin requires the following packages which are not available:")
        print("\n".join(["\t" + _ for _ in missing_packages]))
        if not auto_install:
            answer = input("Do you want to install them using pip ? (Y/N)").lower()
            if answer not in ("y", "yes"):
                print("Aborted for missing dependencies.")
                exit(1)
        for package_name in missing_packages:
            pip_main(["install", "--user", item.name])

    return
