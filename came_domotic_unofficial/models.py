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

from datetime import datetime
from enum import Enum


# region Exceptions
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

    def __init__(self, ack_code=None, reason: str = None):
        """Constructor for the CameDomoticBadAckError class.

        :param ack_code: the ack code returned by the server.
        :param reason: the reason returned by the server (optional).
        """
        if ack_code is None:
            super().__init__("Bad ack code.")
        elif reason and len(str(reason)) > 0:
            super().__init__(f"Bad ack code: {str(ack_code)} - Reason: {str(reason)}")
        else:
            super().__init__(f"Bad ack code: {str(ack_code)}")


# endregion

# region Enums


class CameEnum(Enum):
    """Base class for all the CAME-related enums."""


class EntityType(CameEnum):
    """Enum listing all the CAME entity types.

    The :name of each enum member maps to feature.name.upper(),
    where 'feature' is a Feature instance.

    The :value of each enum member is the command to send to the remote server
    if you want to retrieve the list of items related to that entity type.
    """

    FEATURES = "feature_list_req"
    LIGHTS = "light_list_req"
    # LIGHTS = "nested_light_list_req"
    OPENINGS = "openings_list_req"
    # OPENINGS = "nested_openings_list_req"
    DIGITALIN = "digitalin_list_req"
    SCENARIOS = "scenarios_list_req"
    # UPDATE = "status_update_req"
    # RELAYS = "relays_list_req"
    # CAMERAS = "tvcc_cameras_list_req"
    # TIMERS = "timers_list_req"
    # THERMOREGULATION = "thermo_list_req"
    # ANALOGIN = "analogin_list_req"
    # USERS = "sl_users_list_req"
    # MAPS = "map_descr_req"


class EntityStatus(CameEnum):
    """Enum listing all the status of the CAME entities."""

    OFF_STOPPED = 0
    ON_OPEN_TRIGGERED = 1
    CLOSED = 2
    UNKNOWN = -1
    NOT_APPLICABLE = -99


class LightType(CameEnum):
    """Enum listing the light types."""

    ON_OFF = "STEP_STEP"
    DIMMABLE = "DIMMER"


class OpeningType(CameEnum):
    """Enum listing the opening types."""

    OPEN_CLOSE = 0


class DigitalInputType(CameEnum):
    """Enum listing the digital input types."""

    BUTTON = 1


class ScenarioIcon(CameEnum):
    """Enum listing the scenario icons."""

    LIGHTS = 14
    OPENINGS_OPEN = 22
    OPENINGS_CLOSE = 23
    UNKNOWN = -1


class ScenarioStatus(CameEnum):
    """Enum listing the scenario status."""

    NOT_APPLIED = 0
    ONGOING = 1
    APPLIED = 2


class SeasonSetting(Enum):
    """Enum listing the available seasons settings."""

    PLANT_OFF = "off"
    WINTER = "winter"
    SUMMER = "summer"


class ThermoZoneStatus(Enum):
    """Enum listing the available thermostat zone status."""

    OFF = 0
    MANUAL = 1
    AUTO = 2
    JOLLY = 3


# endregion

# region CAME entities


