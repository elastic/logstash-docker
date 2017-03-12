from .fixtures import node_info
from .constants import pipeline_workers, pipeline_batch_size, pipeline_batch_delay


def test_pipeline_workers(node_info):
    # This setting was changed from the default by an environement variable.
    assert node_info['pipeline']['workers'] == pipeline_workers


def test_pipeline_batch_size(node_info):
    # This setting was changed from the default by an environement variable.
    assert node_info['pipeline']['batch_size'] == pipeline_batch_size


def test_pipeline_batch_delay(node_info):
    # This setting was changed from the default by an environement variable.
    assert node_info['pipeline']['batch_delay'] == pipeline_batch_delay
