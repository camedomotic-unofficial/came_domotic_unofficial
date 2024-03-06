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
This library allows to interact with a CAME ETI/Domo server.

The login to the remote server is managed by the library, and performed only
when required. You can always check the status of the server with the
is_authenticated property.

The library is based on the HTTP messages exchanged by the CAME Domotic Android
app. The library is not complete and does not cover all the features
of a CAME ETI/Domo server.

The library is not official and is not supported by CAME.
Use it at your own risk


Usage:
    from came_domotic_unofficial import CameETIDomoServer

    with CameETIDomoServer("192.168.0.0", "username", "password") as server:
        features = server.get_features() # list of available features
        entities = server.get_entities() # list of managed entities
        server.set_entity_status(entities[0], EntityStatus.ON)
"""

from functools import wraps
from datetime import datetime, timezone, timedelta

import json
import logging
import traceback
from typing import Optional
from typing import Dict, Any, Type
import requests

from .models.helpers import (
    _EntityType2Class,
    _Class2SwitchCommand,
)
from .models.exceptions import (
    CameDomoticBadAckError,
    CameDomoticServerNotFoundError,
    CameDomoticAuthError,
    CameDomoticRequestError,
)
from .models.enums import (
    EntityStatus,
    EntityType,
)
from .models.came_entity import (
    CameEntitySet,
    CameEntity,
)
from .models.feature import (
    Feature,
    FeatureSet,
)
from .models.light import Light
from .models.opening import Opening
from .models.scenario import Scenario

_LOGGER = logging.getLogger(__package__)

# region Wrappers


def ensure_login(func):
    """
    Ensures that the server is authenticated before executing
    the decorated method.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_authenticated:
            try:
                if not self._login():  # pylint: disable=protected-access
                    raise CameDomoticAuthError("Login failed.")
            except CameDomoticAuthError as e:
                raise e
            except Exception as e:
                _LOGGER.error("Error trying to login with the server. Error: %s", e)
                raise CameDomoticAuthError(
                    "Error trying to login with the server"
                ) from e
        return func(self, *args, **kwargs)

    return wrapper


# endregion