class CameEntity:
    """Base class for all the CAME entities.

    :property id: the entity ID.
    :property name: the entity name (default "Unknown" if None or empty).
    :property status: the entity status (default EntityStatus.NOT_APPLICABLE).
    """

    _DEFAULT_NAME = "Unknown"
    _DEFAULT_STATUS = EntityStatus.UNKNOWN

    def __init__(
        self,
        entity_id: int,
        name: str = _DEFAULT_NAME,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
    ):
        """Constructor for the CameEntity class.

        :param id: the entity ID
        :param name: the entity name ("Unknown" if None or empty)
        :param status: the entity status (can be None for some entities)

        :raises TypeError: if the entity ID is not an integer.
        :raises TypeError: if the entity name is not a string.
        :raises TypeError: if the entity status is not a valid EntityStatus.
        """
        # Validate the input.
        if not isinstance(entity_id, int):
            raise TypeError("The entity ID must be an integer")

        self._id = entity_id
        self._name = (
            name
            if name and isinstance(name, str) and name != ""
            else self._DEFAULT_NAME
        )
        self._status = (
            status if status and status in EntityStatus else self._DEFAULT_STATUS
        )

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
    def status(self) -> EntityStatus:
        """Returns the entity status."""
        return self._status

    @status.setter
    def status(self, value: EntityStatus):
        """Sets the entity status.

        :param value: the entity status (EntityStatus)

        :raises TypeError: if the value is not a valid EntityStatus.
        """
        # Validate the input.
        if value not in EntityStatus:
            raise TypeError("The entity status must be a valid EntityStatus")

        self._status = value

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} #{self.id}: {self.name} - Status: "
            f"{self.status.name}"
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",' f"status={self.status})"
        )

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.__repr__() == other.__repr__()

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((type(self), self.__repr__()))


class CameEntitySet(set):
    """Represents a set of CAME entities.

    :param entities: the list of entities to add to the set (optional).

    :method add: adds a CameEntity object to the set, validating its type.

    :raises TypeError: if the item is not of type CameEntity.
    """

    def __init__(self, entities=None):
        super().__init__()

        if entities is not None:
            for entity in entities:
                self.add(entity)

    def add(self, item):
        if not isinstance(item, CameEntity):
            raise TypeError("Item must be of type 'CameEntity'")
        super().add(item)


class Feature(CameEntity):
    """Represents a CAME server feature.

    The Feature class is a subclass of the CameEntity class, and it's used to
    represent a CAME server feature. The feature name is used as the unique
    identifier for the feature, and it's used to generate the entity ID.

    :property name: the feature name.
    """

    def __init__(self, name: str):
        """Constructor for the Feature class.

        :param name: the feature name
        """

        # Validate the input.
        if name is None or not isinstance(name, str) or name == "":
            raise TypeError("The feature name must be a non-empty string")

        super().__init__(
            entity_id=hash(name),  # Use an arbitrary ID, based on the name
            name=name,
            status=EntityStatus.NOT_APPLICABLE,
        )

    @property
    def name(self) -> str:
        """Returns the feature name."""
        return self._name

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.name}"

    def __repr__(self) -> str:
        return f'{type(self).__name__}("{self.name}")'

    # #Override the equality operator: features with the same name are the same
    # def __eq__(self, other):
    #     return type(self) is type(other) and self.name == other.name

    # # Override the inequality operator
    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # # Override the hash function
    # def __hash__(self):
    #     return hash((type(self), self.name))


class FeaturesSet(CameEntitySet):
    """Represents a set of features managed by a CAME ETI/Domo server.

    :method add: adds a Feature object to the set, validating its type.

    :raises TypeError: if the item is not of type Feature.
    """

    def add(self, item):
        if not isinstance(item, Feature):
            raise TypeError("Item must be of type 'Feature'")
        super().add(item)

    @staticmethod
    def from_json(features_list: dict):
        """Creates a Feature object from a JSON dictionary.

        Example of JSON input:
        ["lights", "openings", "thermoregulation", "energy", "loadsctrl"]

        :param features_list: the list of strings representing the features.

        :raises TypeError: if features_list is not a list if strings.
        :raises ValueError: if some of the values are not strings.
        """

        # Ensure the input is a list
        if not isinstance(features_list, list):
            raise TypeError("Input should be a list of strings.")

        # Ensure all elements in the list are strings
        if not all(isinstance(item, str) for item in features_list):
            raise ValueError("All elements in the list should be strings.")

        return FeaturesSet([Feature(feature) for feature in features_list])


