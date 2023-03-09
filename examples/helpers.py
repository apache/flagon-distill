import sys
# Put the path to distill here
sys.path.append('..\..\incubator-flagon-distill')

from datetime import datetime, timedelta
import distill
import json
import networkx as nx
import pandas as pd
import plotly.express as px
import re
import collections
import plotly.graph_objects as go
import os
from PIL import Image
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt

def setup(file, date_type, filter_func=None):
    with open(file) as text_file:
        text = text_file.read()
    
    # Filter and parse JSON file
    text = re.sub(r'\n\t,\n', "\n", text)
    data = json.loads(text)
    data = list(filter(lambda x: x and 'clientTime' in x, data))
    data = list(filter(filter_func, data)) if filter_func else data
    
    # Convert clientTime to specified type
    for log in data:
        client_time = log['clientTime']
        if date_type == "integer":
            log['clientTime'] = distill.epoch_to_datetime(client_time)
        elif date_type == "datetime":
            log['clientTime'] = pd.to_datetime(client_time, unit='ms', origin='unix')
    
    # Index data on UUID
    data = {distill.getUUID(log): log for log in data}

    # Sort data based off clientTime, return dict
    return dict(sorted(data.items(), key=lambda kv: kv[1]['clientTime']))

def get_color_graph(log_dict, color_dict, partition_func):
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

def display_segments(segments, log_dict, get_partition, name_dict):
    """
    Displays a Plotly timeline of Segment objects.

    :param segments: A Segments object containing the Segment objects to display.
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
    fig.show()
    
def click_rate(file):
    def filter_func(log):
        return log and log['logType'] == 'raw'
    
    sorted_dict = setup(file, "datetime")
    times = []
    clicks = 0
    for key, value in sorted_dict.items():
        times.append((value["clientTime"]))
        if value['type'] == 'click':
            clicks = clicks + 1
                         
    totalTime = (times[len(times)-1] - times[0]).total_seconds()
    clickrate = round((clicks / totalTime),2)
    return(clickrate, totalTime, clicks)
def click_plot_ani(sorted_dict, img_location, gif_save_name = None):
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
    scat_m = ax.scatter(x_m, y_m, c='g', s = 3)
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