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
from unittest.mock import patch, Mock
import requests
import pytest
from mocked_responses import FEATURE_LIST_RESP
from utils import (
    mock_get_init,
    mock_post_method,
    mock_post_method_error_non_auth,
)
from came_domotic_unofficial.came_etidomo_server import CameETIDomoServer
from came_domotic_unofficial.models import CameDomoticRequestError


# Assuming these are the public properties of your class
public_properties = {
    "is_authenticated": True,
    "keycode": FEATURE_LIST_RESP["keycode"],
    "software_version": FEATURE_LIST_RESP["swver"],
    "server_type": FEATURE_LIST_RESP["type"],
    "board": FEATURE_LIST_RESP["board"],
    "serial_number": FEATURE_LIST_RESP["serial"],
}


@patch("requests.Session.get", side_effect=mock_get_init)
@pytest.mark.parametrize("property_name, expected_value", public_properties.items())
def test_properties_already_retrieved(mock_get, property_name, expected_value):
    server = CameETIDomoServer("192.168.x.x", "user", "password")

    # Manually set session attributes to emulate the authentication
    server._session_id = "my_session_id"
    server._session_keep_alive_timeout_sec = 900
    server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)
    server._cseq = 0
    server._keycode = str(FEATURE_LIST_RESP["keycode"])
    server._software_version = str(FEATURE_LIST_RESP["swver"])
    server._type = str(FEATURE_LIST_RESP["type"])
    server._board = str(FEATURE_LIST_RESP["board"])
    server._serial_number = str(FEATURE_LIST_RESP["serial"])

    # Override the dispose method to avoid calling the remote server
    server.dispose = lambda: None  # type: ignore

    assert getattr(server, property_name) == expected_value


# Patched GET to mock the check of the server availability in the __init__ phase
# and POST to mock the retrieval of the properties values from the server
@patch("requests.Session.get", side_effect=mock_get_init)
@patch("requests.Session.post", side_effect=mock_post_method)
@pytest.mark.parametrize("property_name, expected_value", public_properties.items())
def test_properties_not_retrieved(mock_post, mock_get, property_name, expected_value):
    server = CameETIDomoServer("192.168.x.x", "user", "password")
    server.dispose = lambda: None  # type: ignore

    if property_name == "is_authenticated":
        assert getattr(server, property_name) is False  # We're not yet authenticated
    else:
        assert getattr(server, property_name) == expected_value


@patch("requests.Session.get", side_effect=mock_get_init)
@patch("requests.Session.post", side_effect=mock_post_method_error_non_auth)
@pytest.mark.parametrize("property_name, expected_value", public_properties.items())
def test_properties_not_retrieved_request_error(
    mock_post, mock_get, property_name, expected_value
):
    server = CameETIDomoServer("192.168.x.x", "user", "password")
    server.dispose = lambda: None  # type: ignore

    if property_name == "is_authenticated":
        assert getattr(server, property_name) is False
    else:
        with pytest.raises(CameDomoticRequestError):
            getattr(server, property_name)
