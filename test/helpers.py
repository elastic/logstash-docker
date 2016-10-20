import subprocess
import os

version = os.environ['LOGSTASH_VERSION']
docker_image = 'docker.elastic.co/logstash/logstash:' + version


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
