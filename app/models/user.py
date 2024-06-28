from app.extensions import db
from flask_login import UserMixin
import datetime
import jwt
from flask import current_app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def get_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)},
            current_app.config['JWT_SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['id']
        except:
            return None
        return User.query.get(id)