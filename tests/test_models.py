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

# pylint: disable=too-many-lines
# pylint: disable=missing-function-docstring

"""
Tests for all the CAME Domotic entities.
"""

from datetime import datetime
import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from, lists
from came_domotic_unofficial.models import (
    CameDomoticAuthError,
    CameDomoticBadAckError,
    CameDomoticError,
    CameDomoticRemoteServerError,
    CameDomoticRequestError,
    CameDomoticServerNotFoundError,
    CameEntitiesSet,
    CameEntity,
    DigitalInputType,
    DigitalInput,
    Feature,
    FeaturesSet,
    Light,
    EntityStatus,
    LightType,
    Opening,
    OpeningType,
)

# region Exceptions


def test_came_domotic_error():
    """
    Test if the CameDomoticRemoteServerError can be raised correctly.
    """
    with pytest.raises(CameDomoticError) as exc_info:
        raise CameDomoticError("Test error message")

    assert isinstance(exc_info.value, Exception)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_server_not_found_error():
    """
    Test if the CameDomoticServerNotFoundError can be raised correctly.
    """
    with pytest.raises(CameDomoticServerNotFoundError) as exc_info:
        raise CameDomoticServerNotFoundError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_auth_error():
    """
    Test if the CameDomoticAuthError can be raised correctly.
    """
    with pytest.raises(CameDomoticAuthError) as exc_info:
        raise CameDomoticAuthError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_remote_server_error():
    """
    Test if the CameDomoticRemoteServerError can be raised correctly.
    """
    with pytest.raises(CameDomoticRemoteServerError) as exc_info:
        raise CameDomoticRemoteServerError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_request_error():
    """
    Test if the CameDomoticRequestError can be raised correctly.
    """
    with pytest.raises(CameDomoticRequestError) as exc_info:
        raise CameDomoticRequestError("Test error message")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Test error message"


def test_came_domotic_bad_ack_error():
    """ "
    Test if the CameDomoticBadAckError can be raised correctly with a reason.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError(9, "Session expired.")

    assert isinstance(exc_info.value, CameDomoticError)
    assert str(exc_info.value) == "Bad ack code: 9 - Reason: Session expired."


def test_came_domotic_bad_ack_error_without_reason():
    """
    Test if the CameDomoticBadAckError can be raised without a reason.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError(9)

    assert str(exc_info.value) == "Bad ack code: 9"


def test_came_domotic_bad_ack_error_no_ack_or_wrong():
    """
    Test if the CameDomoticBadAckError can be raised correctly without inputs.
    """
    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError()

    assert str(exc_info.value) == "Bad ack code."

    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError("TEST")

    assert str(exc_info.value) == "Bad ack code: TEST"

    with pytest.raises(CameDomoticBadAckError) as exc_info:
        raise CameDomoticBadAckError("TEST", 9)

    assert str(exc_info.value) == "Bad ack code: TEST - Reason: 9"


# endregion

# region CameEntity


@given(
    input_id=integers(),
    input_name=text(min_size=1),
    input_status=sampled_from(EntityStatus),
)
def test_came_entity_init_complete(input_id, input_name, input_status):
    """
    Test the initialization of the CameEntity class with all the parameters.
    """
    entity = CameEntity(input_id, input_name, status=input_status)

    assert entity.id == input_id
    assert entity.name == input_name
    assert entity.status == input_status


def test_came_entity_init_invalid_id():
    with pytest.raises(TypeError):
        CameEntity("QAW")


def test_came_entity_init_invalid_name():
    with pytest.raises(TypeError):
        CameEntity(1, 2)


def test_came_entity_init_invalid_status():
    with pytest.raises(TypeError):
        CameEntity(1, "Test", status="Not a valid status")


def test_came_entity_init_no_status():
    entity = CameEntity(1, "Test")

    assert entity.id == 1
    assert entity.name == "Test"
    assert entity.status == EntityStatus.UNKNOWN


def test_came_entity_init_no_name():
    entity = CameEntity(1)

    assert entity.id == 1
    assert entity.name == "Unknown"
    assert entity.status == EntityStatus.UNKNOWN


@given(
    new_status=sampled_from(EntityStatus),
)
def test_came_entity_set_status(new_status):
    entity = CameEntity(1)

    entity.status = new_status
    assert entity.status == new_status


