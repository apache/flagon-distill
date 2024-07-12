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
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from .base import BaseSchema


class Browser(BaseModel):
    browser: str
    version: str


class UserAleBaseSchema(BaseSchema):
    """
    A raw or custom log produced by UserAle
    """

    target: str
    path: List[str]
    page_url: str
    page_title: str
    page_referrer: str
    browser: Browser
    type_field: str = Field(..., validation_alias="type", serialization_alias="type")
    log_type: str
    user_action: bool
    user_id: str
    tool_version: Optional[str]
    tool_name: Optional[str]
    userale_version: Optional[str]
    session_id: str
    http_session_id: str
    browser_session_id: str

    def _timestamp(self):
        """
        Returns:
            float: POSIX time from userALE log's client_time field
        """
        pass
