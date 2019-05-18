#for collecting info from user pages
import datetime

from sqlalchemy.exc import SQLAlchemyError

import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as Sub
import Models.SQLModels.Subreddit as SR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#every instance of this class should be its own thread
class UserContainer:
    ##session need
    @staticmethod
    def startSession():
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/redditStalker?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session

    def __init__(self, user):
        self.user = user
        self.userPageLink = 'https://old.reddit.com/user/' + user.username


    def insertSubreddit(self, subredditName):
        session = UserContainer.startSession()

        #check if subreddit entry exists
        checkSubreddit = session.query(Sub.Subreddit).filter_by(name = subredditName).first()

        # link user and subreddit
        if checkSubreddit != None:
            new_subreddit =  Sub.Subreddit(
                name = subredditName
            )
            session.add(new_subreddit)

            new_subreddit_user = Sub.SubredditUserJoin(
                user = self.user,
                subredditName = new_subreddit

            )

            session.add(new_subreddit_user)
            session.commit()
        else:

            new_subreddit_user = Sub.SubredditUserJoin(
                user=self.user,
                subredditName=checkSubreddit

            )

            session.add(new_subreddit_user)
            session.commit()


    def run(self):
        #thread runner class...
        pass


