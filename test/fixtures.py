import os
import pytest
import json
from retrying import retry
from .constants import version


class Logstash:
    def __init__(self, container_name, process):
        self.container_name = container_name
        self.process = process


@pytest.fixture()
def logstash(Process, File, TestinfraBackend, Command):
    return Logstash(
        container_name=TestinfraBackend.get_hostname(),
        process=Process.get(comm='java'),
    )


@pytest.fixture()
@retry(wait_fixed=1000, stop_max_attempt_number=120)
def node_info(Command):
    """ Return the contents of Logstash's node info API.

    Retries for a while, since Logstash may still be coming up.
    Refer: https://www.elastic.co/guide/en/logstash/master/node-info-api.html
    """
    return json.loads(Command('curl http://localhost:9600/_node').stdout)
