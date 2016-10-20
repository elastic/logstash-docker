import subprocess
import os

version = os.environ['LOGSTASH_VERSION']
docker_image = 'docker.elastic.co/logstash/logstash:' + version


def docker_run(command):
    cli = ['docker', 'run', '--interactive', docker_image] + command.split()
    print(' '.join(cli))
    result = subprocess.run(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.stdout = result.stdout.rstrip()
    return result


def docker_env(varname):
    environ = {}
    for line in docker_run('env').stdout.decode().split("\n"):
        var, value = line.split('=')
        environ[var] = value
    return environ[varname]





