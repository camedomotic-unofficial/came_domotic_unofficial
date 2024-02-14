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


class CameDomoticBadAckError(CameDomoticRequestError):
    """Raised when the server returns a bad ack reason"""


class CommandNotFoundError(CameDomoticError):
    """
    Raised if the user tries to send a command to the server that
    does not exists
    """


class FeatureNotSupportedError(CameDomoticError):
    """
    Raised if the user tries to use a feature to get a list of entities
    that are not supported by the CAME ETI/Domo server
    """


# endregion


# region Enums
class CameEnum(Enum):
    """Base class for all the CAME enums."""


class EntityType(CameEnum):
    """
    Enum listing all the CAME entity types.

    The :name of each enum member maps to feature.name.upper(),
    where feature is a Feature instance.

    The :value of each enum member is the command to retrieve the list of items
    related to that entity type.

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


# available_commands = {
#         "update": "status_update_req",
#         "relays": "relays_list_req",
#         "cameras": "tvcc_cameras_list_req",
#         "timers": "timers_list_req",
#         "thermoregulation": "thermo_list_req",
#         "analogin": "analogin_list_req",
#         "digitalin": "digitalin_list_req",
#         "lights": "nested_light_list_req",
#         "features": "feature_list_req",
#         "users": "sl_users_list_req",
#         "maps": "map_descr_req"
#     }


class EntityStatus(CameEnum):
    """Enum listing all the status of the CAME entities."""

    ON_OPEN = 1
    OFF_CLOSED = 0
    NOT_APPLICABLE = -99


class LightType(CameEnum):
    """Enum listing the light types."""

    ON_OFF = "STEP_STEP"
    DIMMABLE = "DIMMER"


class OpeningType(CameEnum):
    """Enum listing the opening types."""

    OPEN_CLOSE = 0


class DigitalInType(CameEnum):
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

    _DEFAULT_NAME = "Unknown"

    def __init__(
        self,
        entity_id: int,
        name: str = _DEFAULT_NAME,
        *,
        status: EntityStatus = None,
    ):
        """
        Constructor for the CameEntity class.

        :param id: the entity ID
        :param name: the entity name ("Unknown" if None or empty)
        :param status: the entity status (can be None for some entities)
        """

        self._id = entity_id
        self._name = self._DEFAULT_NAME if name is None or name == "" else name
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
        return (
            f"{self.type.__name__} #{self.id}: {self.name} - Status: "
            f"{self.status.name if self.status else 'None'}"
        )

    def __repr__(self) -> str:
        return (
            f'{self.type.__name__}({self.id},"{self.name}",'
            f"status={self.status})"
            if self.status
            else f'{self.type.__name__}({self.id},"{self.name}")'
        )


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

    @property
    def name(self) -> str:
        """
        Returns the feature name.
        """
        return self._name

    def __str__(self) -> str:
        return f"{self.type.__name__}: {self.name}"

    def __repr__(self) -> str:
        return f'{self.type.__name__}("{self.name}")'

    # Override the equality operator: features with the same name are the same
    def __eq__(self, other):
        return self.type == other.type and self.name == other.name

    # Override the inequality operator
    def __ne__(self, other):
        return not self.__eq__(other)

    # Override the hash function
    def __hash__(self):
        return hash((self.type, self.name))


class FeaturesSet(set):
    """
    Represents a set of features managed by a CAME ETI/Domo server.
    """

    def add(self, item):
        if not isinstance(item, Feature):
            # _LOGGER.error(
            #     "Item must be of type 'CameEntity'. Type: %s", type(item)
            # )
            raise TypeError("Item must be of type 'Feature'")
        super().add(item)


class Light(CameEntity):
    """
    Represents a CAME light.
    """

    _DEFAULT_STATUS = EntityStatus.OFF_CLOSED
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

        :param entity_id: the light ID
        :param name: the light name
        :param status: the light status (default: OFF)
        :param light_type: the light type (default: ON_OFF)
        :param brightness: the light brightness (range: 0-100, default: 100)
        """

        self._light_type = light_type

        # Set brightness, with range from 0 to 100
        if brightness is None:
            self._brightness = 100
        elif brightness < 0:
            self._brightness = 0
        elif brightness > 100:
            self._brightness = 100
        else:
            self._brightness = brightness

        super().__init__(
            entity_id,
            name,
            status=status,
        )

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
        if value is None or value < 0 or value > 100:
            raise ValueError("The brightness value must be between 0 and 100")
        self._brightness = value

    @property
    def light_type(self) -> LightType:
        """
        Returns the light type.
        """
        return self._light_type

    def __str__(self) -> str:
        result = (
            f"{self.type.__name__} #{self.id}: {self.name} - "
            f"Type: ({self.light_type.name}) - Status: {self.status.name}"
        )

        if self.light_type == LightType.DIMMABLE:
            result += f" - Brightness: {self.brightness}"

        return result

    def __repr__(self) -> str:
        return (
            f'{self.type.__name__}({self.id},"{self.name}",'
            f"status={self.status},light_type={self.light_type},"
            f"brightness={self.brightness})"
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
        # 	"type":	"DIMMER",
        #   "perc":	66
        # }
        # status, type, perc

        return Light(
            json_data["act_id"],
            (
                json_data["name"]
                if "name" in json_data
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"] in EntityStatus
                else Light._DEFAULT_STATUS
            ),
            light_type=(
                LightType(json_data["type"])
                if "type" in json_data and json_data["type"] in LightType
                else Light._DEFAULT_LIGHT_TYPE
            ),
            brightness=(
                json_data["perc"]
                if "perc" in json_data
                else Light._DEFAULT_BRIGHTNESS
            ),
        )


class Opening(CameEntity):
    """
    Represents a CAME opening.
    """

    _DEFAULT_STATUS = EntityStatus.OFF_CLOSED
    _DEFAULT_OPENING_TYPE = OpeningType.OPEN_CLOSE

    def __init__(
        self,
        entity_id: int,
        close_entity_id: int = None,
        name: str = None,
        *,
        status: EntityStatus = EntityStatus.ON_OPEN,
        opening_type: OpeningType = OpeningType.OPEN_CLOSE,
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

        self._close_entity_id = (
            close_entity_id if close_entity_id else entity_id
        )
        self._opening_type = opening_type
        self._partial_openings = partial_openings if partial_openings else []

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def opening_type(self) -> OpeningType:
        """
        Returns the cover type.
        """
        return self._opening_type

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

    def __str__(self) -> str:
        return (
            f"{self.type.__name__} #{self.id}/{self.close_entity_id}: "
            f"{self.name} - Type: {self.opening_type} - "
            f"Status: {self.status.name} - Partials: {self.partial_openings}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.type.__name__}({self.id},{self.close_entity_id},"
            f'"{self.name}",status={self.status},'
            f"opening_type={self.opening_type},"
            f"partial_openings={self.partial_openings})"
        )

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

        return Opening(
            entity_id=json_data["open_act_id"],
            close_entity_id=(
                json_data["close_act_id"]
                if "close_act_id" in json_data
                else json_data["open_act_id"]
            ),
            name=(
                json_data["name"]
                if "name" in json_data
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"] in EntityStatus
                else Opening._DEFAULT_STATUS
            ),
            opening_type=(
                OpeningType(json_data["type"])
                if "type" in json_data and json_data["type"] in OpeningType
                else Opening._DEFAULT_OPENING_TYPE
            ),
            partial_openings=(
                json_data["partial"] if "partial" in json_data else []
            ),
        )


class DigitalIn(CameEntity):
    """
    Represents a CAME digital input (button).
    """

    _DEFAULT_BUTTON_TYPE = DigitalInType.BUTTON
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
        button_type: DigitalInType = _DEFAULT_BUTTON_TYPE,
        address: int = _DEFAULT_ADDRESS,
        ack_code: int = _DEFAULT_ACK_CODE,
        radio_node_id: str = _DEFAULT_RADIO_NODE_ID,
        rf_radio_link_quality: int = _DEFAULT_RF_RADIO_LINK_QUALITY,
        utc_time: int = _DEFAULT_UTC_TIME,
    ):
        """
        Constructor for the Came DigitalIn class.

        :param entity_id: the digital input ID
        :param name: the digital input name
        :param button_type: the digital input type (default: BUTTON)
        :param address: the digital input address (default: 0)
        :param ack_code: the digital input ack code (default: 1)
        :param radio_node_id: radio node ID (default: "00000000")
        :param rf_radio_link_quality: radio link quality (default: 0)
        :param utc_time: the digital input UTC time offset (default: 0)
        """

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
    def button_type(self) -> DigitalInType:
        """
        Returns the digital input type.
        """
        return self._button_type

    @property
    def address(self) -> int:
        """
        Returns the digital input address.
        """
        return self._address

    @property
    def ack_code(self) -> int:
        """
        Returns the digital input ack code.
        """
        return self._ack_code

    @property
    def radio_node_id(self) -> str:
        """
        Returns the digital input radio node ID.
        """
        return self._radio_node_id

    @property
    def rf_radio_link_quality(self) -> int:
        """
        Returns the digital input radio link quality.
        """
        return self._rf_radio_link_quality

    @property
    def last_pressed(self) -> datetime:
        """
        Returns the digital input UTC time offset.
        """
        return datetime.fromtimestamp(self._utc_time)

    def __str__(self) -> str:
        return (
            f"{self.type.__name__} #{self.id}: {self.name} - "
            f"Type: {self.button_type.name} - Address: {self.address} - "
            f"Ack code: {self.ack_code} - Radio node ID: {self.radio_node_id} - "
            f"Radio link quality: {self.rf_radio_link_quality} - "
            f"UTC time: {self.last_pressed}"
        )

    def __repr__(self) -> str:
        return (
            f'{self.type.__name__}({self.id},"{self.name}",'
            f"button_type={self.button_type},address={self.address},"
            f"ack_code={self.ack_code},radio_node_id={self.radio_node_id},"
            f"rf_radio_link_quality={self.rf_radio_link_quality},"
            f"utc_time={self._utc_time})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """
        Updates the digital input properties from a JSON dictionary.

        :param json_data: the JSON dictionary representing the digital input
        """

        # Example of JSON representation
        # {
        #     "name":	"My button",
        #     "act_id":	11,
        #     "type":	1,
        #     "addr":	0,
        #     "ack":	1,
        #     "radio_node_id":	"00000000",
        #     "rf_radio_link_quality":	0,
        #     "utc_time":	0
        # }

        return DigitalIn(
            entity_id=json_data["act_id"],
            name=(
                json_data["name"]
                if "name" in json_data
                else CameEntity._DEFAULT_NAME
            ),
            button_type=(
                DigitalInType(json_data["type"])
                if "type" in json_data and json_data["type"] in DigitalInType
                else DigitalIn._DEFAULT_BUTTON_TYPE
            ),
            address=(
                json_data["addr"]
                if "addr" in json_data
                else DigitalIn._DEFAULT_ADDRESS
            ),
            ack_code=(
                json_data["ack"]
                if "ack" in json_data
                else DigitalIn._DEFAULT_ACK_CODE
            ),
            radio_node_id=(
                json_data["radio_node_id"]
                if "radio_node_id" in json_data
                else DigitalIn._DEFAULT_RADIO_NODE_ID
            ),
            rf_radio_link_quality=(
                json_data["rf_radio_link_quality"]
                if "rf_radio_link_quality" in json_data
                else DigitalIn._DEFAULT_RF_RADIO_LINK_QUALITY
            ),
            utc_time=(
                json_data["utc_time"]
                if "utc_time" in json_data
                else DigitalIn._DEFAULT_UTC_TIME
            ),
        )


class Scenario(CameEntity):
    """
    Represents a CAME scenario.
    """

    _DEFAULT_STATUS = EntityStatus.OFF_CLOSED
    _DEFAULT_SCENARIO_STATUS = ScenarioStatus.NOT_APPLIED
    _DEFAULT_ICON_ID = ScenarioIcon.UNKNOWN

    def __init__(
        self,
        entity_id: int,
        name: str = None,
        *,
        status: EntityStatus = EntityStatus.OFF_CLOSED,
        scenario_status: ScenarioStatus = ScenarioStatus.NOT_APPLIED,
        icon: ScenarioIcon = ScenarioIcon.UNKNOWN,
        is_user_defined: bool = False,
    ):
        """
        Constructor for the Came Scenario class.

        :param entity_id: the scenario ID
        :param name: the scenario name
        :param status: the scenario status (default: OFF, ON when ongoing)
        :param scenario_status: the scenario status (default: NOT_APPLIED)
        :param icon: the scenario icon type (default: UNKNOWN)
        :param is_user_defined: the scenario is user defined (default: false)
        """

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
        """
        Returns the scenario status.
        """
        return self._scenario_status

    @scenario_status.setter
    def scenario_status(self, value: ScenarioStatus):
        """
        Sets the scenario status.
        """
        self._scenario_status = value

    @property
    def icon(self) -> ScenarioIcon:
        """
        Returns the scenario icon.
        """
        return self._icon

    @property
    def is_user_defined(self) -> bool:
        """
        Returns whether the scenario is user defined.
        """
        return self._is_user_defined

    def __str__(self) -> str:
        return (
            f"{self.type.__name__} #{self.id}: {self.name} - "
            f"Status: {self.status.name} - Scenario status: {self.scenario_status.name} - "
            f"Icon: {self.icon.name} - User defined: {self.is_user_defined}"
        )

    def __repr__(self) -> str:
        return (
            f'{self.type.__name__}({self.id},"{self.name}",'
            f"status={self.status},scenario_status={self.scenario_status},"
            f"icon={self.icon},is_user_defined={self.is_user_defined})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """
        Updates the scenario properties from a JSON dictionary.

        :param json_data: the JSON dictionary representing the scenario
        """

        # Example of CAME scenario entity:
        # {
        # 	"name":	"Close all openings",
        # 	"id":	6,
        # 	"status":	0,
        # 	"scenario_status":	0,
        # 	"icon_id":	23,
        # 	"user-defined":	0
        # }

        return Scenario(
            entity_id=json_data["id"],
            name=(
                json_data["name"]
                if "name" in json_data
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"] in EntityStatus
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
                if "icon_id" in json_data
                and json_data["icon_id"] in ScenarioIcon
                else Scenario._DEFAULT_ICON_ID
            ),
            is_user_defined=(
                bool(json_data["user-defined"])
                if "user-defined" in json_data
                else False
            ),
        )


# endregion

# region Mappers

EntityType2Class = {
    EntityType.FEATURES: Feature,
    EntityType.LIGHTS: Light,
    EntityType.OPENINGS: Opening,
    EntityType.DIGITALIN: DigitalIn,
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

# endregion
