# # Copyright 2024 - GitHub user: fredericks1982

# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at

# #     http://www.apache.org/licenses/LICENSE-2.0

# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# from datetime import datetime, timedelta, timezone
# import json
# import requests
# from came_domotic_unofficial import _LOGGER
# from typing import List
# from came_domotic_unofficial.helpers import find_leaf_nodes
# from came_domotic_unofficial.models import (
#     CameDomoticRequestError,
#     CameDomoticServerNotFoundError,
#     CameDomoticAuthError,
#     CameDomoticRemoteServerError,
#     CameEntitiesSet,
#     CameEntity,
#     Feature,
#     Light,
# )
# from came_domotic_unofficial.const import (
#     Command,
#     EntityStatus,
#     EntityType,
#     LightType,
#     SeasonSetting,
#     ThermoZoneStatus,
# )


# # Came Domotic server class
# class CameDomoticServer:
#     """
#     Represents a CAME Domotic server.

#     :param host: the CAME ETI/Domo server host
#     :param username: the username
#     :param password: the password

#     :raises: ValueError in case of invalid input
#     :raises: CameDomoticServerNotFoundError if the server is not available
#     """

#     # CAME server settings
#     _HTTP_HEADERS = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Connection": "Keep-Alive",
#     }
#     _HTTP_TIMEOUT = 10

#     _came_features = {
#             "update": "status_update_req",
#             "relays": "relays_list_req",
#             "cameras": "tvcc_cameras_list_req",
#             "timers": "timers_list_req",
#             "thermoregulation": "thermo_list_req",
#             "analogin": "analogin_list_req",
#             "digitalin": "digitalin_list_req",
#             "lights": "nested_light_list_req",
#             "features": "feature_list_req",
#             "users": "sl_users_list_req",
#             "maps": "map_descr_req",
#         }

#     def __init__(self, host: str, username: str, password: str):
#         """
#         Constructor for the CameDomoticServer class.

#         :param host: the server host
#         :param username: the username
#         :param password: the password
#         """
#         # Validate the parameters
#         if host is None or host == "":
#             _LOGGER.error("The host cannot be empty")
#             raise ValueError("The host cannot be empty")
#         if username is None or username == "":
#             _LOGGER.error("The username cannot be empty")
#             raise ValueError("The username cannot be empty")
#         if password is None or password == "":
#             _LOGGER.error("The password cannot be empty")
#             raise ValueError("The password cannot be empty")

#         self._host: str = f"http://{host}/domo/"
#         self._username: str = username
#         self._password: str = password
#         self._session_id: str = ""
#         self._session_expiration_datetime: datetime = datetime(2000, 1, 1)
#         self._cseq: int = 0
#         self.entities: CameEntitiesSet = None

#         # Check if the host is available
#         try:
#             response = requests.get(
#                 self._host,
#                 headers=_HTTP_HEADERS,
#                 timeout=_HTTP_TIMEOUT,
#             )

#             # If not then raise an exception
#             if response.status_code != 200:
#                 _LOGGER.error("The server is not available")
#                 raise CameDomoticServerNotFoundError

#         except CameDomoticServerNotFoundError as e:
#             raise e
#         except Exception as e:
#             _LOGGER.error("The server is not available")
#             raise CameDomoticServerNotFoundError from e

#     # Tells if the session is authenticated
#     @property
#     def is_authenticated(self) -> bool:
#         """
#         Tells if the session is authenticated.
#         """
#         return (
#             self._session_id != ""
#             and self._session_expiration_datetime>datetime.now(timezone.utc)
#         )

#     # Send a command to the CAME server
#     def _send_came_command(
#         self,
#         data: dict,
#         *,
#         skip_authentication: bool = False,
#         increase_cseq: bool = True,
#     ) -> dict:
#         """
#         Sends a command to the CAME server.

#         :param data: the JSON data to send
#         :param skip_authentication: if False (default) ensures authentication
#         :param increase_cseq: if True (default), the cseq is incremented

#         :return: the JSON response from the CAME server
#         :raises: ValueError in case of invalid input
#         :raises: CameDomoticAuthError for authentication errors
#         :raises: CameDomoticRequestError for errors while sending the command
#         """

#         # Validate input
#         if data is None or data == {}:
#             _LOGGER.error("The data cannot be empty")
#             raise ValueError("The data cannot be empty")

#         try:
#             # Check the session and refresh if needed
#             if skip_authentication is False:
#                 self.ensure_authentication()

#             # TODO Manage here the cseq increment
#             # if increase_cseq is True:
#             #     self._cseq += 1  # Increment the cseq

#             response = requests.post(
#                 self._host,
#                 data={"command": json.dumps(data)},
#                 headers=_HTTP_HEADERS,
#                 timeout=_HTTP_TIMEOUT,
#             )

#             # If HTTP response status not valid, raise an exception
#             response.raise_for_status()

#             # Ensure that the response is not empty
#             if response.text is None or response.text == "":
#                 _LOGGER.error("The response is empty")
#                 raise CameDomoticRequestError("The response is empty")

