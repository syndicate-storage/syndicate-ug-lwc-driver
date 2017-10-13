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
    'sgwcdriver',
    'sgwcdriver.lib',
    'sgwcdriver.plugins'
]

# detect plugins
plugins = os.listdir('src/sgwcdriver/plugins')
for plugin in plugins:
    if os.path.isdir(os.path.join('src/sgwcdriver/plugins', plugin)):
        packages.append('sgwcdriver.plugins.' + plugin)

# dependencies
dependencies = [
]

setup(
    name='sgwcdriver',
    version='0.1',
    description='Syndicate User Gateway Web-Cache Driver',
    url='https://github.com/syndicate-storage/syndicate-webcache-driver',
    author='Illyoung Choi',
    author_email='syndicate@lists.cs.princeton.edu',
    license='Apache 2.0',
    packages=packages,
    package_dir={
        'sgwcdriver': 'src/sgwcdriver'
    },
    install_requires=dependencies,
    zip_safe=False
)
