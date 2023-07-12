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

import collections
import networkx as nx
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import pandas as pd
import plotly.express as px
import re
from PIL import Image
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import os

def get_partition(log, partition_elements):
    """
    Creates a partition of logs
    :param log: Log file
    :param partition_elements: Dictionary of elements mapped to colors
    :return: Partition
    """   
    partition = list(set(log['path']) & set(partition_elements))
    if len(partition) == 1:
        return partition[0]
    if len(partition) == 0:
        return "Other"
    return "Error with partitioning"

def get_color_graph(log_dict, color_dict, partition_func):
    """
    Creates a colored NetworkX Directed Graph Object (G) from a dictionary of logs
    :param log_dict: Dictionary of logs
    :param color_dict: Dictionary of elements:colors (mapping colors to nodes)
    :param partition_func: creates a partition of logs
    :return: A NetworkX graph object with the colors for each node
    """    

    targets = []
    partition_dict = {}
    label_dict = {}
    for log in log_dict.values():
        targets.append(''.join(log['path']))
        partition_dict[targets[-1]] = partition_func(log, color_dict.keys())
        label_dict[targets[-1]] = log['target']
        
    edges = list(nx.utils.pairwise(targets))

    graph = nx.DiGraph((x, y, {'capacity': v}) for (x, y), v in collections.Counter(edges).items())
    nx.set_node_attributes(graph, partition_dict, "partition")
    nx.set_node_attributes(graph, label_dict, "label")
    colors = [color_dict[p] for p in nx.get_node_attributes(graph, "partition").values()]
    return (graph, colors)


def show_color_sankey(graph, color_dict):
    """
    Creates a colored Sankey Graph
    :param graph: The graph created from get_color_graph
    :param color_dict: Dictionary of element:colors (mapping colors to nodes)
    :return: A Sankey graph
    """   
    labels = []
    colors = []
    nodes = []
    edges = list(graph.edges(data=True))
    for node in graph.nodes(data=True):
        nodes.append(node[0])
        labels.append(node[1]["label"])
        colors.append(color_dict[node[1]["partition"]])

    sources = [nodes.index(edge[0]) for edge in edges]
    targets = [nodes.index(edge[1]) for edge in edges]
    values = [edge[2]['capacity'] for edge in edges]

    go.Figure(data=[go.Sankey(
            textfont=dict(color="rgba(0,0,0,0)"),
            node=dict(label=labels, color=colors),
            link=dict(source=sources, target=targets, value=values))]).show()


def createDiGraph(nodes, edges, *, drop_recursions: bool=False, node_labels=False):
    """
    Creates NetworkX Directed Graph Object (G) from defined node, edge list
    :param nodes: Series or List of Events, Elements
    :param edges: Series or List of Pairs
    :param drop_recursions: if True eliminates self:self pairs in edges
    :return: A NetworkX graph object
    """

    # Replace node names with the node_labels if it is given as an argument
    if node_labels:
        nodes = [node if node not in node_labels else node_labels[node] for node in nodes]
        for i in range(len(edges)):
            edges[i] = tuple([node if node not in node_labels else node_labels[node] for node in edges[i]])

    # Remove self-to-self recursions
    if drop_recursions:
        edges = list(filter(lambda row: row[0] != row[1], edges))

    # Create a digraph with capacity attributes that represent the number of edges between nodes
    graph = nx.DiGraph((x, y, {'capacity': v}) for (x, y), v in collections.Counter(edges).items())
    graph.add_nodes_from(nodes)
    return graph

def sankey(edges, node_labels=False, *, drop_recursions=False):
    """
    Creates Sankey Graph from defined edge list and optional user-provided labels
    :param edges_segmentN: List of Tuples
    :param node_labels: Optional Dictionary of Values; keys are originals, values are replacements
    :return: A Sankey graph
    """

    # Convert raw edges to a weighted digraph
    graph = createDiGraph(list(), edges, node_labels=node_labels, drop_recursions=drop_recursions)
    nodes = list(graph.nodes())
    edges = graph.edges(data=True)
    
    # Format weighted edge data for the sankey function
    sources = [nodes.index(edge[0]) for edge in edges]
    targets = [nodes.index(edge[1]) for edge in edges]
    values = [edge[2]['capacity'] for edge in edges]
                                      
    return go.Figure(data=[go.Sankey(
        node=dict(label=nodes),
        link=dict(source=sources, target=targets, value=values))])

