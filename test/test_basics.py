from helpers import environment, stdout_of, stderr_of
from constants import logstash_version_string


def test_logstash_is_the_correct_version():
    assert logstash_version_string in stdout_of('logstash --version')


def test_the_default_user_is_logstash():
    assert stdout_of('whoami') == 'logstash'


def test_that_the_user_home_directory_is_usr_share_logstash():
    assert environment('HOME') == '/usr/share/logstash'


def test_locale_variables_are_set_correctly():
    assert environment('LANG') == 'en_US.UTF-8'
    assert environment('LC_ALL') == 'en_US.UTF-8'


def test_opt_logstash_is_a_symlink_to_usr_share_logstash():
    assert stdout_of('realpath /opt/logstash') == '/usr/share/logstash'


def test_all_logstash_files_are_owned_by_logstash():
    assert stdout_of('find /usr/share/logstash ! -user logstash') == ''


def test_logstash_user_is_uid_1000():
    assert stdout_of('id -u logstash') == '1000'


def test_logstash_user_is_gid_1000():
    assert stdout_of('id -g logstash') == '1000'


def test_logging_config_does_not_log_to_files():
    assert stdout_of('grep RollingFile /logstash/config/log4j2.properties') == ''
