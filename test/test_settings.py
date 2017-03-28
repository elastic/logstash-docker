from .fixtures import logstash


def test_setting_pipeline_workers_from_environment(logstash):
    logstash.restart(args='-e env2yaml=1 -e pipeline.workers=6')
    assert logstash.get_node_info()['pipeline']['workers'] == 6


def test_setting_pipeline_batch_size_from_environment(logstash):
    logstash.restart(args='-e env2yaml=1 -e pipeline.batch.size=123')
    assert logstash.get_node_info()['pipeline']['batch_size'] == 123


def test_setting_pipeline_batch_delay_from_environment(logstash):
    logstash.restart(args='-e env2yaml=1 -e pipeline.batch.delay=36')
    assert logstash.get_node_info()['pipeline']['batch_delay'] == 36


def test_setting_things_with_upcased_and_underscored_env_vars(logstash):
    logstash.restart(args='-e ENV2YAML=1 -e PIPELINE_BATCH_DELAY=24')
    assert logstash.get_node_info()['pipeline']['batch_delay'] == 24


def test_invalid_settings_in_environment_are_ignored(logstash):
    logstash.restart(args='-e cheese.ftw=true')
    assert not logstash.settings_file.contains('cheese.ftw')


def test_not_opting_in_to_experimental_env2yaml_support(logstash):
    logstash.restart(args='-e pipeline.batch.delay=47')  # No '-e env2yaml'
    assert logstash.get_node_info()['pipeline']['batch_delay'] != 47
