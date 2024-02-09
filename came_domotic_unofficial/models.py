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

from enum import Enum

# from came_domotic_unofficial import _LOGGER

# from came_domotic_unofficial.const import EntityStatus, EntityType, LightType


# region Exceptions
class CameDomoticError(Exception):
    """
    Base exception class for the Came Domotic package.
    """


class CameDomoticServerNotFoundError(CameDomoticError):
    """Raised when the specified host is not available"""


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
    """Raised when a user send an invalid request to the server"""


class CommandNotFound(CameDomoticError):
    """
    Raised if the user tries to send a command to the server that
    does not exists
    """


# endregion


# region Enums
class CameEnum(Enum):
    """Base class for all the CAME enums."""


class EntityType(CameEnum):
    """Enum listing all the CAME entity types."""

    FEATURE = None
    LIGHT = None
    OPENING = None
    RELAY = None
    CAMERA = None
    TIMER = None
    THERMOREGULATION = None
    ANALOGIN = None
    DIGITALIN = None
    USER = None
    MAP = None


class EntityStatus(CameEnum):
    """Enum listing all the status of the CAME entities."""

    ON_OPEN = 1
    OFF_CLOSED = 0


class LightType(CameEnum):
    """Enum listing the light types."""

    ON_OFF = "STEP_STEP"
    DIMMABLE = "DIMMER"


class OpeningType(CameEnum):
    OPEN_CLOSE = 0


class SeasonSetting(Enum):
    """Enum listing the available seasons settings."""

    PLAMT_OFF = "off"
    WINTER = "winter"
    SUMMER = "summer"


class ThermoZoneStatus(Enum):
    """Enum listing the available thermostat zone status."""

    OFF = 0
    MAN = 1
    AUTO = 2
    JOLLY = 3


# endregion

# region CAME entities


class CameEntity:
    """
    Base class for all the CAME entities.
    """

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = None,
    ):
        """
        Constructor for the CameEntity class.

        :param id: the entity ID
        :param name: the entity name ("Unkwnon" if None or empty)
        :param status: the entity status (can be None for some entities)
        """

        self._id = entity_id
        self._name = "Unknown" if name is None or name == "" else name
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
    def type(self) -> type:
        """
        Returns the entity type.
        """
        return type(self)

    @property
    def status(self) -> EntityStatus:
        """
        Returns the entity status.
        """
        return self._status

    @status.setter
    def status(self, value: EntityStatus):
        """
        Sets the entity status.
        """
        self._status = value

    def __str__(self) -> str:
        return f"{self.type.__name__} #{self.id}: {self.name} - Status: \
                {self.status.name if self.status else 'None'}"

    #  Entities with same entity type and ID are the same entity)

    # Override the equality operator
    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    # Override the inequality operator
    def __ne__(self, other):
        return not self.__eq__(other)

    # Override the hash function
    def __hash__(self):
        return hash((self.type, self.id))


class CameEntitiesSet(set):
    """
    Represents a set of CAME entities.
    """

    def add(self, item):
        if not isinstance(item, CameEntity):
            # _LOGGER.error(
            #     "Item must be of type 'CameEntity'. Type: %s", type(item)
            # )
            raise TypeError("Item must be of type 'CameEntity'")
        super().add(item)


class Feature(CameEntity):
    """
    Represents a CAME server feature.
    """

    def __init__(self, name: str):
        """
        Constructor for the Feature class.

        :param name: the feature name
        """
        super().__init__(
            entity_id=hash(name),
            name=name,
        )


class Light(CameEntity):
    """
    Represents a CAME light.
    """

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = EntityStatus.OFF_CLOSED,
        light_type: LightType = LightType.ON_OFF,
        brightness: int = 100,
    ):
        """
        Constructor for the Came Light class.

        :param entity_id: the light ID
        :param name: the light name
        :param status: the light status (default: OFF)
        :param light_type: the light type (default: ON_OFF)
        :param brightness: the light brightness (default: 100)
        """

        self._light_type = light_type

        # Set brightness, with range from 0 to 100
        if brightness < 0:
            self._brightness = 0
            # _LOGGER.warning(
            #     "Invalid brightness (%s) setting to 0.",
            #     brightness,
            # )
        elif brightness > 100:
            self._brightness = 100
            # _LOGGER.warning(
            #     "Invalid brightness (%s), setting to 100.",
            #     brightness,
            # )
        else:
            self._brightness = brightness

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    @staticmethod
    def from_json(json_data: dict):
        """
        Updates the light properties from a JSON dictionary.

        :param json_data: the JSON dictionary representing the light
        """
        # Example of CAME light entity:
        # {
        # 	"act_id": 1,
        # 	"name": "My light",
        # 	"floor_ind":6,
        # 	"room_ind": 9,
        # 	"status": 0,
        # 	"type": "STEP_STEP"
        # }

        result = Light(
            entity_id=json_data["act_id"],
            name=json_data["name"] if "name" in json_data else None,
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                else EntityStatus.OFF_CLOSED
            ),
            light_type=(
                LightType(json_data["type"])
                if "type" in json_data
                else LightType.ON_OFF
            ),
        )

        return result

    # Properties
    @property
    def brightness(self) -> int:
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


class Opening(CameEntity):
    """
    Represents a CAME opening.
    """

    def __init__(
        self,
        entity_id: int,
        close_entity_id: int = None,
        name: str = None,
        *,
        status: EntityStatus = EntityStatus.ON_OPEN,
        cover_type: OpeningType = OpeningType.OPEN_CLOSE,
        partial_openings: list = None,
    ):
        """
        Constructor for the Came Opening class.

        :param entity_id: the opening ID
        :param close_entity_id: the closing ID (default: same as entity_id)
        :param name: the opening name
        :param status: the opening status (default: OPEN)
        :param cover_type: the opening type (default: OPEN_CLOSE)
        :param partial_openings: the list of partial openings (default: empty)
        """

        self._cover_type = cover_type
        self._close_entity_id = (
            close_entity_id if close_entity_id else entity_id
        )
        self._partial_openings = partial_openings if partial_openings else []

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def cover_type(self) -> OpeningType:
        """
        Returns the cover type.
        """
        return self._cover_type

    @property
    def close_entity_id(self) -> int:
        """
        Returns the closing entity ID.
        """
        return self._close_entity_id

    @property
    def partial_openings(self) -> list:
        """
        Returns the list of partial openings.
        """
        return self._partial_openings

    # TODO Implement partial_openings management (once examples are available)
    # @partial_openings.setter
    # def partial_openings(self, value: list):
    #     """
    #     Sets the list of partial openings.
    #     """
    #     self._partial_openings = value

    @staticmethod
    def from_json(json_data: dict):
        """
        Updates the light properties from a JSON dictionary.

        :param json_data: the JSON dictionary representing the light
        """

        # Example of CAME opening entity:
        # {
        #    "open_act_id": 26,
        #    "close_act_id": 27,
        #    "name": "My opening",
        #    "floor_ind": 17,
        #    "room_ind": 48,
        #    "status": 0,
        #    "partial": [],
        #    "type": 0
        # }

        result = Opening(
            entity_id=json_data["open_act_id"],
            close_entity_id=(
                json_data["close_act_id"]
                if "close_act_id" in json_data
                else json_data["open_act_id"]
            ),
            name=json_data["name"] if "name" in json_data else None,
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                else EntityStatus.ON_OPEN
            ),
            cover_type=(
                OpeningType(json_data["type"])
                if "type" in json_data
                else OpeningType.OPEN_CLOSE
            ),
        )

        return result


# endregion
