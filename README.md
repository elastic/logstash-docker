[![Build Status](https://travis-ci.org/elastic/logstash-docker.svg?branch=master)](https://travis-ci.org/elastic/logstash-docker)

## Description

This repository contains the official [Logstash][logstash] Docker image from
[Elastic][elastic].

Documentation can be found on the [Elastic website](https://www.elastic.co/guide/en/logstash/current/docker.html).

[logstash]: https://www.elastic.co/products/logstash
[elastic]: https://www.elastic.co/

## Supported Docker versions

The images have been tested on Docker 17.03.1-ce

## Requirements
A full build and test requires:
* Docker
* GNU Make
* Python 3.5 with Virtualenv

## Contributing, issues and testing

Acceptance tests for the image are located in the `test` directory, and can
be invoked with `make test`.

This image is built on [Centos 7][centos-7].

[centos-7]: https://github.com/CentOS/sig-cloud-instance-images/blob/50281d86d6ed5c61975971150adfd0ede86423bb/docker/Dockerfile
