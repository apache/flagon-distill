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
import networkx as nx

class graph:
    """
    Distill's graph analytics package. Apply graph algorithms
    to User Ale log data.
    """

    @staticmethod
    def createDiGraph(nodes, edges, *, drop_recursions: bool = False):
        """
        Creates NetworkX Directed Graph Object (G) from defined node, edge list
        :param nodes: Series or List of Events, Elements
        :param edges: Series or List of Pairs
        :param drop_recursions: if True eliminates self:self pairs in edges
        :return: A NetworkX graph object
        """
        G=nx.DiGraph()
        G.add_nodes_from(nodes)
        if drop_recursions==True:
            edges_filtered = []
            for row in edges:
                if row[0] != row[1]:
                    edges_filtered.append(row)
            G.add_edges_from(edges_filtered)
            return G
        else:
            G.add_edges_from(edges)
            return G

    @staticmethod
#    TODO complete function (args--input edge-list, labels)
    def sankey ():
        """

        :return:
        """
        edge_list_temp = []
        for row in edges_segmentN:
            if row[0] != row[1]:
                edge_list_temp.append(row)
        edge_list = edge_list_temp

        edge_list_counter = Counter(edge_list)

        source_list = [i[0] for i in edge_list_counter.keys()]
        target_list = [i[1] for i in edge_list_counter.keys()]
        value_list = [i for i in edge_list_counter.values()]

        nodes = []
        for row in edge_list:
            for col in row:
                if col not in nodes:
                    nodes.append(col)

        sources = []
        for i in source_list:
            sources.append(nodes.index(i))
        targets = []
        for i in target_list:
            targets.append(nodes.index(i))
        values = value_list

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=[nodes[item].split("|")[0] for item in range(len(nodes))],
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            ))])

        fig.show()

    @staticmethod
#   TODO complete function (args--input edge-list, labels)
    def funnel():
