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

"""
Tests for all the CAME Domotic entities.
"""

from datetime import datetime
from unittest.mock import Mock, PropertyMock, patch
from freezegun import freeze_time
import requests
import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from, lists

from came_domotic_unofficial import (
    CameETIDomoServer,
    CameDomoticServerNotFoundError,
)
from came_domotic_unofficial.models import (
    CameDomoticRequestError,
    EntityStatus,
    Light,
)

# from came_domotic_unofficial.models import (
#     CameEntitiesSet,
#     CameEntity,
#     Feature,
#     Light,
#     EntityStatus,
#     LightType,
#     Opening,
#     OpeningType,
# )

# region CameETIDomoServer tests


# region __init__ tests


@patch("requests.get")
@given(
    host1=integers(min_value=0, max_value=255),
    host2=integers(min_value=0, max_value=255),
    host3=integers(min_value=0, max_value=255),
    host4=integers(min_value=0, max_value=255),
)  # Generate a random IP address
@given(username=text(min_size=1), password=text(min_size=1))
def test_init_with_valid_host(
    mock_get, host1, host2, host3, host4, username, password
):
    """
    Test that the Domo object is correctly initialized with a valid host.
    """
    mock_get.return_value.status_code = 200
    domo = CameETIDomoServer(f"{host1}.{host2}.{host3}.{host4}")
    assert (
        domo._host  # pylint: disable=protected-access
        == f"http://{host}/domo/"
    )
    assert domo._username == username  # pylint: disable=protected-access
    assert domo._password == password  # pylint: disable=protected-access

    assert domo._cseq == 0  # pylint: disable=protected-access
    assert domo._session_id == ""  # pylint: disable=protected-access
    assert (
        domo._session_expiration_timestamp  # pylint: disable=protected-access
        is None
    )
    assert domo._username == username  # pylint: disable=protected-access
    assert domo._password == password  # pylint: disable=protected-access

    assert domo._keycode == ""  # pylint: disable=protected-access
    assert domo._software_version == ""  # pylint: disable=protected-access
    assert domo._server_type == ""  # pylint: disable=protected-access
    assert domo._server_board == ""  # pylint: disable=protected-access
    assert domo._serial_number == ""  # pylint: disable=protected-access
    assert (
        not domo._entities  # pylint: disable=protected-access
    )  # An empty dict is falsey

    assert domo._keycode == domo._keycode  # pylint: disable=protected-access
    assert (
        domo.software_version
        == domo._software_version  # pylint: disable=protected-access
    )
    assert (
        domo.server_type
        == domo._server_type  # pylint: disable=protected-access
    )
    assert (
        domo.server_board
        == domo._server_board  # pylint: disable=protected-access
    )
    assert (
        domo.serial_number
        == domo._serial_number  # pylint: disable=protected-access
    )


def test_init_with_empty_or_not_valid_host():
    """
    Test that the Domo object raises a TypeError
    when the host is not a valid string.
    """
    with pytest.raises(TypeError):
        CameETIDomoServer(None)

    with pytest.raises(TypeError):
        CameETIDomoServer("")

    with pytest.raises(TypeError):
        CameETIDomoServer(123)


@patch("requests.get")
def test_init_with_unavailable_host(mock_get):
    """
    Test that the Domo object raises a CameDomoticServerNotFoundError
    when the host is unavailable.
    """
    mock_get.return_value.status_code = 404
    with pytest.raises(CameDomoticServerNotFoundError):
        CameETIDomoServer("99.99.99.99")


@patch("requests.get")
def test_init_with_valid_host_and_request_exception(mock_get):
    """
    Test that the Domo object raises a CameDomoticServerNotFoundError
    when the host is valid but the request raises an exception.
    """
    mock_get.side_effect = requests.exceptions.ConnectTimeout
    with pytest.raises(CameDomoticServerNotFoundError):
        CameETIDomoServer("1.2.3.4")


# endregion


# region _send_command tests


@patch("requests.get")
@patch("requests.post")
def test_send_command_with_successful_request(mock_post, mock_get):
    """
    Test that the _send_command method returns the response
    when the request is successful.
    """
    mock_get.return_value.status_code = 200
    mock_post.return_value.status_code = 200
    # mock_response_post = mock_post.return_value
    # mock_response_post.json.return_value = {"key": "value"}
    domo = CameETIDomoServer("127.0.0.1")
    response = domo._send_command(  # pylint: disable=protected-access
        {"key": "value"}
    )
    assert response.status_code == 200
    mock_post.assert_called_once_with(
        "http://127.0.0.1/domo/",
        data={"command": '{"key": "value"}'},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "Keep-Alive",
        },
        timeout=10,
    )


