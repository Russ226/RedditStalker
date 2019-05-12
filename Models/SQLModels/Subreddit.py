from Models.SQLModels import User, Post
import sqlalchemy
from sqlalchemy.orm import relationship


class Subreddit(User.Base):
    __tablename__ = "subreddits"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return "<Post(id = %d, name = %s)>" % (self.id, self.name)



class SubredditPostJoin(User.Base):
    __tablename__ = "subredditsPostsJoin"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Post.Post.id), nullable=False)
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.id), nullable=False)
    post = relationship("Post")
    subreddit = relationship("Subreddit")

    def __repr__(self):
        return "<Post(id = %d, post_id = %d, , subreddit_id = %d)>" % (self.id, self.post_id, self.subreddit_id)

class SubredditUserJoin(User.Base):
    __tablename__ = "subredditsUsersJoin"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.User.id), nullable=False)
    subreddit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Subreddit.id), nullable=False)
    user = relationship("User")
    subreddit = relationship("Subreddit")

    def __repr__(self):
        return "<Post(id = %d, user_id = %d, , subreddit_id = %d)>" % (self.id, self.user_id, self.subreddit_id)
