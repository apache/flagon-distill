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

# @TODO add header with description of file

import json
import os

# Util Tests
import distill
from tests.data_config import DATA_DIR


def test_UUID_with_type():
    # Load in file and convert to raw data
    file = os.path.join(DATA_DIR, "sample_data.json")

    with open(file) as json_file:
        raw_data = json.load(json_file)

    data = {}

    # Assert the same log will produce the same UID
    id1 = distill.getUUID(raw_data[0])
    id2 = distill.getUUID(raw_data[0])
    assert id1 == id2

    for log in raw_data:
        data[distill.getUUID(log)] = log

    # Assert UID uniqueness
    assert len(data) == len(raw_data)
    assert len(data) == 19


def test_UUID_without_type():
    # Load in file and convert to raw data
    file = os.path.join(DATA_DIR, "sample_data_without_type.json")

    with open(file) as json_file:
        raw_data = json.load(json_file)

    data = {}

    # Assert the same log will produce the same UID
    id1 = distill.getUUID(raw_data[0])
    id2 = distill.getUUID(raw_data[0])
    assert id1 == id2

    for log in raw_data:
        data[distill.getUUID(log)] = log

    # Assert UID uniqueness
    assert len(data) == len(raw_data)
    assert len(data) == 19


def test_chunk_to_usersessions():
    # Load in file and convert to raw data
    file = os.path.join(DATA_DIR, "sample_data_multiusers.json")
    with open(file) as json_file:
        raw_data = json.load(json_file)

    result = distill.chunk_to_usersessions(raw_data)

    # Assert that there are two distinct users
    assert len(result) == 2

    # Assert that there 3 distinct tabs for user: 9486d2f32a8f9d4ef0dae14430c3b918
    result_tab = distill.chunk_to_usersessions(raw_data, group_by_type="tab")
    assert len(result_tab['9486d2f32a8f9d4ef0dae14430c3b918']) == 3

    # Assert that there is logs with pageURL include www.google.com for user: 06b0db1ab30e8e92819ba3d4091b83bc
    # But none for user: 9486d2f32a8f9d4ef0dae14430c3b918
    result_url = distill.chunk_to_usersessions(raw_data, group_by_type="URL", url_re="*.google.*")
    assert "*.google.*" not in result_url['9486d2f32a8f9d4ef0dae14430c3b918']
    assert "*.google.*" in result_url['06b0db1ab30e8e92819ba3d4091b83bc']
