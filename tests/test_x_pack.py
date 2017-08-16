from .fixtures import logstash


def test_x_pack_installation(logstash):
    installed = ('x-pack') in logstash.stdout_of('/usr/share/logstash/bin/logstash-plugin list')
    if logstash.image_flavor == 'oss':
        assert not installed
    else:
        assert installed
