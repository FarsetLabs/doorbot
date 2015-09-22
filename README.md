# Doorbot

==========================

Doorbot Package for Farset Labs

## Package

Basic structure of package is

```
--- doorbot
  \ doorbot.py
  \ version.py
  \ interfaces.py
  \ jsonify.py
  \ views.py
--- tests
  \ tests_helper.py
  --- unit    # Unit Tests
  --- helpers # Test Helpers
\ Doorbot.apache.conf
\ doorbot.wsgi
\ requirements.txt
\ setup.py
```

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Setup

Doorbot is designed to be setup under `/opt/`, where `Doorbot.apache.conf` is copied into the Apache `sites-available` directory (usually `/etc/apache2/sites-available`)

Then, enable the site with `sudo a2ensite Doorbot.apache.conf; sudo service apache2 reload`

## Configuration

Doorbot is configured using two JSON dotfiles in the operating-users home directory (`/var/www/` for default apache config)

### `.doorbot_users`

Contains authentication information of the form:

  { "username": "PassWord", "otheruser":"otherPass" }

These are 'authorised accounts' that can perform admin tasks, specifically opening the doors.

The intention is not for this file to be populated with each and every member or user of the system, but rather that authentication responsibility is delegated to secondary systems, eg a web front end, RFID reader, etc. Muliple usernames are enabled to support service-based monitoring (as in the RFID would have it's own username, etc.)


### `.doorbot_config`

Multiple doors can be configured based on the available interfaces. There is also a `dummy` interface that provides logging-based debugging.

In the case of the `piface` interface, the `interfaceopt` is the output port which triggers the doors opening/unlocking.

  {
      'doors':[
          {'door_name':"Front Door",
           'doorid':"front",
          'interface': "piface",
          'interfaceopt':0},

          {'door_name':"Back Door",
           'doorid':"back",
          'interface': "piface",
          'interfaceopt':1},
      ]
  }

## API Routes

### `/`

Dummy 'Hello World', shuold probably be populated with an api catalogue

### `/open/<doorid>`

Authenticated route: opens the given doorid based on the `doorbot_config`

### `/status`

Currently Authenticated but doesn't need to be; returns a list of the doorids

## Current Hardware Config in Farset Labs

### Wiring

Inside the enclosure above the network rack in the co-working space, the piface as as wired up as it needs to be for the foreseeable.

**IF ANYONE WANTS TO INTERFACE WITH OR EVEN CONSIDER OPENING THE ENCLOSURE, RECORDED DIRECTOR CONFIRMATION IS REQUIRED IN ADVANCE AND THE ENCLOSURE MUST BE RESEALED BY A DIRECTOR OR DI NEM AFTERWARDS**

There are 12 interface lines wired up to the terminal strip in the top lid of the enclosure; they are split into two 'sectors' of 6, which represent the two proposed 'door' controls, with the front door on the 'left' and the currently unpopulated back door on the right.

| Terminal No | Connection | Notes                                |
| ----------- | ---------- | ------------------------------------ |
| 1           | Relay 0 NO | Front Door Keypad Input (Blue)       |
| 2           | Relay 0 C  | Front Door Keypad Input (Blue/White) |
| 3           | Input 0    | Front Door Not Used (Green)          |
| 4           | Ground     | Front Door Not Used (Green/White)    |
| 5           | Output 2   | Front Door Not Used (Orange)         |
| 6           | +5v        | Front Door Not Used (Orange/White)   |
| 7           | Relay 1 NO | Back Door Not Wired                  |
| 8           | Relay 1 C  | Back Door Not Wired                  |
| 9           | Input 1    | Back Door Not Wired                  |
| 10          | Ground     | Back Door Not Wired                  |
| 11          | Output 3   | Back Door Not Wired                  |
| 12          | +5v        | Back Door Not Wired                  |

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

There are no currently valid tests yet.

## Travis CI

There is a ```.travis.yml``` file that is set up to run your tests for python 2.7
and python 3.2, should you choose to use it.

## License

Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
