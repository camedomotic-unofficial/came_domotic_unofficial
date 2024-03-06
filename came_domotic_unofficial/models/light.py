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

"""This module contains the class representing a CAME light."""


from typing import Optional
from .came_entity import CameEntity
from .enums import EntityStatus, LightType


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
        name: Optional[str] = CameEntity._DEFAULT_NAME,
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
        if brightness is None or brightness > 100:
            self._brightness = 100
        elif brightness < 0:
            self._brightness = 0
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
        to their default values (name="Unknown", status=UNKNOWN, type=ON_OFF,
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
                in EntityStatus._value2member_map_  # pylint: disable=protected-access
                else Light._DEFAULT_STATUS
            ),
            light_type=(
                LightType(json_data["type"])
                if "type" in json_data
                and json_data["type"]
                in LightType._value2member_map_  # pylint: disable=protected-access
                else Light._DEFAULT_LIGHT_TYPE
            ),
            brightness=(
                min(max(json_data["perc"], 0), 100)
                if "perc" in json_data and isinstance(json_data["perc"], int)
                else Light._DEFAULT_BRIGHTNESS
            ),
        )
