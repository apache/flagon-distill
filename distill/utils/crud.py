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

import pandas as pd


def epoch_to_datetime(epoch_string):
    """
    Turns Unix/Epoch DateTime string into a unix-based int
    :param epoch_string: Unix/Epoch DateTime string (e.g., UserALE:clientTime)
    :return: int
    """

    new_datetime = (
        pd.to_datetime(epoch_string, unit="ms", origin="unix")
        - pd.Timestamp("1970-01-01")
    ) // pd.Timedelta("1ms")
    return new_datetime


def getUUID(log):
    """
    Creates a unique id for a userale log.
    :param log: Userale log in the form of a dictionary
    :return: A string representing a unique identifier for the log
    """

    if "type" in log:
        return (
            str(log["sessionID"])
            + str(log["clientTime"])
            + str(log["logType"])
            + str(log["type"])
        )
    else:
        return str(log["sessionID"]) + str(log["clientTime"]) + str(log["logType"])
    
def group_by_sessionID_userID(log):
    """
    A helper function to create separate logs associated with unique users
    where a unique user to is a combination of the log's session ID and user ID  
    :param log: Userale log in the form of dictionary
    :return: A dictionary that represent logs belonging to unique users
    """
    grouped_data = {}
    for d in log:
        # Create a combination of the two key values userId and sessionID
        userId = d.get('userId', '')
        sessionId = d.get('sessionID', '')
        combined_key = str(userId) + "_" + str(sessionId)
        if combined_key not in grouped_data:
            grouped_data[combined_key] = []
        grouped_data[combined_key].append(d)
    return grouped_data

def chunk_by_idle_time(log, inactive_interval_s=60):
    """
    This function will divide/chunk sets which clientTime is separated by 
    idle time where idle time is defined as period of inactivity that exceeds
    the specified inactive_interval (in seconds)
    By default, the interval is 60 seconds
    :param log: Userale log in the form of dictionary
    :param inactive_interval_s: Threshold of inactivity (no logged activity) in seconds
    :return: A dictionary that represent sets separated by the idle time
    """
    separated_sets = []
    current_set = []
    # Assume that clientTime is in the integer (unix time) which expressed in milliseconds
    difference_in_ms = inactive_interval_s * 1000

    # Initialize the current timestamp
    if len(log) > 0:
        if 'clientTime' in log[0]:
            previous_timestamp = log[0]['clientTime']
        else:
            previous_timestamp = log[0]['endTime']

    for item in log:
        if 'clientTime' in item:
            current_timestamp = item['clientTime']
        else:  
            current_timestamp = item['endTime']
        if current_timestamp - previous_timestamp > difference_in_ms:
            # If the current set is not empty, add it to the list of sets
            if current_set:
                separated_sets.append(current_set)
                current_set = []

        # Add the current item to the current set and update the previous timestamp
        current_set.append(item)
        previous_timestamp = current_timestamp

    # Add the last set if it's not empty
    if current_set:
        separated_sets.append(current_set)

    return separated_sets

def chunk_by_tabId(log):
    """
    Separate logs by their tab ID
    :param log: Userale log in the form of dictionary
    :return: A dictionary that represent sets separated by unique tab ID
    """
    grouped_data = {}
    for d in log:
        # Depending on the log types, tabID can be inside the details element
        if 'tabId' in d:
            tab_key = 'tab_' + str(d['tabId'])
        elif 'details' in d:
            if 'id' in d['details']:            
                tab_key = 'tab_' + str(d['details']['id'])
            else:
                tab_key = 'unknown' 
                print('TabId not found')
        else:
            tab_key = 'unknown' 
        if tab_key not in grouped_data:
            grouped_data[tab_key] = []
        grouped_data[tab_key].append(d)
    return grouped_data

def chunk_to_usersessions(log, inactive_interval_s = 60):
    """
    Separate a raw log to sets of user sessions.
    A user session is defined by: unique session ID, user ID, and separated by idle time
    that exceeds the specified inactive_interval (in seconds). By default, the interval is 60 seconds.
    This set is further separated by the windows tab in which the user activities occurred
    :param log: Userale log in the form of dictionary
    :param inactive_interval_s: Threshold of inactivity (no logged activity) in seconds
    :return: A dictionary that represent sets of user sessions
    """
    data_by_users = {}
    data_by_users = group_by_sessionID_userID(log)

    chunk_data_by_users_sessions = {}
    for user in data_by_users:
        user_session_sets = {}
        # Sort the logs associated by each users so we can create sets accordingly
        sorted_data = sorted(data_by_users[user], key=lambda item: item.get('clientTime', item.get('endTime')))

        # We first detect if there is an idle time between the logs that exceed X seconds
        # And separate the logs when it is detected
        chunked_set_time = chunk_by_idle_time(sorted_data, inactive_interval_s)

        # for each chunk, we further chunk the data based on their tabID
        for index, value in enumerate(chunked_set_time):
            chunked_set_tab = chunk_by_tabId(value)
            user_session_sets[index] = chunked_set_tab
        chunk_data_by_users_sessions[user] = user_session_sets

    return chunk_data_by_users_sessions