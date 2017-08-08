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

import itertools
import json
import collections

from elasticsearch import helpers

from distill import es


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

class GraphAnalytics (object):
    """
    Distill's graph analytics package. Apply graph algorithms
    to User Ale log data.
    """

    @staticmethod
    def generate_graph(app,
                       app_type='logs',
                       log_type='raw',
                       # version='0.2.0',
                       target_events=[],
                       time_range=['now-1h', 'now'],
                       size=20):
        """
        Return all elements from an application, possible matching against
        a specific event (e.g. click, mouseover, etc)
        """
        # @TODO ref_url filter

        # Filtering
        should_query = []
        if (target_events):
            for event in target_events:
                res = {
                    "term": {
                        "type": event
                    }
                }
                should_query.append(res)

        must_not_query = [
            {
                "term": {
                    "type": "mousedown"
                }
            },
            {
                "term": {
                    "type": "mouseup"
                }
            }
        ]

        filter_query = [
            {
                "term": {
                    "logType": log_type
                }
            },
            # {
            #     "term": {
            #         "useraleVersion": version
            #     }
            # }
        ]

        # Sort By Time
        sort_query = [
            {
                "clientTime": {
                    "order": "asc"
                }
            }
        ]

        # Timestamp range - date math
        timestamp_query = {
            "range": {
                "@timestamp": {
                    "gte": time_range[0],
                    "lte": time_range[1]
                }
            }
        }
        filter_query.append(timestamp_query)

        agg_query = dict()

        # Get all unique sessions
        session_query = {
                "terms": {
                    "field": "sessionID.keyword",
                    "min_doc_count": 1
                }
            }

        agg_query['sessions'] = session_query

        # Generating all top targets
        target_query = {
                "terms": {
                    "field": "target.keyword",
                    "min_doc_count": 1,
                    "size": size
                },
                "aggs": {
                    "events": {
                        "terms": {
                            "field": "type.keyword",
                            "min_doc_count": 1,
                            "size": size
                        }
                    }
                }
            }

        agg_query['targets'] = target_query

        # Main query
        query = {
            "sort": sort_query,
            "query": {
                "bool": {
                    "should": should_query,
                    "filter": filter_query,
                    "must_not": must_not_query,
                }
            },
            "aggs": agg_query
        }

        # Process Aggregate Results
        response = es.search(app, doc_type=app_type, body=query, size=0)

        # Only want to look at aggregations
        sessions = response['aggregations']['sessions']['buckets']
        allSessions = { x['key']: [] for x in sessions }
        intervalSessions = { x['key']: [] for x in sessions }

        # Deal with bar chart
        allTargets = response['aggregations']['targets']['buckets']

        # Re-execute query to get all hits
        iter = helpers.scan(es,
                            query=query,
                            index=app,
                            doc_type=app_type,
                            preserve_order=True)

        # Store all hits in the user's bucket.
        for elem in iter:
            data = elem['_source']
            if 'sessionID' in data:
                sessionID = data['sessionID']
                if sessionID in allSessions:
                    allSessions[sessionID].append(data)

        # Remove all duplicates (and only leave behind interval)
        # More than likely will need to create new list
        for sessionID in allSessions:
            data = allSessions[sessionID]

            newData = []
            intervalLog = []
            for curr, next in zip(data, data[1:]):
                target1 = curr['target']
                event1 = curr['type']
                target2 = next['target']
                event2 = next['type']

                if target1 != target2:
                    targetChange = int(True)
                    eventChange = int(False)
                    if event1 != event2:
                        eventChange = int(True)

                    # Starting over no matter what
                    # Based off of curr, update the log
                    curr['targetChange'] = targetChange
                    curr['typeChange'] = eventChange
                    curr['intervalCount'] = len(intervalLog)   # some number maybe 0
                    # if len(intervalLog) >= 2:
                    #     # Calculate duration
                    #     curr['duration'] = intervalLog[-1:]['clientTime'] - \
                    #                        intervalLog[0]['clientTime']
                    # else:
                    #     curr['duration'] = 0
                    newData.append(curr)
                    intervalLog = []
                else:
                    # They are the same
                    targetChange = int(False)
                    eventChange = int(False)
                    if event1 != event2:
                        eventChange = int(True)
                        # starting over
                        curr['targetChange'] = targetChange
                        curr['typeChange'] = eventChange
                        curr['intervalCount'] = len(intervalLog)
                        # if len(intervalLog) >= 2:
                        #     # Calculate duration
                        #     curr['duration'] = intervalLog[-1:]['clientTime'] - \
                        #                        intervalLog[0]['clientTime']
                        # else:
                        #     curr['duration'] = 0
                        newData.append(curr)
                        intervalLog = []
                    else:
                        # increase counter
                        intervalLog.append(curr)
            intervalSessions[sessionID] = newData


        newSessions = []

        # Generate all edges tied to a user
        # [ edge list, edge list, ... ]
        for k, v in intervalSessions.items():
            pairs = pairwise(v) # list of edges for a user
            newSessions.append(pairs)

        # Node Map
        node_list = []   # Need to keep 0-based index for sankey diagram
        links = []      # Aggregate sequence list
        node_map = set([])   # Final node map {"name": "foo", "id": 0"}

        # Align the sequences
        alignment = itertools.izip_longest(*newSessions)

        for step in alignment:
            # step through every users sequence
            c = collections.Counter()
            visitedLinks = []
            nodenames = set([])
            sources = set([])
            targets = set([])
            # Process all the edges
            for edge in step:
                if edge:
                    node1 = edge[0]
                    node2 = edge[1]

                    nodename1 = node1['target']
                    nodename2 = node2['target']

                    # Generate sequence ID
                    seqID = '%s->%s' % (nodename1, nodename2)

                    # @todo Ensure src and target are not the same (self-loop)
                    if nodename1 != nodename2:
                        # Add src and targetids
                        nodenames.add(nodename1)
                        nodenames.add(nodename2)
                        sources.add(nodename1)
                        targets.add(nodename2)

                        link = {
                            'sequenceID': seqID,
                            'sourceName': nodename1,
                            'targetName': nodename2,
                            'type': node1['type'],
                            # 'duration': node1['duration'],
                            'pathLength': len(node1['path']),
                            'targetChange': node1['targetChange'],
                            'typeChange': node1['typeChange']
                        }
                        visitedLinks.append(link)

            # How many users visited a sequence at this step
            counts = collections.Counter(k['sequenceID'] for k in visitedLinks if k.get('sequenceID'))

            # Append into growing node_list
            # map(lambda x: node_list.append(x), sources)
            # map(lambda x: node_list.append(x) if x not in sources, targets)

            # Only treat sources as new nodes if not visited already
            for x in sources:
                if x not in node_list:
                    node_list.append(x)

            # Treat all targets as new nodes
            map(lambda x: node_list.append(x), targets)

            map(lambda x: node_map.add(hashabledict({ "name": x,
                                                        "id": len(node_list) - 1 - node_list[::-1].index(x)})), sources)

            map(lambda x: node_map.add(hashabledict({ "name": x,
                                                        "id": len(node_list) - 1 - node_list[::-1].index(x)})), targets)

            for v in visitedLinks:
                # Pass through and update count, also generate src and target id
                v['value'] = counts[v['sequenceID']]
                # Last occurence is the src and target id
                v['source'] = len(node_list) -1 - node_list[::-1].index(v['sourceName'])
                v['target'] = len(node_list) -1 - node_list[::-1].index(v['targetName'])
                links.append(v)

        # Save everything
        res  = dict()
        res['bargraph'] = generate_bargraph(allTargets)
        res['sankey'] = {
            'links': links,
            'nodes': list(node_map)
        }

        with open('sankey.json', 'w') as outfile:
            json.dump(res, outfile, indent=4, sort_keys=False)

        # with open('data.txt', 'w') as outfile:
        #     json.dump(intervalSessions, outfile, indent=4, sort_keys=False)
        #
        # with open('query.json', 'w') as outfile:
        #     json.dump(query, outfile, indent=4, sort_keys=False)
        # Iterate first to get nodes
        # pairs = pairwise(iter)
        #
        # nodes = []
        # links = []

        # for p in pairs:
        #     node1 = p[0]['_source']
        #     node2 = p[1]['_source']

        #     # Append nodes to list
        #     nodes.append(node1['target'])
        #     nodes.append(node2['target'])

        # Iterate again to get edges
        # pairs = pairwise(iter2)

        # srcID = targetID = None
        # for p in pairs:
        #     node1 = p[0]['_source']
        #     node2 = p[1]['_source']
        #
        #     # Append nodes to list
        #     nodes.append(node1['target'])
        #     # nodes.append(node2['target'])
        #
        #     srcID = len(nodes) - 1
        #     targetID = len(nodes)
        #
        #     # if (node1['target'] != node2['target']):
        #     # Append links to list (remove self-loops)
        #     link = {
        #         'sourceID': srcID,
        #         'targetID': targetID,
        #         'sourceName': node1['target'],
        #         'targetName': node2['target'],
        #         'type': node1['type'],
        #         'duration': node1['duration'],
        #         'value': node1['count'],
        #         'pathLength': len(node1['path']),
        #         'targetChange': int(node1['targetChange']),
        #         'typeChange': int(node1['typeChange'])
        #     }
        #     links.append(link)
        #
        # # Get all unique nodes
        # # node_names = np.unique(nodes).tolist()
        # node_list = []
        #
        # for indx, name in enumerate(nodes):
        #     n = {'id': indx, 'name': name}
        #     node_list.append(n)
        #
        # # Remove self-loops
        # newLinks = []
        # for indx, elem in enumerate(links):
        #     srcID = elem['sourceID']
        #     targetID = elem['targetID']
        #
        #     if srcID != targetID:
        #         newLinks.append(elem)
        #

        #
        return res


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def generate_bargraph(data, filename='bargraph.json'):
    results = []
    for target in data:
        target_name = target['key']
        type_bucket = target['events']['buckets']
        for t in type_bucket:
            event = t['key']
            event_count = t['doc_count']
            res = {"target": target_name, "count": event_count, "type": event}
            results.append(res)

    return results

    # with open(filename, 'w') as outfile:
    #     json.dump(results, outfile, indent=4, sort_keys=False)

def generate_sankey(data, filename='sankey.json'):
    pass