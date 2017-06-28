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

test: build
	bin/testinfra -v tests/

build: dockerfile docker-compose.yml env2yaml
	docker build --pull -t $(VERSIONED_IMAGE) build/logstash

demo: docker-compose.yml clean-demo
	docker-compose up

# Push the image to the dedicated push endpoint at "push.docker.elastic.co"
push: test
	docker tag $(VERSIONED_IMAGE) push.$(VERSIONED_IMAGE)
	docker push push.$(VERSIONED_IMAGE)
	docker rmi push.$(VERSIONED_IMAGE)

# The tests are written in Python. Make a virtualenv to handle the dependencies.
venv: requirements.txt
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txt
	touch venv

# Make a Golang container that can compile our env2yaml tool.
golang:
	docker build -t golang:env2yaml build/golang

# Compile "env2yaml", the helper for configuring logstash.yml via environment
# variables.
env2yaml: golang
	docker run --rm -i \
	  -v ${PWD}/build/logstash/env2yaml:/usr/local/src/env2yaml \
	  golang:env2yaml

# Generate the Dockerfile from a Jinja2 template.
dockerfile: venv templates/Dockerfile.j2
	jinja2 \
	  -D elastic_version='$(ELASTIC_VERSION)' \
          -D staging_build_num='$(STAGING_BUILD_NUM)' \
          -D version_tag='$(VERSION_TAG)' \
	  templates/Dockerfile.j2 > build/logstash/Dockerfile

# Generate docker-compose.yml from a Jinja2 template.
docker-compose.yml: venv templates/docker-compose.yml.j2
	jinja2 \
	  -D version_tag='$(VERSION_TAG)' \
	  templates/docker-compose.yml.j2 > docker-compose.yml

clean: clean-demo
	rm -f build/logstash/env2yaml/env2yaml build/logstash/Dockerfile
	rm -rf venv

clean-demo:
	docker-compose down
	docker-compose rm --force

.PHONY: build clean clean-demo demo push test
