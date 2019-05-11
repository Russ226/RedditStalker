from . import User
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Post(User.Base):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable = False, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id))
    title = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable = True)
    text_post = sqlalchemy.Column(sqlalchemy.String, nullable = True)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    user = relationship("User")

    def __repr__(self):
        return "<Post(id = %d, user_id = %d, title= %s, link = %s, text_post = %s, created_on = %s)>" % (self.id, self.user_id, self.title, self.link, self.text_post)
