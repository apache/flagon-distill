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

FROM python:2

# install system wide deps
RUN apt-get -yqq update
RUN apt-get -yqq install nginx

# Install Supervisord
RUN pip install supervisor-stdout

# Add configuration files
ADD ./supervisord.conf /etc/supervisord.conf
ADD ./gunicorn.cfg /etc/gunicorn.cfg
ADD ./nginx.conf /etc/nginx/nginx.conf

# restart nginx to load the config
RUN service nginx stop

# start supervisor to run our wsgi server
CMD supervisord -c /etc/supervisord.conf -n 