#!/usr/bin/env python

"""
   Copyright 2016 The Trustees of University of Arizona

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from setuptools import setup

import os

packages = [
    'uglwcdriver',
    'uglwcdriver.lib',
    'uglwcdriver.plugins'
]

# detect plugins
plugins = os.listdir('src/uglwcdriver/plugins')
for plugin in plugins:
    if os.path.isdir(os.path.join('src/uglwcdriver/plugins', plugin)):
        packages.append('uglwcdriver.plugins.' + plugin)

# dependencies
dependencies = [
]

setup(
    name='uglwcdriver',
    version='0.1',
    description='Locally-configurable web-cache driver for Syndicate UG ',
    url='https://github.com/syndicate-storage/syndicate-ug-lwc-driver',
    author='Illyoung Choi',
    author_email='syndicate@lists.cs.princeton.edu',
    license='Apache 2.0',
    packages=packages,
    package_dir={
        'uglwcdriver': 'src/uglwcdriver'
    },
    install_requires=dependencies,
    zip_safe=False
)
