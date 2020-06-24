from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    """
    User Table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    access_cards = db.relationship('Card', backref='user', lazy=True)
    access_areas = db.relationship('Area', backref='user', lazy=True)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Card(db.Model):
    """
    Card Table
    Cards are assigned to users
    Cards of Users assigned to Areas open Doors in that Area
    """

    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class Area(db.Model):
    """
    Create a Area table
    Areas have users that are permitted to be in them
    """

    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    permitted_users = db.relationship('User', backref='areas',
                                lazy='dynamic')

    def __repr__(self):
        return '<Area: {}>'.format(self.name)

class Devices(UserMixin,db.model):
    """
    Create a Devices table
    Devices are assigned to Areas
    Devices can access Areas via their device id and a presented Card ID
    """
    id = db.Column(db.Integer, primary_key=True)
    device_id=db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return

    def __repr__(self):
        return '<Device: {}>'.format(self.device_id)


