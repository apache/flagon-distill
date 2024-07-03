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

import os

import distill
from tests import testing_utils
from tests.data_config import DATA_DIR
import pytest
from core import feature_definition


def test_pairwiseStag_1():
    test_list = [1, 2, 3, 4]
    result = distill.pairwiseStag(test_list)
    assert result == [(1, 2), (3, 4)]


def test_pairwiseStag_2():
    test_list = [1, 2, 3, 4]
    result = distill.pairwiseStag(test_list, split=True)
    assert result == ((1, 3), (2, 4))


def test_pairwiseSeq_1():
    test_list = [1, 2, 3, 4]
    result = distill.pairwiseSeq(test_list)
    assert result == [(1, 2), (2, 3), (3, 4)]


def test_pairwiseSeq_2():
    test_list = [1, 2, 3, 4]
    result = distill.pairwiseSeq(test_list, split=True)
    assert result == ((1, 2, 3), (2, 3, 4))
    
data = testing_utils.setup(os.path.join(DATA_DIR, "sample_data.json"), "integer")
logs = data[1]

def input_rule(log):
    return "target" in log and "input" in log["target"]

def test_label_features_1():
    result = distill.label_features(logs,[FeatureDefinition(input_rule, "input_target")])
    assert result

def test_label_features_2():
    with pytest.raises(TypeError):
        result = distill.label_features(logs,[FeatureDefinition(input_rule, 10)])

def test_label_features_2():
    with pytest.raises(TypeError):
        result = distill.label_features(logs,[FeatureDefinition("input_rule", "input_target")])
    


