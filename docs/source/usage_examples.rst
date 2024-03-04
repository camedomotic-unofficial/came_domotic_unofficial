Usage examples
==============

This section provides **practical examples** to help you get started with the
CAME Domotic Unofficial library. From initializing the server connection to
managing devices, you'll find examples for each public property and method.

.. note:: 
    The examples assume you have already installed the library and are familiar
    with the basics of Python programming.

Essential imports for working with this library
-----------------------------------------------

To effectively interact with and control your CAME domotic environment using the
``came_domotic_unofficial`` library, certain import directives are necessary at the
beginning of your file. This section outlines the essential imports needed to work with
the ``CameETIDomoServer`` class and various entity types within the library.

Basic import for server interaction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To initiate communication with the CAME ETI/Domo server:

.. code-block:: python

    from came_domotic_unofficial import CameETIDomoServer

This import is fundamental for creating an instance of the server to manage your domotic
devices. Also, the following imports are likely to be needed in most use cases:

.. code-block:: python

    from came_domotic_unofficial.models import EntityType, EntityStatus

Working with lists and generic entities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``get_features()`` and ``get_entities()`` methods return a list of objects of type
``Feature`` and ``CameEntity``, respectively. The ``Feature`` class represents a server
capability, while the ``CameEntity`` class serves as a base class for all the entities
in the CAME domotic system, such as lights, openings, scenarios, etc.

To work with these lists and generic entities, you'll need the following imports:

.. code-block:: python

    from came_domotic_unofficial.models import FeatureSet, Feature, CameEntitySet, CameEntity

Working with specific entities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to the above, depending on the entities you plan to interact with,
also other imports from the ``came_domotic_unofficial.models`` module may be required.

Lights
""""""

For operations related to light entities, such as retrieving their status or controlling
them:

.. code-block:: python

    from came_domotic_unofficial.models import Light, LightType

Openings
""""""""

To manage openings like doors and windows:

.. code-block:: python

    from came_domotic_unofficial.models import Opening, OpeningType

