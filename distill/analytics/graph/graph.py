#
# Copyright 2022 The Applied Research Laboratory for Intelligence and Security (ARLIS)
#
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
import plotly.graph_objects as go

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


#    TODO complete function (args--input edge-list, labels)
def sankey(edges_segmentN, node_labels=False):
    """
    Creates Sankey Graph from defined edge list and optional user-provided labels
    :param edges_segmentN: List of Tuples
    :param node_labels: Optional Dictionary of Values; keys are originals, values are replacements
    :return: A Sankey graph
    """
    # Remove self-to-self recursions
    edge_list_temp = []
    for row in edges_segmentN:
        if row[0] != row[1]:
            edge_list_temp.append(row)
    edge_list = edge_list_temp

    # Create a counter to count how many elements are in the edge list
    edge_list_counter = collections.Counter(edge_list)

    # Extract source list, target list, and value list from the tuples
    source_list = [i[0] for i in edge_list_counter.keys()]
    target_list = [i[1] for i in edge_list_counter.keys()]
    value_list = [i for i in edge_list_counter.values()]

    # Extract the node names if node_labels does not exist as an argument
    nodes = []
    for row in edge_list:
        for col in row:
            if col not in nodes:
                nodes.append(col)
    # Replace node names with the give node_labels if it is given as an argument
    if node_labels:
        new_nodes = []
        for node in nodes:
            if node in node_labels:
                new_nodes.append(node_labels[node])
            else:
                new_nodes.append(node)
    # Sources are the nodes sending connections
    sources = []
    for i in source_list:
        sources.append(nodes.index(i))
    # Targets are the nodes receiving connections
    targets = []
    for i in target_list:
        targets.append(nodes.index(i))
    # Values are the weight of the connections
    values = value_list

    # If node labels is given as an argument, we replace nodes with node labels
    # If not, we use the original node names
    if node_labels:
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=[new_nodes[item].split("|")[0] for item in range(len(new_nodes))],
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            ))])
    else:
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

    return fig


#   TODO complete function (args--input edge-list, labels)
def funnel(edges_segmentN,
           user_specification,
           node_labels=False):

    """
    Creates Funnel Graph from defined edge list and optional user-provided labels
    :param edges_segmentN: List of Tuples
    :param user_specification: String of Target of interest e.g. #document
    :param node_labels: Optional Dictionary of key default values, value replacements
    :return: A Funnel graph
    """

    ## Removing duplicates

    edge_list_temp = []
    for row in edges_segmentN:
        if row[0] != row[1]:
            edge_list_temp.append(row)
    edge_list = edge_list_temp

    ## Convert from list of 2s to list of 1s

    edgelist_list = []
    length = len(edge_list) - 1
    for i in edge_list:
        if edge_list.index(i) != length:
            edgelist_list.append(i[0])
        else:
            edgelist_list.append(i[0])
            edgelist_list.append(i[1])

    # Remove the None values

    funnel_targets_temp = []
    for item in edgelist_list:
        if item != None:
            funnel_targets_temp.append(item)
    funnel_targets = funnel_targets_temp

    ## Convert that list into a list of 3s
    edge_list = []
    for i in range(len(funnel_targets)):
        if i == (len(funnel_targets) - 2):
            break
        else:
            edge_list.append((funnel_targets[i], funnel_targets[i + 1], funnel_targets[i + 2]))

    ## Convert the list of 3s to a counter

    edge_list_counter = collections.Counter(edge_list)
    first_rung = user_specification
    new_edge_list = []
    for i in edge_list:
        if i[0] == user_specification:
            new_edge_list.append((i[0], i[1], i[2]))

    new_edge_list_counter = collections.Counter(new_edge_list)
    new_edge_list_counter.most_common(1)

    first_rung = new_edge_list_counter.most_common(1)[0][0][0]
    second_rung = new_edge_list_counter.most_common(1)[0][0][1]
    third_rung = new_edge_list_counter.most_common(1)[0][0][2]

    counter1 = 0
    counter2 = 0
    counter3 = 0
    for i in edge_list:
        if i[0] == first_rung:
            counter1 += 1
            if i[1] == second_rung:
                counter2 += 1
                if i[2] == third_rung:
                    counter3 += 1

    # Numbers are how many times each target occured
    # Edges are the targets
    numbers = [counter1, counter2, counter3]
    edges = [first_rung, second_rung, third_rung]

    # If node labels was given as an argument, replaces the targets with the provided names
    if node_labels:
        new_edges = []
        for edge in edges:
            if edge in node_labels:
                new_edges.append(node_labels[edge])
            else:
                new_edges.append(edge)
        edges = new_edges


    # Plotting labels from the list with the values from the dictionary
    data = dict(
        number=numbers,
        edge=edges)

    # Plotting the figure
    fig = go.Figure(go.Funnel(
        y=edges,
        x=numbers,
        textposition="inside",
        textinfo="value+percent initial",
        opacity=0.65, marker={"color": ["deepskyblue", "lightsalmon", "tan"],
                              "line": {"width": [2]}},
        connector={"line": {"color": "lime", "dash": "dot", "width": 5}})
    )

    fig.show()

    return fig
