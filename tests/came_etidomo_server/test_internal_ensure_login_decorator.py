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

# from datetime import datetime

# from freezegun import freeze_time
# import requests
# import pytest
# from hypothesis import given
# from hypothesis.strategies import integers, text, sampled_from, lists

# import os
# import time
# import pytest
# from came_domotic_unofficial import (
#     CameETIDomoServer,
#     # CameDomoticServerNotFoundError,
# )
# from came_domotic_unofficial.models import (
#     EntityStatus,
#     EntityType,
#     Light,
# )

# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=no-name-in-module

from unittest.mock import Mock
import pytest
from came_domotic_unofficial.came_etidomo_server import ensure_login
from came_domotic_unofficial.models import CameDomoticAuthError


@pytest.fixture
def mock_func():
    return Mock()


@pytest.fixture
def decorated_func(mock_func):
    return ensure_login(mock_func)


def test_ensure_login_when_already_authenticated(decorated_func, mock_func):
    obj = Mock()
    obj.is_authenticated = True

    decorated_func(obj)

    mock_func.assert_called_once_with(obj)


def test_ensure_login_when_login_succeeds(decorated_func, mock_func):
    obj = Mock()
    obj.is_authenticated = False
    obj._login.return_value = True

    decorated_func(obj)

    mock_func.assert_called_once_with(obj)


def test_ensure_login_when_login_fails(decorated_func):
    obj = Mock()
    obj.is_authenticated = False
    obj._login.return_value = False

    with pytest.raises(CameDomoticAuthError):
        decorated_func(obj)


def test_ensure_login_when_login_raises_exception(decorated_func):
    obj = Mock()
    obj.is_authenticated = False
    obj._login.side_effect = Exception("Login error")

    with pytest.raises(CameDomoticAuthError):
        decorated_func(obj)
