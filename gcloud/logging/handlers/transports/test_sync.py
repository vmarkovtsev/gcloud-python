# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import unittest2


class TestSyncHandler(unittest2.TestCase):

    PROJECT = 'PROJECT'

    def _getTargetClass(self):
        from gcloud.logging.handlers.transports import SyncTransport
        return SyncTransport

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        NAME = "python_logger"
        transport = self._makeOne(client, NAME)
        self.assertEqual(transport.logger.name, "python_logger")

    def test_send(self):
        client = _Client(self.PROJECT)
        STACKDRIVER_LOGGER_NAME = "python"
        PYTHON_LOGGER_NAME = "mylogger"
        transport = self._makeOne(client, STACKDRIVER_LOGGER_NAME)
        MESSAGE = "hello world"
        record = _Record(PYTHON_LOGGER_NAME, logging.INFO, MESSAGE)

        transport.send(record, MESSAGE)
        EXPECTED_STRUCT = {
            "message": MESSAGE,
            "python_logger": PYTHON_LOGGER_NAME
        }
        EXPECTED_SENT = (EXPECTED_STRUCT, logging.INFO)
        self.assertEqual(
            transport.logger.log_struct_called_with, EXPECTED_SENT)


class _Record(object):

    def __init__(self, name, level, message):
        self.name = name
        self.levelname = level
        self.message = message
        self.exc_info = None
        self.exc_text = None
        self.stack_info = None


class _Logger(object):

    def __init__(self, name):
        self.name = name

    def log_struct(self, message, severity=None):
        self.log_struct_called_with = (message, severity)


class _Client(object):

    def __init__(self, project):
        self.project = project

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger


class _Handler(object):

    def __init__(self, level):
        self.level = level  # pragma: NO COVER

    def acquire(self):
        pass  # pragma: NO COVER

    def release(self):
        pass  # pragma: NO COVER
