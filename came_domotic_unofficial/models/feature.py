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

"""This module contains the class representing a CAME feature."""

from .came_entity import CameEntity, CameEntitySet
from .enums import EntityStatus


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


class FeatureSet(CameEntitySet):
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

        return FeatureSet([Feature(feature) for feature in features_list])
