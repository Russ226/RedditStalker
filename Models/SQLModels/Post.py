from Models.SQLModels import User
from Models.SQLModels import Subreddit
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Post(User.Base):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable = False, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.User.id))
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.Subreddit.id))
    title = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable = True)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    user = relationship("User")
    subreddit = relationship("Subreddit")

    def __repr__(self):
        return "<Post(id = %d, user_id = %d, title= %s, link = %s, created_on = %s)>" % (self.id, self.user_id, self.title, self.link, self.created_on)

