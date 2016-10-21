import subprocess
import os

version_tag = os.environ['LOGSTASH_VERSION']
if os.environ['STAGING_BUILD_NUM']:
    version_tag += '-'
    version_tag += os.environ['STAGING_BUILD_NUM']
docker_image = 'docker.elastic.co/logstash/logstash:' + version_tag


def run(command):
    cli = ['docker', 'run', '--rm', '--interactive', docker_image] + command.split()
    print(' '.join(cli))
    result = subprocess.run(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.stdout = result.stdout.rstrip()
    return result


def stdout_of(command):
    return(run(command).stdout.decode())


def stderr_of(command):
    return(run(command).stderr.decode())


def environment(varname):
    environ = {}
    for line in run('env').stdout.decode().split("\n"):
        var, value = line.split('=')
        environ[var] = value
    return environ[varname]
