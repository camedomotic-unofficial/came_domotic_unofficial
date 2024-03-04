Getting started
====================================================

This guide will walk you through the steps to quickly start using the CAME Domotic
Unofficial library in your projects.

Prerequisites
-------------

Before you begin, ensure you have:

- Python 3.6 or newer installed on your system.
- Access to a CAME ETI/Domo server.

Installation
------------

Install the library using `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: bash

    pip install came-domotic-unofficial

This command installs the latest version of the CAME Domotic Unofficial library and its
dependencies.

Quick Start
-----------

Here's a simple example to demonstrate how to use the library to interact with your
CAME ETI/Domo server.

Let's say that you want to turn on a light connected to your server. Here's how you can
do it using the library in a few lines:

.. code-block:: python

    from came_domotic_unofficial import CameETIDomoServer, EntityType, EntityStatus

    with CameETIDomoServer("192.168.0.0", "username", "password") as server:

        lights = server.get_entities(EntityType.LIGHT)

        bedroom_light = next((light for light in lights if light.name == "My bedroom lamp"), None)

        if bedroom_light:
            server.set_entity_status(Light, bedroom_light.id, EntityStatus.ON_OPEN_TRIGGERED)
            print("Bedroom light turned on.")
        else:
            print("Bedroom light not found.")
           
Or, if you already know the entity ID (e.g. 12), you can write directly:

.. code-block:: python

    from came_domotic_unofficial import CameETIDomoServer, EntityType, EntityStatus

    with CameETIDomoServer("192.168.0.0", "username", "password") as server:

        server.set_entity_status(Light, 12, EntityStatus.ON_OPEN_TRIGGERED)


Let's go step by step:

1. **Creating a Server Instance**:

    First, import the `CameETIDomoServer` class from the library and initialize it with
    the server's IP address, username, and password.

    .. code-block:: python

        from came_domotic_unofficial import CameETIDomoServer
        from came_domotic_unofficial.models import EntityStatus, EntityType

        with CameETIDomoServer("192.168.0.0", "username", "password") as server:
            print("Server initialized successfully.")

    This command will raise a ``CameDomoticServerNotFoundError`` exception if the server
    is not found.

2. **Fetching Server Features**:

    You can retrieve a list of all the features supported by the server using the
    `get_features` method.

    .. code-block:: python

        features = server.get_features()
        print("Supported features:", features)

    The output will look like this:

    .. code-block:: output

        Supported features: {
            Feature("lights"),
            Feature("digitalin"),
            Feature("scenarios"),
            Feature("openings"),
            Feature("loadsctrl"),
            Feature("energy"),
            Feature("thermoregulation")
        }
   
    Since this is the first actual call to the server, the library will authenticate
    now, using the provided credentials: if those are not valid, a
    ``CameDomoticAuthError`` exception will be raised.

3.  **Managing Entities**:

    Fetch the list of all the 'entities' (i.e. devices) configured on the CAME server
    by using the `get_entities` method.

    .. code-block:: python
     
        entities = server.get_entities()
        print("Entities:", entities)  # The list may be very long!

    This is an example of output:

    .. code-block:: output

        Entities: [
            {"type": "Light", "id": 1, "name": "My light 1", "status": "ON_OPEN_TRIGGERED", "light_type": "ON_OFF"},
            {"type": "Light", "id": 3, "name": "My light 3", "status": "OFF_STOPPED", "light_type": "ON_OFF"},
            {"type": "Light", "id": 4, "name": "My light 4", "status": "OFF_STOPPED", "light_type": "DIMMABLE", "brightness": 52},
            ...
            {"type": "Opening", "id": 22, "name": "My opening", "close_entity_id": 1, "status": "OFF_STOPPED", "opening_type": "OPEN_CLOSE", "partial_openings": []}
            ...
            {"type": "Scenario", "id": 7, "name": "Switch off all the lights", "status": "OFF_STOPPED", "scenario_status": "NOT_APPLIED", "icon": "LIGHTS", "is_user_defined": false},
            ...
            {"type": "DigitalInput", "id": 1, "name": "My button 1", "button_type": "BUTTON", "address": 201, "ack_code": 0, "radio_node_id": "00000000", "rf_radio_link_quality": 0, "utc_time": 1708366780},
            ...
        ]


    You can also retrieve a filtered list based on a specific entity type.

    .. code-block:: python

        lights = server.get_entities(EntityType.LIGHT)
        print("Lights:", lights)
         
    Change the status of an entity using the `set_entity_status` method.

    .. code-block:: python

        bedroom_light = next((light for light in lights if light.name == "My bedroom lamp"), None)
        if bedroom_light:
            if server.set_entity_status(Light, bedroom_light.id, EntityStatus.ON_OPEN_TRIGGERED)
                print("Bedroom light turned on.")
            else:
                print("Bedroom light not found.")

    Or, if you already know the ID of the light (e.g. 12):

    .. code-block:: python

        successful = server.set_entity_status(Light, 12, EntityStatus.ON_OPEN_TRIGGERED)
        if successful: 
            print("Bedroom light turned on.")
        else:
            print("Bedroom light not found.")

Congratulations! You've successfully used the CAME Domotic Unofficial library to
interact with your CAME ETI/Domo server.

Exploring Further
-----------------

- For more detailed examples, including how to manage lights, openings, scenarios, 
  and more, see the :doc:`usage_examples` section.
- To learn about the functionalities provided by the library and how to use them, visit
  the :doc:`api_reference`.

Contributing
------------

We welcome contributions to improve the library. Whether it's adding new features,
fixing bugs, or improving documentation, your help is appreciated. Check our
:doc:`contributing` section for more information on how to contribute.

Thank you for choosing the CAME Domotic Unofficial library. Happy automating!

