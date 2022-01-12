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
    data = testing_utils.setup("./data/sample_data.json", "integer")
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
    data = testing_utils.setup("./data/sample_data.json", "integer")
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
    data = testing_utils.setup("./data/sample_data.json", "datetime")
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
    assert result["test_segment_all"].start_end_val == (testing_utils.to_datetime(1623691890656),
                                                        testing_utils.to_datetime(1623691909728))

    assert result["test_segment_same_client_time"].num_logs == 2
    assert result["test_segment_same_client_time"].segment_name == "test_segment_same_client_time"
    assert result["test_segment_same_client_time"].start_end_val == \
           (testing_utils.to_datetime(1623691904488),
            testing_utils.to_datetime(1623691904488))
    assert result["test_segment_same_client_time"].uids == ["session_16236918905391623691904488rawclick",
                                                            "session_16236918905391623691904488customclick"]

    assert result["test_segment_extra_log"].num_logs == 8
    assert result["test_segment_extra_log"].segment_name == "test_segment_extra_log"
    assert result["test_segment_extra_log"].start_end_val == (testing_utils.to_datetime(1623691904212),
                                                              testing_utils.to_datetime(1623691904923))

def test_create_segment_error_1():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((testing_utils.to_datetime(sorted_data[0][1]['clientTime']),
                               testing_utils.to_datetime(sorted_data[18][1]['clientTime'])))
        segment_names = ["test_segment_error"]

        result = distill.create_segment(sorted_dict, segment_names, start_end_vals)

def test_create_segment_error_2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "string")
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
    data = testing_utils.setup("./data/sample_data.json", "integer")
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
    data = testing_utils.setup("./data/sample_data.json", "datetime")
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
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((testing_utils.to_datetime(sorted_data[0][1]['clientTime']),
                               testing_utils.to_datetime(sorted_data[18][1]['clientTime'])))
        segment_names = ["test_segment_error"]

        result = distill.write_segment(sorted_dict, segment_names, start_end_vals)

def test_write_segment_error_2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "string")
        sorted_data = data[0]
        sorted_dict = data[1]

        # Create Test Segment Tuples
        start_end_vals = []
        start_end_vals.append((testing_utils.to_datetime(sorted_data[0][1]['clientTime']),
                               testing_utils.to_datetime(sorted_data[18][1]['clientTime'])))
        segment_names = ["test_segment_error"]

        result = distill.write_segment(sorted_dict, segment_names, start_end_vals)

