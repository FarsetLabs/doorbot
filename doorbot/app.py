from flask import Flask, Response, request
from flask.ext.httpauth import HTTPBasicAuth
import logging

from interfaces import Dummy, PiFace

import json
import os.path

app = Flask(__name__)
auth = HTTPBasicAuth()
logging.basicConfig(level=logging.DEBUG)

user_db = json.load(
    open(os.path.expanduser("~/.doorbot_users"), 'r')
)
card_db = json.load(
    open(os.path.expanduser("~/.doorbot_cards"), 'r')
)
config_settings = json.load(
    open(os.path.expanduser("~/.doorbot_config"), 'r')
)


def pick_interface(choice):
    """
    Select and return an interface definition
    :param choice:
    :return:
    """

    candidate_cls = {
        'dummy': Dummy,
        'piface': PiFace
    }.get(choice)
    try:
        candidate_cls.import_prerequisites()
        return candidate_cls
    except ImportWarning as e:
        logging.error("Prequsite Failed, loading dummy interface: {}".format(e))
        return Dummy

app.doors = {
    door_config['door_id']:pick_interface(
        door_config['interface']
    )(**door_config) for door_config in config_settings['doors']
}

logging.debug("Got Doors: {} from Config {}".format(app.doors, config_settings))

@auth.verify_password
def verify(username, password):
    # Actual user from .doorbot_users
    if username in user_db:
        return user_db.get(username) == password
    # 'Virtual' User representing a card reader, so username is the cardreader's device id
    # So to test if the password is valid, look up the card_set mapping from device id to 'card_set' from
    # .doorbot_config
    if username in app.doors.keys():
        door_group = app.doors[username].door_name
        if door_group in card_db:
            return password in card_db[door_group]
    return False