#             return response.json()
#         except CameDomoticAuthError as e:
#             _LOGGER.error("Error while authenticating")
#             raise e
#         except CameDomoticRequestError as e:
#             # TODO if increase_cseq is True:
#             #     self._cseq -= 1  # Rollback the cseq
#             raise e
#         except Exception as e:
#             _LOGGER.error("Error while sending command to the CAME server")
#             # TODO if increase_cseq is True:
#             #     self._cseq -= 1  # Rollback the cseq
#             raise CameDomoticRequestError(
#                 "Error while sending command to the CAME server"
#             ) from e

#     def _get_features_from_server_(self) -> CameEntitiesSet:
#         """
#         Gets from the CAME server the list of supported features

#         :return: the list of features
#         :raises: CameDomoticRequestError for errors while getting the list
#         """
#         # Input payload example:
#         # {
#         #     "sl_appl_msg": {
#         #         "client": "session_id",
#         #         "cmd_name": "feature_list_req",
#         #         "cseq": 1
#         #     },
#         #     "sl_appl_msg_type": "domo",
#         #     "sl_client_id": "session_id",
#         #     "sl_cmd": "sl_data_req"
#         # }

#         data = {
#             "sl_appl_msg": {
#                 "client": self._session_id,
#                 "cmd_name": Command.LIST_FEATURES.value,
#                 "cseq": self._cseq + 1,
#             },
#             "sl_appl_msg_type": "domo",
#             "sl_client_id": self._session_id,
#             "sl_cmd": "sl_data_req",
#         }

#         # Get data from server
#         try:
#             response = self._send_came_command(data)

#             # Parse the response recurring in the tree to get all the items
#             # tagged with "leaf": True
#             nodes = response["list"]

#             _LOGGER.debug(
#                 "Got valid response from the server, found %s nodes",
#                 len(nodes),
#             )

#             # Example of leaf node for lights:
#             # {
#             #     "act_id": 3,
#             #     "name": "My dimmerable light",
#             #     "floor_ind": 11,
#             #     "room_ind": 31,
#             #     "status": 0,
#             #     "type": "DIMMER",
#             #     "perc": 80,
#             #     "leaf": true,
#             # }

#             # Define an empty list of Lights
#             entities = CameEntitiesSet()

#             # Map the status value to its EntityStatus enum element
#             for node in nodes:
#                 entities.add(Feature(name=node))

#             return entities

#         except Exception as e:
#             _LOGGER.error(
#                 "Error while getting the list of features.Error details: %s",
#                 e,
#             )
#             raise CameDomoticRequestError(
#                 "Error while getting the list of features"
#             ) from e

#     def _get_entities_from_server(self, Feature) -> CameEntitiesSet:
#         """
#         Gets the list of specified entities from the CAME server.

#         :return: the list of Lights
#         :raises: CameDomoticRequestError for errors while getting the list
#         """
#         # Input payload example:
#         # {
#         #     "sl_appl_msg": {
#         #         "client": "my_session",
#         #         "cmd_name": "light_list_req",
#         #         "cseq": 5,
#         #         "topologic_scope": "plant",
#         #         "value": 0
#         #     },
#         #     "sl_appl_msg_type": "domo",
#         #     "sl_client_id": "my_session",
#         #     "sl_cmd": "sl_data_req"
#         # }

#         data = {
#             "sl_appl_msg": {
#                 "client": self._session_id,
#                 "cmd_name": Command.LIST_LIGHTS.value,
#                 "cseq": self._cseq + 1,
#                 "topologic_scope": "plant",
#                 "value": 0,
#             },
#             "sl_appl_msg_type": "domo",
#             "sl_client_id": self._session_id,
#             "sl_cmd": "sl_data_req",
#         }

#         # Get data from server
#         try:
#             response = self._send_came_command(data)

#             # Parse the response recurring in the tree to get all the items
#             # tagged with "leaf": True
#             nodes = response["array"]

#             _LOGGER.debug(
#                 "Got valid response from the server, found %s nodes",
#                 len(nodes),
#             )

#             # Example of leaf node for lights:
#             # {
#             #     "act_id": 3,
#             #     "name": "My dimmerable light",
#             #     "floor_ind": 11,
#             #     "room_ind": 31,
#             #     "status": 0,
#             #     "type": "DIMMER",
#             #     "perc": 80,
#             #     "leaf": true,
#             # }

#             # Define an empty list of Lights
#             entities = CameEntitiesSet()

#             # Map the status value to its EntityStatus enum element
#             for node in nodes:
#                 # Check if the node has the "act_id" key
#                 if "act_id" not in node:
#                     _LOGGER.warning(
#                         "Invalid node, skipping (missing ID). Node:, %s",
#                         node,
#                     )
#                     continue

#                 if "status" not in node or "type" not in node:
#                     _LOGGER.info(
#                         "Some required node attributes are missing, \
#                             assuming default values. Node:, %s",
#                         node,
#                     )

