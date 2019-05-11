from . import User
from . import Post
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Subreddit(User.Base):
    __tablename__ = "subreddits"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class SubredditPostJoin(User.Base):
    __tablename__ = "subredditsPostsJoin"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Post.id), nullable=False)
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.id), nullable=False)
    post = relationship("Post")
    subreddit = relationship("Subreddit")

class SubredditPostJoin(User.Base):
    __tablename__ = "subredditsUsersJoin"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=False)
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.id, nullable=False))
    user = relationship("User")
    subreddit = relationship("Subreddit")
