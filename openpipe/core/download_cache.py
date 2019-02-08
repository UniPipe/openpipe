import hashlib
import os
import zipfile
import urllib.request
from glob import glob
from os.path import expanduser, join, exists
from urllib.parse import urlparse


def download_and_cache(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'github.com':
        url += "/archive/master.zip"

    print("URL", url)

    cache_dir = join(expanduser("~"), ".openpipe", "libraries_cache")
    if not exists(cache_dir):
        os.makedirs(cache_dir, 0o700)
    libname_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    cached_lib_name = join(cache_dir, libname_hash)
    if not exists(cached_lib_name):
        zip_file_name = cached_lib_name + ".zip"
        try:
            os.unlink(zip_file_name)
        except FileNotFoundError:
            pass

        urllib.request.urlretrieve(url, zip_file_name)

        with zipfile.ZipFile(zip_file_name) as zf:
            zf.extractall(cached_lib_name)

    plugins_dir = glob(join(cached_lib_name, '*'))
    if len(plugins_dir) == 1 and not plugins_dir[0].endswith('openpipe'):
        cached_lib_name = plugins_dir[0]
    return cached_lib_name