@patch("requests.get")
@patch("requests.post")
def test_send_command_with_failed_request(mock_post, mock_get):
    """
    Test that the _send_command method raises a CameDomoticRequestError
    when the request fails.
    """
    mock_get.return_value.status_code = 200
    mock_post.return_value.status_code = 500
    domo = CameETIDomoServer("127.0.0.1")
    with pytest.raises(CameDomoticRequestError):
        domo._send_command(  # pylint: disable=protected-access
            {"command": "test"}
        )


@patch("requests.get")
@patch("requests.post")
def test_send_command_with_request_exception(mock_post, mock_get):
    """
    Test that the _send_command method raises a CameDomoticRequestError
    when the request raises an exception.
    """
    mock_get.return_value.status_code = 200
    mock_post.side_effect = requests.exceptions.RequestException
    domo = CameETIDomoServer("127.0.0.1")
    with pytest.raises(CameDomoticRequestError):
        domo._send_command(  # pylint: disable=protected-access
            {"command": "test"}
        )


# endregion


# region login tests


@patch("requests.get", return_value=Mock(status_code=200))
@patch.object(
    CameETIDomoServer,
    "is_authenticated",
    new_callable=PropertyMock,
    return_value=True,
)
def test_login_when_already_authenticated(_, __):
    """
    Test that the login method returns True
    when the user is already authenticated.
    """
    domo = CameETIDomoServer("127.0.0.1", "username", "password")
    assert domo._login() is True


@patch("requests.get", return_value=Mock(status_code=200))
@patch.object(CameETIDomoServer, "_send_command")
@patch.object(
    CameETIDomoServer,
    "is_authenticated",
    new_callable=PropertyMock,
    return_value=False,
)
@freeze_time("2024-01-01")
def test_login_with_valid_response(
    mock_is_authenticated, mock_send_command, mock_get
):
    """
    Test that the login method correctly handles a valid response
    from the server.
    """
    mock_send_command.return_value = {
        "sl_cmd": "sl_registration_ack",
        "sl_client_id": "my_session_id",
        "sl_keep_alive_timeout_sec": 900,
        "sl_data_ack_reason": 0,
    }
    domo = CameETIDomoServer("127.0.0.1", "username", "password")
    assert domo._login() is True
    assert (
        domo._session_id == "my_session_id"  # pylint: disable=protected-access
    )
    assert (
        domo._session_expiration_timestamp  # pylint: disable=protected-access
        == (datetime(2024, 1, 1, 0, 14, 30))
    )


@patch("requests.get", return_value=Mock(status_code=200))
@patch.object(CameETIDomoServer, "_send_command")
@patch.object(
    CameETIDomoServer,
    "is_authenticated",
    new_callable=PropertyMock,
    return_value=False,
)
def test_login_with_error_response(_, mock_send_command, __):
    """
    Test that the login method correctly handles an error response from the server.
    """
    mock_send_command.return_value = {
        "sl_cmd": "sl_registration_ack",
        "sl_data_ack_reason": 1,
    }
    domo = CameETIDomoServer("127.0.0.1", "username", "password")
    assert domo._login() is False


@patch("requests.get", return_value=Mock(status_code=200))
@patch.object(CameETIDomoServer, "_send_command")
@patch.object(
    CameETIDomoServer,
    "is_authenticated",
    new_callable=PropertyMock,
    return_value=False,
)
def test_login_with_request_error(_, mock_send_command, __):
    """
    Test that the login method correctly handles a CameDomoticRequestError.
    """
    mock_send_command.side_effect = CameDomoticRequestError("Request error")
    domo = CameETIDomoServer("127.0.0.1", "username", "password")
    assert domo._login() is False


@patch("requests.get", return_value=Mock(status_code=200))
@patch.object(CameETIDomoServer, "_send_command")
@patch.object(
    CameETIDomoServer,
    "is_authenticated",
    new_callable=PropertyMock,
    return_value=False,
)
def test_login_with_unexpected_error(_, mock_send_command, __):
    """
    Test that the login method correctly handles an unexpected error.
    """
    mock_send_command.side_effect = Exception("Unexpected error")
    domo = CameETIDomoServer("127.0.0.1", "username", "password")
    assert domo._login() is False


# endregion
