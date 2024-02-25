# Copyright 2024 - GitHub user: fredericks1982

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=protected-access
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

"""
Test the public special methods of the CameETIDomoServer class (__init__, __enter__,
__exit__, __del__).
"""

from datetime import datetime, timezone
from unittest.mock import patch
import pytest
from mocked_responses import FEATURE_LIST_RESP
from came_domotic_unofficial.came_etidomo_server import CameETIDomoServer

# Assuming these are the public properties of your class
public_properties = {
    "is_authenticated": True,
    "keycode": FEATURE_LIST_RESP["keycode"],
    "software_version": FEATURE_LIST_RESP["swver"],
    "server_type": FEATURE_LIST_RESP["type"],
    "board": FEATURE_LIST_RESP["board"],
    "serial_number": FEATURE_LIST_RESP["serial"],
}


@pytest.fixture
@patch("requests.Session.get")
def mocked_server_auth(mock_get) -> CameETIDomoServer:
    """
    Fixture that provides an authenticated instance of CameETIDomoServer.
    """
    mock_get.return_value.status_code = 200
    server = CameETIDomoServer("192.168.0.3", "user", "password")

    # Manually set session attributes to emulate the authentication
    server._session_id = "my_session_id"
    server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)
    server._cseq = 0
    server._keycode = FEATURE_LIST_RESP["keycode"]
    server._software_version = FEATURE_LIST_RESP["swver"]
    server._type = FEATURE_LIST_RESP["type"]
    server._board = FEATURE_LIST_RESP["board"]
    server._serial_number = FEATURE_LIST_RESP["serial"]

    # Emulate the dispose method to avoid calling the remote server
    server.dispose = lambda: None

    return server


@pytest.mark.parametrize("property_name, expected_value", public_properties.items())
def test_properties(mocked_server_auth, property_name, expected_value):
    # Test that each property can be retrieved without error
    assert hasattr(mocked_server_auth, property_name)
    assert getattr(mocked_server_auth, property_name) == expected_value
