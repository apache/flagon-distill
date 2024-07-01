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
from typing import Any

from distill.core.core_types import JsonObject 
from distill.schemas.userale import LogSchema


class Log:
    """
    Base class for log object representation.
    Arguments:
        data: a json parsable string or JsonObject to validate and parse
        schema: a pydantic schema from which to validate the provided log;
                defaults to UserAle log schema
    """

    def __init__(self, data: str | JsonObject, schema=LogSchema):
        if not issubclass(schema, BaseModel):
            raise TypeError("schema should inherit from pydantic.BaseModel")

        if isinstance(data, dict):
            schema.model_validate(data, strict=True)

            self.data = LogSchema(**data)
        elif isinstance(data, str):
            schema.model_validate_json(data, strict=True)

            json_str_data = json.loads(data)
            self.data = schema(**json_str_data)
        else:
            raise TypeError("ERROR: " + str(type(data)) + " data should be either a string or a JsonObject")

        # TODO: need to create ID field here on object initialization

    def to_json(self) -> str:
        return self.data.model_dump_json(by_alias=True)

    def to_dict(self) -> JsonObject:
        return self.data.model_dump(by_alias=True)