###########################
# GENERATE_SEGMENTS TESTS #
###########################
def test_generate_segments_integer():
    data = testing_utils.setup("./data/segment_generator_sample_data.json", "integer")
    sorted_data = data[0]
    sorted_dict = data[1]

    load_result = distill.generate_segments(sorted_dict, 'type', ['load'], 1, 1)
    assert len(load_result) == 2
    assert load_result["session_16236918905391623691890600rawload"].start_end_val == (1623691889600, 1623691891600)
    assert load_result["session_16236918905391623691890600rawload"].num_logs == 3
    assert load_result["session_16236918905391623691907302rawload"].start_end_val == (1623691906302, 1623691908302)
    assert load_result["session_16236918905391623691907302rawload"].num_logs == 7

    click_result = distill.generate_segments(sorted_dict, 'type', ['click'], 1, 1)
    assert len(click_result) == 11
    assert click_result["session_16236918905391623691904200rawclick"].start_end_val == (1623691903200, 1623691905200)
    assert click_result["session_16236918905391623691904200rawclick"].num_logs == 2
    assert click_result["session_16236918905391623691904200customclick"].start_end_val == (1623691903200, 1623691905200)
    assert click_result["session_16236918905391623691904200customclick"].num_logs == 2
    assert click_result["session_16236918905391623691905488rawclick"].start_end_val == (1623691904488, 1623691906488)
    assert click_result["session_16236918905391623691905488rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905488customclick"].start_end_val == (1623691904488, 1623691906488)
    assert click_result["session_16236918905391623691905488customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724rawclick"].start_end_val == (1623691904724, 1623691906724)
    assert click_result["session_16236918905391623691905724rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724customclick"].start_end_val == (1623691904724, 1623691906724)
    assert click_result["session_16236918905391623691905724customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923rawclick"].start_end_val == (1623691904923, 1623691906923)
    assert click_result["session_16236918905391623691905923rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923customclick"].start_end_val == (1623691904923, 1623691906923)
    assert click_result["session_16236918905391623691905923customclick"].num_logs == 7
    assert click_result["session_16236918905391623691906955rawclick"].start_end_val == (1623691905955, 1623691907955)
    assert click_result["session_16236918905391623691906955rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691907135rawclick"].start_end_val == (1623691906135, 1623691908135)
    assert click_result["session_16236918905391623691907135rawclick"].num_logs == 8
    assert click_result["session_16236918905391623691908100rawclick"].start_end_val == (1623691907100, 1623691909100)
    assert click_result["session_16236918905391623691908100rawclick"].num_logs == 5

    load_click_result = distill.generate_segments(sorted_dict, 'type', ['load', 'click'], 1, 1)
    assert len(load_click_result) == 13
    assert load_click_result["session_16236918905391623691890600rawload"].start_end_val == (1623691889600,
                                                                                            1623691891600)
    assert load_click_result["session_16236918905391623691890600rawload"].num_logs == 3
    assert load_click_result["session_16236918905391623691904200rawclick"].start_end_val == (1623691903200,
                                                                                             1623691905200)
    assert load_click_result["session_16236918905391623691904200rawclick"].num_logs == 2
    assert load_click_result["session_16236918905391623691904200customclick"].start_end_val == (1623691903200,
                                                                                                1623691905200)
    assert load_click_result["session_16236918905391623691904200customclick"].num_logs == 2
    assert load_click_result["session_16236918905391623691905488rawclick"].start_end_val == (1623691904488,
                                                                                             1623691906488)
    assert load_click_result["session_16236918905391623691905488rawclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691905488customclick"].start_end_val == (1623691904488,
                                                                                                1623691906488)
    assert load_click_result["session_16236918905391623691905488customclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691905724rawclick"].start_end_val == (1623691904724,
                                                                                             1623691906724)
    assert load_click_result["session_16236918905391623691905724rawclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691905724customclick"].start_end_val == (1623691904724,
                                                                                                1623691906724)
    assert load_click_result["session_16236918905391623691905724customclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691905923rawclick"].start_end_val == (1623691904923,
                                                                                             1623691906923)
    assert load_click_result["session_16236918905391623691905923rawclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691905923customclick"].start_end_val == (1623691904923,
                                                                                                1623691906923)
    assert load_click_result["session_16236918905391623691905923customclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691906955rawclick"].start_end_val == (1623691905955,
                                                                                             1623691907955)
    assert load_click_result["session_16236918905391623691906955rawclick"].num_logs == 7
    assert load_click_result["session_16236918905391623691907135rawclick"].start_end_val == (1623691906135,
                                                                                             1623691908135)
    assert load_click_result["session_16236918905391623691907135rawclick"].num_logs == 8
    assert load_click_result["session_16236918905391623691908100rawclick"].start_end_val == (1623691907100,
                                                                                             1623691909100)
    assert load_click_result["session_16236918905391623691908100rawclick"].num_logs == 5
    assert load_click_result["session_16236918905391623691907302rawload"].start_end_val == (1623691906302,
                                                                                            1623691908302)
    assert load_click_result["session_16236918905391623691907302rawload"].num_logs == 7