def test_came_entity_set_not_valid_status():
    entity = CameEntity(1)

    with pytest.raises(TypeError):
        entity.status = "Not a valid status"

    assert entity.status == EntityStatus.UNKNOWN


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_eq(entity_id, name, status):
    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id, name, status=status)
    came_entity3 = CameEntity(entity_id + 1, name, status=status)
    came_entity4 = CameEntity(entity_id, name + "_", status=status)
    other_type = repr(came_entity1)

    assert came_entity1 == came_entity2
    with pytest.raises(AssertionError):
        assert came_entity1 == came_entity3
    with pytest.raises(AssertionError):
        assert came_entity1 == came_entity4
    assert came_entity1 != other_type


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_ne(entity_id, name, status):
    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id + 1, name, status=status)
    came_entity3 = CameEntity(entity_id, name + "_", status=status)
    came_entity4 = CameEntity(
        entity_id,
        name,
        status=(
            EntityStatus.UNKNOWN
            if status != EntityStatus.UNKNOWN
            else EntityStatus.ON_OPEN
        ),
    )
    came_entity_identical = CameEntity(entity_id, name, status=status)

    assert came_entity1 != came_entity2
    assert came_entity1 != came_entity3
    assert came_entity1 != came_entity4
    with pytest.raises(AssertionError):
        assert came_entity1 != came_entity_identical


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_hash(entity_id, name, status):
    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id, name, status=status)
    came_entity3 = CameEntity(entity_id + 1, name, status=status)
    other_type = repr(came_entity1)

    assert hash(came_entity1) == hash(came_entity2)
    assert hash(came_entity1) != hash(came_entity3)
    assert hash(came_entity1) != hash(other_type)


# endregion

# region CameEntitiesSet


def test_came_entitiesset_initialization():
    """
    Test the initialization of the CameEntitiesSet class.
    """
    entities_set = CameEntitiesSet()

    assert isinstance(entities_set, set)
    assert len(entities_set) == 0


def test_came_entitiesset_initialization_with_items():
    """
    Test the initialization of the CameEntitiesSet class with items.
    """
    entity1 = CameEntity(1, "Test Entity 1")
    entity2 = CameEntity(2, "Test Entity 2")
    entities_set = CameEntitiesSet([entity1, entity2])

    assert entity1 in entities_set
    assert entity2 in entities_set
    assert len(entities_set) == 2


def test_came_entitiesset_eq():
    """
    Test the equality operator for the CameEntitiesSet class.
    """
    entity1 = CameEntity(1, "Test Entity 1")
    entity2 = CameEntity(2, "Test Entity 2")
    entity3 = CameEntity(3, "Test Entity 3")
    entities_set1 = CameEntitiesSet([entity1, entity2])
    entities_set2 = CameEntitiesSet([entity1, entity2])
    entities_set3 = CameEntitiesSet([entity1, entity3])

    assert entities_set1 == entities_set2
    assert entities_set1 != entities_set3


def test_came_entitiesset_add_valid_item():
    """
    Test if a valid item can be added to the CameEntitiesSet.
    """
    entities_set = CameEntitiesSet()
    entity = CameEntity(1, "Test Entity")
    entities_set.add(entity)

    assert entity in entities_set


def test_came_entitiesset_add_invalid_item():
    """
    Test if an invalid item cannot be added to the CameEntitiesSet.
    """
    entities_set = CameEntitiesSet()

    with pytest.raises(TypeError) as exc_info:
        entities_set.add("Invalid Item")

    assert str(exc_info.value) == "Item must be of type 'CameEntity'"


def test_came_entitiesset_add_duplicate_item():
    """
    Test if a duplicate item can be added to the CameEntitiesSet.
    """
    entities_set = CameEntitiesSet()
    entity = CameEntity(1, "Test Entity")
    entities_set.add(entity)
    entities_set.add(entity)

    assert len(entities_set) == 1


# endregion

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

    assert isinstance(feature_set, CameEntitiesSet)
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
    features_set1 = CameEntitiesSet([feature1, feature2])
    features_set2 = CameEntitiesSet([feature1, feature2])
    features_set3 = CameEntitiesSet([feature1, feature3])

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

