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
from enum import Enum
import json

class Sessions_Type(Enum):
    TAB = "tab"
    DOMAIN = "domain"
    DEFAULT = "default"

class Sessions:
    """
    A collection of Session objects.
    """

    ##############################################
    # IMPLEMENTATION OF PYTHON DEFINED FUNCTIONS #
    ##############################################

    def __init__(self, sessions=[]):
        """
        Sessions initialization function.

        :param sessions ({}): A dictionary that describe the parsed logs to sessions
        """
        self.sessions = sessions
        self.sessions_type = Sessions_Type.DEFAULT

    def __iter__(self):
        """
        Allows Sessions to be iterable.
        """
        return iter(self.sessions)

    def __len__(self):
        """
        Allows Sessions to return the number of sessions it contains.
        """
        return len(self.sessions)

    def get_sessions_type(self):
        """
        Gets the type of a groupings/parsing that were used to create the sessions.

        :return: The sessions type.
        """
        return self.sessions_type
    
    def __str__(self):
        """
        Creates a readable string for Sessions.
        """
        sessions_in_str = "{"
        for session in self.sessions:
            # Remove the bracket
            sessions_in_str += str(session)[1:-1] + ","
        sessions_in_str = sessions_in_str[:-1] + "}"
        #Remove the last "," and add the closing bracket
        return sessions_in_str


    ############################
    # DATA STRUCTURE FUNCTIONS #
    ############################

    def get_session_list(self):
        """
        Returns a list of Session objects in Sessions.

        :return: A list of session objects.
        """
        return self.sessions
    
    def get_session_names(self):
        """
        Returns the names session names (key of the session dictionary).

        :return: A list of session names
        """
        session_names = []
        for session in self.sessions:
            session_names.append(session.get_session_name())
        return session_names

    
