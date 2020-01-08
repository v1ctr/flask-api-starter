from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid
from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(32), nullable=True)
    surname = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