# region Light


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    light_type=sampled_from(LightType),
    brightness=integers(),
)
def test_light_constructor(entity_id, name, status, light_type, brightness):
    """
    Test if the Light constructor works correctly.
    """
    light = Light(
        entity_id,
        name,
        status=status,
        light_type=light_type,
        brightness=brightness,
    )

    assert isinstance(light, CameEntity)
    assert light.id == entity_id
    assert light.name == name
    assert light.status == status
    assert light.light_type == light_type
    assert light.brightness == min(max(0, brightness), 100)


def test_light_constructor_defaults():
    """
    Test if the Light constructor works correctly with default values.
    """
    light = Light(1)

    assert light.id == 1
    assert light.name == "Unknown"
    assert light.status == EntityStatus.UNKNOWN
    assert light.light_type == LightType.ON_OFF
    assert light.brightness == 100


def test_light_constructor_invalid_light_type():
    """
    Test if the Light constructor raises an error with an invalid light type.
    """
    with pytest.raises(TypeError) as exc_info:
        Light(1, "Test Light", light_type="Not a valid light type")

    assert str(exc_info.value) == "The light type must be a valid LightType"


def test_light_constructor_invalid_brightness():
    """
    Test if the Light constructor raises an error with an invalid brightness.
    """
    with pytest.raises(TypeError) as exc_info:
        Light(1, "Test Light", brightness="Invalid brightness")

    assert str(exc_info.value) == "The brightness value must be an integer"


def test_light_brightness_property():
    """
    Test if the Light brightness property works correctly.
    """
    light = Light(1, brightness=50)

    with pytest.raises(ValueError):
        light.brightness = -1

    with pytest.raises(ValueError):
        light.brightness = 101

    light.brightness = 0
    assert light.brightness == 0

    light.brightness = 100
    assert light.brightness == 100


def test_light_str_method():
    """
    Test if the Light __str__ method works correctly.
    """
    light = Light(
        1,
        "Test Light",
        status=EntityStatus.ON_OPEN,
        light_type=LightType.DIMMABLE,
        brightness=50,
    )

    assert str(light) == (
        "Light #1: Test Light - Type: (DIMMABLE) - "
        "Status: ON_OPEN - Brightness: 50"
    )


def test_light_repr_method():
    """
    Test if the Light __repr__ method works correctly.
    """
    light = Light(
        1,
        "Test Light",
        status=EntityStatus.ON_OPEN,
        light_type=LightType.DIMMABLE,
        brightness=50,
    )

    assert repr(light) == (
        'Light(1,"Test Light",status=EntityStatus.ON_OPEN,'
        "light_type=LightType.DIMMABLE,brightness=50)"
    )


def test_light_equality_hash_operators():
    """
    Test if the Light equality and hash operators work correctly.
    """
    light_name = "Test light"
    light1 = Light(1, light_name)
    light2 = Light(1, light_name)
    light3 = Light(1, light_name, status=EntityStatus.UNKNOWN)
    light4 = Light(2, light_name, status=EntityStatus.UNKNOWN)
    light5 = Light(1, light_name + "_", status=EntityStatus.UNKNOWN)
    light6 = Light(1, light_name, status=EntityStatus.ON_OPEN)
    other_type1 = CameEntity(1, light_name, status=EntityStatus.UNKNOWN)
    other_type2 = repr(light1)
    other_type3 = light_name

    assert light1 == light2
    assert light1 == light3
    assert light1 != light4
    assert light1 != light5
    assert light1 != light6
    assert light1 != other_type1
    assert light1 != other_type2
    assert light1 != other_type3
    assert hash(light1) == hash(light2)
    assert hash(light1) == hash(light3)
    assert hash(light1) != hash(light4)
    assert hash(light1) != hash(light5)
    assert hash(light1) != hash(light6)
    assert hash(light1) != hash(other_type1)
    assert hash(light1) != hash(other_type2)
    assert hash(light1) != hash(other_type3)


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=integers(min_value=0, max_value=2),
    light_type=sampled_from(["STEP_STEP", "DIMMER"]),
    brightness=integers(min_value=0, max_value=100),
)
def test_light_from_json_method(
    entity_id, name, status, light_type, brightness
):
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": entity_id,
        "name": name,
        "status": status,
        "type": light_type,
        "perc": brightness,
    }
    light = Light.from_json(json_data)

    assert light.id == entity_id
    assert light.name == name
    assert light.status == EntityStatus(status)

    assert light.light_type == LightType(light_type)
    assert light.brightness == brightness


