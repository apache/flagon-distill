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
RUN apt-get -yqq install netcat

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4

ENV KIBANA_VERSION 4.5.4
ENV KIBANA_REPO_BASE http://packages.elasticsearch.org/kibana/4.5/debian

RUN echo "deb $KIBANA_REPO_BASE stable main" > /etc/apt/sources.list.d/kibana.list

# install kibana
RUN set -x \
	&& apt-get -yqq update \
	&& apt-get -yqq install --no-install-recommends kibana=$KIBANA_VERSION \
	&& rm -rf /var/lib/apt/lists/*

ENV PATH /opt/kibana/bin:$PATH

WORKDIR /opt/kibana

RUN set -ex \
	&& for path in \
		./config \
	; do \
		chown -R kibana:kibana "$path"; \
	done

COPY kibana.yml /opt/kibana/config

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

# Install Sense plugin
RUN kibana plugin --install elastic/sense

USER kibana

CMD ["/tmp/entrypoint.sh"]

# Run on port 5601
EXPOSE 5601