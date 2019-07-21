import datetime

from sqlalchemy.exc import SQLAlchemyError
import logging
import
import Models.SQLModels.Subreddit as Sub
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostContainer:

    @staticmethod
    def startSession():
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/redditStalker?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine, expire_on_commit=False)
        session = session_maker()
        return session

    def __init__(self, comment, user):

        self.content = comment.find('div', {'class', 'usertext-body'}).find('div', {'class', 'md'}).findAll('p')
        self.subreddit = comment['data-subreddit']
        self.author = comment['data-author']
        self.type = comment['data-domain']
        self.url = comment['data-url']
        # link to comments to determine if post exists in db...
        self.comments_link = comment["data-permalink"]
        self.id = 0
        #only set it to post after commiting it to db
        self.comment = None
        self.user = user

    def createComment(self):
        pass


