from .fixtures import logstash


def test_setting_pipeline_workers_from_environment(logstash):
    logstash.restart(args='-e pipeline.workers=6')
    assert logstash.get_node_info()['pipeline']['workers'] == 6


def test_setting_pipeline_batch_size_from_environment(logstash):
    logstash.restart(args='-e pipeline.batch.size=123')
    assert logstash.get_node_info()['pipeline']['batch_size'] == 123


def test_setting_pipeline_batch_delay_from_environment(logstash):
    logstash.restart(args='-e pipeline.batch.delay=36')
    assert logstash.get_node_info()['pipeline']['batch_delay'] == 36
