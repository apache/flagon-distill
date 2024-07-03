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

import json
import os

from pydantic import ValidationError

from distill.core.log import Log 
from tests.data_config import DATA_DIR
from datetime import datetime


def test_log_constructor():
    exception_thrown = False
    try:
        _ = Log(data="garbage data")
    except ValidationError:
        exception_thrown = True
    assert exception_thrown == True

    data = load_log()
    data_object = json.loads(data)

    test_log = Log(data=data)
    assert test_log is not None

    test_log2 = Log(data=data_object)
    assert test_log2 is not None

    pageUrl = test_log.data.page_url
    assert pageUrl == "https://github.com/apache/flagon/tree/master/docker"

    id = test_log.id
    assert id.get_timestamp() == 1719530111079 // 1000
    assert id.prefix == "log"


def test_log_serialize():
    data = load_log()
    test_log = Log(data=data)

    correct_str = json.dumps(
        json.loads(data), separators=(",", ":"), ensure_ascii=False
    )
    serialized_data = test_log.to_json()
    assert serialized_data == correct_str


def test_log_deserialize():
    data = load_log()
    test_log = Log(data=data)

    correct_object = json.loads(data)
    deserialized_data = test_log.to_dict()
    assert deserialized_data == correct_object


def test_log_normalize_timestamp():
    data = load_log()
    test_log = Log(data=data)

    # note provided UserAle schema has clientTime in milliseconds but need it in 
    # seconds to be able to parse
    correct_ms = 1719530111079
    correct_dt = datetime.fromtimestamp(correct_ms / 1000)

    assert test_log.data.client_time == correct_dt
    assert test_log.to_dict()["clientTime"] == correct_ms


def load_log() -> str:
    with open(os.path.join(DATA_DIR, "log_test_data.json")) as f:
        data = f.readline()
    return data
