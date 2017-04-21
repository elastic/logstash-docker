SHELL=/bin/bash
export PATH := ./bin:./venv/bin:$(PATH)

ifndef ELASTIC_VERSION
export ELASTIC_VERSION := $(shell cat version.txt)
endif

ifdef STAGING_BUILD_NUM
VERSION_TAG=$(ELASTIC_VERSION)-${STAGING_BUILD_NUM}
else
VERSION_TAG=$(ELASTIC_VERSION)
endif

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSIONED_IMAGE=$(IMAGE):$(VERSION_TAG)

test: venv build
	bin/testinfra -v test/

build: dockerfile env2yaml
	docker build --pull -t $(VERSIONED_IMAGE) build/logstash

demo: clean-demo
	docker-compose --file docker-compose.demo.yml up

push: build test
	docker push $(VERSIONED_IMAGE)

# The tests are written in Python. Make a virtualenv to handle the dependencies.
venv: requirements.txt
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txt
	touch venv

# Make a Golang container that can compile our env2yaml tool.
golang:
	docker build -t golang:env2yaml build/golang

env2yaml: golang
	docker run --rm -i \
	  -v ${PWD}/build/logstash/env2yaml:/usr/local/src/env2yaml \
	  golang:env2yaml


# Generate the Dockerfile from a Jinja2 template.
dockerfile: venv templates/Dockerfile.j2
	jinja2 \
	  -D elastic_version='$(ELASTIC_VERSION)' \
	  -D version_tag='$(VERSION_TAG)' \
	  templates/Dockerfile.j2 > build/logstash/Dockerfile

clean: clean-demo
	docker-compose down
	docker-compose rm --force
	rm -f build/logstash/env2yaml/env2yaml build/logstash/Dockerfile
	rm -rf venv

clean-demo:
	docker-compose --file docker-compose.demo.yml down
	docker-compose --file docker-compose.demo.yml rm --force

.PHONY: build clean clean-demo demo push test
