FROM ubuntu:16.04
MAINTAINER Elastic Docker Team <docker@elastic.co>

ARG LOGSTASH_VERSION

# Install curl for downloading, Java for running Logstash/JRuby, and netbase
# to resolve a warning from JRuby (https://github.com/jruby/jruby/issues/3955).
RUN apt-get update && \
    apt-get install -y curl netbase openjdk-8-jdk-headless && \
    apt-get clean

# Provide a non-root user to run Logstash.
RUN adduser --disabled-password --gecos=logstash --uid=1000 logstash

# Add Logstash itself.
RUN curl -so - https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz | \
    tar zxf - -C /opt && \
    mv /opt/logstash-${LOGSTASH_VERSION} /opt/logstash && \
    chown --recursive logstash:logstash /opt/logstash
ENV PATH=/opt/logstash/bin:$PATH

# Ensure Logstash has a UTF-8 locale available.
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# Provide a minimal configuration, so that a simple 'docker run -it' will provide
# a good experience.
ADD config/stdin-stdout-rubydebug.conf /opt/logstash/conf.d/logstash.conf
USER logstash
CMD ["logstash", "-f", "/opt/logstash/conf.d/"]
