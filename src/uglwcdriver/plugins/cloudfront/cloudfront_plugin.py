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
CloudFront Plugin
"""
import logging
import urlparse
import uglwcdriver.lib.abstractlwc as abstractlwc

logger = logging.getLogger('syndicate_cloudfront_cdn')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('syndicate_cloudfront_cdn.log')
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

        cloudfront_config = config.get("cloudfront")
        if not cloudfront_config:
            raise ValueError("cloudfront configuration is not given correctly")

        self.cloudfront_config = cloudfront_config

        # parse map
        url_mappings = self.cloudfront_config.get("map")
        if not url_mappings:
            raise ValueError("cloudfront url mapping configuration is not given correctly")

        if not isinstance(url_mappings, list):
            raise ValueError("cloudfront url mapping configuration is not an array")

        self.url_mappings = url_mappings
        self.mappings = {}

        for url_mapping in self.url_mappings:
            host = url_mapping.get("host")
            host = host.encode('ascii', 'ignore')
            if not host:
                raise ValueError("cloudfront host is not given correctly")

            cdn_prefix = url_mapping.get("cdn_prefix")
            cdn_prefix = cdn_prefix.encode('ascii', 'ignore')

            key = None
            if host in ["*"]:
                key = "*"
            else:
                host_parts = urlparse.urlparse(host)
                host_scheme = None
                host_host = None
                if len(host_parts.scheme) > 0:
                    host_scheme = host_parts.scheme
                    host_host = host_parts.netloc
                else:
                    host_scheme = "http"
                    host_host = host_parts.path
                key = "%s://%s" % (host_scheme, host_host)

            if cdn_prefix:
                prefix_parts = urlparse.urlparse(cdn_prefix)
                prefix_scheme = None
                prefix_host = None
                if len(prefix_parts.scheme) > 0:
                    prefix_scheme = prefix_parts.scheme
                    prefix_host = prefix_parts.netloc
                else:
                    prefix_scheme = "http"
                    prefix_host = prefix_parts.path

                self.mappings[key] = (cdn_prefix, prefix_scheme, prefix_host)
            else:
                self.mappings[key] = (None, None, None)

    def translate(self, url):
        """
        make the URL accessible via the CloudFront CDN prefix
        """
        url_parts = urlparse.urlparse(url)

        url_scheme = None
        url_host = None
        url_scheme = url_parts.scheme
        url_host = url_parts.netloc

        key = "%s://%s" % (url_scheme, url_host)
        if key in self.mappings:
            _, prefix_scheme, prefix_host = self.mappings.get(key)
            if prefix_scheme and prefix_host:
                return '{}://{}/{}'.format(prefix_scheme, prefix_host, url_parts.path)
            else:
                return url
        else:
            # wildcard
            if "*" in self.mappings:
                _, prefix_scheme, prefix_host = self.mappings.get("*")
                if prefix_scheme and prefix_host:
                    return '{}://{}/{}{}'.format(prefix_scheme, prefix_host, url_parts.path)
                else:
                    return url

        return url
