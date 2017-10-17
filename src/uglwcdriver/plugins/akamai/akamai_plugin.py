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

"""
Akamai Plugin
"""
import logging
import urlparse
import uglwcdriver.lib.abstractlwc as abstractlwc

logger = logging.getLogger('syndicate_akamai_cdn')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('syndicate_akamai_cdn.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)


class plugin_impl(abstractlwc.awcbase):
    def __init__(self, config):
        logger.info("__init__")

        if not config:
            raise ValueError("wc configuration is not given correctly")

        akamai_config = config.get("akamai")
        if not akamai_config:
            raise ValueError("akamai configuration is not given correctly")

        self.akamai_config = akamai_config

        # we convert unicode (maybe) strings to ascii
        # since python-irodsclient cannot accept unicode strings
        cdn_prefix = self.akamai_config["cdn_prefix"]
        self.cdn_prefix = cdn_prefix.encode('ascii', 'ignore')
        if not self.cdn_prefix:
            raise ValueError("akamai CDN PREFIX is not given correctly")

        prefix_parts = urlparse.urlparse(prefix)
        self.prefix_scheme = None
        self.prefix_host = None
        if len(prefix_parts.scheme) > 0:
            self.prefix_scheme = prefix_parts.scheme
            self.prefix_host = prefix_parts.netloc
        else:
            self.prefix_scheme = "http"
            self.prefix_host = prefix_parts.path

    def translate(self, url):
        """
        make the URL accessible via the Akamai CDN prefix
        """
        url_parts = urlparse.urlparse(url)
        return '{}://{}/{}{}'.format(self.prefix_scheme, self.prefix_host, url_parts.netloc, url_parts.path)
