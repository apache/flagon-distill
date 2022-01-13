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

import itertools
from collections import Counter, deque

def pairwiseStag(iterable, *, split: bool = False):
    '''
    Creates sequence of staggered, pairwise tuples for edge-lists: "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    :param iterable: a series or list
    :param split: split=True returns pairwise elements in two separate lists of same len (default=False)
    :return: returns list object(s)
    '''
    a = iter(iterable)
    pairs = zip(a, a)
    if split == True:
        list1, list2 = zip(*pairs)
        return list1, list2
    else:
        return list(pairs)

def pairwiseSeq(iterable, *, split: bool = False):
    """
    Creates sequence of pairwise tuples that can be used as edge-lists: "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    :param iterable: a series or list
    :param split=True returns pairwise elements in two separate lists of same len (default=False)
    :return: returns list object(s)
    """
    a, b = itertools.tee(iterable, 2)
    next(b, None)
    pairs = zip(a, b)
    if split == True:
        list1, list2 = zip(*pairs)
        return list1, list2
    else:
        return list(pairs)
