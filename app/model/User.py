from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    # nome da tabela
    __tablename__ = "user"

    # campos da tabela
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