Scenarios
"""""""""

For activating or deactivating scenarios:

.. code-block:: python

    from came_domotic_unofficial.models import Scenario, ScenarioStatus, ScenarioIcon

Digital Inputs
""""""""""""""

When working with digital inputs, such as sensors or switches:

.. code-block:: python

    from came_domotic_unofficial.models import DigitalInput, DigitalInputType

Handling Exceptions
^^^^^^^^^^^^^^^^^^^

To properly handle potential errors and exceptions from the library:

.. code-block:: python

    from came_domotic_unofficial.models import (
        CameDomoticError, # Generic error raised by the library
        CameDomoticServerNotFoundError, # When declaring the server object
        CameDomoticAuthError, # When the authentication fails
        CameDomoticRemoteServerError, # Unexpected error from the server
        CameDomoticRequestError, # Response from the server is not well-formatted
        CameDomoticBadAckError, # Server responded with an error message
    )

Initializing the server
-----------------------

Initialize a ``CameETIDomoServer`` instance to connect to your CAME ETI/Domo server. 
This step verifies the server's **reachability** but **does not** immediately
**validate credentials** or **establish a session**. Sessions are managed internally
and **initiated on-demand**, optimizing resource use and security.

.. code-block:: python

    from came_domotic_unofficial import CameETIDomoServer

    with CameETIDomoServer("192.168.0.0", "username", "password") as server:
        print("The server is reachable, you're ready to go!")

This design allows you to focus on device interaction without any need for manual session
management.

Checking Authentication Status
------------------------------

Should you need for some reason to check the server's authentication status, you can use
the ``is_authenticated`` property of the ``CameETIDomoServer`` instance.

.. code-block:: python

    if server.is_authenticated:
        print("Server session is authenticated and valid.")

Please note that, in general, you don't need to check if the session is authenticated,
as the library will handle this for you, (re)authenticating as needed.

Retrieving server information
-----------------------------

After initializing the ``CameETIDomoServer`` instance, you can access its properties to
obtain various information about the server. Should you need for your code a **unique
ID** for the server, you can use the ``keycode`` property.

Below is how you might print these properties:

.. code-block:: python

    print(f"Keycode: {server.keycode}")
    print(f"Software version: {server.software_version}")
    print(f"Server type: {server.server_type}")
    print(f"Board type: {server.board}")
    print(f"Serial number: {server.serial_number}")

Assuming a successful interaction with the server, the output might look like this:

.. code-block:: text

    Keycode: 0000FFFF9999AAAA
    Software version: 1.2.3
    Server type: 0
    Board type: 3
    Serial number: 0011ffee

Fetching Supported Features
---------------------------

To understand what capabilities your CAME domotic plant offers, you can fetch
a list of all configured features on the ETI/Domo server. These features
represent the functional blocks you would see in the Came Domotic mobile
app's homepage, such as lights, openings, or scenarios.

.. code-block:: python

    features = server.get_features()
    for feature in features:
        print(f"Feature: {feature.name}")

This operation retrieves a ``FeatureSet``, containing multiple ``Feature`` objects. Each
``Feature`` represents a server capability. Below is an example output, showcasing the
server's available features:

.. code-block:: text

    Feature: lights
    Feature: openings
    Feature: thermoregulation
    Feature: scenarios
    Feature: digitalin
    Feature: energy
    Feature: loadsctrl

The `get_features` method checks the server's configuration and returns a set of
features, allowing you to programmatically explore and interact with your domotic
environment. This method makes it easy to align your automation or monitoring tasks with
the **capabilities actually available** in your **specific** CAME domotic setup.


Listing managed entities
------------------------

Interacting with the CAME domotic environment involves listing various entity types
managed by the ETI/Domo server. This section demonstrates how to retrieve and print
details of all managed entities (like lights and openings, each representing components
in your home) by utilizing the generic `get_entities()` method for a comprehensive
overview, and then accessing specific entity types for targeted information.

Retrieving and printing all entity types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fetch every entity type managed by the server using the ``get_entities()`` method
without parameters. This prints a summary of each entity, including its type and status:

.. code-block:: python

    all_entities = server.get_entities()
    for entity in all_entities:
        entity_type = type(entity).__name__
        print(f"Type: {entity_type}, ID: {entity.id}, Name: {entity.name}, "
              f"Status: {entity.status.name}")

This operation retrieves a ``CameEntitySet``, containing multiple ``CameEntity``
objects. Each ``CameEntity`` represents a managed entity in the CAME domotic system.
Below is an example output, showcasing the server's managed entities:

.. code-block:: text

    Type: Light, ID: 1, Name: Kitchen Ceiling Light, Status: ON_OPEN_TRIGGERED
    Type: Opening, ID: 2, Name: Front Entrance Door, Status: CLOSED
    Type: Scenario, ID: 3, Name: Evening Ambiance, Status: NOT_APPLIED
    Type: DigitalInput, ID: 4, Name: Backyard Motion Sensor, Status: UNKNOWN

Specific Entity Types
^^^^^^^^^^^^^^^^^^^^^

Retrieve and list specific types of entities by supplying the appropriate `EntityType`.

Retrieving Lights
"""""""""""""""""

.. code-block:: python

    lights = server.get_entities(EntityType.LIGHTS)
    for light in lights:
        print(f"Type: Light, ID: {light.id}, Name: {light.name}, "
              f"Status: {light.status.name}, Light Type: {light.light_type.name}, "
              f"Brightness: {light.brightness}%")

Example output for lights:

.. code-block:: text

    Type: Light, ID: 1, Name: Living Room Chandelier, Status: ON, Light Type: DIMMABLE, Brightness: 75%
    Type: Light, ID: 2, Name: Hallway Night Light, Status: OFF, Light Type: ON_OFF, Brightness: 100%

Retrieving Openings
"""""""""""""""""""

