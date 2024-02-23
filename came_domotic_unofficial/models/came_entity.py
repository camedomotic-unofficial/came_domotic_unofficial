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
This module contains the base class for all the CAME entities.

Raises:
    TypeError: if the entity ID is not an integer.
"""


from typing import Optional
from .enums import (
    EntityStatus,
)


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
        name: Optional[str] = _DEFAULT_NAME,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
    ):
        """Constructor for the CameEntity class.

        :param id: the entity ID
        :param name: the entity name ("Unknown" if None or empty)
        :param status: the entity status (can be None for some entities)

        :raises TypeError: if the entity ID is not an integer.
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
        return f'{type(self).__name__}({self.id},"{self.name}",status={self.status})'

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.__repr__() == other.__repr__()

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((type(self), self.__repr__()))

    @staticmethod
    def from_json(json_data: dict):
        """Creates a CameEntity object from a JSON dictionary.

        Example of JSON input:
        {
            "act_id": 1,
            "name": "My entity",
            "status": 0,
        }

        All the properties except "act_id" are optional, and they are set
        to their default values (name="Unknown", status=UNKNOWN).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the light.

        :raises KeyError: if the JSON dictionary doesn't contain the "act_id".
        """

        return CameEntity(
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
                else CameEntity._DEFAULT_STATUS
            ),
        )


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
