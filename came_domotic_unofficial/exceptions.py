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
CAME Domotic exceptions.
"""


class CameDomoticError(Exception):
    """Base exception class for the Came Domotic package."""


class CameDomoticServerNotFoundError(CameDomoticError):
    """Raised when the specified host is not available"""


# Authentication exception class
class CameDomoticAuthError(CameDomoticError):
    """Raised when there is an authentication error with the remote server."""


# Server exception class
class CameDomoticRemoteServerError(CameDomoticError):
    """Raised when there is an error related to the Came Domotic server."""


class CameDomoticRequestError(CameDomoticError):
    """Raised when the server doesn't accept a user request."""


class CameDomoticBadAckError(CameDomoticRequestError):
    """Raised when the server returns a bad ack code/reason.

    :param ack_code: the ack code returned by the server.
    :param reason: the reason returned by the server."""

    def __init__(self, ack_code=None, reason=None):
        """Constructor for the CameDomoticBadAckError class.

        :param ack_code: the ack code returned by the server.
        :param reason: the reason returned by the server (optional).
        """

        # Convert with str() to ensure that will never raise an exception
        super().__init__(
            f"Bad ack code: {str(ack_code) if ack_code else 'N/A'} - "
            f"Reason: {str(reason) if reason else 'N/A'}"
        )
