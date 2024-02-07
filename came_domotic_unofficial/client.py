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

from datetime import datetime, timedelta, timezone
import json
import requests
from came_domotic_unofficial import _LOGGER
from typing import List
from came_domotic_unofficial.models import (
    CameDomoticResponseDataError,
    CameDomoticServerNotFoundError,
    CameDomoticAuthError,
    CameDomoticRemoteServerError,
    CameEntitiesSet,
    CameEntity,
    Light,
)
from came_domotic_unofficial.const import (
    Command,
    EntityStatus,
    EntityType,
    LightType,
    SeasonSetting,
    ThermoZoneStatus,
)

# CAME server settings
_HTTP_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
}
_HTTP_TIMEOUT = 10


# Came Domotic server class
class CameDomoticServer:
    """
    Represents a CAME Domotic server.
    """

    def __init__(self, host: str, username: str, password: str):
        """
        Constructor for the CameDomoticServer class.

        :param host: the server host
        :param username: the username
        :param password: the password
        """
        # Validate the parameters
        if host is None or host == "":
            _LOGGER.error("The host cannot be empty")
            raise ValueError("The host cannot be empty")
        if username is None or username == "":
            _LOGGER.error("The username cannot be empty")
            raise ValueError("The username cannot be empty")
        if password is None or password == "":
            _LOGGER.error("The password cannot be empty")
            raise ValueError("The password cannot be empty")

        self._host: str = f"http://{host}/domo/"
        self._username: str = username
        self._password: str = password
        self._session_id: str = ""
        self._session_expiration_datetime: datetime = None
        self._cseq: int = 0
        self.entities: CameEntitiesSet = None

        # Check if the host is available
        try:
            response = requests.get(
                self._host,
                headers=_HTTP_HEADERS,
                timeout=_HTTP_TIMEOUT,
            )

            # If not then raise an exception
            if not response.status_code == 200:
                _LOGGER.error("The server is not available")
                raise CameDomoticServerNotFoundError

        except CameDomoticServerNotFoundError as e:
            raise e
        except Exception as e:
            _LOGGER.error("The server is not available")
            raise CameDomoticServerNotFoundError from e

    # Send a command to the CAME server
    def _send_came_command(
        self, data: dict, *, skip_authentication: bool = False
    ) -> dict:
        """
        Sends a command to the CAME server.

        :param data: the data to send
        :return: the JSON response
        """
        # Validate input
        if data is None or data == {}:
            _LOGGER.error("The data cannot be empty")
            raise ValueError("The data cannot be empty")

        try:
            # Check the session and refresh if needed
            if skip_authentication is False:
                self._ensure_authentication()
                self._cseq += 1  # Increment the cseq

            response = requests.post(
                self._host,
                data={"command": json.dumps(data)},
                headers=_HTTP_HEADERS,
                timeout=_HTTP_TIMEOUT,
            )

            # If HTTP response status not valid, raise an exception
            response.raise_for_status()

            # Ensure that the response is not empty
            if response.text is None or response.text == "":
                _LOGGER.error("The response is empty")
                raise ValueError("The response is empty")

            return response.json()

        except Exception as e:
            _LOGGER.error("Error while sending command to the CAME server")
            self._cseq -= 1  # Rollback the cseq
            raise CameDomoticRemoteServerError(
                "Error while sending command to the CAME server"
            ) from e

    # Ensure that the user is authenticated
    def _ensure_authentication(self) -> None:
        """
        Authenticates the user with the server.
        """
        # Check if the session is still valid
        if (
            self._session_id != ""
            and self._session_expiration_datetime is not None
            and self._session_expiration_datetime
            > datetime.now(timezone.utc)
            + timedelta(seconds=max(_HTTP_TIMEOUT, 30))  # Be conservative
        ):
            _LOGGER.debug(
                "Session is still valid. Expiration token: %s",
                self._session_expiration_datetime,
            )
            return

        # Input payload example:
        # command={
        #     "sl_cmd": "sl_registration_req",
        #     "sl_login": "my_username",
        #     "sl_pwd": "my_password"
        # }

        data = {
            "sl_cmd": "sl_registration_req",
            "sl_login": self._username,
            "sl_pwd": self._password,
        }

        # Send the post request with the login parameters
        try:
            response = self._send_came_command(data, skip_authentication=True)

            # Output payload example:
            # {
            #     "sl_cmd":	"sl_registration_ack",
            #     "sl_client_id":	"my_session_token",
            #     "sl_keep_alive_timeout_sec":	900,
            #     "sl_data_ack_reason":	0
            # }

            if (
                response["sl_cmd"] == "sl_registration_ack"
                and response["sl_data_ack_reason"] == 0
                and response["sl_client_id"] is not None
                and response["sl_keep_alive_timeout_sec"] is not None
            ):

                # Set the session id and the session expiration datetime
                self._session_id = response["sl_client_id"]
                self._session_expiration_datetime = datetime.now(
                    timezone.utc
                ) + timedelta(
                    seconds=response["sl_keep_alive_timeout_sec"]
                    - max(_HTTP_TIMEOUT, 30)  # Be conservative
                )

                _LOGGER.debug(
                    "Authenticated, session expiration set to: %s",
                    self._session_expiration_datetime,
                )
                return

            else:
                # Reset authentication data
                self._session_id = ""
                self._session_expiration_datetime = None
                self._cseq = 0
                _LOGGER.error(
                    "Authentication failed. API response: %s", response.text
                )
                raise CameDomoticAuthError(
                    f"Authentication failed. API response: {response.text}"
                )

        except Exception as e:
            _LOGGER.error("Error while authenticating")
            raise CameDomoticAuthError("Error while authenticating") from e

    def keep_alive(self):
        """
        Sends a keep alive command to the CAME server.
        """

        try:
            data = {
                "sl_client_id": self._session_id,
                "sl_cmd": "sl_keep_alive_req",
            }

            # Ensures authentication if needed
            response = self._send_came_command(data, skip_authentication=False)

            return response["sl_data_ack_reason"] == 0
        except Exception as e:  # pylint disable=broad-exception-caught
            _LOGGER.error(
                "Error while keeping the session alive. Error details: %s", e
            )
            return False

    # Get the list of entities from the CAME server
    def get_entities(self, entity_type: EntityType) -> dict:
        # TODO: Implement this method. Check cache first,
        # if needed ask to the came server
        """Gets the list of entities from the CAME server."""

        new_entities = self._get_list_from_server(entity_type)

        if self.entities is None:
            self.entities = CameEntitiesSet()

        # Cache the new entities
        self.entities.add(new_entities)

        return new_entities

    # Gets from the JSON response all the items with "leaf": true
    @staticmethod
    def _find_leaf_nodes(node):
        if isinstance(node, dict):
            if node.get("leaf") is True:
                yield node
            for child in node.values():
                yield from CameDomoticServer._find_leaf_nodes(child)
        elif isinstance(node, list):
            for child in node:
                yield from CameDomoticServer._find_leaf_nodes(child)

    def _get_list_from_server(
        self, entity_type: EntityType
    ) -> CameEntitiesSet:
        """Gets the list of entities from the CAME server."""

        # Validate input
        if entity_type is None:
            _LOGGER.error("The entity type cannot be None")
            raise ValueError("The entity type cannot be None")

        # if (entity_type) == EntityType.MAP:
        #     # TODO Manage this case
        #     return None
        # elif (entity_type) == EntityType.USER:
        #     # TODO Manage this case
        #     return None
        # elif (entity_type) == EntityType.DIGITALIN:
        #     # TODO Manage this case
        #     return None

        # Map each entity type to the value of the corresponding command
        command = {EntityType.LIGHT: Command.LIST_LIGHTS}.get(entity_type)

        # Input payload example:
        # {
        #     "sl_appl_msg": {
        #         "client": "my_session",
        #         "cmd_name": "nested_light_list_req",
        #         "cseq": 5,
        #         "topologic_scope": "plant",
        #         "value": 0
        #     },
        #     "sl_appl_msg_type": "domo",
        #     "sl_client_id": "my_session",
        #     "sl_cmd": "sl_data_req"
        # }

        # TODO Experiment with topologic_scope = room or floor

        data = {
            "sl_appl_msg": {
                "client": self._session_id,
                "cmd_name": command.value,
                "cseq": self._cseq + 1,  # TODO manage better, if possible
                "topologic_scope": "plant",
                "value": 0,
            },
            "sl_appl_msg_type": "domo",
            "sl_client_id": self._session_id,
            "sl_cmd": "sl_data_req",
        }

        # Get data from server
        try:
            response = self._send_came_command(data)

            # Parse the response recurring in the tree to get all the items
            # tagged with "leaf": True
            leaf_nodes = list(CameDomoticServer._find_leaf_nodes(response))

            # Example of leaf node for lights:
            # {
            #     "act_id": 3,
            #     "name": "My dimmerable light",
            #     "floor_ind": 11,
            #     "room_ind": 31,
            #     "status": 0,
            #     "type": "DIMMER",
            #     "perc": 80,
            #     "leaf": true,
            # }

            # Define an empty list of Lights
            entities = CameEntitiesSet()

            # Map the status value to its EntityStatus enum element
            for node in leaf_nodes:
                # Check if the node has the "act_id" key
                if "act_id" not in node:
                    _LOGGER.warning(
                        "Skipping the node (missing ID). Node:, %s",
                        node,
                    )
                    continue

                if "status" not in node or "type" not in node:
                    _LOGGER.info(
                        "Some required node attributes are missing, assuming \
                            default values. Node:, %s",
                        node,
                    )

                entities.add(
                    Light(
                        entity_id=node["act_id"],
                        name=node["name"],
                        status=(
                            EntityStatus.ON
                            if node["status"] == 1
                            else EntityStatus.OFF
                        ),
                        light_type=(
                            LightType.DIMMERABLE
                            if node["type"] == "DIMMER"
                            else LightType.ON_OFF
                        ),
                        brightness=(
                            node["perc"] if "perc" in node else 100
                        ),  # normalized to 0-100 by the Light constructor
                    )
                )

            return entities

        except Exception as e:
            _LOGGER.error(
                "Error while getting the list of entities. Error details: %s",
                e,
            )
            raise CameDomoticResponseDataError(
                "Error while getting the list of entities"
            ) from e

    # Set the status of an entity
    def set_entity_status(
        self, entity: CameEntity, id: str, status: bool
    ) -> bool:
        """Sets the status of an entity."""
        pass
