# Segment Testing
import pytest
import json
import pandas as pd
import distill
import testing_utils
import datetime

########################
# SEGMENT OBJECT TESTS #
########################
def test_getters():
    data = testing_utils.setup("integer")
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

########################
# CREATE_SEGMENT TESTS #
########################
def test_create_segment_integer():
    data = testing_utils.setup("integer")
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
    assert result["test_segment_same_client_time"].uids == ["session_16236918905391623691904488rawclick",
                                                            "session_16236918905391623691904488customclick"]

    assert result["test_segment_extra_log"].num_logs == 8
    assert result["test_segment_extra_log"].segment_name == "test_segment_extra_log"
    assert result["test_segment_extra_log"].start_end_val == (1623691904212, 1623691904923)

def test_create_segment_datetime():
    data = testing_utils.setup("datetime")
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
    assert result["test_segment_all"].start_end_val == (pd.to_datetime(1623691890656, unit='ms', origin='unix'),
                                                        pd.to_datetime(1623691909728, unit='ms', origin='unix'))

    assert result["test_segment_same_client_time"].num_logs == 2
    assert result["test_segment_same_client_time"].segment_name == "test_segment_same_client_time"
    assert result["test_segment_same_client_time"].start_end_val == \
           (pd.to_datetime(1623691904488, unit='ms', origin='unix'),
            pd.to_datetime(1623691904488, unit='ms', origin='unix'))
    assert result["test_segment_same_client_time"].uids == ["session_16236918905391623691904488rawclick",
                                                            "session_16236918905391623691904488customclick"]

    assert result["test_segment_extra_log"].num_logs == 8
    assert result["test_segment_extra_log"].segment_name == "test_segment_extra_log"
    assert result["test_segment_extra_log"].start_end_val == (pd.to_datetime(1623691904212, unit='ms', origin='unix'),
                                                              pd.to_datetime(1623691904923, unit='ms', origin='unix'))

def test_create_segment_error_1():
    with pytest.raises(TypeError):
        data = testing_utils.setup("integer")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((pd.to_datetime(sorted_data[0][1]['clientTime'], unit='ms', origin='unix'),
                               pd.to_datetime(sorted_data[18][1]['clientTime'], unit='ms', origin='unix')))
        segment_names = ["test_segment_error"]

        result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

def test_create_segment_error_2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("string")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append(("random_string_1", "random_string_2"))
        segment_names = ["test_segment_error"]

        result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

#######################
# WRITE_SEGMENT TESTS #
#######################
def test_write_segment_integer():
    data = testing_utils.setup("integer")
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

    # Assert dictionary lengths
    assert len(result["test_segment_all"]) == 19
    assert len(result["test_segment_same_client_time"]) == 2
    assert len(result["test_segment_extra_log"]) == 8

    # Assert clientTime types
    for uid in result['test_segment_all']:
        assert isinstance(result['test_segment_all'][uid]['clientTime'], int)
    for uid in result['test_segment_same_client_time']:
        assert isinstance(result['test_segment_same_client_time'][uid]['clientTime'], int)
    for uid in result['test_segment_extra_log']:
        assert isinstance(result['test_segment_extra_log'][uid]['clientTime'], int)

def test_write_segment_datetime():
    data = testing_utils.setup("datetime")
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

    # Assert clientTime types
    for uid in result['test_segment_all']:
        assert isinstance(result['test_segment_all'][uid]['clientTime'], datetime.datetime)
        assert isinstance(result['test_segment_all'][uid]['clientTime'], pd.Timestamp)
    for uid in result['test_segment_same_client_time']:
        assert isinstance(result['test_segment_same_client_time'][uid]['clientTime'], datetime.datetime)
        assert isinstance(result['test_segment_same_client_time'][uid]['clientTime'], pd.Timestamp)
    for uid in result['test_segment_extra_log']:
        assert isinstance(result['test_segment_extra_log'][uid]['clientTime'], datetime.datetime)
        assert isinstance(result['test_segment_extra_log'][uid]['clientTime'], pd.Timestamp)

