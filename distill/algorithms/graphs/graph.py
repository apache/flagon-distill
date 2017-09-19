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

class GraphAnalytics (object):
    """
    Distill's graph analytics package. Apply graph algorithms
    to User Ale log data.
    """

    @staticmethod
    def generate_graph(app,
                       app_type='logs',
                       log_type='raw',
                       targets=[],
                       events=[],
                       time_range=['now-1h', 'now'],
                       size=20):
        """
        Return all elements from an application, possible matching against
        a specific event type (e.g. click, mouseover, etc)
        """
        # @TODO ref_url filter

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
                },
            },
        ]

        # Filtering
        should_query = []
        must_query = []

        # Include these events in the request
        if events:
            include_events = {
                "terms": {
                    "type.keyword": events
                }
            }
            filter_query.append(include_events)

        target_in = targets[0]
        target_out = targets[1]

        if target_in:
            include_targets = {
                "terms": {
                    "target.keyword": target_in
                }
            }

            filter_query.append(include_targets)

        # Remove these elementids from result set
        for target in target_out:
            res = {
                "term": {
                    "target.keyword": target
                }
            }
            must_not_query.append(res)

        # Finish off should query
        # must_query.append({"bool": {"should": should_query}})

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
                    "field": "sessionID",
                    "min_doc_count": 1
                }
            }

        agg_query['sessions'] = session_query

        # Generating all top targets and breakdowns by type, including path_length
        target_query = {
                "terms": {
                    "field": "target",
                    "min_doc_count": 1,
                    "size": size
                },
                "aggs": {
                    "events": {
                        "terms": {
                            "field": "type",
                            "min_doc_count": 1,
                            "size": size
                        }
                    },
                    "top_target": {
                        "top_hits": {
                            "script_fields": {
                                "path_length": {
                                    "script": {
                                        "lang": "painless",
                                        "inline": "doc['path'].length;"
                                    }
                                }
                            },
                            "size": 1
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
                    # "must": must_query,
                    # "should": should_query,
                    "filter": filter_query,
                    "must_not": must_not_query,
                    # "minimum_should_match": len(should_query) - 1
                }
            },
            "_source": {
                "includes": ['*'],
            },
            "script_fields": {
                "path_length": {
                    "script": {
                        "lang": "painless",
                        "inline": "doc['path'].length;"
                    }
                }
            },
            "aggregations": agg_query
        }

        # return query
        # Process Aggregate Results
        response = es.search(app, doc_type=app_type, body=query, size=0)
        # Only want to look at aggregations
        sessions = response['aggregations']['sessions']['buckets']
        # allSessions = { x['key']: [] for x in sessions }
        # intervalSessions = { x['key']: [] for x in sessions }

        # Deal with bar chart
        allTargets = response['aggregations']['targets']['buckets']

        # Re-execute query to get all hits
        iter = helpers.scan(es,
                            query=query,
                            index=app,
                            doc_type=app_type,
                            preserve_order=True)

        allSessions = dict()
        # Store all hits in the user's bucket.
        for elem in iter:
            data = elem['_source']
            data['pathLength'] = elem['fields']['path_length'][0]
            if 'sessionID' in data:
                sessionID = data['sessionID']
                if sessionID in allSessions:
                    allSessions[sessionID].append(data)
                else:
                    allSessions[sessionID] = [data]

        # This fixed sequence/interval logging that what was produced in
        # UserALE.js v 0.2.0
        # Possible to remove self-loops here as well (html->html->html->window) := (html->window)
        intervalSessions = dict()
        for sessionID in allSessions:
            data = allSessions[sessionID]
            newData = []
            intervalLog = []
            pairs = zip(data, data[1:])

            for curr, next in pairs:
                target1 = curr['target']
                event1 = curr['type']
                target2 = next['target']
                event2 = next['type']
                if target1 != target2: # ignore self-loops
                    targetChange = int(True)
                    eventChange = int(False)
                    if event1 != event2:
                        eventChange = int(True)

                    # Starting over no matter what
                    # Based off of curr, update the log
                    curr['targetChange'] = targetChange
                    curr['typeChange'] = eventChange
                    curr['intervalCount'] = len(intervalLog)   # some number maybe 0
                    if len(intervalLog) >= 2:
                        # Calculate duration
                        curr['duration'] = intervalLog[-1:]['clientTime'] - \
                                           intervalLog[0]['clientTime']
                    else:
                        curr['duration'] = 0
                    newData.append(curr)
                    intervalLog = []
                # else:
                #     # They are the same
                #     targetChange = int(False)
                #     eventChange = int(False)
                #     if event1 != event2:
                #         eventChange = int(True)
                #         # starting over
                #         curr['targetChange'] = targetChange
                #         curr['typeChange'] = eventChange
                #         curr['intervalCount'] = len(intervalLog)
                #         # if len(intervalLog) >= 2:
                #         #     # Calculate duration
                #         #     curr['duration'] = intervalLog[-1:]['clientTime'] - \
                #         #                        intervalLog[0]['clientTime']
                #         # else:
                #         #     curr['duration'] = 0
                #         newData.append(curr)
                #         intervalLog = []
                #     else:
                #         # increase counter
                #         intervalLog.append(curr)
            intervalSessions[sessionID] = newData

        # return intervalSessions
        newSessions = []

        # Generate all edges tied to a user
        # [ edge list, edge list, ... ]
        for k, v in intervalSessions.items():
            pairs = pairwise(v) # list of edges for a user
            newSessions.append(pairs)

        # Node Map
        node_list = []   # Need to keep 0-based index for sankey diagram
        links = []      # Aggregate sequence list
        node_map = []   # Final node map {"name": "foo", "id": 0"}

        # Align the sequences
        alignment = itertools.izip_longest(*newSessions)
        src_ids = {}
        target_ids = {}

        for i, step in enumerate(alignment):
            # print(i)
            c = collections.Counter()
            visitedLinks = []
            # visitedLinksUnique = set([])
            nodenames = set([])

            for edge in step:   # for a single step look at all links
                if edge:
                    node1 = edge[0]
                    node2 = edge[1]
                    session = node1['sessionID']
                    nodename1 = node1['target']
                    nodename2 = node2['target']

                    seqID = '%s->%s' % (nodename1, nodename2)
                    #print(seqID)

                    if nodename1 != nodename2:  #double check again for self-loops
                        #print(node1)
                        link = {
                            'sequenceID': seqID,
                            'sourceName': nodename1,
                            'targetName': nodename2,
                            'type': node1['type'],
                            'duration': node1['duration'],
                            'pathLength': len(node1['path']) if node1['path'] is not None else 0,
                            'targetChange': node1['targetChange'],
                            'typeChange': node1['typeChange']
                        }
                        visitedLinks.append(link)

            # Done with visits in a step. Now calculate counts
            counts = collections.Counter(k['sequenceID'] for k in visitedLinks if k.get('sequenceID'))
            # print(counts)
            visitedLinksUnique = { v['sequenceID']:v for v in visitedLinks}.values()
            # print(visitedLinksUnique)

            # Visit unique links and generate src/targetid
            if len(node_map) == 0:
                for link in visitedLinksUnique:
                    # Add all sources
                    if link['sourceName'] not in src_ids:
                        node_map.append({"name": link['sourceName']})
                        src_ids[link['sourceName']] = len(node_map)-1

                    # Add all targets
                    if link['targetName'] not in target_ids:
                        node_map.append({"name": link['targetName']})
                        target_ids[link['targetName']] = len(node_map)-1

            else:
                src_ids = target_ids    # sources were previous targets
                target_ids = {}
                for link in visitedLinksUnique:
                    # Add all sources
                    # if link['sourceName'] not in src_ids.values():
                    #     node_map.append(link['sourceName'])
                    #     src_ids[len(node_map)-1] = link['sourceName']

                    # Add all targets
                    if link['targetName'] not in target_ids:
                        node_map.append({"name": link['targetName']})
                        target_ids[link['targetName']] = len(node_map)-1

            for link in visitedLinksUnique:
                # Perform lookup for ids
                # Perform lookup for counts
                link['source'] = src_ids[link['sourceName']]
                link['target'] = target_ids[link['targetName']]
                link['value'] = counts[link['sequenceID']]

                links.append(link)

        # for step in alignment:
        #     # step through every users sequence
        #     c = collections.Counter()
        #     visitedLinks = []
        #     nodenames = set([])
        #
        #     # Process all the edges
        #     for edge in step:
        #         if edge:
        #             node1 = edge[0]
        #             node2 = edge[1]
        #
        #             nodename1 = node1['target']
        #             nodename2 = node2['target']
        #
        #             # Add src and targetids
        #             nodenames.add(nodename1)
        #             nodenames.add(nodename2)
        #
        #             # Generate sequence ID
        #             seqID = '%s->%s' % (nodename1, nodename2)
        #
        #             # @todo Ensure src and target are not the same (self-loop)
        #             if nodename1 != nodename2:
        #                 link = {
        #                     'sequenceID': seqID,
        #                     'sourceName': nodename1,
        #                     'targetName': nodename2,
        #                     'type': node1['type'],
        #                     # 'duration': node1['duration'],
        #                     'pathLength': len(node1['path']),
        #                     'targetChange': node1['targetChange'],
        #                     'typeChange': node1['typeChange']
        #                 }
        #                 visitedLinks.append(link)
        #
        #     # How many users visited a sequence at this step
        #     counts = collections.Counter(k['sequenceID'] for k in visitedLinks if k.get('sequenceID'))
        #     # print(counts)
        #     # Append into growing node_list
        #     map(lambda x: node_list.append(x), nodenames)
        #
        #     # map(lambda x: node_map.append({ "name": x}
        #     #                                 "id": len(node_list) - 1 - node_list[::-1].index(x)}), nodenames)
        #
        #     map(lambda x: node_map.append({ "name": x}), nodenames)
        #                                     # "id": len(node_list) - 1 - node_list[::-1].index(x)}), nodenames)
        #     for v in visitedLinks:
        #         # Pass through and update count, also generate src and target id
        #         v['value'] = counts[v['sequenceID']]
        #         # Last occurence is the src and target id
        #         v['source'] = len(node_list) -1 - node_list[::-1].index(v['sourceName'])
        #         v['target'] = len(node_list) -1 - node_list[::-1].index(v['targetName'])
        #         links.append(v)

        # Save everything
        res = dict()
        res['histogram'] = generate_bargraph(allTargets)
        # res['sankey'] = {
        #     # 'sessions': sessions,
        #     'links': links,
        #     'nodes': node_map
        # }

        res['nodes'] = node_map
        res['links'] = links
        res['sessions'] = sessions
        with open('sankey.json', 'w') as outfile:
            json.dump(res, outfile, sort_keys=False, indent=4)

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
        types = []
        counts = []
        type_bucket = target['events']['buckets']
        for t in type_bucket:
            types.append(t['key'])
            counts.append(t['doc_count'])

        top_bucket = target['top_target']['hits']['hits'][0]
        path_length = top_bucket['fields']['path_length'][0]
        res = {
            "target": target_name,
            "counts": counts,
            "types": types,
            "pathLength": path_length
        }
        results.append(res)

    return results

    # with open(filename, 'w') as outfile:
    #     json.dump(results, outfile, indent=4, sort_keys=False)

def generate_sankey(data, filename='sankey.json'):
    pass
