import os

java_version_string = 'openjdk version "1.8.0_121"'

try:
    version = os.environ['ELASTIC_VERSION']
except KeyError:
    version = open('version.txt').read().strip()

logstash_version_string = 'logstash ' + version

# Define some Logstash setting that we can set and then make assertions
# about.
pipeline_workers = 3
pipeline_batch_size = 123
pipeline_batch_delay = 10
