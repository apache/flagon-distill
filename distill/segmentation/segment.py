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

import datetime

class Segment():
    """
    Distill's segmentation package. Allows the user to segment User Ale log data.
    """

    def __init__(self, segment_name, start_end_val, num_logs, uids):
        """
        Initializes a Segment object.  This object contains metadata for the associated Segment.

        :param segment_name (string): Name associated with the segment
        :param start_end_val ([(Date/Time or int, Date/Time or int)]): A list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects or integers
        :param num_logs (int): Number of logs in the segment
        :param uids ([strings]): A list of strings representing the associated uids of logs within the segment
        """

        self.segment_name = segment_name
        self.start_end_val = start_end_val
        self.num_logs = num_logs
        self.uids = uids

    def get_segment_name(self):
        """
        Retreives the name of a given segment.

        :return: The segment name of the given segment.
        """
        return self.segment_name
        
    def get_start_end_val(self):
        """
        Retreives the start and end values of a given segment.

        :return: The start and end values of the given segment.
        """
        return self.start_end_val

    def get_num_logs(self):
        """
        Retreives the number of logs within a given segment.

        :return: The number of logs within the given segment.
        """
        return self.num_logs
    
    def get_segment_uids(self):
        """
        Retreives the uid list of a given segment.

        :return: The uid list of the given segment.
        """
        return self.uids


#######################
# SET LOGIC FUNCTIONS #
#######################

def union(segment_name, segment1, segment2):
    """
    Creates a new segment based on the union of given segments' uids.

    :param segment_name (string): Name associated with the new segment
    :param segment1 (Segment): First segment involved in union.
    :param segment2 (Segment): Second segment involved in union.

    :return: A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the union of the uids of segment1 and segment2.
    """

    if not isinstance(segment1.start_end_val[0], type(segment2.start_end_val[0])) or \
            not isinstance(segment1.start_end_val[1], type(segment2.start_end_val[1])):
        raise TypeError("Segment start and end values must be of the same type between segments.")

    # Union uids
    uids = segment1.uids
    for uid in segment2.uids:
        if uid not in uids:
            uids.append(uid)
        
    # Get earliest starting val and latest end val
    start_time = segment1.start_end_val[0]
    end_time = segment1.start_end_val[1]
    if segment1.start_end_val[0] > segment2.start_end_val[0]:
        start_time = segment2.start_end_val[0]
    if segment1.start_end_val[1] < segment2.start_end_val[1]:
        end_time = segment2.start_end_val[1]

    # Create segment to return
    segment = Segment(segment_name, (start_time, end_time), len(uids), uids)
    return segment


def intersection(segment_name, segment1, segment2):
    """
    Creates a new segment based on the intersection of given segments' uids.

    :param segment_name (string): Name associated with the new segment
    :param segment1 (Segment): First segment involved in intersection.
    :param segment2 (Segment): Second segment involved in intersection.

    :return: A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the intersection of the uids of segment1 and segment2.
    """

    if not isinstance(segment1.start_end_val[0], type(segment2.start_end_val[0])) or \
            not isinstance(segment1.start_end_val[1], type(segment2.start_end_val[1])):
        raise TypeError("Segment start and end values must be of the same type between segments.")

    # intersections uids
    uids = []
    for uid in segment2.uids:
        if uid in segment1.uids:
            uids.append(uid)

    # Get the earliest start and latest end value
    start_time = segment1.start_end_val[0]
    end_time = segment1.start_end_val[1]
    if segment1.start_end_val[0] > segment2.start_end_val[0]:
        start_time = segment2.start_end_val[0]
    if segment1.start_end_val[1] < segment2.start_end_val[1]:
        end_time = segment2.start_end_val[1]

    segment = Segment(segment_name, (start_time, end_time), len(uids), uids)
    return segment
    

####################
# SEGMENT CREATION #
####################

def create_segment(target_dict, segment_names, start_end_vals):
    """
    Creates a dictionary of Segment objects representing the metadata
    associated with each defined segment.

    :param target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects or integers)
    :param segment_names ([strings]): A list of segment_names ordered in the same way as the start_end_vals
    :param start_end_vals ([(Date/Time or int, Date/Time or int)]): A list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects or integers

    :return: A dictionary of segment_name to Segment objects
    """

    result = {}
    for i in range(len(segment_names)):
        num_logs = 0
        segment_name = segment_names[i]
        start_time = start_end_vals[i][0]
        end_time = start_end_vals[i][1]
        uids = []
        for uid in target_dict:
            log = target_dict[uid]
            if (isinstance(log['clientTime'], int) and isinstance(start_time, int) and isinstance(end_time, int)) or (isinstance(log['clientTime'], datetime.datetime) and isinstance(start_time, datetime.datetime) and isinstance(end_time, datetime.datetime)):
                if log['clientTime'] >= start_time and log['clientTime'] <= end_time:
                    # Perform data collection on log
                    num_logs += 1
                    uids.append(uid)
            else:
                raise TypeError("clientTime and start/end times must be represented as the same type and must either be a datetime object or integer.")
            segment = Segment(segment_name, start_end_vals[i], num_logs, uids)
            result[segment_name] = segment
    return result

