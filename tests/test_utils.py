# Util Tests
import json
import datetime
from distill.utils import crud

##############
# Test Setup #
##############

def setup():
    # Load in file and convert to raw data
    file = "./data/sample_data.json"

    with open(file) as json_file:
        raw_data = json.load(json_file)
    
    return raw_data

def setup_with_uid():
    # Load in file and convert to raw data
    file = "./data/sample_data.json"

    with open(file) as json_file:
        raw_data = json.load(json_file)
    
    # Add UIDs to raw data
    data = {}
    for log in raw_data:
        data[crud.getUUID(log)] = log

    return data

##############
# Test Cases #
##############

def test_UUID():
    raw_data = setup()

    data = {}

    # Assert the same log will produce the same UID
    id1 = crud.getUUID(raw_data[0])
    id2 = crud.getUUID(raw_data[0])
    assert id1 == id2

    for log in raw_data:
        data[crud.getUUID(log)] = log

    # Assert UID uniqueness
    assert len(data) == len(raw_data)
    assert len(data) == 19 
    