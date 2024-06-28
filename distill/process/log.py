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
from pydantic import BaseModel, Field, ValidationError
from pydantic.config import ConfigDict

from decimal import Decimal
from typing import List, Union, Any
from enum import Enum

class Browser(BaseModel):
    browser: str
    version: str

class Location(BaseModel):
    x: Union[int, None]
    y: Union[int, None]

class ScrnRes(BaseModel):
    width: int
    height: int 

class LogType(str, Enum):
    raw = "raw"
    custom = "custom"

class Details(BaseModel):
    window: bool

class LogSchema(BaseModel):
    """
    A raw or custom log produced by userale
    """
    model_config = ConfigDict(title="Log")

    target: str
    path: List[str]
    pageUrl: str 
    pageTitle: str
    pageReferrer: str
    browser: Browser
    clientTime: int 
    microTime: int = Field(..., lt=2)
    location: Location 
    scrnRes: ScrnRes 
    type_field: str = Field(..., alias="type", serialization_alias="type")
    logType: LogType
    userAction: bool
    details: Details
    userId: str 
    toolVersion: Union[str, None] 
    toolName: Union[str, None]
    useraleVersion: Union[str, None] 
    sessionID: str 

class Log():
    def __init__(self, log_data: str):
        LogSchema.model_validate_json(log_data)

        json_data = json.loads(log_data)
        self.data = LogSchema(**json_data)       

        # TODO: need to create ID field here on object initialization

    def serializeJson(self) -> str:
        return self.data.model_dump_json(by_alias=True)

    def deserializeJson(self) -> dict[str, Any]:
        return self.data.model_dump(by_alias=True)

