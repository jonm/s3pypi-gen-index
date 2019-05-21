# Copyright 2019 Jonathan T. Moore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import re

import boto3

def _set_logging():
    lvl = os.environ.get('LOG_LEVEL','INFO')
    names = { 'DEBUG' : logging.DEBUG, 'INFO' : logging.INFO,
              'WARN' : logging.WARN, 'WARNING' : logging.WARNING,
              'ERROR' : logging.ERROR, 'CRITICAL' : logging.CRITICAL,
              'FATAL' : logging.FATAL }
    if lvl not in names:
        logging.warn("unexpected LOG_LEVEL %s" % (lvl,))
        lvl = 'INFO'
    logging.getLogger().setLevel(names[lvl])

def _get_configuration():
    config = {}
    for v in ['INDEX_BUCKET']:
        config[v] = os.environ[v]
    return config

def handle(event, context):
    # cf. https://www.python.org/dev/peps/pep-0503/
    _set_logging()
    config = _get_configuration()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config['INDEX_BUCKET'])

    projects = []
    for obj in bucket.objects.all():
        if obj.key != "index.html" and obj.key.find("/") >= 0:
            path, filename = obj.key.split("/")
            if filename == "index.html" and path not in projects:
                projects.append(path)

    projects.sort()

    html = ("<!DOCTYPE html><html><body>" +
            ' '.join(map(lambda p: "<a href=\"./%s/\">%s</a>" % (p, p),
                         projects)) +
            "</body></html>")
    
    idx = s3.Object(config['INDEX_BUCKET'], 'index.html')
    idx.put(html)
        