def test_light_from_json_method_defaults():
    """
    Test if the Light from_json method works correctly when optional keys
    are missing.
    """

    json_data = {
        "act_id": 1,
    }
    light = Light.from_json(json_data)
    check_light = Light(1)

    assert light == check_light


def test_light_from_json_method_missing_required_keys():
    """
    Test if the Light from_json method raises an exception when the id
    is missing.
    """

    json_data = {
        "name": "Test",
        "status": 0,
        "type": "DIMMER",
        "perc": 100,
    }
    with pytest.raises(KeyError):
        Light.from_json(json_data)


@given(
    status=integers(min_value=100),
    light_type=text(min_size=1),
)
def test_light_from_json_unknown_status_and_light_type(status, light_type):
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": 1,
        "name": "Test",
        "status": status,
        "type": light_type,
    }
    light = Light.from_json(json_data)
    check_light = Light(1, "Test")

    assert light == check_light


def test_light_from_json_invalid_values():
    """
    Test if the Light from_json method raises an exception when the JSON
    data contains invalid values.
    """

    json_data = {
        "act_id": 1,  # Should be an integer
        "name": "Test",
        "status": "unexpected",  # Should be an EntityStatus value
        "type": "invalid",  # Should be a LightType value
        "perc": "unexpected",  # Should be an integer
    }
    light = Light.from_json(json_data)
    check_light = Light(1, "Test")

    assert light == check_light


def test_light_from_json_out_of_range_brightness():
    """
    Test if the Light from_json method works correctly.
    """

    json_data1 = {
        "act_id": 1,
        "type": "DIMMER",
        "perc": -1,
    }
    json_data2 = {
        "act_id": 1,
        "type": "DIMMER",
        "perc": 101,
    }
    light1 = Light.from_json(json_data1)
    light2 = Light.from_json(json_data2)

    assert light1.brightness == 0
    assert light2.brightness == 100


def test_light_from_json_method_unexpected_properties():
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": 1,
        "name": "Test",
        "status": 0,
        "type": "DIMMER",
        "perc": 50,
        "my_unexpected_key": "unexpected",
    }
    light = Light.from_json(json_data)
    check_light = Light(
        1,
        "Test",
        status=EntityStatus(0),
        light_type=LightType("DIMMER"),
        brightness=50,
    )

    assert light == check_light


# endregion

# region Opening


@given(
    entity_id=integers(min_value=1),
    close_entity_id=integers(min_value=1),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    opening_type=sampled_from(OpeningType),
)
def test_opening_constructor(
    entity_id, close_entity_id, name, status, opening_type
):
    """
    Test if the Opening constructor works correctly.
    """
    opening = Opening(
        entity_id,
        close_entity_id=close_entity_id,
        name=name,
        status=status,
        opening_type=opening_type,
    )
    assert isinstance(opening, CameEntity)
    assert opening.id == entity_id
    assert opening.close_entity_id == close_entity_id
    assert opening.name == name
    assert opening.status == status
    assert opening.opening_type == opening_type
    assert not opening.partial_openings


@given(
    entity_id=integers(min_value=1),
)
def test_opening_init_defaults(entity_id):
    """
    Test if the Opening constructor works correctly with default values.
    """
    opening = Opening(entity_id)
    assert opening.id == entity_id
    assert opening.close_entity_id == opening.id
    assert opening.name == "Unknown"
    assert opening.status == EntityStatus.UNKNOWN
    assert opening.opening_type == OpeningType.OPEN_CLOSE
    assert not opening.partial_openings


def test_opening_init_invalid_close_entity_id():
    """
    Test if the Opening constructor raises an error with an invalid
    close entity id.
    """
    with pytest.raises(TypeError):
        Opening(1, close_entity_id="invalid")


def test_opening_init_invalid_opening_type():
    """
    Test if the Opening constructor raises an error with an invalid
    opening type.
    """
    with pytest.raises(TypeError):
        Opening(1, opening_type="invalid")


