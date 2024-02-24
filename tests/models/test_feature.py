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
Unit tests for the Feature and FeatureSet classes.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, lists
from came_domotic_unofficial.models import (
    CameEntitySet,
    CameEntity,
    Feature,
    FeaturesSet,
    EntityStatus,
)

# region Feature


@given(
    input_name=text(min_size=1, max_size=256),
)
def test_feature_constructor(input_name):
    """
    Test if the Feature constructor works correctly.
    """
    feature = Feature(input_name)

    assert isinstance(feature, CameEntity)
    assert feature.name == input_name
    assert feature.id == hash(input_name)
    assert feature.status == EntityStatus.NOT_APPLICABLE


def test_feature_constructor_invalid_name():
    """
    Test if the Feature constructor raises an error with an invalid name.
    """
    with pytest.raises(TypeError) as exc_info:
        Feature(5)

    assert str(exc_info.value) == "The feature name must be a non-empty string"


def test_feature_constructor_empty_name():
    """
    Test if the Feature constructor raises an error with an invalid name.
    """
    with pytest.raises(TypeError) as exc_info:
        Feature("")

    assert str(exc_info.value) == "The feature name must be a non-empty string"


def test_feature_str_method():
    """
    Test if the Feature __str__ method works correctly.
    """
    feature = Feature("Test Feature")

    assert str(feature) == "Feature: Test Feature"


def test_feature_repr_method():
    """
    Test if the Feature __repr__ method works correctly.
    """
    feature = Feature("Test Feature")

    assert repr(feature) == 'Feature("Test Feature")'


def test_feature_equality_operators():
    """
    Test if the Feature equality operator works correctly.
    """
    feature_name = "Test Feature"
    feature1 = Feature(feature_name)
    feature2 = Feature(feature_name)
    feature3 = Feature("Different Feature")
    other_type1 = CameEntity(
        hash(feature_name), feature_name, status=EntityStatus.NOT_APPLICABLE
    )
    other_type2 = repr(feature1)
    other_type3 = feature_name

    assert feature1 == feature2
    assert feature1 != feature3
    assert feature1 != other_type1
    assert feature1 != other_type2
    assert feature1 != other_type3


def test_feature_hash_function():
    """
    Test if the Feature hash function works correctly.
    """
    feature_name = "Test Feature"
    feature1 = Feature(feature_name)
    feature2 = Feature(feature_name)
    feature3 = Feature("Different Feature")
    other_type1 = CameEntity(
        hash(feature_name), feature_name, status=EntityStatus.NOT_APPLICABLE
    )
    other_type2 = repr(feature1)
    other_type3 = feature_name

    assert hash(feature1) == hash(feature2)
    assert hash(feature1) != hash(feature3)
    assert hash(feature1) != hash(other_type1)
    assert hash(feature1) != hash(other_type2)
    assert hash(feature1) != hash(other_type3)


# endregion

# region FeatureSet


def test_featureset_initialization():
    """
    Test the initialization of the CameEntitiesSet class.
    """
    feature_set = FeaturesSet()

    assert isinstance(feature_set, CameEntitySet)
    assert len(feature_set) == 0


def test_featureset_initialization_with_items():
    """
    Test the initialization of the CameEntitiesSet class with items.
    """
    entity1 = Feature("Test 1")
    entity2 = Feature("Test 2")
    feature_set = FeaturesSet([entity1, entity2])

    assert entity1 in feature_set
    assert entity2 in feature_set
    assert len(feature_set) == 2


def test_featuresset_eq():
    """
    Test the equality operator for the CameEntitiesSet class.
    """
    feature1 = Feature("Test feature 1")
    feature2 = Feature("Test feature 2")
    feature3 = Feature("Test feature 3")
    features_set1 = CameEntitySet([feature1, feature2])
    features_set2 = CameEntitySet([feature1, feature2])
    features_set3 = CameEntitySet([feature1, feature3])

    assert features_set1 == features_set2
    assert features_set1 != features_set3


def test_featureset_add_valid_item():
    """
    Test if a valid item can be added to the CameEntitiesSet.
    """
    feature_set = FeaturesSet()
    entity = Feature("Test")
    feature_set.add(entity)

    assert entity in feature_set


def test_featureset_add_invalid_item():
    """
    Test if an invalid item cannot be added to the CameEntitiesSet.
    """
    feature_set = FeaturesSet()

    with pytest.raises(TypeError) as exc_info:
        feature_set.add("Invalid Item")

    assert str(exc_info.value) == "Item must be of type 'Feature'"


def test_featureset_add_duplicate_item():
    """
    Test if a duplicate item can be added to the CameEntitiesSet.
    """
    feature_set = FeaturesSet()
    entity = Feature("Test")
    feature_set.add(entity)
    feature_set.add(entity)

    assert len(feature_set) == 1


@given(features_list=lists(elements=text(min_size=1), min_size=0))
def test_featureset_from_json(features_list):
    """Test the from_json function with valid input."""
    features_set = FeaturesSet.from_json(features_list)
    assert isinstance(features_set, FeaturesSet)
    assert all(isinstance(feature, Feature) for feature in features_set)

    assert set([feature.name for feature in features_set]) == set(
        features_list
    )  # Don't take in account duplicates and elements order


def test_featureset_from_json_invalid_input_not_list():
    """Test the from_json function with invalid input: not a list."""
    with pytest.raises(TypeError):
        FeaturesSet.from_json("not a list")


@given(features_list=lists(elements=integers(), min_size=1))
def test_featureset_from_json_invalid_input_not_strings(features_list):
    """
    Test the from_json function with invalid input: not a list of strings.
    """
    with pytest.raises(ValueError):
        FeaturesSet.from_json(features_list)


# endregion
