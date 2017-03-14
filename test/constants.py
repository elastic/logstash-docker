import os

java_version_string = 'openjdk version "1.8.0_121"'

try:
    version = os.environ['ELASTIC_VERSION']
except KeyError:
    version = open('version.txt').read().strip()

logstash_version_string = 'logstash ' + version
image = 'docker.elastic.co/logstash/logstash:' + version
container_name = 'logstash'
