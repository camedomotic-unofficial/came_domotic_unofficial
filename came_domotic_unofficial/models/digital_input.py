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
This module contains the DigitalInput class, which represents a CAME digital input 
(e.g. a physical button).
"""

from datetime import datetime, UTC
from typing import Optional
from .came_entity import CameEntity
from .enums import DigitalInputType, EntityStatus


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
        name: Optional[str] = CameEntity._DEFAULT_NAME,
        *,
        button_type: DigitalInputType = _DEFAULT_BUTTON_TYPE,
        address: int = _DEFAULT_ADDRESS,
        ack_code: int = _DEFAULT_ACK_CODE,
        radio_node_id: str = _DEFAULT_RADIO_NODE_ID,
        rf_radio_link_quality: int = _DEFAULT_RF_RADIO_LINK_QUALITY,
        utc_time: int = _DEFAULT_UTC_TIME,
    ):
        """Constructor for the DigitalInput class.

        Args:
            entity_id (int): the digital input ID.
            name (Optional[str], optional): name of the device. Defaults to "Unknown".
            button_type (DigitalInputType, optional): type of the device. Defaults to DigitalInputType.BUTTON.
            address (int, optional): address of the device. Defaults to 0.
            ack_code (int, optional): ack code of the device. Defaults to 1.
            radio_node_id (str, optional): radio_node_id. Defaults to "00000000".
            rf_radio_link_quality (int, optional): rf radio link quality. Defaults to 0.
            utc_time (int, optional): UNIX epoch of the last trigger of the device. Defaults to 0.
        """
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
        return datetime.fromtimestamp(self._utc_time, UTC)

    def __str__(self) -> str:
        return (
            f'{type(self).__name__} #{self.id}: "{self.name}" - '
            f"Type: {self.button_type.name} - Address: {self.address} - "
            f'Ack code: {self.ack_code} - Radio node ID: "{self.radio_node_id}" - '
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
