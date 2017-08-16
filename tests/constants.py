import os
import pytest
from subprocess import run, PIPE

version = run('./bin/elastic-version', stdout=PIPE).stdout.decode().strip()

logstash_version_string = 'logstash ' + version  # eg. 'logstash 5.3.0'

try:
    if len(os.environ['STAGING_BUILD_NUM']) > 0:
        version += '-%s' % os.environ['STAGING_BUILD_NUM']  # eg. '5.3.0-d5b30bd7'
except KeyError:
    pass

container_name = 'logstash-test'
