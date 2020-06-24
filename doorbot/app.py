import json
import logging
import os.path

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from interfaces import Dummy, PiFace
from config import Config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)
auth = HTTPBasicAuth()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

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
    door_config['door_id']: pick_interface(
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