def test_opening_init_invalid_partial_openings():
    """
    Test if the Opening constructor raises an error with
    an invalid partial openings.
    """
    with pytest.raises(TypeError):
        Opening(1, partial_openings="invalid")


def test_opening_str_method():
    """
    Test if the Opening __str__ method works correctly.
    """
    opening = Opening(
        1,
        "Test Opening",
        close_entity_id=2,
        status=EntityStatus.ON_OPEN,
        opening_type=OpeningType.OPEN_CLOSE,
    )

    assert str(opening) == (
        'Opening #1/2: "Test Opening" - Type: OPEN_CLOSE - '
        "Status: ON_OPEN - Partials: []"
    )


def test_opening_repr_method():
    """
    Test if the Opening __repr__ method works correctly.
    """
    opening = Opening(
        1,
        "Test Opening",
        close_entity_id=2,
        status=EntityStatus.ON_OPEN,
        opening_type=OpeningType.OPEN_CLOSE,
    )

    assert repr(opening) == (
        'Opening(1,2,"Test Opening",status=EntityStatus.ON_OPEN,'
        "opening_type=OpeningType.OPEN_CLOSE,partial_openings=[])"
    )


def test_opening_equality_hash_operators():
    """
    Test if the Opening equality and hash operators work correctly.
    """
    opening_name = "Test"
    opening1 = Opening(1, opening_name)
    opening2 = Opening(1, opening_name)
    opening3 = Opening(
        1,
        opening_name,
        close_entity_id=1,
        opening_type=OpeningType.OPEN_CLOSE,
        status=EntityStatus.UNKNOWN,
    )
    opening4 = Opening(2, opening_name)
    opening5 = Opening(1, opening_name + "_")
    opening6 = Opening(1, opening_name, status=EntityStatus.ON_OPEN)
    other_type1 = CameEntity(1, opening_name, status=EntityStatus.UNKNOWN)
    other_type2 = repr(opening1)
    other_type3 = opening_name

    assert opening1 == opening2
    assert opening1 == opening3
    assert opening1 != opening4
    assert opening1 != opening5
    assert opening1 != opening6
    assert opening1 != other_type1
    assert opening1 != other_type2
    assert opening1 != other_type3

    assert hash(opening1) == hash(opening2)
    assert hash(opening1) == hash(opening3)
    assert hash(opening1) != hash(opening4)
    assert hash(opening1) != hash(opening5)
    assert hash(opening1) != hash(opening6)
    assert hash(opening1) != hash(other_type1)
    assert hash(opening1) != hash(other_type2)
    assert hash(opening1) != hash(other_type3)


@given(
    entity_id=integers(min_value=1),
    close_entity_id=integers(min_value=1),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    opening_type=sampled_from(OpeningType),
)
def test_opening_from_json(
    entity_id, close_entity_id, name, status, opening_type
):
    """
    Test if the Opening from_json method works correctly.
    """
    json_data = {
        "open_act_id": entity_id,
        "close_act_id": close_entity_id,
        "name": name,
        "status": status.value,
        "partial": [],
        "type": opening_type.value,
    }
    opening = Opening.from_json(json_data)
    assert opening.id == entity_id
    assert opening.close_entity_id == close_entity_id
    assert opening.name == name
    assert opening.status == status
    assert opening.opening_type == opening_type
    assert not opening.partial_openings


