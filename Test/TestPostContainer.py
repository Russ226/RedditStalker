# test parser and container
#must be able to save post and subreddit

import os
import unittest
from bs4 import BeautifulSoup
from Main.Parser import Parser
import datetime
import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as sub
import Models.Containers.UserContainer as UserContainer
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
import Models.SQLModels.Subreddit as Sub



class testUserSubreddit(unittest.TestCase):

    @staticmethod
    def startSession():
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/redditStalker?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session

    # read from html doc
    def setUp(self):
        script_dir = os.path.dirname(__file__)
        file = open('TestHTMLFiles/TestPostContainerHTML/TestPostContainer1.html', 'r')
        self.soup = BeautifulSoup(file.read(), 'html.parser')
        file.close()

    def testPostParserPage1(self):
        # create bs var and pass to parse post function in parser file
        posts, nextPage = Parser.get_reddit_posts(self.soup)

        for post in posts:
            title = post.findAll('p', {'class', 'title'})[0].findAll('a')[0].text
            subreddit = post['data-subreddit']
            author = post['data-author']
            assert author, 'IjustLikeToShitPost'
            assert subreddit, 'The_Donald'
            assert title, 'The people that Ice will apprehend have already been ordered to be deported. This means that they have run from the law and run from the courts. These are people that are supposed to go back to their home country. They broke the law by coming into the country, &amp; now by staying.'

    def SavingPosts(self):
        pass

    def tearDown(self):
        #delete all new entries to db
        pass