def test_write_segment_error_1():
    with pytest.raises(TypeError):
        data = testing_utils.setup("integer")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((pd.to_datetime(sorted_data[0][1]['clientTime'], unit='ms', origin='unix'),
                               pd.to_datetime(sorted_data[18][1]['clientTime'], unit='ms', origin='unix')))
        segment_names = ["test_segment_error"]

        result = distill.write_segment(sorted_dict, segment_names, start_end_vals)

def test_write_segment_error_2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("string")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((pd.to_datetime(sorted_data[0][1]['clientTime'], unit='ms', origin='unix'),
                               pd.to_datetime(sorted_data[18][1]['clientTime'], unit='ms', origin='unix')))
        segment_names = ["test_segment_error"]

        result = distill.write_segment(sorted_dict, segment_names, start_end_vals)

###################
# SET LOGIC TESTS #
###################
def test_union_integer():
    data = testing_utils.setup("integer")
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


def test_union_datetime():
    data = testing_utils.setup("datetime")
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

def test_union_error():
    with pytest.raises(TypeError):
        data_integer = testing_utils.setup("integer")
        sorted_data_integer = data_integer[0]
        sorted_dict_integer = data_integer[1]

        data_datetime = testing_utils.setup("datetime")
        sorted_data_datetime = data_datetime[0]
        sorted_dict_datetime = data_datetime[1]

        segment_name_integer = ["test_segment_integer"]
        segment_name_datetime = ["test_segment_datetime"]

        start_end_integer = []
        start_end_integer.append((sorted_data_integer[0][1]['clientTime'], sorted_data_integer[18][1]['clientTime']))
        start_end_datetime = []
        start_end_datetime.append((sorted_data_datetime[3][1]['clientTime'], sorted_data_datetime[9][1]['clientTime']))

        int_segment = distill.create_segment(sorted_dict_integer, segment_name_integer, start_end_integer)
        datetime_segment = distill.create_segment(sorted_dict_datetime, segment_name_datetime, start_end_datetime)

        distill.union("new_segment", int_segment["test_segment_integer"], datetime_segment["test_segment_datetime"])

def test_intersection_integer():
    data = testing_utils.setup("integer")
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
    assert new_segment.num_logs == 2
    assert new_segment.uids == [sorted_data[5][0], sorted_data[6][0]]
    assert new_segment.start_end_val == (sorted_data[5][1]['clientTime'], sorted_data[7][1]['clientTime'])

def test_intersection_datetime():
    data = testing_utils.setup("datetime")
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
    assert new_segment.num_logs == 2
    assert new_segment.uids == [sorted_data[5][0], sorted_data[6][0]]
    assert new_segment.start_end_val == (sorted_data[5][1]['clientTime'], sorted_data[7][1]['clientTime'])

def test_intersection_error():
    with pytest.raises(TypeError):
        data_integer = testing_utils.setup("integer")
        sorted_data_integer = data_integer[0]
        sorted_dict_integer = data_integer[1]

        data_datetime = testing_utils.setup("datetime")
        sorted_data_datetime = data_datetime[0]
        sorted_dict_datetime = data_datetime[1]

        segment_name_integer = ["test_segment_integer"]
        segment_name_datetime = ["test_segment_datetime"]

        start_end_integer = []
        start_end_integer.append((sorted_data_integer[0][1]['clientTime'], sorted_data_integer[18][1]['clientTime']))
        start_end_datetime = []
        start_end_datetime.append((sorted_data_datetime[3][1]['clientTime'], sorted_data_datetime[9][1]['clientTime']))

        int_segment = distill.create_segment(sorted_dict_integer, segment_name_integer, start_end_integer)
        datetime_segment = distill.create_segment(sorted_dict_datetime, segment_name_datetime, start_end_datetime)

        distill.intersection("new_segment", int_segment["test_segment_integer"], datetime_segment["test_segment_datetime"])