@given(
    entity_id=integers(min_value=1),
)
def test_opening_from_json_defaults(entity_id):
    """
    Test if the Opening from_json method works correctly when optional keys
    """
    json_data = {
        "open_act_id": entity_id,
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(entity_id)

    assert opening == check_opening


def test_opening_from_json_invalid_values():
    """
    Test if the Opening from_json method raises an exception when the JSON
    """
    json_data = {
        "open_act_id": 1,
        "close_act_id": 2,
        "name": "Test",
        "status": "Invalid",
        "partial": [],
        "type": "Invalid",
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(1, "Test", close_entity_id=2)

    assert opening == check_opening


def test_opening_from_json_missing_required_keys():
    """
    Test if the Opening from_json method raises an exception when the JSON
    """
    json_data = {
        "close_act_id": 2,
        "name": "Test",
        "status": 0,
        "partial": [],
        "type": 0,
    }
    with pytest.raises(KeyError):
        Opening.from_json(json_data)


def test_opening_from_json_unexpected_properties():
    """Test if the Opening from_json method works correctly."""
    json_data = {
        "open_act_id": 1,
        "close_act_id": 2,
        "name": "Test",
        "status": 0,
        "partial": [],
        "type": 0,
        "unexpected": "unexpected",
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(
        1,
        "Test",
        close_entity_id=2,
        status=EntityStatus(0),
        partial_openings=[],
        opening_type=OpeningType(0),
    )

    assert opening == check_opening


# endregion

# region DigitalInput


@given(
    entity_id=integers(min_value=1),
    name=text(min_size=1),
    button_type=sampled_from(DigitalInputType),
    address=integers(),
    ack_code=integers(),
    radio_node_id=text(min_size=1),
    rf_radio_link_quality=integers(),
    utc_time=integers(min_value=0, max_value=int(datetime.now().timestamp())),
)
def test_digital_input_init(
    entity_id,
    name,
    button_type,
    address,
    ack_code,
    radio_node_id,
    rf_radio_link_quality,
    utc_time,
):
    """
    Test if the DigitalInput constructor works correctly.
    """
    digital_input = DigitalInput(
        entity_id,
        name,
        button_type=button_type,
        address=address,
        ack_code=ack_code,
        radio_node_id=radio_node_id,
        rf_radio_link_quality=rf_radio_link_quality,
        utc_time=utc_time,
    )

    assert isinstance(digital_input, CameEntity)
    assert digital_input.id == entity_id
    assert digital_input.name == name
    assert digital_input.button_type == button_type
    assert digital_input.address == address
    assert digital_input.ack_code == ack_code
    assert digital_input.radio_node_id == radio_node_id
    assert digital_input.rf_radio_link_quality == rf_radio_link_quality
    assert digital_input.last_pressed == datetime.fromtimestamp(utc_time)
    assert digital_input.status == EntityStatus.NOT_APPLICABLE


def test_digital_input_init_defaults():
    """
    Test if the DigitalInput constructor works correctly with default values.
    """
    digital_input = DigitalInput(1)

    assert digital_input.id == 1
    assert digital_input.name == "Unknown"
    assert digital_input.button_type == DigitalInputType.BUTTON
    assert digital_input.address == 0
    assert digital_input.ack_code == 1
    assert digital_input.radio_node_id == "00000000"
    assert digital_input.rf_radio_link_quality == 0
    assert digital_input.last_pressed == datetime.fromtimestamp(0)
    assert digital_input.status == EntityStatus.NOT_APPLICABLE


def tests_digital_input_init_invalid_button_type():
    """
    Test if the DigitalInput constructor raises an error with an invalid button
    """
    with pytest.raises(TypeError):
        DigitalInput(1, button_type="Invalid")


def test_digital_input_init_invalid_address():
    """
    Test if the DigitalInput constructor raises an error
    with an invalid address
    """
    with pytest.raises(TypeError):
        DigitalInput(1, address="Invalid")


def test_digital_input_init_invalid_ack_code():
    """
    Test if the DigitalInput constructor raises an error with an invalid ack
    """
    with pytest.raises(TypeError):
        DigitalInput(1, ack_code="Invalid")


def test_digital_input_init_invalid_radio_node_id():
    """
    Test if the DigitalInput constructor raises an error with an invalid radio
    """
    with pytest.raises(TypeError):
        DigitalInput(1, radio_node_id=1)


def test_digital_input_init_invalid_rf_radio_link_quality():
    """
    Test if the DigitalInput constructor raises an error with an invalid RF
    """
    with pytest.raises(TypeError):
        DigitalInput(1, rf_radio_link_quality="Invalid")


def test_digital_input_init_invalid_utc_time():
    """
    Test if the DigitalInput constructor raises an error with an invalid UTC
    """
    with pytest.raises(TypeError):
        DigitalInput(1, utc_time="Invalid")


def test_digital_input_str_method():
    """
    Test if the DigitalInput __str__ method works correctly.
    """
    digital_input = DigitalInput(
        1,
        "Test Digital Input",
        button_type=DigitalInputType.BUTTON,
        address=2,
        ack_code=3,
        radio_node_id="Test",
        rf_radio_link_quality=4,
        utc_time=5,
    )
    assert str(digital_input) == (
        'DigitalInput #1: "Test Digital Input" - Type: BUTTON - '
        'Address: 2 - Ack code: 3 - Radio node ID: "Test" - '
        "RF radio link quality: 4 - Last pressed: "
        f"{datetime.fromtimestamp(5)}"
    )


def test_digital_input_repr_method():
    """
    Test if the DigitalInput __repr__ method works correctly.
    """
    digital_input = DigitalInput(
        1,
        "Test Digital Input",
        button_type=DigitalInputType.BUTTON,
        address=2,
        ack_code=3,
        radio_node_id="Test",
        rf_radio_link_quality=4,
        utc_time=5,
    )
    assert repr(digital_input) == (
        'DigitalInput(1,"Test Digital Input",'
        "button_type=DigitalInputType.BUTTON,address=2,ack_code=3,"
        'radio_node_id="Test",rf_radio_link_quality=4,utc_time=5)'
    )


def test_digitalinput_equality_hash_operators():
    """
    Test if the DigitalInput equality and hash operators work correctly.
    """
    entity_name = "Test"
    entity1 = DigitalInput(1, entity_name)
    entity2 = DigitalInput(1, entity_name)
    entity3 = DigitalInput(1, entity_name, address=0)
    entity4 = DigitalInput(2, entity_name)
    entity5 = DigitalInput(1, entity_name + "_")
    entity6 = DigitalInput(1, entity_name, address=1)
    other_type1 = CameEntity(
        1, entity_name, status=EntityStatus.NOT_APPLICABLE
    )
    other_type2 = repr(entity1)
    other_type3 = entity_name

    assert entity1 == entity2
    assert entity1 == entity3
    assert entity1 != entity4
    assert entity1 != entity5
    assert entity1 != entity6
    assert entity1 != other_type1
    assert entity1 != other_type2
    assert entity1 != other_type3

    assert hash(entity1) == hash(entity2)
    assert hash(entity1) == hash(entity3)
    assert hash(entity1) != hash(entity4)
    assert hash(entity1) != hash(entity5)
    assert hash(entity1) != hash(entity6)
    assert hash(entity1) != hash(other_type1)
    assert hash(entity1) != hash(other_type2)
    assert hash(entity1) != hash(other_type3)


def test_digital_input_from_json():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "name": "Test",
        "act_id": 11,
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
    }
    digital_input = DigitalInput.from_json(json_data)

    assert digital_input.id == 11
    assert digital_input.name == "Test"
    assert digital_input.button_type == DigitalInputType(1)
    assert digital_input.address == 0
    assert digital_input.ack_code == 1
    assert digital_input.radio_node_id == "00000000"
    assert digital_input.rf_radio_link_quality == 0
    assert digital_input.last_pressed == datetime.fromtimestamp(0)


def test_digital_input_from_json_defaults():
    """
    Test if the DigitalInput from_json method works correctly when
    optional keys are missing.
    """
    json_data = {
        "act_id": 1,
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(1)

    assert digital_input == check


def test_digital_input_from_json_invalid_values():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "act_id": 1,
        "name": "Test",
        "type": "Invalid",
        "addr": "Invalid",
        "ack": "Invalid",
        "radio_node_id": 1,
        "rf_radio_link_quality": "Invalid",
        "utc_time": "Invalid",
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(1, "Test")

    assert digital_input == check


def test_digital_input_from_json_missing_required_keys():
    """
    Test if the DigitalInput from_json method raises an exception when the id
    is missing.
    """

    json_data = {
        "name": "Test",
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
    }
    with pytest.raises(KeyError):
        DigitalInput.from_json(json_data)


def test_digital_input_from_json_unexpected_properties():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "act_id": 1,
        "name": "Test",
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
        "unexpected": "unexpected",
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(
        1,
        "Test",
        button_type=DigitalInputType(1),
        address=0,
        ack_code=1,
        radio_node_id="00000000",
        rf_radio_link_quality=0,
        utc_time=0,
    )

    assert digital_input == check


# endregion
