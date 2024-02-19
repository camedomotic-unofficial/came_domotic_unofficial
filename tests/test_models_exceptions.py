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
Unit tests for the CameDomoticError class and its subclasses.
"""

import pytest
from came_domotic_unofficial.models import (
    CameDomoticAuthError,
    CameDomoticBadAckError,
    CameDomoticError,
    CameDomoticRemoteServerError,
    CameDomoticRequestError,
    CameDomoticServerNotFoundError,
)


def test_came_domotic_error():
    """
    Test if the CameDomoticRemoteServerError can be raised correctly.
    """
    with pytest.raises(CameDomoticError) as exc_info:
        raise CameDomoticError("Test error message")

    assert isinstance(exc_info.value, Exception)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_server_not_found_error():
    """
    Test if the CameDomoticServerNotFoundError can be raised correctly.
    """
    with pytest.raises(CameDomoticServerNotFoundError) as exc_info:
        raise CameDomoticServerNotFoundError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_auth_error():
    """
    Test if the CameDomoticAuthError can be raised correctly.
    """
    with pytest.raises(CameDomoticAuthError) as exc_info:
        raise CameDomoticAuthError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_remote_server_error():
    """
    Test if the CameDomoticRemoteServerError can be raised correctly.
    """
    with pytest.raises(CameDomoticRemoteServerError) as exc_info:
        raise CameDomoticRemoteServerError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_request_error():
    """
    Test if the CameDomoticRequestError can be raised correctly.
    """
    with pytest.raises(CameDomoticRequestError) as exc_info:
        raise CameDomoticRequestError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_bad_ack_error():
    """ "
    Test if the CameDomoticBadAckError can be raised correctly with a reason.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError(9, "Session expired.")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Bad ack code: 9 - Reason: Session expired."


def test_came_domotic_bad_ack_error_without_reason():
    """
    Test if the CameDomoticBadAckError can be raised without a reason.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError(9)

    assert str(exc_info.value) == "Bad ack code: 9"


def test_came_domotic_bad_ack_error_no_ack_or_wrong():
    """
    Test if the CameDomoticBadAckError can be raised correctly without inputs.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError()

    assert str(exc_info.value) == "Bad ack code."

    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError("TEST")

    assert str(exc_info.value) == "Bad ack code: TEST"

    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError("TEST", 9)

    assert str(exc_info.value) == "Bad ack code: TEST - Reason: 9"
