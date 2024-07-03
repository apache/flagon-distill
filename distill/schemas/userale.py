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
from typing import List, Optional

from pydantic import AliasGenerator, BaseModel, Field, field_serializer, field_validator
from pydantic.alias_generators import to_camel
from pydantic.config import ConfigDict
from datetime import datetime


class Browser(BaseModel):
    browser: str
    version: str


class Location(BaseModel):
    x: Optional[int]
    y: Optional[int]


class ScrnRes(BaseModel):
    width: int
    height: int


class Details(BaseModel):
    window: bool


class UserAleSchema(BaseModel):
    """
    A raw or custom log produced by UserAle
    """

    model_config = ConfigDict(
        title="Log",
        alias_generator=AliasGenerator(
            validation_alias=to_camel, serialization_alias=to_camel
        ),
    )

    target: str
    path: List[str]
    page_url: str
    page_title: str
    page_referrer: str
    browser: Browser
    client_time: int 
    micro_time: int = Field(..., lt=2)
    location: Location
    scrn_res: ScrnRes
    type_field: str = Field(..., validation_alias="type", serialization_alias="type")
    log_type: str
    user_action: bool
    details: Details
    user_id: str
    tool_version: Optional[str]
    tool_name: Optional[str]
    userale_version: Optional[str]
    session_id: str

    @field_validator("client_time")
    def validate_ct(cls, ct: float):
        return datetime.fromtimestamp(ct / 1000)

    @field_serializer("client_time")
    def serialize_ct(self, ct: datetime):
        return int(ct.timestamp() * 1000)

