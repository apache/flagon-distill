#
# Copyright 2022 The Applied Research Laboratory for Intelligence and Security (ARLIS)
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

import distill

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