def write_segment(target_dict, segment_names, start_end_vals):
    """
    Creates a nested dictionary of segment names to UIDs which then map to individual
    logs (i.e result['segment_name'][uid] --> log).  This assists with easy iteration over
    defined segments.
        
    :param target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects or integers).
    :param segment_names ([strings]): A list of segment_names ordered in the same way as the start_end_vals.
    :param start_end_vals ([(Date/Time or int, Date/Time or int)]): A list of tuples (i.e [(start_time, end_time)]), where start_time and end_time are Date/Time Objects or integers.
        
    :return: A nested dictionary of segment_names to uids to individual logs.
    """
    result = {}
    create_result = create_segment(target_dict, segment_names, start_end_vals)

    # Iterate through segments to get logs
    for segment_name in create_result:
        result[segment_name] = {}
        for uid in create_result[segment_name].uids:
            result[segment_name][uid] = target_dict[uid]

    return result

def generate_segments(target_dict, field_name, field_values, start_time_limit, end_time_limit):
    """
    Generates a list of Segment objects corresponding to windows of time defined by the given time limits,
    field name, and associated values meant to match the field name indicated.

    :param target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects or integers).
    :param field_name (string): A string indicating the field name meant to be matched by the field values.
    :param field_values ([object]): A list of field values to be matched in order to start a segment.
    :param start_time_limit (int): Amount of time (in seconds) prior to a detected event that should be included in the generated segment.
    :param end_time_limit (int): Amount of time (in seconds) to keep the segment window open after a detected event.
                
    :return: A dictionary of segment_names to generated Segment objects.
    """

    # Iterate through the target dictionary using key list
    start_end_vals = []
    segment_names = []
    end_time = 0
    keylist = list(target_dict.keys())
    for i in range(len(keylist)):
        if field_name in target_dict[keylist[i]]:
            # Matches value in field_values list with dict values (str or list)
            if any(item in target_dict[keylist[i]][field_name] for item in field_values):
                # Matches values - Create segment
                orig_start_time = target_dict[keylist[i]]['clientTime']
                if isinstance(orig_start_time, int):
                    start_time = orig_start_time - (start_time_limit*1000)
                    # new window doesn't overlap with last
                    # @TODO might try refactoring start > end time -- make more succinct
                    if start_time > end_time:
                        end_time = start_time + (end_time_limit*1000)
                        start_end_tuple = (start_time, end_time)
                        start_end_vals.append(start_end_tuple)
                        segment_names.append(keylist[i])
                elif isinstance(orig_start_time, datetime.datetime):
                    start_time = orig_start_time - datetime.timedelta(seconds=start_time_limit)
                    # new window doesn't overlap with last
                    if start_time > end_time:
                        end_time = start_time + datetime.timedelta(seconds=end_time_limit)
                        start_end_tuple = (start_time, end_time)
                        start_end_vals.append(start_end_tuple)
                        segment_names.append(keylist[i])
                else:
                    raise TypeError('clientTime field is not represented as an integer or datetime object')

    # Create segment dictionary with create_segment
    segments = create_segment(target_dict, segment_names, start_end_vals)
    return segments

def detect_deadspace(target_dict, deadspace_limit, start_time_limit, end_time_limit):
    """
    Detects deadspace in a dictionary of User Ale logs.  Detected instances of deadspace are captured in Segment
    objects based on the start and end time limits indicated by the function parameters.

    :param target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects or integers).
    :param deadspace_limit (int): An integer representing the amount of time (in seconds) considered to be 'deadspace'.
    :param start_time_limit (int): Amount of time (in seconds) prior to a detected deadspace event that should be included in the deadspace segment.
    :param end_time_limit (int): Amount of time (in seconds) to keep the segment window open after a detected deadspace event.

    :return: A dictionary of segment_names to generated Segment objects containing detected deadspace.
    """

    # Iterate through the target dictionary using key list
    start_end_vals = []
    segment_names = []
    key_list = list(target_dict.keys())
    for i in range(len(key_list)):
        # Check for deadspace
        if i < len(key_list) - 1:
            curr_time = target_dict[key_list[i]]['clientTime']
            next_time = target_dict[key_list[i + 1]]['clientTime']
            time_delta = next_time - curr_time
            if isinstance(curr_time, int) and isinstance(next_time, int):
                if time_delta > deadspace_limit * 1000:
                    # Deadspace detected
                    start_time = curr_time - (start_time_limit * 1000)
                    end_time = next_time + (end_time_limit * 1000)
                    start_end_tuple = (start_time, end_time)
                    start_end_vals.append(start_end_tuple)
                    segment_names.append(key_list[i])
            elif isinstance(curr_time, datetime.datetime) and isinstance(next_time, datetime.datetime):
                if time_delta > datetime.timedelta(seconds=deadspace_limit):
                    # Deadspace detected
                    start_time = curr_time - datetime.timedelta(seconds=start_time_limit)
                    end_time = next_time + datetime.timedelta(seconds=end_time_limit)
                    start_end_tuple = (start_time, end_time)
                    start_end_vals.append(start_end_tuple)
                    segment_names.append(key_list[i])
            else:
                raise TypeError('clientTime field is not consistently represented as an integer or datetime object')

    # Create segment dictionary with create_segment
    segments = create_segment(target_dict, segment_names, start_end_vals)
    return segments