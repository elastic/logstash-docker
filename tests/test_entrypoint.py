from .fixtures import logstash
from .helpers import run
import pytest

@pytest.mark.xfail
def test_whitespace_in_config_string_cli_flag():
    config = 'input{heartbeat{}}    output{stdout{}}'
    assert run("-t -e '%s'" % config).returncode == 0


def test_running_an_arbitrary_command():
    result = run('uname --all')
    assert result.returncode == 0
    assert 'GNU/Linux' in str(result.stdout)
