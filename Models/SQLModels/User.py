import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable = False, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)

    def __repr__(self):
        return "<Post(id = %d, username = %s)>" % (self.id, self.username)

