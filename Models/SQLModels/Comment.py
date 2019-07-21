from Models.SQLModels import User
from Models.SQLModels import Subreddit
import sqlalchemy
from sqlalchemy.orm import relationship

# this is only for inserting comments parsed from the user page not from the comments from a post
class Comment(User.Base):
    __tablename__ = "comments"
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.User.id))
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.Subreddit.id))
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    user = relationship("User")
    subreddit = relationship("Subreddit")

    def __repr__(self):
        return "<Post(id = %d, user_id = %d, content= %s, created_on = %s)>" % \
               (self.id, self.user_id, self.content, self.created_on)

