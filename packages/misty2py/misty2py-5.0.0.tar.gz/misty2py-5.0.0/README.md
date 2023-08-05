# Misty2py

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/ChrisScarred/misty2py/blob/main/LICENSE)

Misty2py is a Python 3 package for Misty II development using [Misty's REST API](https://docs.mistyrobotics.com/misty-ii/rest-api/api-reference/ "Misty Robotics REST API").

Read the full documentation [here](https://chrisscarred.github.io/misty2py)!

## Installation

### Poetry

To install misty2py, run `pip install misty2py`.

### From source

- If this is your first time using `misty2py` from source, do following:

  - Get Poetry (`python -m pip install poetry`) if you do not have it yet.
  - Copy `.env.example` to `.env`.
  - Replace the placeholder values in the new `.env` file.
  - Run `poetry install` to obtain all dependencies.

- Run the desired script via `poetry run python -m [name]` where `[name]` is the placeholder for the module location (in Python notation).
- If the scripts run but your Misty does not seem to respond, you have most likely provided an incorrect IP address for `MISTY_IP_ADDRESS` in `.env`.
- Pytests can be run via `poetry run pytest .`.
- The coverage report can be obtained via `poetry run pytest --cov-report html --cov=misty2py tests` for HTML output or via `poetry run pytest --cov=misty2py tests` for terminal output.

## Features

Misty2py can be used to develop complex skills (behaviours) for the Misty II robot utilising:

- **actions** via sending a `POST` or `DELETE` requests to Misty's API;
- **informations** via sending a `GET` request to Misty's API;
- **continuous streams of data** via subscribing to event types on Misty's websockets.

Misty2py uses following concepts for easy of usage:

- **action keywords** - customisable python-styled keywords for endpoints of Misty's API that correspond to performing actions;
- **information keywords** - customisable python-styled keywords for endpoints of Misty's API that correspond to retrieving information;
- **data shortcuts** - customisable python-styled keywords for commonly used data that are supplied to Misty's API as the body of a `POST` request.

## Usage

### Getting started

The main object of this package is `Misty`, which is an abstract representation of Misty the robot. To initialise this object, it is required to know the IP address of the Misty robot that should be used.

The most direct way to initialise a `Misty` object is to use the IP address directly, which allows the user to get the object in one step via:

``` python
from misty2py.robot import Misty

my_misty = Misty("192.168.0.1")  #example IP address
```

This may be impractical and potentially even unsafe, so it is recommended to create a .env file in the project's directory, specify the IP address there via `MISTY_IP_ADDRESS="[ip_address_here]"` and use Misty2py's `EnvLoader` to load the IP address via:


``` python
from misty2py.robot import Misty
from misty2py.utils.env_loader import EnvLoader

env_loader = EnvLoader()
my_misty = Misty(env_loader.get_ip())
```

Assuming a `Misty` object called `my_misty` was obtained, all required actions can be performed via the following three methods:

``` python
# Performing an action (a POST or DELETE request):
my_misty.perform_action("<action_keyword>")

# Obtaining information (a GET request):
my_misty.get_info("<information_keyword>")

# Event related methods 
# (subscribing to an event, getting event data
# or event log and unsubscribing from an event):
my_misty.event("<parameter>")
```

### Responses

Any action performed via Misty2py which contains communication with Misty's APIs returns the `Misty2pyResponse` object. `Misty2pyResponse` is a uniform representation of two sub-responses that are present in any HTTP or WebSocket communication with Misty's APIs using Misty2py. The first sub-response is always from Misty2py and is represented by the attributes `Misty2pyResponse.misty2py_status` (`True` if no Misty2py-related errors were encountered) and potentially empty `Misty2pyResponse.error_msg` and `Misty2pyResponse.error_type` that contain error information if a Misty2py-related error was encountered. The other sub-response is either from Misty's REST API or Misty's WebSocket API. In the first case, it is represented by the attribute `Misty2pyResponse.rest_response` (Dict), and in the second case, it is represented by the attribute `Misty2pyResponse.ws_response`. One of these is always empty, because no action in Misty2py includes simultaneous communication with both APIs. For convenience, a `Misty2pyResponse` object can be easily parsed to a dictionary via the method `Misty2pyResponse.parse_to_dict`.

### Obtaining information

Obtaining digital information is handled by `misty2py.robot::get_info` method which has two arguments. The argument `info_name` is required and it specifies the string information keyword corresponding to an endpoint in Misty's REST API. The argument `params` is optional and it supplies a dictionary of parameter name and parameter value pairs. This argument defaults to `{}` (an empty dictionary).

### Performing actions

Performing physical and digital actions including removal of non-system files is handled by `misty2py.robot::perform_action()` method which takes two arguments. The argument `action_name` is required and it specifies the string action keyword corresponding to an endpoint in Misty’s REST API. The second argument, `data`, is optional and it specifies the data to pass to the request as a dictionary or a data shortcut (string). The `data` argument defaults to `{}` (an empty dictionary).

### Event types

Misty's WebSocket API follows PUB-SUB architecture, which means that in order to obtain event data in Misty's framework, it is required to **subscribe** to an event type on Misty's WebSocket API. The WebSocket server then streams data to the WebSocket client, which receives it a separate thread. To **access the data,** `misty2py.robot::event` method must be called with `"get_data"` parameter from the main thread. When the data are no longer required to be streamed to the client, an event type can be **unsubscribed** which both kills the event thread and stops the API from sending more data.

**Subscribing** to an event is done via `misty2py.robot::event` with the parameter `"subscribe"` and following keyword arguments:

- `type` - *required;* event type string as documented in [Event Types Docs](https://docs.mistyrobotics.com/misty-ii/robot/sensor-data/ "Misty Robotics Event Types").
- `name` - *optional;* a custom event name string; must be unique.
- `return_property` - *optional;* the property to return from Misty's websockets; all properties are returned if return_property is not supplied.
- `debounce` - *optional;* the interval in ms at which new information is sent; defaults to `250`.
- `len_data_entries` - *optional;* the maximum number of data entries to keep (discards in fifo style); defaults to `10`.
- `event_emitter` - *optional;* an event emitter function which emits an event upon message recieval. Supplies the message content as an argument.

**Accessing the data** of an event or its log is done via `misty2py.robot::event` with the parameter `"get_data"` or `"get_log"` and a keyword argument `name` (the name of the event).

**Unsubscribing** from an event is done via `misty2py.robot::event` with the parameter `"unsubscribe"` and a keyword argument `name` (the name of the event).

A bare-bones implementation of event subscription can be seen below.

```python
import time

from misty2py.robot import Misty
from misty2py.utils.env_loader import EnvLoader

env_loader = EnvLoader

m = Misty(env_loader.get_ip())

d = m.event("subscribe", type = "BatteryCharge")
e_name = d.get("event_name")

time.sleep(1)

d = m.event("get_data", name = e_name)

d = m.event("unsubscribe", name = e_name)
```

The following example shows a more realistic scenario which includes an event emitter and an event listener.

```python
import time
from pymitter import EventEmitter

from misty2py.robot import Misty
from misty2py.utils.env_loader import EnvLoader

env_loader = EnvLoader

m = Misty(env_loader.get_ip())
ee = EventEmitter()
event_name = "myevent_001"

@ee.on(event_name)
def listener(data):
    print(data)

d = m.event("subscribe", type = "BatteryCharge", 
            name = event_name, event_emitter = ee)

time.sleep(2)

d = m.event("unsubscribe", name = event_name)
```

### Adding custom keywords and shortcuts

Custom keywords and shortcuts can be passed to a Misty object while declaring a new instance by using the optional arguments `custom_info`, `custom_actions` and `custom_data`. 

The argument `custom_info` can be used to pass custom information keywords as a dictionary with keys being the information keywords and values being the endpoints. An information keyword can only be used for a `GET` method supporting endpoint.

The argument `custom_actions` can be used to pass custom action keywords as a dictionary with keys being the action keywords and values being a dictionary of an `"endpoint"` key (str) and a `"method"` key (str). The `"method"` values must be one of `post`, `delete`, `put`, `head`, `options` and `patch`. However, it should be noted that Misty's REST API currently only has `GET`, `POST` and `DELETE` methods. The rest of the methods was implement in Misty2py for forwards-compatibility.

The argument `custom_data` can be used to pass custom data shortcuts as a dictionary with keys being the data shortcuts and values being the dictionary of data values.

For futher illustration, an example of passing custom keywords and shortcuts can be seen below.

```python
custom_allowed_infos = {
    "hazards_settings": "api/hazards/settings"
}

custom_allowed_data = {
    "amazement": {
        "FileName": "s_Amazement.wav"
    },
    "red": {
        "red": "255",
        "green": "0",
        "blue": "0"
    }
}

custom_allowed_actions = {
    "audio_play" : {
        "endpoint" : "api/audio/play",
        "method" : "post"
    },
    "delete_audio" : {
        "endpoint" : "api/audio",
        "method" : "delete"
    }
}

misty_robot = Misty("0.0.0.0", 
    custom_info=custom_allowed_infos, 
    custom_actions=custom_allowed_actions, 
    custom_data=custom_allowed_data)
```