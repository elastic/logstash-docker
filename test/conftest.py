from subprocess import run
from .constants import image, container_name


def pytest_configure(config):
    run(['docker', 'run', '-d', '--name', container_name, image])


def pytest_unconfigure(config):
    run(['docker', 'kill', container_name])
    run(['docker', 'rm', container_name])
