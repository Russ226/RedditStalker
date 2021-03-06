# test parser and container
#must be able to save post and subreddit

import json
import unittest
from bs4 import BeautifulSoup
from Main.Parser import Parser
import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as Sub
import Models.SQLModels.Post as Post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models.Containers.PostContainer import PostContainer


class testPostContainer(unittest.TestCase):

    def startSession(self):
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/redditStalker?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session

    def nextPage(self, link):
        file = open(link, 'r')
        soup = BeautifulSoup(file.read(), 'html.parser')
        file.close()

        return soup

    # read from html first page doc
    def setUp(self):
        intialHtmlFile = open('TestHTMLFiles/TestPostContainerHTML/TestPostContainer1.html', 'r')
        self.soup = BeautifulSoup(intialHtmlFile.read(), 'html.parser')
        intialHtmlFile.close()

        testFile = open('TestHTMLFiles/ParsedData/DataToTestAgainst', 'r')
        self.testData = json.load(testFile)
        testFile.close()

    def testPostParserPage1(self):
        # create bs var and pass to parse post function in parser file
        posts, nextPage = Parser.get_reddit_posts(self.soup)

        for post in posts:
            title = post.findAll('p', {'class', 'title'})[0].findAll('a')[0].text.strip()
            subreddit = post['data-subreddit']
            author = post['data-author']
            self.assertEqual(author, 'IjustLikeToShitPost')
            self.assertEqual(subreddit, 'The_Donald')
            self.assertEqual(title, 'The people that Ice will apprehend have already been ordered to be deported. This means that they have run from the law and run from the courts. These are people that are supposed to go back to their home country. They broke the law by coming into the country, & now by staying.')


    def testSavingPosts(self):
        posts, nextPage = Parser.get_reddit_posts(self.soup)
        counter = 0

        while(counter < 2):
            for post in posts:
                newPost = PostContainer(post)
                newPost.create_user_model()
                newPost.create_post_model()

            if nextPage is not None:
                soup = self.nextPage(nextPage)
                posts, nextPage = Parser.get_reddit_posts(soup)

            counter += 1


        session = self.startSession()

        #check if info was saved correctly

        self.assertEqual(session.query(Sub.Subreddit).filter_by(name = "The_Donald").count(), 1)

        # #checking for users
        self.assertEqual(session.query(User.User).filter_by(username = "IjustLikeToShitPost").first().username, self.testData['data'][0]["username"])
        self.assertEqual(session.query(User.User).filter_by(username = "Lovinnit").first().username, self.testData['data'][1]["username"])
        self.assertEqual(session.query(User.User).filter_by(username = "KeepMarxInTheGround").first().username, self.testData['data'][2]["username"])
        #
        # #checking the posts
        self.assertEqual(session.query(Post.Post).filter_by(title="Antifa").first().title, self.testData['data'][1]["title"])
        self.assertEqual(session.query(Post.Post).filter_by(title="Little Ben Shapiro").first().title, self.testData['data'][2]["title"])

        session.close()


    def testDuplicatePosts(self):
        soup = self.nextPage('TestHTMLFiles/TestPostContainerHTML/TestDuplicatePosts.html')
        posts, nextPage = Parser.get_reddit_posts(soup)

        for post in posts:
            newPost = PostContainer(post)
            newPost.create_user_model()
            newPost.create_post_model()

        session = self.startSession()

        self.assertEqual(session.query(Post.Post).filter_by(title="Antifa").count(), 1)

        session.close()


    def tearDown(self):
        pass

if __name__ == '__main__':
    testPostContainer.main()