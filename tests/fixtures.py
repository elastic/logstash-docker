import json
import yaml
import pytest
from .constants import image, container_name
from retrying import retry
from subprocess import run


@pytest.fixture()
def logstash(Process, Command, File):
    class Logstash:
        def __init__(self):
            self.name = container_name
            self.process = Process.get(comm='java')
            self.settings_file = File('/usr/share/logstash/config/logstash.yml')

        def start(self, args=None):
            if args:
                arg_array = args.split(' ')
            else:
                arg_array = []
            run(['docker', 'run', '-d', '--name', self.name] + arg_array + [image])

        def stop(self):
            run(['docker', 'kill', self.name])
            run(['docker', 'rm', self.name])

        def restart(self, args=None):
            self.stop()
            self.start(args)

        @retry(wait_fixed=1000, stop_max_attempt_number=60)
        def get_node_info(self):
            """Return the contents of Logstash's node info API.

            It retries for a while, since Logstash may still be coming up.
            Refer: https://www.elastic.co/guide/en/logstash/master/node-info-api.html
            """
            result = json.loads(Command.check_output('curl -s http://localhost:9600/_node'))
            assert 'workers' in result['pipelines']['main']
            return result

        def get_settings(self):
            return yaml.load(self.settings_file.content_string)

    return Logstash()
