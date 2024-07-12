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

from pydantic import AliasGenerator, BaseModel, Field, field_serializer, field_validator
from pydantic.alias_generators import to_camel
from pydantic.config import ConfigDict

from .useralebase import UserAleBaseSchema


class Location(BaseModel):
    x: Optional[int]
    y: Optional[int]


class ScrnRes(BaseModel):
    width: int
    height: int


class Details(BaseModel):
    window: bool


class UserAleRawSchema(UserAleBaseSchema):
    """
    A raw or custom log produced by UserAle
    """

    model_config = ConfigDict(
        title="RawLog",
        alias_generator=AliasGenerator(
            validation_alias=to_camel, serialization_alias=to_camel
        ),
    )

    client_time: int
    micro_time: int = Field(..., lt=2)
    location: Location
    scrn_res: ScrnRes
    details: Details

    @field_validator("client_time")
    def validate_ct(cls, ct: float):
        return datetime.fromtimestamp(ct / 1000)

    @field_serializer("client_time")
    def serialize_ct(self, ct: datetime):
        return int(ct.timestamp() * 1000)

    def _timestamp(self):
        """
        Returns:
            float: POSIX time from userALE log's client_time field
        """
        return self.client_time.timestamp()
