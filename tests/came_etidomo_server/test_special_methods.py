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
import gc
from unittest.mock import patch
import pytest
import requests
from came_domotic_unofficial.came_etidomo_server import (
    CameETIDomoServer,
    CameDomoticServerNotFoundError,
)


@pytest.fixture
@patch("requests.Session.get")
def mocked_server(mock_get) -> CameETIDomoServer:
    """
    Fixture that provides an authenticated instance of CameETIDomoServer.
    """
    mock_get.return_value.status_code = 200
    server = CameETIDomoServer("192.168.0.3", "user", "password")
    return server


@patch("requests.Session.get")
def test_init_with_valid_input(mock_get):
    mock_get.return_value.status_code = 200
    server = CameETIDomoServer("192.168.0.3", "user", "password")
    assert server._host == "192.168.0.3"
    assert server._username == "user"
    assert server._password == "password"
    # Emulate the dispose method to avoid calling the remote server
    server.dispose = lambda: None


def test_init_with_empty_host():
    with pytest.raises(TypeError):
        CameETIDomoServer("", "user", "password")


def test_init_with_non_string_host():
    with pytest.raises(TypeError):
        CameETIDomoServer(123, "user", "password")


def test_init_with_non_string_username():
    with pytest.raises(TypeError):
        CameETIDomoServer("192.168.0.3", 123, "password")


def test_init_with_non_string_password():
    with pytest.raises(TypeError):
        CameETIDomoServer("192.168.0.3", "user", 123)


@patch("requests.Session.get")
def test_init_with_unavailable_server(mock_get):
    mock_get.return_value.status_code = 404
    with pytest.raises(CameDomoticServerNotFoundError):
        CameETIDomoServer("192.168.0.3", "user", "password")


@patch("requests.Session.get")
def test_init_with_request_exception(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Request error")
    with pytest.raises(CameDomoticServerNotFoundError):
        CameETIDomoServer("192.168.0.3", "user", "password")


def test_context_manager_entering(mocked_server):
    """
    Test that entering a 'with' construct the instance of the CameETIDomo object
    is returned correctly.
    """
    with mocked_server as s:
        assert s is mocked_server
        # Emulate the dispose method to avoid calling the remote server
        s.dispose = lambda: None


@patch.object(CameETIDomoServer, "dispose", autospec=True)
def test_context_manager_exit_dispose(mock_dispose, mocked_server):
    """Test that leaving a 'with' construct the 'dispose' method is called."""
    with mocked_server:
        pass
    mock_dispose.assert_called_once()


@patch.object(CameETIDomoServer, "dispose", autospec=True)
def test_context_manager_exit_dispose_with_exception(mock_dispose, mocked_server):
    """
    Test that leaving a 'with' construct with an exception the 'dispose' method
    is called.
    """
    try:
        with mocked_server:
            raise Exception("Test exception")
    except Exception:
        pass
    mock_dispose.assert_called_once()


@patch("requests.Session.get")
@patch.object(CameETIDomoServer, "dispose", autospec=True)
def test_garbage_collector_calls_dispose(mock_dispose, mock_get):
    """
    Test that the __del__ method calls the dispose method.
    """
    mock_get.return_value.status_code = 200
    server = CameETIDomoServer("192.168.0.3", "user", "password")

    # Force the garbage collector to call the __del__ method
    del server
    gc.collect()

    assert mock_dispose.call_count >= 1
