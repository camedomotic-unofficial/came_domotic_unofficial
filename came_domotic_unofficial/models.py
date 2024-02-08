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
CAME Domotic entities.
"""

# Generic exception class
from came_domotic_unofficial import _LOGGER
from came_domotic_unofficial.const import EntityStatus, EntityType, LightType


class CameDomoticError(Exception):
    """
    Base exception class for the Came Domotic package.
    """


# Server not found
class CameDomoticServerNotFoundError(CameDomoticError):
    """
    Exception raised when the remote server is not found.
    """


# Authentication exception class
class CameDomoticAuthError(CameDomoticError):
    """
    Exception raised when there is an authentication error
    with the remote server.
    """


# Server exception class
class CameDomoticRemoteServerError(CameDomoticError):
    """
    Exception raised when there is an error related to the Came Domotic server.
    """


class CameDomoticRequestError(CameDomoticError):
    """
    Exception raised when there is an error when sending a request
    to the Came Domotic server.
    """


# Generic CAME entity class
class CameEntity:
    """
    Represents a generic CAME entity.
    """

    def __init__(
        self,
        *,
        entity_id: int,
        name: str,
        entity_type: EntityType,
        status: EntityStatus,
    ):
        """
        Constructor for the CameEntity class.

        :param id: the entity ID
        :param name: the entity name
        :param entity_type: the entity type
        :param status: the entity status
        """
        self._id = entity_id
        self._name = "Unknown" if name is None or name == "" else name
        self._entity_type = entity_type
        self._status = status

    @property
    def id(self) -> int:
        """
        Returns the entity ID.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Returns the entity name.
        """
        return self._name

    @property
    def entity_type(self) -> EntityType:
        """
        Returns the entity type.
        """
        return self._entity_type

    @property
    def status(self) -> EntityStatus:
        """
        Returns the entity status.
        """
        return self._status

    def __str__(self) -> str:
        return f"Entity: {self._name} - ID: {self._id} - \
            Type: {self._entity_type.name} - Status: {self._status.name}"

    #  Entities with same entity type and ID are the same entity)

    # Override the equality operator
    def __eq__(self, other):
        return self._entity_type == other.entity_type and self._id == other.id

    # Override the inequality operator
    def __ne__(self, other):
        return not self.__eq__(other)

    # Override the hash function
    def __hash__(self):
        return hash((self._entity_type, self._id))


class CameEntitiesSet(set):
    """
    Represents a set of CAME entities.
    """

    def add(self, item):
        if not isinstance(item, CameEntity):
            _LOGGER.error("Item must be of type MyClass. Type: %s", type(item))
            raise TypeError("Item must be of type CameEntity")
        super().add(item)


# Light entity class
class Light(CameEntity):
    """
    Represents a CAME light.
    """

    def __init__(
        self,
        *,
        entity_id: int,
        name: str,
        status: EntityStatus,
        light_type: LightType,
        brightness: int = 100,
    ):
        """
        Constructor for the CameLight class.

        :param id: the light ID
        :param name: the light name
        :param status: the light status
        :param brightness: the light brightness (from 0% to 100%)
        """
        # Set brightness, with range from 0 to 100
        if brightness < 0:
            self._brightness = 0
            _LOGGER.warning(
                "Invalid brightness, setting to 0. Provided value: %s",
                brightness,
            )
        elif brightness > 100:
            self._brightness = 100
            _LOGGER.warning(
                "Invalid brightness, setting to 100. Provided value: %s",
                brightness,
            )
        else:
            self._brightness = brightness

        # Set light type
        self._light_type = light_type

        # Ensure that the status is within this list: ON, OFF, OPEN, CLOSE
        if status not in [EntityStatus.ON, EntityStatus.OFF]:
            _LOGGER.warning(
                "The status provided is not within the allowed values. \
                Provided value: %s",
                status,
            )
            status = EntityStatus.OFF

        super().__init__(
            entity_id=entity_id,
            name=name,
            entity_type=EntityType.LIGHT,
            status=status,
        )

    def __str__(self):
        return f"Light: {self._name} - ID: {self._id} - Status: {self._status.name}"

    # Properties
    @property
    def brightness(self) -> float:
        """
        Returns the light brightness.
        """
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        """
        Sets the light brightness.
        """
        if value < 0 or value > 100:
            raise ValueError("The brightness must be between 0 and 100")
        self._brightness = value

    @property
    def light_type(self) -> LightType:
        """
        Returns the light type.
        """
        return self._light_type
