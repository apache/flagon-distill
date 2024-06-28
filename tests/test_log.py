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
from distill.process.log import Log
from tests.data_config import DATA_DIR

def test_log_constructor():
    exception_thrown = False
    try:
        _ = Log("garbage data")
    except ValidationError:
        exception_thrown = True
    assert exception_thrown == True

    with open(os.path.join(DATA_DIR, "log_test_data.json")) as f:
        data = f.readline()
    test_log = Log(data)
    assert test_log is not None

    pageUrl = test_log.data.pageUrl
    assert pageUrl == "https://github.com/apache/flagon/tree/master/docker" 

def test_log_serialize():
    with open(os.path.join(DATA_DIR, "log_test_data.json")) as f:
        data = f.readline()
    test_log = Log(data)

    correct_str = json.dumps(json.loads(data), separators=(',', ':'), ensure_ascii=False)
    serialized_data = test_log.serializeJson()
    assert serialized_data == correct_str

def test_log_deserialize():
    with open(os.path.join(DATA_DIR, "log_test_data.json")) as f:
        data = f.readline()
    test_log = Log(data)

    correct_object = json.loads(data)
    deserialized_data = test_log.deserializeJson()
    assert deserialized_data == correct_object
    
