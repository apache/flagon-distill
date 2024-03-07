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

import re
import json
from urllib.parse import urlparse

from distill.sessions.sessions import Sessions
from distill.sessions.sessions import Sessions_Type

class Session:
    """
    Distill's sessions package. Allows the user to parse User Ale log data to user sessions.
    """

    def __init__(self, session={}):
        """
        Initializes a Session object.  This object contains\
        metadata for the associated Session.

        :param session: a set of key value pair representing a session
        """

        self.session = session
        self.session_name = list(session.keys())[0]
        self.num_logs = len(list(session.values())[0])
        self.logs = list(session.values())[0]

    def __str__(self):
        return json.dumps(self.session)

    def get_session_name(self):
        """
        Gets the name of a given session.

        :return: The session name of the given session.
        """
        return self.session_name
    
    def get_num_logs(self):
        """
        Gets the number of logs within a given session.

        :return: The number of logs within the given session.
        """
        return self.num_logs
    
    def get_logs(self):
        """
        Gets the logs within a given session.

        :return: The logs within the given session.
        """
        return self.logs

    #######################
    # SET LOGIC FUNCTIONS #
    #######################

    def chunk_by_user_sessions(log, inactive_interval_s = 60, group_by_type = "None", url_re = "."):
        """
        Separate a raw log to sets of user sessions.
        A user session is defined by: unique session ID, user ID, and separated by idle time
        that exceeds the specified inactive_interval (in seconds). By default, the interval is 60 seconds.
        This set is further separated by the windows tab in which the user activities occurred
        :param log: Userale log in the form of dictionary
        :param inactive_interval_s: Threshold of inactivity (no logged activity) in seconds
        :param url_re: Regular expression to filter the log
        :param group_by_type: either group by tab, URL, browser (None)
        :return: A dictionary that represent sets of user sessions
        """
        data_by_users = {}
        data_by_users = Session.__group_by_user(log)

        chunk_data_by_users_sessions = {}
        for user in data_by_users:
            user_session_sets = {}
            # Sort the logs associated by each users so we can create sets accordingly
            sorted_data = sorted(data_by_users[user], key=lambda item: item.get('clientTime', item.get('endTime')))
            chunked_group = {}
            # Separate by browser tab
            if (group_by_type == "tab"):
                chunked_group = Session.__chunk_by_tabId(sorted_data)
                for g_id in chunked_group:
                    # For each set, detect if there is an idle time between the logs that exceed X seconds
                    user_session_sets[g_id] = Session.__chunk_by_idle_time(chunked_group[g_id], inactive_interval_s)
                chunk_data_by_users_sessions[user] = user_session_sets
            # Separate by domain application
            elif (group_by_type == "domain"):
                # Do something
                chunked_group = Session.__chunk_by_domain(sorted_data, url_re)
                for g_id in chunked_group:
                    # For each set, detect if there is an idle time between the logs that exceed X seconds
                    user_session_sets[g_id] = Session.__chunk_by_idle_time(chunked_group[g_id], inactive_interval_s)
                chunk_data_by_users_sessions[user] = user_session_sets
            else:
                # For each set, detect if there is an idle time between the logs that exceed X seconds
                chunk_data_by_users_sessions[user] = Session.__chunk_by_idle_time(sorted_data, inactive_interval_s)

        # Flatten the structure into a collection of sessions
        flattened_results = Session.__flatten_dict(chunk_data_by_users_sessions)
        parsed_sessions = []
        for result in flattened_results:
            parsed_sessions.append(Session({result: flattened_results[result]}))
        sessions_set = Sessions(parsed_sessions)
        if (group_by_type == "tab"):
            sessions_set.sessions_type = Sessions_Type.TAB
        elif (group_by_type == "domain"):
            sessions_set.sessions_type = Sessions_Type.DOMAIN
        return sessions_set


    ##############################
    # SUPPORTING FUNCTIONS FOR PARSING SESSION #
    ###############################
    def __group_by_user(log):
        """
        A helper function to create separate logs associated with unique users
        where a unique user to is the browserSessionId
        :param log: Userale log in the form of dictionary
        :return: A dictionary that represent logs belonging to unique users
        """
        grouped_data = {}
        for d in log:
            # Create a combination of the two key values userId and sessionID
            sessionId = d.get('browserSessionId', '')
            combined_key = str(sessionId)
            if combined_key not in grouped_data:
                grouped_data[combined_key] = []
            grouped_data[combined_key].append(d)
        return grouped_data

    def __chunk_by_idle_time(log, inactive_interval_s=60):
        """
        This function will divide/chunk sets which clientTime is separated by 
        idle time where idle time is defined as period of inactivity that exceeds
        the specified inactive_interval (in seconds)
        By default, the interval is 60 seconds
        :param log: Userale log in the form of dictionary
        :param inactive_interval_s: Threshold of inactivity (no logged activity) in seconds
        :return: A dictionary that represent sets of logs separated by the idle time
        """
        separated_sets = {}
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
                    key = "time" + str(current_timestamp)
                    separated_sets[key] = current_set
                    current_set = []

            # Add the current item to the current set and update the previous timestamp
            current_set.append(item)
            previous_timestamp = current_timestamp

        # Add the last set if it's not empty
        if current_set:
            key = "time" + str(current_timestamp)
            separated_sets[key] = current_set
        return separated_sets

    def __chunk_by_tabId(log):
        """
        Separate logs by their browserSessionId
        :param log: Userale log in the form of dictionary
        :return: A dictionary that represent sets separated by unique browserSessionId
        """
        grouped_data = {}
        for key in log:
            # Depending on the log types, tabID can be inside the details element
            if 'browserSessionId' in key:
                tab_key = 'tab' + str(key['httpSessionId'])
            else:
                tab_key = 'unknown' 
            if tab_key not in grouped_data:
                grouped_data[tab_key] = []
            grouped_data[tab_key].append(key)
        return grouped_data

    def __match_url(url, pattern):
        # Escape dots in the pattern since dot is a special character in regex
        # and replace '*' with '.*' to match any characters sequence
        regex_pattern = re.escape(pattern).replace('\\*', '.*')
        
        # Add anchors to match the entire string
        regex_pattern = '^' + regex_pattern + '$'
        
        # Compile the regex pattern
        compiled_pattern = re.compile(regex_pattern)
        
        # Check if the URL matches the pattern
        return bool(compiled_pattern.match(url))
    
    def __flatten_dict(orig_dict, sep="_"):
        """
        Given a possibly nested dictionary containing logs, make a flat
        dictionary where each key-value pair represent one user session
        """
        new_dict = {}
        for first_key in orig_dict:
            if (isinstance(orig_dict[first_key], dict)):
                for second_key in orig_dict[first_key]:
                    if (isinstance(orig_dict[first_key][second_key], dict)):
                        for time_key in orig_dict[first_key][second_key]:
                            combined_key = first_key + sep + second_key + sep + time_key
                            new_dict[combined_key] = orig_dict[first_key][second_key][time_key]
                    else:
                        combined_key = first_key + sep + second_key
                        new_dict[combined_key] = orig_dict[first_key][second_key]
            else:
                new_dict[first_key] = orig_dict[first_key]

        return new_dict

    def __chunk_by_domain(log, re):
        """
        Separate logs by the site that users interact with
        :param log: Userale log in the form of dictionary
        :param log: 
        :return: A dictionary that represent sets separated by unique browserSessionId
        """
        grouped_data = {}
        for key in log:
            # Depending on the log types, tabID can be inside the details element
            if 'pageUrl' in key:
                domain = 'domain' + urlparse(key['pageUrl']).netloc
                # Filter with the "re" parameter
                if (re != "."):
                    if (Session.__match_url(domain, re)):
                        domain_key = 'domain' + re
                    else:
                        #Does not match, so we are skipping it
                        continue
                else:
                    domain_key = domain
            else:
                domain_key = 'unknown' 

            if domain_key not in grouped_data:
                grouped_data[domain_key] = []
            grouped_data[domain_key].append(key)
        return grouped_data