from pathlib import Path
from time import sleep

import requests
import tomli

THIS_DIR = Path(__file__).parent

session = requests.Session()


def update_lib(lib, *, retry=0):
    pass


with (THIS_DIR / 'using.toml').open('rb') as f:
    table = tomli.load(f)

libs = table['libs']
for lib in libs:
    update_lib(lib)

libs.sort(key=lambda lib: lib['stars'], reverse=True)

with (THIS_DIR / 'using.toml').open('w') as f:
    for lib in libs:
        f.write('[[libs]]\nrepo = "{repo}"\nstars = {stars}\n'.format(**lib))