def funnel(edges, targets, node_labels=False, *, infer=True):
    """
    Creates Funnel Graph from defined edge list and optional user-provided labels
    :param edges: List of Tuples
    :param targets: String or list of strings representing elements of interest
    :param node_labels: Optional Dictionary of key default values, value replacements
    :param infer: Optional boolean, true = consider nondirect paths between targets and elements after the last target, false = only consider the provided elements    
    :return: A Funnel graph
    """
    
    # Convert raw edges to a weighted digraph
    graph = createDiGraph(list(), edges, drop_recursions=True, node_labels=node_labels)
    
    # Put raw strings into a list of one 
    if isinstance(targets, str):
        targets = [targets]
        
    target_edges = list()
    if infer:
        # Find the path through each provided target that maximizes flow
        for i in range(len(targets) - 1):
            path = max([path for path in nx.all_simple_paths(graph, targets[i], targets[i+1])],
                    key=lambda path: nx.path_weight(graph, path, "capacity"))
            target_edges.extend(nx.utils.pairwise(path))
        
        # Extend the path constructed above as much as possible without creating cycles
        dests = filter(lambda dest: dest not in targets, graph.nodes())
        paths = [path for path in nx.all_simple_paths(graph, targets[len(targets) - 1], dests)]
        targets = [edge[0] for edge in target_edges]
        path = max(filter(lambda path: not (set(path) & set(targets)), paths), key=len)
        target_edges.extend(nx.utils.pairwise(path))
        targets.extend(path)
    else:
        # Otherwise construct a path literally
        target_edges = nx.utils.pairwise(targets)

    # Get the total outflow of the starting node
    counts = sum([graph.get_edge_data(*edge)['capacity'] for edge in graph.out_edges(target_edges[0][0])])
    
    # Get the flow at every other node in the path
    counts = [counts] + [graph.get_edge_data(*edge)['capacity'] for edge in target_edges]
    counts = [min(counts[0:i]) for i in range(1, len(counts)+1)]
    
    # Return a funnel representing the flow throughout the constructed path
    return go.Figure(go.Funnel(y=targets, x=counts))

    def display_segments(segments, log_dict, get_partition, name_dict):
    """
    Displays a Plotly timeline of Segment objects.

    :param segments: A Segments object containing the Segment objects to display
    :param log_dict: Dictionary of the logs
    :param get_partition: function to create our partitions
    :param name_dict: Dictionary of partitions, elements can be renamed in dictionary using "k:v"
    """

    segment_metadata = []
    for segment in segments:
        first_log = log_dict[segment.get_segment_uids()[0]]
        segment_metadata.append({"Start Time": segment.get_start_end_val()[0],
                                "End Time": (segment.get_start_end_val()[1] + timedelta(seconds=0.5)),
                                "Partition": name_dict[get_partition(first_log, name_dict.keys())],
                                "Number of Clicks": segment.get_num_logs()})
        
    fig = px.timeline(segment_metadata, x_start="Start Time", x_end="End Time", y="Partition", color="Number of Clicks")
    fig.update_yaxes(autorange="reversed")
    return fig


    def click_plot_ani(sorted_dict, img_location, gif_save_name = None):
    """
    Displays a heatmap, overlaying clicks and mouseover events on top of an image

    :param sorted_dict: ADictionary of sorted logs
    :param img_location: location of the snapshot image
    :param gif_save_name: the name to save the GIF as
    """
        
    xy_values_clicks = []
    xy_values_mouseover = []
    res_values = []
    
    for key, value in sorted_dict.items():
        if "location" in value:
            if "x" in value["location"] and "y" in value["location"]:
                if value['type'] == 'click':
                    xy_values_clicks.append((value["location"]["x"], value["location"]["y"]))
                if value['type'] == 'mouseover':
                    xy_values_mouseover.append((value["location"]["x"], value["location"]["y"]))
            if "width" in value["scrnRes"] and "height" in value["scrnRes"]:
                if (value["scrnRes"]["width"], value["scrnRes"]["height"]) not in res_values:
                    res_values.append((value["scrnRes"]["width"], value["scrnRes"]["height"]))
    
    x_c = [x[0] for x in xy_values_clicks]
    y_c = [y[1] for y in xy_values_clicks]
    x_m = [x[0] for x in xy_values_mouseover]
    y_m = [y[1] for y in xy_values_mouseover]
    x_range, y_range = res_values[0]
    
    # Load the image
    img = Image.open(img_location)

    # Define the new size
    new_width, new_height = x_range, y_range

    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

    fig, ax = plt.subplots()
    # Set color and size for mouseover events
    scat_m = ax.scatter(x_m, y_m, c='g', s = 3)
    # Set color and size for click events
    scat_c = ax.scatter(x_c, y_c, c='r', s = 10)
    ax.set_xlabel('Screen Width ({})'.format(x_range))
    ax.set_ylabel('Screen Height ({})'.format(y_range))
    ax.imshow(img_resized)
    
    
    def update(frame, x_m, y_m):
        plt.clf()
        plt.scatter(x_m[:frame], y_m[:frame], c='g', s=3)
        plt.scatter(x_c, y_c, c='r', s=10)
        plt.xlabel('Screen Width ({})'.format(x_range))
        plt.ylabel('Screen Height ({})'.format(y_range))
        plt.title(gif_save_name)
        plt.imshow(img_resized)

    ani = animation.FuncAnimation(plt.gcf(), update, frames=len(x_m), fargs=(x_m, y_m), repeat=False)
    ani.save(gif_save_name+".gif", writer='imagemagick')
    plt.show(ani)