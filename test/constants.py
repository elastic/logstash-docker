import os

try:
    version = os.environ['ELASTIC_VERSION']
except KeyError:
    version = open('version.txt').read().strip()

logstash_version_string = 'logstash ' + version  # eg. 'logstash 5.3.0'

if '-' not in version:
    # Then we don't have a "staging build number yet", look for one in the
    # environment just in case.
    try:
        version += '-%s' % os.environ['STAGING_BUILD_NUM']  # eg. '5.3.0-d5b30bd7'
    except KeyError:
        pass

image = 'docker.elastic.co/logstash/logstash:' + version
container_name = 'logstash'
