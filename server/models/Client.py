from server.server_utils.server_ini import db
from sqlalchemy import Integer, String


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=None)
    email = db.Column(String, nullable=None)

    def __repr__(self):
        return '{}<{}>'.format(self.name, self.email)
