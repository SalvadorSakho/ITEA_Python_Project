from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=None)
    email = Column(String, nullable=None)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (
            self.name, self.email
        )
