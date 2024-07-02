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

from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter
from typing import Dict, Union
from datetime import datetime, timezone, tzinfo
import dateparser

from distill.core.types import JsonDict, JSONSerializable, Timestamp
from distill.schemas.userale import UserAleSchema

ta = TypeAdapter(JsonDict)

class Log:
    """
    Base class for log object representation.
    Arguments:
        data: a json parsable string or JsonObject to validate and parse
        schema: a pydantic schema from which to validate the provided log;
                defaults to UserAle log schema
    """

    def __init__(self, data: Union[str, JsonDict], schema=UserAleSchema):
        if not issubclass(schema, BaseModel):
            raise TypeError("schema should inherit from pydantic.BaseModel")

        if isinstance(data, str):
            schema.model_validate_json(data, strict=True)
            data = json.loads(data)
        elif ta.validate_python(data):
            schema.model_validate(data, strict=True)
        else:
            raise TypeError("ERROR: " + str(type(data)) + " data should be either a string or a JsonDict")
        self.data = schema(**data)

        # TODO: need to create ID field here on object initialization

    def to_json(self) -> str:
        return self.data.model_dump_json(by_alias=True)

    def to_dict(self) -> JsonDict:
        return self.data.model_dump(by_alias=True)


def normalize_timestamp(timestamp: Timestamp, tz: str ='+0000') -> datetime:
    """
    Attempts to normalize a given timestamp to a datetime object 
    Arguments:
        timestamp: a int or float representing (milli)seconds since the epoch or an 
            arbitrary timestamp string (ex: '02/19/24 10:32:02', 1719530111079)
        tz: an arbitrary timestamp string (ex: '+0100')
    """
    if isinstance(timestamp, str):
        # Only uses US/Eastern if there is no associated timezone
        parsed = dateparser.parse(timestamp, settings={'TIMEZONE': tz})
        if parsed is None:
            raise ValueError("ERROR: could not parse timestamp " + str(timestamp))
        return parsed.astimezone(timezone.utc)
    elif isinstance(timestamp, float) or isinstance(timestamp, int):
        tzinformation = dateparser.parse("00:01", settings={'TIMEZONE': tz}).tzinfo

        if timestamp > datetime.now().timestamp():
            timestamp = timestamp / 1000
        return datetime.fromtimestamp(float(timestamp), tzinformation)
    else:
        raise TypeError("ERROR: " + str(type(timestamp)) + " timestamp should be a string, int, or datetime object")