.. code-block:: python

    openings = server.get_entities(EntityType.OPENINGS)
    for opening in openings:
        print(f"Type: Opening, ID: {opening.id}, Name: {opening.name}, "
              f"Status: {opening.status.name}, Opening Type: {opening.opening_type.name}")

Example output for openings:

.. code-block:: text

    Type: Opening, ID: 1, Name: Kitchen Window, Status: ON_OPEN_TRIGGERED, Opening Type: OPEN_CLOSE
    Type: Opening, ID: 3, Name: Garage Door, Status: CLOSED, Opening Type: OPEN_CLOSE

Retrieving Scenarios
""""""""""""""""""""

.. code-block:: python

    scenarios = server.get_entities(EntityType.SCENARIOS)
    for scenario in scenarios:
        print(f"Type: Scenario, ID: {scenario.id}, Name: {scenario.name}, "
              f"Status: {scenario.scenario_status.name}, Icon: {scenario.icon.name}, "
              f"User Defined: {scenario.is_user_defined}")

Example output for scenarios:

.. code-block:: text

    Type: Scenario, ID: 1, Name: Leave Home, Status: APPLIED, Icon: OPENINGS_CLOSE, User Defined: True
    Type: Scenario, ID: 2, Name: Wake Up, Status: NOT_APPLIED, Icon: LIGHTS, User Defined: False

This examples provide a practical guide for querying and understanding the diverse
entities within your CAME domotic setup, supporting management and automation of your
smart home environment.

Updating an entity's status
---------------------------

Interact with and control your CAME domotic environment by updating the status of
various entities using the ``set_entity_status`` method.

Updating Light status
^^^^^^^^^^^^^^^^^^^^^

Change the status of a light entity, including adjusting brightness for dimmable lights.
Please note that the ``brightness`` parameter is not mandatory: if not provided, the
brightness will remain unchanged.

.. code-block:: python

    # Example 1: Turning off an ON_OFF type light
    kitchen_ceiling_light_id = 1  # Assuming 1 is the ID for the Kitchen Ceiling Light
    success_kitchen = server.set_entity_status(
        Light, 
        kitchen_ceiling_light_id, 
        status=EntityStatus.OFF_STOPPED
    )

    print("Update status for Kitchen Ceiling Light:", "Success" if success_kitchen else "Failed")

    # Example 2: Turning on a dimmable light (Living Room Dimmer) to 70% brightness
    living_room_dimmer_id = 7  # Assuming 7 is the ID for the Living Room Dimmer
    success_living_room = server.set_entity_status(
        Light, 
        living_room_dimmer_id, 
        status=EntityStatus.ON_OPEN_TRIGGERED, 
        brightness=70 # Set brightness to 70%
    )
    print("Update status for Living Room Dimmer:", "Success" if success_living_room else "Failed")

Example output:

.. code-block:: text

    Update status for Kitchen Ceiling Light: Success
    Update status for Living Room Dimmer: Success


Updating Opening status
^^^^^^^^^^^^^^^^^^^^^^^

Modify the status of an opening entity (e.g. roller shutter,  or awning). This example
demonstrates closing the bedroom roller shutter.

.. code-block:: python

    bedroom_roller_shutter_id = 22  # Assuming 22 is the ID for the Living Room Dimmer
    success = server.set_entity_status(
        Opening, 
        bedroom_roller_shutter_id, 
        status=EntityStatus.CLOSED
    )
    print("Update Status:", "Success" if success else "Failed")

Example Output:

.. code-block:: text

    Update Status: Success

Scenario activation
^^^^^^^^^^^^^^^^^^^

Trigger a predefined scenario. This example shows how to activate the "Good night"
scenario.

.. code-block:: python

    goodnight_scenario_id = 5  # Assuming 5 is the ID for the Living Room Dimmer
    success = server.set_entity_status(
        Scenario, 
        goodnight_scenario_id, 
        status=EntityStatus.ON_OPEN_TRIGGERED
    )
    print("Activation Status:", "Triggered" if success else "Failed")

Example Output:

.. code-block:: text

    Activation Status: Triggered
