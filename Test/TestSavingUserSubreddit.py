import unittest
import datetime
import Models.SQLModels.User as User
import Models.SQLModels.Subreddit as sub
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

    def setUp(self):
        session = testUserSubreddit.startSession()
        new_user = User.User(
            username="bobtest",
            email= 'bobtest@email.com',
            password='123456',
            created_on=datetime.datetime.now()
        )
        session.add(new_user)
        session.commit()

    def testSubredditDoesntExist(self):
        pass

    def tearDown(self):
        session = testUserSubreddit.startSession()
        deleteUser = session.query(User.User).filter_by(username = "bobtest").first()
        deleteSubreddit = session.query(sub.Subreddit).filter_by(username = "r/test").first()
        deleteJoin = session.query(sub.SubredditUserJoin).filter_by(and_(subreddit_id = deleteSubreddit.id, user_id = deleteUser.id)).first()

        session.delete(deleteJoin)
        session.delete(deleteSubreddit)
        session.delete(deleteUser)

        session.commit()
