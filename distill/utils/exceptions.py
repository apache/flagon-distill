# -*- coding: utf-8 -*-
#
# This file is part of Distill.
# Copyright 2016 The Charles Stark Draper Laboratory, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Error (Exception):
    """Base class for exceptions."""
    pass

class ValidationError (Error):
	""" Exceptions raised for errors in validated a url."""

	def __init__ (self, url, msg):
		self.url = url
		self.msg = msg
