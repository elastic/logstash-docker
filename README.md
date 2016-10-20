## Description

This repository contains the official [Logstash][logstash] Docker image from
[Elastic][elastic].

It currently provides a release candidate version of Logstash 5.0, and is thus
not recommended for production use.

## Image tags and hosting

The image is hosted in Elastic's own docker registry at `docker.elastic.co`.

The full path for this image is `docker.elastic.co/logstash/logstash`.

Available tags:

- `5.0.0-beta1`
- `5.0.0-rc1`
- `latest` -> `5.0.0-rc1`

## Quick start demo
Clone this repository, ensure you
have [docker-compose](https://docs.docker.com/compose/install/) installed if on Linux and run `make demo`. You will then have an example instance of Logstash running, with supporting containers running the following services:

* [Elasticsearch][elasticsearch-docker] for storing events.
* [Kibana][kibana-docker] for browsing and visualizing.
* Redis as a simple example of consuming data from other services.

### Example events
The demo container creates [heartbeat][heartbeat-input]
events every few seconds.  To see them in Kibana, point a browser at
`http://localhost:5601`, and log in with:

* Username: `elastic`
* Password: `changeme`.

In Kibana, click the "Create" button, then the "Discover" tab in the
left-hand navigation pane.

### Redis input
You can also telnet/nc to the redis port and try injecting messages into Redis (alternatively, use [redis-cli](http://redis.io/topics/quickstart)),
which Logstash will then ingest into Elasticsearch. Like this:

``` shell
$ telnet 127.0.0.1 6379
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
LPUSH logstash "I travelled from Redis to meet you."
:1
```

Of course, the Redis input in entirely optional. We simply show it here as one
example of the [many ways to ingest data with Logstash][ls-inputs].

### Monitoring APIs
New in Logstash 5.0, the [monitoring APIs][mon-apis] are available on port 9600:

``` shell
$ curl localhost:9600?pretty
{
  "host" : "8e8471b3e92f",
  "version" : "5.0.0-rc1",
  "http_address" : "0.0.0.0:9600",
  "build_date" : "2016-10-07T15:39:28+00:00",
  "build_sha" : "a02ab45df9385477e9d4a7c05bf2b1261edf9591",
  "build_snapshot" : false
}
```

### How does it work?
If you're curious about the demo configuration, you can see how it's defined
in:
* [docker-compose.demo.yml](./docker-compose.demo.yml)
* [examples/elastic-stack-demo/logstash.conf](./examples/elastic-stack-demo/logstash.conf)

[logstash]: https://www.elastic.co/products/logstash
[elastic]: https://www.elastic.co
[elasticsearch-docker]: https://github.com/elastic/elasticsearch-docker
[kibana-docker]: https://github.com/elastic/kibana-docker
[heartbeat-input]: https://www.elastic.co/guide/en/logstash/5.0/plugins-inputs-heartbeat.html
[redis-cli]: http://redis.io/topics/rediscli
[ls-inputs]: https://www.elastic.co/guide/en/logstash/5.0/input-plugins.html
[mon-apis]: https://www.elastic.co/guide/en/logstash/5.0/monitoring.html

### UDP input
The demo system will also accept arbitrary messages over UDP port 43448. One
to try it out is with Netcat, like so:

``` shell
echo 'I ride a horse called "UDP"' | nc -q1 -u localhost 43448
```

## Using the image

To save some keystrokes, first set:

``` shell
export ELASTIC_REG=docker.elastic.co/logstash
export LOGSTASH_VERSION=5.0.0-rc1
export LOGSTASH_IMAGE=$ELASTIC_REG/logstash:$LOGSTASH_VERSION
```

### Configuration

Logstash differentiates between two types of configuration:
['Settings' and 'Pipeline Configuration'][conf-types].

#### Pipeline Configuration

It's essential to place your pipeline configuration where it can be
found by Logstash. By default, the container will look in
`/logstash/pipeline/` for pipeline config files.

In this example we use a bind-mounted volume to provide the configs:

``` shell
docker run -it -v /my/logstash/configs/:/logstash/pipeline/ $LOGSTASH_IMAGE
```

Every file in the host directory `/my/logstash/configs/` will then be parsed
by Logstash as pipeline config.

If you don't provide configuration to Logstash, it will run with a minimal
config that simply echoes `stdin` to `stdout`, through the `rubydebug`
codec. Like this:

```
$ docker run -it $ELASTIC_REG/logstash:5.0.0-rc1
The stdin plugin is now waiting for input:
[2016-10-05T05:05:20,297][INFO ][logstash.pipeline        ] Starting pipeline {"id"=>"main", "pipeline.workers"=>8, "pipeline.batch.size"=>125, "pipeline.batch.delay"=>5, "pipeline.max_inflight"=>1000}
[2016-10-05T05:05:20,301][INFO ][logstash.pipeline        ] Pipeline main started
[2016-10-05T05:05:20,325][INFO ][logstash.agent           ] Successfully started Logstash API endpoint {:port=>9600}
Hi! I am typing this.
{
    "@timestamp" => 2016-10-05T05:07:01.141Z,
      "@version" => "1",
          "host" => "2f773d5a7f29",
       "message" => "Hi! I am typing this."
}
```
This configuration is baked into the image at `/logstash/pipeline/logstash.conf`.
If this is the behaviour that you are observing, ensure that your
pipeline configuration is getting picked up correctly, and that you are replacing
either `logstash.conf` or the entire `pipeline` directory.


#### Settings Files

We can provide settings files through bind-mounts too. Logstash expects to
find them at `/logstash/config/`.

It's possible to provide an entire directory, containing all needed files:

```
docker run -it -v /my/logstash/settings/:/logstash/config/ $LOGSTASH_IMAGE
```

...or just a single file

```
docker run -it -v ~/logstash.yml:/logstash/config/logstash.yml $LOGSTASH_IMAGE
```

[conf-types]: https://www.elastic.co/guide/en/logstash/5.0/config-setting-files.html


### Logging

By default, Logstash logs go to standard output.

### Operational notes

1. Use the env var `LS_JAVA_OPTS` to set heap size, e.g. to use 16GB
   use `-e LS_JAVA_OPTS="-Xms16g -Xmx16g"` with `docker run`. It is
   also recommended to set a memory limit for the container.

2. It is recommended to pin your deployments to a specific version of
   the Logstash Docker image, especially if you are using an
   orchestration framework like Kubernetes, Amazon ECS or Docker
   Swarm.

## Supported Docker versions

The images have been tested on Docker 1.12.1.

## Contributing, issues and testing

Acceptance tests for the image are located in the `test` directory, and can
be invoked with `make test`. Python 3.5 and virtualenv are required to run
the tests.

This image is built on [Ubuntu 16.04][ubuntu-1604].

[ubuntu-1604]: https://github.com/tianon/docker-brew-ubuntu-core/blob/188bcceb999c0c465b3053efefd4e1a03d3fc47e/xenial/Dockerfile
