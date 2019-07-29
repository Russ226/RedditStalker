import datetime

from sqlalchemy.exc import SQLAlchemyError
import logging
import Models.SQLModels.User as User
import Models.SQLModels.Post as Post
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

    def __init__(self, post, user = None):

        self.title = post.findAll('p', {'class', 'title'})[0].findAll('a')[0].text
        self.subreddit = post['data-subreddit']
        self.author = post['data-author']
        self.type = post['data-domain']
        self.url = post['data-url']
        # link to comments to determine if post exists in db...
        self.comments_link = post["data-permalink"]
        self.id = 0
        #only set it to post after commiting it to db
        self.user = user is not None if user else None

    def create_user_model(self):
        session = PostContainer.startSession()
        user = None

        if self.user is None:
            user = session.query(User.User).filter_by(username=self.author).first()
            self.user = user

        if self.user is None and user is None:
            try:
                new_user = User.User(
                    username=self.author,
                    created_on = datetime.datetime.now()
                )
                session.add(new_user)
                session.commit()
                session.flush()
                self.user = new_user
            except SQLAlchemyError as e:
                logging.exception(e)
                return None
            # parallel task to parse user page(have a delay between each call)

        session.close()
        return None

    def create_post_model(self):
        session = PostContainer.startSession()
        try:
            #title will check for uniqueness
            if not self.checkDuplicatePost():
                subreddit = self.insert_subreddit()
                new_post = Post.Post(
                    title=self.title.strip(),
                    link=self.url,
                    user=self.user,
                    subreddit = subreddit,
                    created_on = datetime.datetime.now()
                )
                session.add(new_post)
                session.commit()
        except Exception as e:
            logging.exception(e)

        finally:

            session.close()

    def insert_subreddit(self):

        session = PostContainer.startSession()
        subreddit = session.query(Sub.Subreddit).filter_by(name=self.subreddit).first()

        if subreddit != None:
            session.close()
            return subreddit

        else:
            new_subreddit = Sub.Subreddit(
                name = self.subreddit
            )
            session.add(new_subreddit)
            session.commit()
            session.flush()
            session.close()
            return new_subreddit




    # checks if there a post in the db with the same title created by the same user and posted in the same subreddit
    # other wise its probably a crosspost or repost
    def checkDuplicatePost(self):
        session = PostContainer.startSession()
        dupPost = session.query(Post.Post).filter_by(title = self.title).first()

        if dupPost is not None and dupPost.user.username == self.author:
            checkSubReddit = session.query(Sub.Subreddit).filter_by(id = dupPost.subreddit_id).first()
            if checkSubReddit is not None:
                session.close()
                return True

        session.close()
        return False

