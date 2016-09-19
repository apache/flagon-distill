# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Ubuntu Xenial 16.04 [LTS]
FROM ubuntu:16.04

# install system wide deps
RUN apt-get -yqq update
RUN apt-get -yqq install openjdk-8-jre
RUN apt-get -yqq install wget 
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4

ENV LOGSTASH_VERSION 1:2.3.4-1
ENV LOGSTASH_REPO_BASE http://packages.elasticsearch.org/logstash/2.3/debian

RUN echo "deb $LOGSTASH_REPO_BASE stable main" > /etc/apt/sources.list.d/logstash.list

# install logstash
RUN set -x \
	&& apt-get -yqq update \
	&& apt-get -yqq install --no-install-recommends logstash=$LOGSTASH_VERSION \
	&& rm -rf /var/lib/apt/lists/*

ENV PATH /opt/logstash/bin:$PATH

# Get GeoIP DB
#RUN set -x \
#	&& wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz \
#	&& gunzip GeoIP.dat.gz \
#	&& mkdir -p /usr/share/GeoIP \
#	&& mv GeoIP.dat /usr/share/GeoIP

ADD logstash.conf /etc/logstash/conf.d/logstash.conf
ADD userale.json /etc/logstash/conf.d/userale.json