class CameETIDomoServer:
    """
    Represents a CAME ETI Domo server.

    This is a context manager, so you can use it in a with statement
    to properly manage the resources. The server is authenticated
    only when required, and the session is disposed when the context is exited.

    If you want, you can also manually:
    - check if the server is authenticated with the is_authenticated property.
    - keep the CAME session alive with the keep_alive() method.
    - dispose the resources currently in use with the dispose() method.

    Notice that you can still use the object after disposal, since it
    can recreate automatically the needed resources when required.

    Args:
        host (str): The host address of the server.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Properties:
        is_authenticated (bool): True if the server is authenticated.
        keycode (str): The keycode (unique ID) of the CAME ETI/Domo server.
        software_version (str): The software version of the ETI/Domo server.
        type (str): The type of CAME ETI/Domo server.
        board (str): The board type of the CAME ETI/Domo server.
        serial_number (str): The serial number of the CAME ETI/Domo server.

    Methods:
        get_features() -> CameEntitiesSet: Lists all the supported features.
        get_entities() -> CameEntitiesSet: Lists all the managed entities.
        set_entity_status(entity, status, *, brightness=None): Update an entity
        keep_alive() -> bool: Sends a keep alive request to the CAME server.
        dispose() -> None: Dispose the resources in use.
    """

    # region Constants

    # Header for every http request made to the server
    _HTTP_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
    }

    _HTTP_TIMEOUT = 10  # seconds

    # endregion

    # region Special methods

    def __init__(self, host, username, password):

        # Validate the input
        if not isinstance(host, str) or host == "":
            raise TypeError("host must be a string")
        if (
            username is None
            or password is None
            or not isinstance(username, str)
            or not isinstance(password, str)
        ):
            raise TypeError("username and password must be strings")

        # region private attributes

        # Login attributes
        self._host = host
        self._host_url = "http://" + host + "/domo/"
        self._username = username
        self._password = password

        # Session attributes
        self._http_session = requests.Session()  # This is thread safe
        self._session_id = ""
        self._session_keep_alive_timeout_sec = 0
        self._session_expiration_timestamp = datetime(2000, 1, 1, tzinfo=timezone.utc)
        self._cseq = 0  # The actual sequence starts from 1

        # Server attributes
        self._keycode = ""
        self._software_version = ""
        self._type = ""
        self._board = ""
        self._serial_number = ""

        # Features and entities
        self._features = FeatureSet()  # List of available features
        self._entities = CameEntitySet()  # List of items managed by the server

        # endregion

        # region Check host availability

        try:
            response = self._http_session.get(
                self._host_url,
                headers=self._HTTP_HEADERS,
                timeout=self._HTTP_TIMEOUT,
            )

            if response.status_code != 200:
                _LOGGER.error(
                    "The server '%s' is not available. Status code: %s",
                    host,
                    response.status_code,
                )
                raise CameDomoticServerNotFoundError(f"Server '{host}' not available")

            _LOGGER.debug(
                "The server '%s' is available.",
                self._host,
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error("The server '%s' is not available. Error: %s", host, e)
            raise CameDomoticServerNotFoundError(
                f"Server '{host}' not available"
            ) from e

        # endregion

    def __enter__(self):
        # Return self if you want to use the instance in the context
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Handle exception, if any
        if exc_type is not None:
            _LOGGER.error(
                "An error occurred: %s. Traceback: %s",
                exc_val,
                traceback.format_exc(),
            )

        # Dispose the resources
        self.dispose()

        # Return True if the exception was handled, False to propagate it
        return False

    def __del__(self):
        # Dispose the resources
        self.dispose()

    # endregion

    # region Properties

    @property
    def is_authenticated(self) -> bool:
        """True if the server is authenticated, False otherwise."""
        return (
            self._session_id != ""
            and self._session_expiration_timestamp > datetime.now(timezone.utc)
        )

    @property
    def keycode(self) -> str:
        """Keycode (unique ID) of the CAME Eti/Domo server."""
        if self._keycode == "" or not self.is_authenticated:
            self.get_features()
        return self._keycode

    @property
    def software_version(self) -> str:
        """Software version of the CAME Eti/Domo server."""
        if self._software_version == "" or not self.is_authenticated:
            self.get_features()
        return self._software_version

    @property
    def server_type(self) -> str:
        """Type of CAME Eti/Domo server."""
        if self._type == "" or not self.is_authenticated:
            self.get_features()
        return self._type

    @property
    def board(self) -> str:
        """Board type of the CAME Eti/Domo server."""
        if self._board == "" or not self.is_authenticated:
            self.get_features()
        return self._board

    @property
    def serial_number(self) -> str:
        """Serial number of the CAME Eti/Domo server."""
        if self._serial_number == "" or not self.is_authenticated:
            self.get_features()
        return self._serial_number

    # endregion

    # region Public methods

    def get_features(self) -> FeatureSet:
        """Returns the list of features supported by the server."""
        if not self._features:
            # If features are not cached, fetch them from the API
            resp = self._fetch_features_list()
            self._keycode = resp["keycode"]
            self._software_version = resp["swver"]
            self._type = resp["type"]
            self._board = resp["board"]
            self._serial_number = resp["serial"]
            self._features = FeatureSet.from_json(resp["list"])

        return self._features

    def get_entities(self, entity_type: Optional[EntityType] = None) -> CameEntitySet:
        """Returns the list of entities managed by the server."""

        # Input validation
        if entity_type is not None and not isinstance(entity_type, EntityType):
            raise TypeError("entity_type must be an EntityType")

        if not self._entities:
            entities = self._fetch_entities_list()
            self._entities = entities

        # Return a subset of entities if entity_type is specified
        if entity_type is None:
            return self._entities
        else:
            # TODO Add new mappings once new entity classes are implemented
            if entity_type not in _EntityType2Class:
                raise ValueError(
                    "Invalid entity type. Supported values are: "
                    f"{_EntityType2Class.keys()}"
                )

            return CameEntitySet(
                {
                    item
                    for item in self._entities
                    if isinstance(item, _EntityType2Class[entity_type])
                }
            )

    @ensure_login
    def set_entity_status(
        self,
        entity_type: Type[CameEntity],
        entity_id: int,
        status: EntityStatus,
        *,
        brightness: Optional[int] = 100,
    ) -> bool:
        """
        Sets the status of an entity. Currently supported: ligts, openings and
        scenarios.

        Args:
            entity_type (Type[CameEntity]): The type of the entity.
            entity (Entity): The entity to set the status for.
            status (EntityStatus): The status to set.

        Keyword Args:
            brightness (int, optional): The brightness level. Defaults to None.
        """
        # Input validation
        if not issubclass(entity_type, CameEntity):
            raise TypeError("entity_type must be a subclass of CameEntity")

        if not isinstance(entity_id, int):
            raise TypeError("entity_id must be an integer")

        if not isinstance(status, EntityStatus):
            raise TypeError("status must be an EntityStatus")

        if entity_type not in [Light, Opening, Scenario]:
            _LOGGER.warning("Entity type '%s' not supported. Skipping.", entity_type)
            return False

        if entity_type == Light:
            if brightness is None:
                brightness = (
                    Light._DEFAULT_BRIGHTNESS  # pylint: disable=protected-access
                )
            elif not isinstance(brightness, int):
                raise TypeError("brightness must be an integer beween 0 and 100")
            elif brightness < 0 or brightness > 100:
                _LOGGER.warning(
                    "Brightness must be between 0 and 100 (provided: %s). "
                    "Setting it to %s.",
                    brightness,
                    max(0, min(100, brightness)),
                )
                brightness = max(0, min(100, brightness))

        # LIGHT - Input payload example
        # {
        #     "sl_appl_msg": {
        #         "act_id": 14,
        #         "client": "my_session_id",
        #         "cmd_name": "light_switch_req",
        #         "cseq": 11,
        #         "perc": 46,
        #         "wanted_status": 0
        #     },
        #     "sl_appl_msg_type": "domo",
        #     "sl_client_id": "my_session_id",
        #     "sl_cmd": "sl_data_req"
        # }

        # OPENING - Input payload example
        # {
        #         "act_id": 51,
        #         "client": "my_session_id",
        #         "cmd_name": "opening_move_req",
        #         "cseq": 16,
        #         "wanted_status": 1
        #     },
        #     "sl_appl_msg_type": "domo",
        #     "sl_client_id": "my_session_id",
        #     "sl_cmd": "sl_data_req"
        # }

        # SCENARIO - Input payload example
        # {
        #     "sl_appl_msg": {
        #         "client": "my_session_id",
        #         "cmd_name": "scenario_activation_req",
        #         "cseq": 18,
        #         "id": 7
        #     },
        #     "sl_appl_msg_type": "domo",
        #     "sl_client_id": "my_session_id",
        #     "sl_cmd": "sl_data_req"
        # }

        # Create the request
        self._cseq += 1
        request_data: Dict[str, Any] = {
            "sl_appl_msg": {
                "client": self._session_id,
                "cmd_name": _Class2SwitchCommand[entity_type],
                "cseq": self._cseq,
            },
            "sl_appl_msg_type": "domo",
            "sl_client_id": self._session_id,
            "sl_cmd": "sl_data_req",
        }

        request_data["sl_appl_msg"]["id"] = entity_id
        request_data["sl_appl_msg"]["act_id"] = entity_id
        request_data["sl_appl_msg"]["wanted_status"] = status.value
        request_data["sl_appl_msg"]["perc"] = brightness

        try:
            # Send the post request with the login parameters
            resp = self._send_command(request_data)

            # Output example
            # {
            #     "cseq": 13,
            #     "cmd_name": "light_switch_resp",
            #     "sl_data_ack_reason": 0
            # }

            if resp["sl_data_ack_reason"] == 0:
                _LOGGER.debug("Entity status updated successfully.")
                return True
            else:
                _LOGGER.error(
                    "Entity status update failed. SL_DATA_ACK_REASON: %s",
                    resp["sl_data_ack_reason"],
                )
                return False
        except CameDomoticRequestError as e:
            _LOGGER.error(
                "Unexpected error trying to update the status of the entity. "
                "Error: %s\n%s",
                e,
                traceback.format_exc(),
            )
            self._cseq -= 1
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught
            _LOGGER.error(
                "Unexpected error trying to update the status of the entity. "
                "Error: %s\n%s",
                e,
                traceback.format_exc(),
            )
            self._cseq -= 1
            return False

    # TODO embed the keep alive command in the internal logic of the instance
    # and set it as private
    @ensure_login
    def keep_alive(self) -> bool:
        """
        Sends a keep alive request to the CAME server.

        Returns:
            bool: True if the keep alive was successful, False otherwise.
        """

        # Input example
        # {
        #     "sl_client_id": "my_session_id",
        #     "sl_cmd": "sl_keep_alive_req"
        # }

        # Create the keep alive request
        request_data = {
            "sl_client_id": self._session_id,
            "sl_cmd": "sl_keep_alive_req",
        }

        try:
            # Send the post request with the login parameters
            response = self._send_command(request_data)

            # Valid response example:
            # {
            #     "sl_cmd":	"sl_keep_alive_ack",
            #     "sl_data_ack_reason":	0,
            #     "sl_client_id":	"my_session_id"
            # }

            # Check if the user is authorized and store the session info
            if (
                response["sl_cmd"] == "sl_keep_alive_ack"
                and response["sl_data_ack_reason"] == 0
            ):
                # Refresh the session expiration timestamp
                self._session_expiration_timestamp = datetime.now(
                    timezone.utc
                ) + timedelta(seconds=self._session_keep_alive_timeout_sec)
                _LOGGER.debug("Keep alive successful.")
                return True
            else:
                _LOGGER.error("Keep alive failed. Response: %s", response)
        except CameDomoticRequestError:
            _LOGGER.exception("Error trying to keep alive the session.")
        except Exception:  # pylint: disable=broad-exception-caught
            _LOGGER.exception("Unexpected error trying to keep alive the session.")

        return False

    def dispose(self) -> None:
        """
        Dispose the resources used by the server.

        raise: Nothing, everything is managed internally.
        """
        try:
            if self.is_authenticated and not self._logout():
                _LOGGER.warning("Logout failed.")
            self._http_session.close()
            _LOGGER.debug("Resources disposed.")
        except Exception:  # pylint: disable=broad-exception-caught
            _LOGGER.exception("Unexpected error disposing the resources.")

    # endregion

    # region Protected methods

    def _login(self) -> bool:
        """
        Logs in to the server or reuse a valid session.

        Returns:
            bool: True if the login was successful, False otherwise.
        """

        if self.is_authenticated:
            _LOGGER.debug("Already authenticated.")
            return True

        # Create the login request
        request_data = {
            "sl_cmd": "sl_registration_req",
            "sl_login": self._username,
            "sl_pwd": self._password,
        }

        try:
            # Send the post request with the login parameters
            response = self._send_command(request_data)

            # Valid response example:
            # {
            #     "sl_cmd":	"sl_registration_ack",
            #     "sl_client_id":	"my_session_id",
            #     "sl_keep_alive_timeout_sec":	900,
            #     "sl_data_ack_reason":	0
            # }

            # Check if the user is authorized and store the session info
            if (
                response["sl_cmd"] == "sl_registration_ack"
                and response["sl_data_ack_reason"] == 0
                and len(response["sl_client_id"]) > 0
                and response["sl_keep_alive_timeout_sec"] > 0
            ):
                self._session_id = response["sl_client_id"]
                # Be conservative and set expiration datetime 30 seconds
                # before the actual expiration
                self._session_keep_alive_timeout_sec = (
                    response["sl_keep_alive_timeout_sec"] - 30
                )
                self._session_expiration_timestamp = datetime.now(
                    timezone.utc
                ) + timedelta(seconds=self._session_keep_alive_timeout_sec)
                self._cseq = 0  # Reset the cseq sequence

                _LOGGER.debug(
                    "The user is authorized. Session expiration timestamp: %s",
                    self._session_expiration_timestamp,
                )
                return True
            else:
                _LOGGER.error("The user is not authorized. Response: %s", response)
                return False

        except CameDomoticRequestError:
            _LOGGER.exception("Error trying login with the server.")
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            _LOGGER.exception("Unexpected error trying login with the server.")
            return False

    def _logout(self) -> bool:
        """
        Logs out from the server (if actually authenticated).

        Returns:
            bool: True if the logout was successful, False otherwise.
        """
        if not self.is_authenticated:
            _LOGGER.debug("Not authenticated, nothing to do.")
            return True

        # Create the login request
        request_data = {
            "sl_client_id": self._session_id,
            "sl_cmd": "sl_logout_req",
        }

        try:
            # Send the post request with the login parameters
            response = self._send_command(request_data)

            # Valid response example:
            # {
            #     "sl_cmd": "sl_logout_ack",
            #     "sl_ack_reason": 0,
            #     "sl_data_ack_reason": 0
            # }

            # Check if the user is authorized and store the session info
            if (
                response["sl_cmd"] == "sl_logout_ack"
                and response["sl_ack_reason"] == 0
                and response["sl_data_ack_reason"] == 0
            ):
                # Reset the session
                self._session_id = ""
                self._session_expiration_timestamp = datetime.now(timezone.utc)

                _LOGGER.debug("Logged off.")
                return True
            else:
                _LOGGER.error("Server returned a non-OK response: %s", response)
        except CameDomoticRequestError:
            _LOGGER.exception("Error trying to logoff.")
        except Exception:  # pylint: disable=broad-exception-caught
            _LOGGER.exception("Unexpected error trying to logoff.")
        return False

    def _send_command(self, data: dict):
        try:
            response = self._http_session.post(
                self._host_url,
                data={"command": json.dumps(data)},
                headers=self._HTTP_HEADERS,
                timeout=self._HTTP_TIMEOUT,
            )
            response.raise_for_status()
            if response.status_code != 200:
                _LOGGER.debug(
                    "Request error. HTTP response status code: %s",
                    response.status_code,
                )
                raise CameDomoticRequestError(
                    f"Request error. HTTP response \
status code: {response.status_code}"
                )

            _LOGGER.debug(
                "POST command sent successfully, response retrieved.",
            )

            # Refresh the session expiration timestamp, keeping 30 secs of "safe zone"
            self._session_expiration_timestamp = datetime.now(timezone.utc) + timedelta(
                seconds=self._session_keep_alive_timeout_sec
            )

            return response.json()

        # In case of a request exception, try to dispose the old session
        # and to refresh the HTTP session object, then rethrow the exception
        except requests.RequestException as e:
            _LOGGER.exception(
                "RequestException caught while sending a POST command "
                "to the CAME server."
            )
            _LOGGER.info("Trying to refresh the HTTP session.")
            self._http_session.close()
            self._http_session = requests.Session()
            _LOGGER.info("New HTTP session created successfully.")

            raise CameDomoticRequestError from e

    @ensure_login
    def _fetch_features_list(self) -> dict:

        # Input data example
        # {
        #     "sl_appl_msg": {
        #         "client": "my_session_id",
        #         "cmd_name": "feature_list_req",
        #         "cseq": 1
        #     },
        #     "sl_appl_msg_type": "domo",
        #     "sl_client_id": "my_session_id",
        #     "sl_cmd": "sl_data_req"
        # }

        # Create the login request
        self._cseq += 1
        request_data = {
            "sl_appl_msg": {
                "client": self._session_id,
                "cmd_name": "feature_list_req",
                "cseq": self._cseq,
            },
            "sl_appl_msg_type": "domo",
            "sl_client_id": self._session_id,
            "sl_cmd": "sl_data_req",
        }

        try:
            # Send the post request with the login parameters
            resp = self._send_command(request_data)

            # Valid response example:
            # {
            #     "cmd_name": "feature_list_resp",
            #     "cseq": 1,
            #     "keycode": "MYUNIQUEID",
            #     "swver": "1.2.3",
            #     "type": "2",
            #     "board": "8",
            #     "serial": "hexadecimal_serial",
            #     "list": [
            #         "lights",
            #         "openings",
            #         "scenarios",
            #         "digitalin",
            #         "energy",
            #     ],
            #     "recovery_status": 0,
            #     "sl_data_ack_reason": 0,
            # }

            # Check if the user is authorized and store the session info
            if resp["sl_data_ack_reason"] == 0:
                _LOGGER.debug("Features retrieved: %s", self._features)

                return resp

            else:
                _LOGGER.error(
                    "Features retrieval failed. SL_DATA_ACK_REASON: %s",
                    resp["sl_data_ack_reason"],
                )
                raise CameDomoticBadAckError(
                    resp["sl_data_ack_reason"],
                    "Features list retrieval failed.",
                )
        except CameDomoticBadAckError as e:
            raise e
        except CameDomoticRequestError as e:
            _LOGGER.error(
                "Unexpected error trying to get the features list. Error: %s",
                e,
            )
            self._cseq -= 1  # Rollback the cseq
            raise e
        except Exception as e:
            _LOGGER.error(
                "Unexpected error trying to get the features list. Error: %s",
                e,
            )
            self._cseq -= 1  # Rollback the cseq
            raise CameDomoticRequestError(
                "Unexpected error trying to get the features list."
            ) from e

    def _fetch_entities_list(self) -> CameEntitySet:
        # Ensure that the features have been retrieved
        if not self._features:
            self.get_features()

        # For each feature, fetch the entities
        entities = CameEntitySet()
        for feature in self._features:
            entities.update(self._fetch_entities_list_by_feature(feature))

        return entities

    @ensure_login
    def _fetch_entities_list_by_feature(self, feature: Feature) -> CameEntitySet:

        try:
            entity_type = EntityType[feature.name.upper()]
        except KeyError:
            _LOGGER.warning("Feature '%s' not supported. Skipping.", feature.name)
            return CameEntitySet()

        if entity_type in {
            EntityType.LIGHTS,
            EntityType.OPENINGS,
            EntityType.DIGITALIN,
            EntityType.SCENARIOS,
        }:
            # Input data example
            # {
            #     "sl_appl_msg": {
            #         "client": "my_session_id",
            #         "cmd_name": "openings_list_req",
            #         "cseq": 11
            #     },
            #     "sl_appl_msg_type": "domo",
            #     "sl_client_id": "my_session_id",
            #     "sl_cmd": "sl_data_req"
            # }

            # Create the request
            self._cseq += 1
            request_data = {
                "sl_appl_msg": {
                    "client": self._session_id,
                    "cmd_name": entity_type.value,
                    "cseq": self._cseq,
                },
                "sl_appl_msg_type": "domo",
                "sl_client_id": self._session_id,
                "sl_cmd": "sl_data_req",
            }

            try:
                # Send the post request with the login parameters
                resp = self._send_command(request_data)

                # Output example
                # {
                # 	"cseq":	1,
                # 	"cmd_name":	"light_list_resp",
                # 	"array":	[...], // here are the entities
                # 	"sl_data_ack_reason":	0
                # }

                if resp["sl_data_ack_reason"] == 0:
                    # The following line is anannotation for type checkers (i.e. mypy)
                    provided_type: Type[CameEntity] = _EntityType2Class[entity_type]
                    # Create the entities
                    entities = CameEntitySet(
                        provided_type.from_json(item) for item in resp["array"]
                    )
                    _LOGGER.debug("Entities retrieved: %s", entities)
                    return entities
                else:
                    _LOGGER.error(
                        "Entity '%s' retrieval failed. SL_DATA_ACK_REASON: %s",
                        feature.name,
                        resp["sl_data_ack_reason"],
                    )
                    raise CameDomoticBadAckError(
                        resp["sl_data_ack_reason"],
                        f"Info retrieval for feature '{feature.name}' failed.",
                    )
            except CameDomoticBadAckError as e:
                _LOGGER.error("%s\n%s", e, traceback.format_exc())
                # raise e
            except CameDomoticRequestError as e:
                _LOGGER.error(
                    "Unexpected CameDomoticRequestError trying to get "
                    "the entities for the feature '%s'. Error: %s\n%s",
                    feature.name,
                    e,
                    traceback.format_exc(),
                )
            except KeyError as e:
                _LOGGER.error(
                    "Unexpected KeyError trying to get the entities for "
                    "the feature '%s'. Error: %s\n%s",
                    feature.name,
                    e,
                    traceback.format_exc(),
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                _LOGGER.error(
                    "Unexpected error trying to get the entities for "
                    "the feature %s. Error: %s\n%s",
                    feature.name,
                    e,
                    traceback.format_exc(),
                )

        return CameEntitySet()

    # endregion

    # region Static methods

    # endregion
