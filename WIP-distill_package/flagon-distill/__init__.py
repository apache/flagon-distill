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

from elasticsearch_dsl.connections import connections

from distill.config.elasticsearch import ELASTICSEARCH_PARAMS


# Unpack Elasticsearch configuration and create elasticsearch connection
host = ELASTICSEARCH_PARAMS['host']
port = ELASTICSEARCH_PARAMS['port']
http_auth = ELASTICSEARCH_PARAMS['http_auth']
use_ssl = ELASTICSEARCH_PARAMS['use_ssl']
verify_certs = ELASTICSEARCH_PARAMS['verify_certs']
ca_certs = ELASTICSEARCH_PARAMS['ca_certs']
client_cert = ELASTICSEARCH_PARAMS['client_cert']
client_key = ELASTICSEARCH_PARAMS['client_key']
timeout = ELASTICSEARCH_PARAMS['timeout']

# Initialize Elasticsearch instance
es = connections.create_connection(hosts=host,
                                   port=port,
                                   http_auth=http_auth,
                                   use_ssl=use_ssl,
                                   verify_certs=verify_certs,
                                   ca_certs=ca_certs,
                                   client_cert=client_cert,
                                   client_key=client_key,
                                   timeout=timeout)
