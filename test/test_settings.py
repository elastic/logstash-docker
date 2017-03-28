from .fixtures import logstash
import time


def test_setting_pipeline_workers_from_environment(logstash):
    logstash.restart(args='-e pipeline.workers=6')
    assert logstash.get_node_info()['pipeline']['workers'] == 6


def test_setting_pipeline_batch_size_from_environment(logstash):
    logstash.restart(args='-e pipeline.batch.size=123')
    assert logstash.get_node_info()['pipeline']['batch_size'] == 123


def test_setting_pipeline_batch_delay_from_environment(logstash):
    logstash.restart(args='-e pipeline.batch.delay=36')
    assert logstash.get_node_info()['pipeline']['batch_delay'] == 36


def test_setting_things_with_upcased_and_underscored_env_vars(logstash):
    logstash.restart(args='-e PIPELINE_BATCH_DELAY=24')
    assert logstash.get_node_info()['pipeline']['batch_delay'] == 24


def test_invalid_settings_in_environment_are_ignored(logstash):
    logstash.restart(args='-e cheese.ftw=true')
    assert not logstash.settings_file.contains('cheese.ftw')


def test_settings_file_is_untouched_when_no_settings_in_env(logstash):
    original_timestamp = logstash.settings_file.mtime
    original_hash = logstash.settings_file.sha256sum
    logstash.restart()
    time.sleep(1)  # since mtime() has one second resolution
    assert logstash.settings_file.mtime == original_timestamp
    assert logstash.settings_file.sha256sum == original_hash
