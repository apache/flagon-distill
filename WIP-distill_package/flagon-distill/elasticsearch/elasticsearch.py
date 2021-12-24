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

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

flagonClient = connections.create_connection('flagonTest', hosts=['localhost'], timeout=60)

# create new search object, using cluster alias and index name
AleS = Search(using='flagonTest', index="userale") \
#TO DO: Figure out how to integrate query builder
    .query("match", type="click") \
    .filter("term", target="a.ui big blue button") \
    .scan()

# execute search
response = AleS.execute()

# print Hello World test for total hits, should match kibana output
print(response.hits.total)

AleS = Search(using=client, index="my-index") \
    .filter("term", category="search") \
    .query("match", title="python")   \
    .scan() \
    .exclude("match", description="beta")

AleS.aggs.bucket('per_tag', 'terms', field='tags') \
    .metric('max_lines', 'max', field='lines')

response = AleS.execute()

for hit in response:
    print(hit.meta.score, hit.title)