class Light(CameEntity):
    """Represents a CAME light.

    The Light class is a subclass of the CameEntity class, and it's used to
    represent a CAME light.

    :property id: the light ID.
    :property name: the light name (default: "Unknown").
    :property status: the light status (ON or OFF, default: UNKNOWN).
    :property light_type: the light type (ON_OFF or DIMMABLE, default: ON_OFF).
    :property brightness: the light brightness (range: 0-100, default: 100).

    :method from_json: create a Light object from a JSON dictionary.
    """

    _DEFAULT_STATUS = EntityStatus.UNKNOWN
    _DEFAULT_LIGHT_TYPE = LightType.ON_OFF
    _DEFAULT_BRIGHTNESS = 100

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
        light_type: LightType = _DEFAULT_LIGHT_TYPE,
        brightness: int = _DEFAULT_BRIGHTNESS,
    ):
        """
        Constructor for the Came Light class.

        :param entity_id: the light ID.
        :param name: the light name.
        :param status: the light status (default: OFF).
        :param light_type: the light type (default: ON_OFF).
        :param brightness: the light brightness (range: 0-100, default: 100).
        """

        # Validate the input
        if light_type not in LightType:
            raise TypeError("The light type must be a valid LightType")
        if brightness is not None and not isinstance(brightness, int):
            raise TypeError("The brightness value must be an integer")

        self._light_type = light_type

        # Set brightness, with range from 0 to 100
        self._brightness = (
            100
            if brightness is None or brightness > 100
            else 0 if brightness < 0 else brightness
        )

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def brightness(self) -> int:
        """Returns the light brightness."""
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        """Sets the light brightness.

        :param value: the brightness value (range: 0-100)

        :raises ValueError: if the brightness value is not in the range 0-100
        """
        if value is None or value < 0 or value > 100:
            raise ValueError("The brightness value must be between 0 and 100")
        self._brightness = value

    @property
    def light_type(self) -> LightType:
        """Returns the light type (ON_OFF or DIMMABLE)."""
        return self._light_type

    def __str__(self) -> str:
        result = (
            f"{type(self).__name__} #{self.id}: {self.name} - "
            f"Type: ({self.light_type.name}) - Status: {self.status.name}"
        )

        if self.light_type == LightType.DIMMABLE:
            result += f" - Brightness: {self.brightness}"

        return result

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",'
            f"status={self.status},light_type={self.light_type},"
            f"brightness={self.brightness})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """Creates a Light object from a JSON dictionary.

        Example of JSON input:
        {
            "act_id": 1,
            "name": "My light",
            "status": 0,
            "type":	"DIMMER",
            "perc":	66
        }

        All the properties except "act_id" are optional, and they are set
        to their default values (name="Unknown", status=OFF, type=ON_OFF,
        perc=100).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the light.

        :raises KeyError: if the JSON dictionary doesn't contain the "act_id".
        :raises TypeError: if some of the values are not valid.
        """

        return Light(
            json_data["act_id"],
            (
                json_data["name"]
                if "name" in json_data and isinstance(json_data["name"], str)
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"]
                in EntityStatus._value2member_map_  # pylint: disable=protected-access # noqa: E501
                else Light._DEFAULT_STATUS
            ),
            light_type=(
                LightType(json_data["type"])
                if "type" in json_data
                and json_data["type"]
                in LightType._value2member_map_  # pylint: disable=protected-access # noqa: E501
                else Light._DEFAULT_LIGHT_TYPE
            ),
            brightness=(
                min(max(json_data["perc"], 0), 100)
                if "perc" in json_data and isinstance(json_data["perc"], int)
                else Light._DEFAULT_BRIGHTNESS
            ),
        )


class Opening(CameEntity):
    """Represents a CAME opening.

    The Opening class is a subclass of the CameEntity class, and it's used to
    represent a CAME opening (e.g. a cover).

    :property id: the opening ID.
    :property name: the opening name.
    :property status: the opening status (OPEN, CLOSED or STOPPED).
    :property opening_type: the opening type (OPEN_CLOSE).
    :property close_entity_id: the closing entity ID.
    :property partial_openings: the list of partial openings.

    :method from_json: create an Opening object from a JSON dictionary.
    """

    _DEFAULT_STATUS = EntityStatus.UNKNOWN
    _DEFAULT_OPENING_TYPE = OpeningType.OPEN_CLOSE

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
        close_entity_id: int = None,
        opening_type: OpeningType = _DEFAULT_OPENING_TYPE,
        partial_openings: list = None,
    ):
        """
        Constructor for the Came Opening class.

        :param entity_id: the opening ID.
        :param close_entity_id: the closing ID (default: same as entity_id).
        :param name: the opening name.
        :param status: the opening status (default: UNKNOWN).
        :param opening_type: the opening type (default: OPEN_CLOSE).
        :param partial_openings: the list of partial openings (default: empty).
        """

        # Input validation
        if close_entity_id is not None and not isinstance(close_entity_id, int):
            raise TypeError("The closing entity ID must be an integer")
        if opening_type not in OpeningType:
            raise TypeError("The opening type must be a valid OpeningType")
        if partial_openings is not None and not isinstance(partial_openings, list):
            raise TypeError("The partial openings must be a list")

        self._close_entity_id = close_entity_id if close_entity_id else entity_id
        self._opening_type = (
            opening_type if opening_type else self._DEFAULT_OPENING_TYPE
        )
        self._partial_openings = partial_openings if partial_openings else []

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def opening_type(self) -> OpeningType:
        """Returns the cover type."""
        return self._opening_type

    @property
    def close_entity_id(self) -> int:
        """Returns the closing entity ID."""
        return self._close_entity_id

    @property
    def partial_openings(self) -> list:
        """Returns the list of partial openings."""
        return self._partial_openings

    # TODO Implement partial_openings management (once examples are available)
    # @partial_openings.setter
    # def partial_openings(self, value: list):
    #     """Sets the list of partial openings."""
    #     self._partial_openings = value

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} #{self.id}/{self.close_entity_id}: "
            f'"{self.name}" - Type: {self.opening_type.name} - '
            f"Status: {self.status.name} - Partials: {self.partial_openings}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.id},{self.close_entity_id},"
            f'"{self.name}",status={self.status},'
            f"opening_type={self.opening_type},"
            f"partial_openings={self.partial_openings})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """
        Creates an Opening object from a JSON dictionary.

        Example of JSON input:
        {
            "open_act_id": 26,
            "close_act_id": 27,
            "name": "My opening",
            "status": 0,
            "partial": [],
            "type": 0
        }

        All the properties except "open_act_id" are optional, and they are set
        to their default values (name="Unknown", status=OFF, type=OPEN_CLOSE).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the opening.

        :raises KeyError: if the JSON dictionary doesn't contain the "open_act_id". # noqa: E501
        """

        return Opening(
            entity_id=json_data["open_act_id"],
            close_entity_id=(
                json_data["close_act_id"]
                if "close_act_id" in json_data
                and isinstance(json_data["close_act_id"], int)
                else json_data["open_act_id"]
            ),
            name=(
                json_data["name"]
                if "name" in json_data and isinstance(json_data["name"], str)
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"]
                in EntityStatus._value2member_map_  # pylint: disable=protected-access # noqa: E501
                else Opening._DEFAULT_STATUS
            ),
            opening_type=(
                OpeningType(json_data["type"])
                if "type" in json_data
                and json_data["type"]
                in OpeningType._value2member_map_  # pylint: disable=protected-access # noqa: E501
                else Opening._DEFAULT_OPENING_TYPE
            ),
            partial_openings=(
                json_data["partial"]
                if "partial" in json_data and isinstance(json_data["partial"], list)
                else None
            ),
        )


class DigitalInput(CameEntity):
    """Represents a CAME digital input (e.g. a button).

    The DigitalIn class is a subclass of the CameEntity class, and it's used to
    represent a CAME digital input (e.g. a button).

    :param entity_id: the digital input ID.
    :param name: the digital input name.
    :param button_type: the digital input type (default: BUTTON).
    :param address: the digital input address (default: 0).
    :param ack_code: the digital input ack code (default: 1).
    :param radio_node_id: radio node ID (default: "00000000").
    :param rf_radio_link_quality: radio link quality (default: 0).
    :param utc_time: the digital input UTC time offset (default: 0).
    """

    _DEFAULT_BUTTON_TYPE = DigitalInputType.BUTTON
    _DEFAULT_ADDRESS = 0
    _DEFAULT_ACK_CODE = 1
    _DEFAULT_RADIO_NODE_ID = "00000000"
    _DEFAULT_RF_RADIO_LINK_QUALITY = 0
    _DEFAULT_UTC_TIME = 0

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        button_type: DigitalInputType = _DEFAULT_BUTTON_TYPE,
        address: int = _DEFAULT_ADDRESS,
        ack_code: int = _DEFAULT_ACK_CODE,
        radio_node_id: str = _DEFAULT_RADIO_NODE_ID,
        rf_radio_link_quality: int = _DEFAULT_RF_RADIO_LINK_QUALITY,
        utc_time: int = _DEFAULT_UTC_TIME,
    ):

        # Validate the input
        if button_type not in DigitalInputType:
            raise TypeError("The digital input type must be a valid DigitalInType")
        if address is not None and not isinstance(address, int):
            raise TypeError("The digital input address must be an integer")
        if ack_code is not None and not isinstance(ack_code, int):
            raise TypeError("The digital input ack code must be an integer")
        if radio_node_id is not None and not isinstance(radio_node_id, str):
            raise TypeError("The radio node ID must be a string")
        if rf_radio_link_quality is not None and not isinstance(
            rf_radio_link_quality, int
        ):
            raise TypeError("The radio link quality must be an integer")
        if utc_time is not None and not isinstance(utc_time, int):
            raise TypeError("The UTC time must be an integer (Unix epoch)")

        self._button_type = button_type
        self._address = address
        self._ack_code = ack_code
        self._radio_node_id = radio_node_id
        self._rf_radio_link_quality = rf_radio_link_quality
        self._utc_time = utc_time

        super().__init__(
            entity_id,
            name,
            status=EntityStatus.NOT_APPLICABLE,
        )

    # Properties
    @property
    def button_type(self) -> DigitalInputType:
        """Returns the digital input type."""
        return self._button_type

    @property
    def address(self) -> int:
        """Returns the digital input address."""
        return self._address

    @property
    def ack_code(self) -> int:
        """Returns the digital input ack code."""
        return self._ack_code

    @property
    def radio_node_id(self) -> str:
        """Returns the digital input radio node ID."""
        return self._radio_node_id

    @property
    def rf_radio_link_quality(self) -> int:
        """Returns the digital input radio link quality."""
        return self._rf_radio_link_quality

    @property
    def last_pressed(self) -> datetime:
        """Returns the digital input UTC time offset."""
        return datetime.fromtimestamp(self._utc_time)

    def __str__(self) -> str:
        return (
            f'{type(self).__name__} #{self.id}: "{self.name}" - '
            f"Type: {self.button_type.name} - Address: {self.address} - "
            f'Ack code: {self.ack_code} - Radio node ID: "{self.radio_node_id}" - '  # noqa: E50
            f"RF radio link quality: {self.rf_radio_link_quality} - "
            f"Last pressed: {self.last_pressed}"
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",'
            f"button_type={self.button_type},address={self.address},"
            f'ack_code={self.ack_code},radio_node_id="{self.radio_node_id}",'
            f"rf_radio_link_quality={self.rf_radio_link_quality},"
            f"utc_time={self._utc_time})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """Creates a DigitalIn object from a JSON dictionary.

        Example of JSON input:
        {
            "name":	"My button",
            "act_id":	11,
            "type":	1,
            "addr":	0,
            "ack":	1,
            "radio_node_id":	"00000000",
            "rf_radio_link_quality":	0,
            "utc_time":	0
        }

        All the properties except "act_id" are optional, and they are set
        to their default values (name="Unknown", type=BUTTON, addr=0, ack=1,
        radio_node_id="00000000", rf_radio_link_quality=0, utc_time=0).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the digital input

        :raises KeyError: if the JSON dictionary doesn't contain the "act_id"
        """

        return DigitalInput(
            entity_id=json_data["act_id"],
            name=(
                json_data["name"]
                if "name" in json_data and isinstance(json_data["name"], str)
                else CameEntity._DEFAULT_NAME
            ),
            button_type=(
                DigitalInputType(json_data["type"])
                if "type" in json_data and json_data["type"] in DigitalInputType
                else DigitalInput._DEFAULT_BUTTON_TYPE
            ),
            address=(
                json_data["addr"]
                if "addr" in json_data and isinstance(json_data["addr"], int)
                else DigitalInput._DEFAULT_ADDRESS
            ),
            ack_code=(
                json_data["ack"]
                if "ack" in json_data and isinstance(json_data["ack"], int)
                else DigitalInput._DEFAULT_ACK_CODE
            ),
            radio_node_id=(
                json_data["radio_node_id"]
                if "radio_node_id" in json_data
                and isinstance(json_data["radio_node_id"], str)
                else DigitalInput._DEFAULT_RADIO_NODE_ID
            ),
            rf_radio_link_quality=(
                json_data["rf_radio_link_quality"]
                if "rf_radio_link_quality" in json_data
                and isinstance(json_data["rf_radio_link_quality"], int)
                else DigitalInput._DEFAULT_RF_RADIO_LINK_QUALITY
            ),
            utc_time=(
                json_data["utc_time"]
                if "utc_time" in json_data and isinstance(json_data["utc_time"], int)
                else DigitalInput._DEFAULT_UTC_TIME
            ),
        )


class Scenario(CameEntity):
    """Represents a CAME predefined scenario.

    The Scenario class is a subclass of the CameEntity class, and it's used to
    represent a CAME predefined scenario.

    :property id: the scenario ID
    :property name: the scenario name. Defaults to "Unknown" if None or empty.
    :property status: the scenario status (OFF, ON). Defaults to OFF.
    :property scenario_status: the scenario status (NOT_APPLIED, ONGOING, APPLIED). Defaults to NOT_APPLIED  # noqa: E501 # pylint: disable=line-too-long
    :property icon: the scenario icon type. Defaults to UNKNOWN.
    :property is_user_defined: the scenario is user defined. Defaults to False.

    :method from_json: create a Scenario object from a JSON dictionary.
    """

    _DEFAULT_STATUS = EntityStatus.UNKNOWN
    _DEFAULT_SCENARIO_STATUS = ScenarioStatus.NOT_APPLIED
    _DEFAULT_ICON_ID = ScenarioIcon.UNKNOWN

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
        scenario_status: ScenarioStatus = _DEFAULT_SCENARIO_STATUS,
        icon: ScenarioIcon = _DEFAULT_ICON_ID,
        is_user_defined: bool = False,
    ):
        """
        Constructor for the Came Scenario class.

        Args:
            entity_id (int): the scenario ID.
            name (str, optional): the scenario name. Default: "Unknown" if None/empty.
            status (EntityStatus, optional): the scenario status. Defaults to UNKNOWN.
            scenario_status (ScenarioStatus, optional): the scenario status. Defaults to NOT_APPLIED.
            icon (ScenarioIcon, optional): the scenario icon type. Defaults to UNKNOWN.
            is_user_defined (bool, optional): whether the scenario is user defined. Defaults to False.
        """

        # Validate the input
        if scenario_status not in ScenarioStatus:
            raise TypeError("The scenario status must be a valid ScenarioStatus")
        if icon not in ScenarioIcon:
            raise TypeError("The scenario icon must be a valid ScenarioIcon")
        if is_user_defined is not None and not isinstance(is_user_defined, bool):
            raise TypeError("The is_user_defined value must be a boolean")

        self._scenario_status = scenario_status
        self._icon = icon
        self._is_user_defined = is_user_defined

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def scenario_status(self) -> ScenarioStatus:
        """Returns the scenario status (NOT_APPLIED, ONGOING, APPLIED)."""
        return self._scenario_status

    @scenario_status.setter
    def scenario_status(self, value: ScenarioStatus):
        """Sets the scenario status.

        Args:
            value (ScenarioStatus): the scenario status.

        Raises:
            TypeError: if the value is not a valid ScenarioStatus.
        """
        if value not in ScenarioStatus:
            raise TypeError("The scenario status must be a valid ScenarioStatus")

        self._scenario_status = value

    @property
    def icon(self) -> ScenarioIcon:
        """Returns the scenario icon type."""
        return self._icon

    @property
    def is_user_defined(self) -> bool:
        """Returns whether the scenario is user defined or not."""
        return self._is_user_defined

    def __str__(self) -> str:
        return (
            f'{type(self).__name__} #{self.id}: "{self.name}" - '
            f"Status: {self.status.name} - Scenario status: {self.scenario_status.name} - "  # noqa: E501 # pylint: disable=line-too-long
            f"Icon: {self.icon.name} - User defined: {self.is_user_defined}"
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",'
            f"status={self.status},scenario_status={self.scenario_status},"
            f"icon={self.icon},is_user_defined={self.is_user_defined})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """Creates a Scenario object from a JSON dictionary.

        Example of JSON input:
        {
            "name":	"Close all openings",
            "id":	6,
            "status":	0,
            "scenario_status":	0,
            "icon_id":	23,
            "user-defined":	0
        }

        All the properties except "id" are optional, and they are set
        to their default values (name="Unknown", status=OFF,
        scenario_status=NOT_APPLIED, icon=UNKNOWN, user-defined=False).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the scenario.

        :raises KeyError: if the JSON dictionary doesn't contain the "id".
        """

        return Scenario(
            entity_id=json_data["id"],
            name=(
                json_data["name"] if "name" in json_data else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data and json_data["status"] in EntityStatus
                else Scenario._DEFAULT_STATUS
            ),
            scenario_status=(
                ScenarioStatus(json_data["scenario_status"])
                if "scenario_status" in json_data
                and json_data["scenario_status"] in ScenarioStatus
                else Scenario._DEFAULT_SCENARIO_STATUS
            ),
            icon=(
                ScenarioIcon(json_data["icon_id"])
                if "icon_id" in json_data and json_data["icon_id"] in ScenarioIcon
                else Scenario._DEFAULT_ICON_ID
            ),
            is_user_defined=(
                bool(json_data["user-defined"])
                if "user-defined" in json_data
                and isinstance(json_data["user-defined"], int)
                else False
            ),
        )


# endregion

# region Mappers

_EntityType2Class = {
    EntityType.FEATURES: Feature,
    EntityType.LIGHTS: Light,
    EntityType.OPENINGS: Opening,
    EntityType.DIGITALIN: DigitalInput,
    EntityType.SCENARIOS: Scenario,
    # EntityType.UPDATE:
    # EntityType.RELAYS:
    # EntityType.CAMERAS:
    # EntityType.TIMERS:
    # EntityType.THERMOREGULATION:
    # EntityType.ANALOGIN:
    # EntityType.USERS:
    # EntityType.MAPS:
}

_Class2SwitchCommand = {
    Light: "light_switch_req",
    Opening: "opening_move_req",
    Scenario: "scenario_activation_req",
}

# endregion
