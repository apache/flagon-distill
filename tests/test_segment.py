# Segment Testing
import json
import pandas as pd
import distill

def setup():

    file = "./data/sample_data.json"
    with open(file) as json_file:
        raw_data = json.load(json_file)

    data = {}
    for log in raw_data:
        data[distill.getUUID(log)] = log
    
    # Convert clientTime to Date/Time object
    for uid in data:
        log = data[uid]
        client_time = log['clientTime']
        log['clientTime'] = distill.epoch_to_datetime(client_time)
    
    # Sort
    sorted_data = sorted(data.items(), key = lambda kv: kv[1]['clientTime'])
    sorted_dict = dict(sorted_data)

    return (sorted_data, sorted_dict)

def setup_one_segment():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Test Segment Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[1][1]['clientTime']))

    segment_names = ["test_segment_1"]

    # Call create_segment
    result = distill.create_segment(sorted_dict, segment_names, start_end_vals)
    
    return result["test_segment_1"]


def test_create_segment():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Test Segment Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))

    segment_names = ["test_segment_all", "test_segment_same_client_time", "test_segment_extra_log"]

    # Call create_segment
    result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    assert result["test_segment_all"].num_logs == 19
    assert result["test_segment_all"].segment_name == "test_segment_all"
    assert result["test_segment_all"].start_end_val == (1623691890656, 1623691909728)

    assert result["test_segment_same_client_time"].num_logs == 2
    assert result["test_segment_same_client_time"].segment_name == "test_segment_same_client_time"
    assert result["test_segment_same_client_time"].start_end_val == (1623691904488, 1623691904488)
    assert result["test_segment_same_client_time"].uids == ["session_16236918905391623691904488rawclick", "session_16236918905391623691904488customclick"]

    assert result["test_segment_extra_log"].num_logs == 8
    assert result["test_segment_extra_log"].segment_name == "test_segment_extra_log"
    assert result["test_segment_extra_log"].start_end_val == (1623691904212, 1623691904923)

def test_write_segment():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Test Segment Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))

    segment_names = ["test_segment_all", "test_segment_same_client_time", "test_segment_extra_log"]

    # Call write_segment
    result = distill.write_segment(sorted_dict, segment_names, start_end_vals)

    assert len(result["test_segment_all"]) == 19
    assert len(result["test_segment_same_client_time"]) == 2
    assert len(result["test_segment_extra_log"]) == 8

    #TODO: Create additional tests ensuring the content of logs

def test_union():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[6][1]['clientTime'], sorted_data[7][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))

    segment_names = ["test_segment_1", "test_segment_2", "test_segment_3", "test_segment_4"]

    result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    new_segment = distill.union("new_segment", result["test_segment_2"], result["test_segment_3"])
    
    assert new_segment.segment_name == "new_segment"
    assert new_segment.num_logs == 4
    assert new_segment.uids == [sorted_data[5][0], sorted_data[6][0], sorted_data[7][0], sorted_data[8][0]]
    assert new_segment.start_end_val == (sorted_data[5][1]['clientTime'], sorted_data[7][1]['clientTime'])

def test_getters():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Test Segment
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[1][1]['clientTime']))
    segment_names = ["test_segment_1"]
    result = distill.create_segment(sorted_dict, segment_names, start_end_vals)
    seg = result["test_segment_1"]
    
    assert seg.get_segment_name() == "test_segment_1"
    assert seg.get_start_end_val() == (sorted_data[0][1]['clientTime'], sorted_data[1][1]['clientTime'])
    assert seg.get_num_logs() == 2
    assert seg.get_segment_uids() == [sorted_data[0][0], sorted_data[1][0]]
#Getting intersections 

def test_intersection():
    data = setup()
    sorted_data = data[0]
    sorted_dict = data[1]
    
    # Create Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[6][1]['clientTime'], sorted_data[7][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))

    segment_names = ["test_segment_1", "test_segment_2", "test_segment_3", "test_segment_4"]

    result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    new_segment = distill.intersection("new_segment", result["test_segment_2"], result["test_segment_3"])
    
    assert new_segment.segment_name == "new_segment"
    assert new_segment.num_logs == 4
    assert new_segment.uids == [sorted_data[5][0], sorted_data[6][0], sorted_data[7][0], sorted_data[8][0]]
    assert new_segment.start_end_val == (sorted_data[5][1]['clientTime'], sorted_data[7][1]['clientTime'])
