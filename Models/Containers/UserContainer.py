#for collecting info from user pages
import datetime
import logging
from sqlalchemy.exc import SQLAlchemyError
import Main.Parser.Parser as Parser
import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as Sub
import Models.SQLModels.Subreddit as SR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models.Containers.PostContainer import PostContainer

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


    def parseUserPage(self):
        userEntry, nextPage = Parser.get_user_subreddit_posts(self.userLink)
        for n in range(0,10):
            if userEntry['data-type'] == 'link':
                PostContainer(userEntry, self.user)

            elif userEntry['data-type'] == 'comment':
                self.insertCommnent(userEntry)

            else:
                ## going log it for now before i figure it out what to do with no it
                logging.exception("this was not a comment or post: \n" + userEntry)

            userEntry, nextPage = Parser.get_user_subreddit_posts(nextPage)
