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
This file is used to test the internal code coverage of the CameETIDomoServer class.
"""

# pylint: disable=import-error
# pylint: disable=missing-function-docstring
# pylint: disable=protected-access
# pylint: disable=unused-argument

import datetime
from unittest.mock import patch
import pytest

from utils import (
    mock_get_init,
    mock_post_method,
    mock_post_method_error_auth,
    mock_post_method_error_non_auth,
)
from came_domotic_unofficial.came_etidomo_server import CameETIDomoServer
from came_domotic_unofficial.models import (
    CameDomoticAuthError,
    CameDomoticRequestError,
    Light,
    EntityStatus,
)

public_properties = [
    "keycode",
    "software_version",
    "server_type",
    "board",
    "serial_number",
]


@pytest.fixture
@patch("requests.Session.get", side_effect=mock_get_init)
def mocked_server(mock_get) -> CameETIDomoServer:
    server = CameETIDomoServer("192.168.x.x", "user", "password")
    server.dispose = lambda: None  # type: ignore
    return server


@patch("requests.Session.post", side_effect=mock_post_method)
@pytest.mark.parametrize("property_name", public_properties)
def test_get_property(mock_post, property_name, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    property_value = getattr(mocked_server, property_name)
    assert mocked_server.is_authenticated
    assert property_value and len(property_value) > 0


@patch("requests.Session.post", side_effect=mock_post_method_error_auth)
@pytest.mark.parametrize("property_name", public_properties)
def test_get_property_auth_error(mock_post, property_name, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    with pytest.raises(CameDomoticAuthError):
        getattr(mocked_server, property_name)
    assert not mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method_error_non_auth)
@pytest.mark.parametrize("property_name", public_properties)
def test_get_property_request_error(mock_post, property_name, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    with pytest.raises(CameDomoticRequestError):
        getattr(mocked_server, property_name)
    assert mocked_server.is_authenticated


# TODO Check that when the get_features method of a CameETIDomoServer instance
# is accessed the user is automatically authenticated before to proceed
@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_features(mock_post, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    result = mocked_server.get_features()
    assert mocked_server.is_authenticated
    assert result and len(result) > 0


@patch("requests.Session.post", side_effect=mock_post_method_error_auth)
def test_get_features_auth_error(mock_post, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    with pytest.raises(CameDomoticAuthError):
        mocked_server.get_features()
    assert not mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method_error_non_auth)
def test_get_features_request_error(mock_post, mocked_server):
    # Ensure that it is a "clean" situation
    assert not mocked_server.is_authenticated

    # Call the function that uses requests.Session.post
    with pytest.raises(CameDomoticRequestError):
        mocked_server.get_features()
    assert mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_entities(mock_post, mocked_server):
    # Prepare the server: features already retrieved but session expired
    features = mocked_server.get_features()
    mocked_server._features = features
    mocked_server._session_expiration_timestamp = datetime.datetime(
        2000, 1, 1, tzinfo=datetime.timezone.utc
    )
    assert not mocked_server.is_authenticated

    # Test
    result = mocked_server.get_entities()
    assert mocked_server.is_authenticated
    assert result and len(result) > 0


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_entities_auth_error(mock_post, mocked_server):
    # Prepare the server: features already retrieved but session expired
    features = mocked_server.get_features()
    mocked_server._features = features
    mocked_server._session_expiration_timestamp = datetime.datetime(
        2000, 1, 1, tzinfo=datetime.timezone.utc
    )
    assert not mocked_server.is_authenticated

    # Test
    with patch("requests.Session.post", side_effect=mock_post_method_error_auth):
        with pytest.raises(CameDomoticAuthError):
            mocked_server.get_entities()
    assert not mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_entities_request_error(mock_post, mocked_server):
    # Prepare the server: features already retrieved but session expired
    features = mocked_server.get_features()
    mocked_server._features = features
    mocked_server._session_expiration_timestamp = datetime.datetime(
        2000, 1, 1, tzinfo=datetime.timezone.utc
    )
    assert not mocked_server.is_authenticated

    # Test
    with patch("requests.Session.post", side_effect=mock_post_method_error_non_auth):
        result = mocked_server.get_entities()
    assert mocked_server.is_authenticated
    assert not result  # Empty set of entities


@patch("requests.Session.post", side_effect=mock_post_method)
def test_set_status(mock_post, mocked_server):
    # Prepare the server: features already retrieved but session expired
    assert not mocked_server.is_authenticated

    # Test
    result = mocked_server.set_entity_status(Light, 1, EntityStatus.ON_OPEN_TRIGGERED)
    assert mocked_server.is_authenticated
    assert result


@patch("requests.Session.post", side_effect=mock_post_method_error_auth)
def test_set_status_auth_error(mock_post, mocked_server):
    assert not mocked_server.is_authenticated

    # Test
    with pytest.raises(CameDomoticAuthError):
        mocked_server.set_entity_status(Light, 1, EntityStatus.ON_OPEN_TRIGGERED)
    assert not mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method_error_non_auth)
def test_set_status_request_error(mock_post, mocked_server):
    assert not mocked_server.is_authenticated

    # Test
    successful = mocked_server.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )
    assert not successful
    assert mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method)
def test_keep_alive(mock_post, mocked_server):
    # Prepare the server: features already retrieved but session expired
    assert not mocked_server.is_authenticated

    # Test
    result = mocked_server.keep_alive()
    assert mocked_server.is_authenticated
    assert result


@patch("requests.Session.post", side_effect=mock_post_method_error_auth)
def test_keep_alive_auth_error(mock_post, mocked_server):
    assert not mocked_server.is_authenticated

    # Test
    with pytest.raises(CameDomoticAuthError):
        mocked_server.keep_alive()
    assert not mocked_server.is_authenticated


@patch("requests.Session.post", side_effect=mock_post_method_error_non_auth)
def test_keep_alive_request_error(mock_post, mocked_server):
    assert not mocked_server.is_authenticated

    # Test
    successful = mocked_server.keep_alive()
    assert not successful
    assert mocked_server.is_authenticated
