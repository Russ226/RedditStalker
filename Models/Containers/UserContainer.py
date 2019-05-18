#for collecting info from user pages
import datetime

from sqlalchemy.exc import SQLAlchemyError

import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as Sub
import Models.SQLModels.Subreddit as SR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UserContainer:
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

        #check if subreddit entry exists
        #link user and subreddit
        #save in table
        pass

    def run(self):
        #thread runner class...
        pass


