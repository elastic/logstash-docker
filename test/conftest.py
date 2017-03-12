from subprocess import run
from .fixtures import version
from .constants import pipeline_workers, pipeline_batch_size, pipeline_batch_delay

image = 'docker.elastic.co/logstash/logstash:' + version
container = 'logstash'


def pytest_configure(config):
    run(['docker', 'run', '-d', '--name', container,
         '-e', 'pipeline.workers=%s' % str(pipeline_workers),
         '-e', 'pipeline.batch.size=%s' % str(pipeline_batch_size),
         '-e', 'pipeline.batch.delay=%s' % str(pipeline_batch_delay),
         image])


def pytest_unconfigure(config):
    run(['docker', 'kill', container])
    run(['docker', 'rm', container])
