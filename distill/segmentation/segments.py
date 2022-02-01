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
from distill.segmentation.segmentation_error import SegmentationError

class Segments():
    """
    A list of Segment objects.
    """

    ##############################################
    # IMPLEMENTATION OF PYTHON DEFINED FUNCTIONS #
    ##############################################

    def __init__(self, segments):
        """
        Segments initialization function.

        :param segments ([]): List of Segment objects to be included in the Segments abstraction.
        """
        self.segments = segments

    def __iter__(self):
        """
        Allows Segments to be iterable.
        """
        return iter(self.segments)

    def __len__(self):
        """
        Allows Segments to return a length.
        """
        return len(self.segments)

    def __getitem__(self, item):
        """
        Allows Segments to be subscriptable.
        """
        return self.segments[item]

    def __str__(self):
        """
        Creates a readable string for Segments.
        """
        result = "Segments: [\n"
        for segment in self.segments:
            result += str(segment) + "\n"
        result += "]"
        return result

    ############################
    # DATA STRUCTURE FUNCTIONS #
    ############################

    def get_segment_list(self):
        """
        Returns a list of Segment objects in Segments.

        :return: A list of segment objects.
        """
        return self.segments

    def get_segment_name_dict(self):
        """
        Returns a dictionary of segment_name to Segment objects based on the key parameter.  Note that segment names
        must be unique.
        """
        result = {}
        print(self.segments)
        for segment in self.segments:
            if segment.get_segment_name() in result:
                print(result)
                print(segment.get_segment_name())
                raise SegmentationError("Segment names must be unique")
            else:
                result[segment.get_segment_name()] = segment
        return result

    ######################
    # SEGMENTS FILTERING #
    ######################

    def get_num_logs(self, num_logs):
        """
        Returns a new Segments object only including segments with the specified number of logs.

        :param num_logs: The minimum number of logs (inclusive) necessary to be included in the new Segments object.
        """
        segments = []
        for segment in self.segments:
            if segment.get_num_logs() >= num_logs:
                segments.append(segment)
        return Segments(segments)