#                 entities.add(
#                     Light(
#                         entity_id=node["act_id"],
#                         name=node["name"],
#                         status=(
#                             EntityStatus.ON
#                             if node["status"] == 1
#                             else EntityStatus.OFF
#                         ),
#                         light_type=(
#                             LightType.DIMMERABLE
#                             if node["type"] == "DIMMER"
#                             else LightType.ON_OFF
#                         ),
#                         brightness=(
#                             node["perc"] if "perc" in node else 100
#                         ),  # normalized to 0-100 by the Light constructor
#                     )
#                 )

#             return entities

#         except Exception as e:
#             _LOGGER.error(
#                 "Error while getting the list of lights. Error details: %s",
#                 e,
#             )
#             raise CameDomoticRequestError(
#                 "Error while getting the list of lights"
#             ) from e

#     # Ensure that the user is authenticated
#     def ensure_authentication(self) -> None:
#         """
#         Authenticates the user with the server.

#         :raises: CameDomoticAuthError for authentication errors
#         """
#         # Check if the session is still valid
#         if self.is_authenticated:
#             _LOGGER.debug(
#                 "Session is still valid. Session expires at: %s",
#                 self._session_expiration_datetime,
#             )
#             return

#         # Input payload example:
#         # command={
#         #     "sl_cmd": "sl_registration_req",
#         #     "sl_login": "my_username",
#         #     "sl_pwd": "my_password"
#         # }

#         data = {
#             "sl_cmd": "sl_registration_req",
#             "sl_login": self._username,
#             "sl_pwd": self._password,
#         }

#         # Send the post request with the login parameters
#         try:
#             response = self._send_came_command(
#                 data, skip_authentication=True, increase_cseq=False
#             )

#             # Output payload example:
#             # {
#             #     "sl_cmd":	"sl_registration_ack",
#             #     "sl_client_id":	"my_session_token",
#             #     "sl_keep_alive_timeout_sec":	900,
#             #     "sl_data_ack_reason":	0
#             # }

#             if (
#                 response["sl_cmd"] == "sl_registration_ack"
#                 and response["sl_data_ack_reason"] == 0
#                 and response["sl_client_id"] is not None
#                 and response["sl_client_id"] != ""
#                 and response["sl_keep_alive_timeout_sec"] is not None
#             ):

#                 # Set the session id and the session expiration datetime
#                 self._session_id = response["sl_client_id"]
#                 self._session_expiration_datetime = datetime.now(
#                     timezone.utc
#                 ) + timedelta(
#                     seconds=response["sl_keep_alive_timeout_sec"]
#                     - max(_HTTP_TIMEOUT, 30)  # Be conservative
#                 )
#                 self._cseq = 0  # (Re)initialize the command sequence

#                 _LOGGER.debug(
#                     "Authenticated, session expiration set to: %s",
#                     self._session_expiration_datetime,
#                 )
#                 return

#             else:
#                 _LOGGER.error(
#                     "Authentication failed. API response: %s", response
#                 )
#                 raise CameDomoticAuthError(
#                     f"Authentication failed. API response: {response}"
#                 )
#         except CameDomoticAuthError as e:
#             raise e
#         except Exception as e:
#             _LOGGER.error("Unexpected error while authenticating")
#             raise CameDomoticAuthError(
#                 "Unexpected error while authenticating"
#             ) from e

#     def keep_alive(self):
#         """
#         Sends a keep alive command to the CAME server.
#         """

#         try:
#             data = {
#                 "sl_client_id": self._session_id,
#                 "sl_cmd": "sl_keep_alive_req",
#             }

#             # Ensures authentication if needed
#             response =self._send_came_command(data,skip_authentication=False)

#             return response["sl_data_ack_reason"] == 0
#         except Exception as e:  # pylint disable=broad-exception-caught
#             _LOGGER.warning(
#                 "Error while keeping the session alive. Error details: %s", e
#             )
#             return False

#     # Get the list of entities from the CAME server
#     def get_entities(self, entity_type: EntityType) -> set:
#         """Gets the list of entities from the CAME server."""

#         # TODO Manage the ALL cases

#         if self.entities is None:
#             features = self._get_features_from_server_()
#             if features:
#                 for feature in features:
#                     self.entities.add(feature)

#         # Get from self.entites the subset of entities of the same type
#         result = {
#             item for item in self.entities if isinstance(item, entity_type)
#         }

#         # If result is empty, get the list from the server and cache it
#         if not result:
#             result = self._get_entities_from_server(entity_type)
#             # Add each item to the self.entities Set
#             for item in result:
#                 self.entities.add(item)

#         return result

#     # Set the status of an entity
#     def set_entity_status(
#         self, entity: CameEntity, status: EntityStatus
#     ) -> bool:
#         """
#         Sets the status of an entity.

#         :param entity: the entity to set the status for
#         :param status: the status to set
#         :return: True if the status was set, False otherwise
#         """
#         # TODO
