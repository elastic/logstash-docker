from helpers import docker_run, docker_env
from constants import java_version_string, logstash_version_string


def test_java_is_the_correct_version():
    assert docker_run('java -version').stderr.startswith(java_version_string)


def test_logstash_is_the_correct_version():
    assert docker_run('logstash --version').stdout == logstash_version_string


def test_the_default_user_is_logstash():
    assert docker_run('whoami').stdout == b'logstash'


def test_that_the_user_home_directory_is_slash_logstash():
    assert docker_env('HOME') == '/logstash'


def test_locale_variables_are_set_correctly():
    assert docker_env('LANG') == 'en_US.UTF-8'
    assert docker_env('LC_ALL') == 'en_US.UTF-8'
