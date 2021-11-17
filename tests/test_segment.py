# Segment Testing
import json
import pandas as pd
from distill.segmentation import segment

def get_uuid(log, uid):
    return str(log['sessionID']) + str(log['clientTime']) + str(log["logType"]) + str(uid)

def convert_to_date_time(client_time):
    new_date_time = pd.to_datetime(client_time, unit='ms', origin='unix')
    return (new_date_time - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')

def setup():
    file = "./data/sample_data.json"

    with open(file) as json_file:
        raw_data = json.load(json_file)

    data = {}
    i = 0
    for log in raw_data:
        data[get_uuid(log, i)] = log
        i += 1
    
    # Convert clientTime to Date/Time object
    for uid in data:
        log = data[uid]
        client_time = log['clientTime']
        log['clientTime'] = convert_to_date_time(client_time)
    
    # Sort
    sorted_data = sorted(data.items(), key = lambda kv: kv[1]['clientTime'])
    sorted_dict = dict(sorted_data)

    return (sorted_data, sorted_dict)

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
    result = segment.Segment.create_segment(sorted_dict, segment_names, start_end_vals)

    assert result["test_segment_all"].num_logs == 19
    assert result["test_segment_all"].segment_name == "test_segment_all"
    assert result["test_segment_all"].start_end_val == (convert_to_date_time(1623691890656), convert_to_date_time(1623691909728))

    assert result["test_segment_same_client_time"].num_logs == 2
    assert result["test_segment_same_client_time"].segment_name == "test_segment_same_client_time"
    assert result["test_segment_same_client_time"].start_end_val == (convert_to_date_time(1623691904488), convert_to_date_time(1623691904488))
    assert result["test_segment_same_client_time"].uids == ["session_16236918905391623691904488raw5", "session_16236918905391623691904488custom6"]

    assert result["test_segment_extra_log"].num_logs == 8
    assert result["test_segment_extra_log"].segment_name == "test_segment_extra_log"
    assert result["test_segment_extra_log"].start_end_val == (convert_to_date_time(1623691904212), convert_to_date_time(1623691904923))

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
    result = segment.Segment.write_segment(sorted_dict, segment_names, start_end_vals)

    assert len(result["test_segment_all"]) == 19
    assert len(result["test_segment_same_client_time"]) == 2
    assert len(result["test_segment_extra_log"]) == 8

    #TODO: Create additional tests ensuring the content of logs
