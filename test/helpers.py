import subprocess
import os
from .constants import image, version

try:
    version += '-%s' % os.environ['STAGING_BUILD_NUM']
except KeyError:
    pass


def run(command):
    cli = 'docker run --rm --interactive %s %s ' % (image, command)
    result = subprocess.run(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
