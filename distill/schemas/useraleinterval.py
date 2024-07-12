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

from pydantic import AliasGenerator, field_serializer, field_validator
from pydantic.alias_generators import to_camel
from pydantic.config import ConfigDict

from .useralebase import UserAleBaseSchema


class UserAleIntervalSchema(UserAleBaseSchema):
    """
    A raw or custom log produced by UserAle
    """

    model_config = ConfigDict(
        title="IntervalLog",
        alias_generator=AliasGenerator(
            validation_alias=to_camel, serialization_alias=to_camel
        ),
    )

    count: int
    duration: int
    start_time: int
    end_time: int
    target_change: bool
    type_change: bool

    @field_validator("start_time", "end_time")
    def validate_st(cls, st: float):
        return datetime.fromtimestamp(st / 1000)

    @field_serializer("start_time", "end_time")
    def serialize_st(self, st: datetime):
        return int(st.timestamp() * 1000)

    # add in end_time validator and serializer under same tag

    def _timestamp(self):
        """
        Returns:
            float: POSIX time from userALE log's start_time field
        """
        return self.start_time.timestamp()