def test_generate_segments_datetime():
    data = testing_utils.setup("./data/segment_generator_sample_data.json", "datetime")
    sorted_data = data[0]
    sorted_dict = data[1]

    load_result = distill.generate_segments(sorted_dict, 'type', ['load'], 1, 1)
    assert len(load_result) == 2
    assert load_result["session_16236918905391623691890600rawload"].start_end_val == \
           (testing_utils.to_datetime(1623691889600), testing_utils.to_datetime(1623691891600))
    assert load_result["session_16236918905391623691890600rawload"].num_logs == 3
    assert load_result["session_16236918905391623691907302rawload"].start_end_val == \
           (testing_utils.to_datetime(1623691906302), testing_utils.to_datetime(1623691908302))
    assert load_result["session_16236918905391623691907302rawload"].num_logs == 7

    click_result = distill.generate_segments(sorted_dict, 'type', ['click'], 1, 1)
    assert len(click_result) == 11
    assert click_result["session_16236918905391623691904200rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691903200), testing_utils.to_datetime(1623691905200))
    assert click_result["session_16236918905391623691904200rawclick"].num_logs == 2
    assert click_result["session_16236918905391623691904200customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691903200), testing_utils.to_datetime(1623691905200))
    assert click_result["session_16236918905391623691904200customclick"].num_logs == 2
    assert click_result["session_16236918905391623691905488rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904488), testing_utils.to_datetime(1623691906488))
    assert click_result["session_16236918905391623691905488rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905488customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904488), testing_utils.to_datetime(1623691906488))
    assert click_result["session_16236918905391623691905488customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904724), testing_utils.to_datetime(1623691906724))
    assert click_result["session_16236918905391623691905724rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904724), testing_utils.to_datetime(1623691906724))
    assert click_result["session_16236918905391623691905724customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904923), testing_utils.to_datetime(1623691906923))
    assert click_result["session_16236918905391623691905923rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904923), testing_utils.to_datetime(1623691906923))
    assert click_result["session_16236918905391623691905923customclick"].num_logs == 7
    assert click_result["session_16236918905391623691906955rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691905955), testing_utils.to_datetime(1623691907955))
    assert click_result["session_16236918905391623691906955rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691907135rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691906135), testing_utils.to_datetime(1623691908135))
    assert click_result["session_16236918905391623691907135rawclick"].num_logs == 8
    assert click_result["session_16236918905391623691908100rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691907100), testing_utils.to_datetime(1623691909100))
    assert click_result["session_16236918905391623691908100rawclick"].num_logs == 5

    load_click_result = distill.generate_segments(sorted_dict, 'type', ['load', 'click'], 1, 1)
    assert len(load_click_result) == 13
    assert click_result["session_16236918905391623691904200rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691903200), testing_utils.to_datetime(1623691905200))
    assert click_result["session_16236918905391623691904200rawclick"].num_logs == 2
    assert click_result["session_16236918905391623691904200customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691903200), testing_utils.to_datetime(1623691905200))
    assert click_result["session_16236918905391623691904200customclick"].num_logs == 2
    assert click_result["session_16236918905391623691905488rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904488), testing_utils.to_datetime(1623691906488))
    assert click_result["session_16236918905391623691905488rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905488customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904488), testing_utils.to_datetime(1623691906488))
    assert click_result["session_16236918905391623691905488customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904724), testing_utils.to_datetime(1623691906724))
    assert click_result["session_16236918905391623691905724rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905724customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904724), testing_utils.to_datetime(1623691906724))
    assert click_result["session_16236918905391623691905724customclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904923), testing_utils.to_datetime(1623691906923))
    assert click_result["session_16236918905391623691905923rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691905923customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691904923), testing_utils.to_datetime(1623691906923))
    assert click_result["session_16236918905391623691905923customclick"].num_logs == 7
    assert click_result["session_16236918905391623691906955rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691905955), testing_utils.to_datetime(1623691907955))
    assert click_result["session_16236918905391623691906955rawclick"].num_logs == 7
    assert click_result["session_16236918905391623691907135rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691906135), testing_utils.to_datetime(1623691908135))
    assert click_result["session_16236918905391623691907135rawclick"].num_logs == 8
    assert click_result["session_16236918905391623691908100rawclick"].start_end_val == \
           (testing_utils.to_datetime(1623691907100), testing_utils.to_datetime(1623691909100))
    assert click_result["session_16236918905391623691908100rawclick"].num_logs == 5
    assert load_result["session_16236918905391623691890600rawload"].start_end_val == \
           (testing_utils.to_datetime(1623691889600), testing_utils.to_datetime(1623691891600))
    assert load_result["session_16236918905391623691890600rawload"].num_logs == 3
    assert load_result["session_16236918905391623691907302rawload"].start_end_val == \
           (testing_utils.to_datetime(1623691906302), testing_utils.to_datetime(1623691908302))
    assert load_result["session_16236918905391623691907302rawload"].num_logs == 7

#############################
# DETECT_DEADSPACE TESTS #
#############################
def test_deadspace_detection_integer():
    data = testing_utils.setup("./data/deadspace_detection_sample_data.json", "integer")
    sorted_dict = data[1]

    result = distill.detect_deadspace(sorted_dict, 5, 1, 2)

    assert len(result) == 3
    assert result["session_16236918905391623691891459rawscroll"].start_end_val == (1623691890459, 1623691994888)
    assert result["session_16236918905391623691891459rawscroll"].num_logs == 7
    assert result["session_16236918905391623691992900customclick"].start_end_val == (1623691991900, 1623693994900)
    assert result["session_16236918905391623691992900customclick"].num_logs == 15
    assert result["session_16236918905391623693995550rawload"].start_end_val == (1623693994550, 1623697997550)
    assert result["session_16236918905391623693995550rawload"].num_logs == 3

def test_deadspace_detection_datetime():
    data = testing_utils.setup("./data/deadspace_detection_sample_data.json", "datetime")
    sorted_dict = data[1]

    result = distill.detect_deadspace(sorted_dict, 5, 1, 2)

    assert len(result) == 3
    assert result["session_16236918905391623691891459rawscroll"].start_end_val == \
           (testing_utils.to_datetime(1623691890459), testing_utils.to_datetime(1623691994888))
    assert result["session_16236918905391623691891459rawscroll"].num_logs == 7
    assert result["session_16236918905391623691992900customclick"].start_end_val == \
           (testing_utils.to_datetime(1623691991900), testing_utils.to_datetime(1623693994900))
    assert result["session_16236918905391623691992900customclick"].num_logs == 15
    assert result["session_16236918905391623693995550rawload"].start_end_val == \
           (testing_utils.to_datetime(1623693994550), testing_utils.to_datetime(1623697997550))
    assert result["session_16236918905391623693995550rawload"].num_logs == 3

def test_deadspace_detection_error1():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/deadspace_detection_sample_data.json", "string")
        sorted_dict = data[1]

        distill.detect_deadspace(sorted_dict, 5, 1, 2)

def test_deadspace_detection_error2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/deadspace_detection_sample_data.json", "integer")
        sorted_dict = data[1]

        sorted_dict["session_16236918905391623691891459rawscroll"]['clientTime'] = \
            testing_utils.to_datetime(sorted_dict["session_16236918905391623691891459rawscroll"]['clientTime'])

        distill.detect_deadspace(sorted_dict, 5, 1, 2)

###################
# SET LOGIC TESTS #
###################
def test_union_integer():
    data = testing_utils.setup("./data/sample_data.json", "integer")
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
    data = testing_utils.setup("./data/sample_data.json", "datetime")
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
        data_integer = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_data_integer = data_integer[0]
        sorted_dict_integer = data_integer[1]

        data_datetime = testing_utils.setup("./data/sample_data.json", "datetime")
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
    data = testing_utils.setup("./data/sample_data.json", "integer")
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
    data = testing_utils.setup("./data/sample_data.json", "datetime")
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
        data_integer = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_data_integer = data_integer[0]
        sorted_dict_integer = data_integer[1]

        data_datetime = testing_utils.setup("./data/sample_data.json", "datetime")
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

        distill.intersection("new_segment", int_segment["test_segment_integer"],
                             datetime_segment["test_segment_datetime"])

