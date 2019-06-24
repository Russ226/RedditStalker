import datetime

from sqlalchemy.exc import SQLAlchemyError

import Models.SQLModels.User as User
import Models.SQLModels.Post as Post
import Models.SQLModels.Subreddit as Sub
import Models.SQLModels.Subreddit as SR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# for now hard coding to carporn will change later
# # data-domain = {self.carporn, i.reddit???}

# refactoring objectives
#     change connection string
#     change the way posts are being stored(i only want the link to the post now)
#     get rid of anything to do with comments
#     set up a call for parsing user page(reddit.com/user/username)
#         methods and storage relating to user page parsing going be in another file

class PostContainer:

    @staticmethod
    def startSession():
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/redditStalker?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session

    def __init__(self, post):

        self.title = post.findAll('p', {'class', 'title'})[0].findAll('a')[0].text
        self.subreddit = post['data-subreddit']
        self.author = post['data-author']
        self.type = post['data-domain']
        self.url = post['data-url']
        # link to comments to determine if post exists in db...
        self.comments_link = post["data-permalink"]
        self.id = 0
        #only set it to post after commiting it to db
        self.post = None
        self.user = None

    def create_user_model(self):
        session = PostContainer.startSession()

        user = session.query(User).filter_by(username=self.author).first()
        self.user = user

        if user is None:
            try:
                new_user = User.User(
                    username=self.author,
                    email=self.author + '@email.com',
                    password='123456',
                    created_on = datetime.datetime.now()
                )
                session.add(new_user)
                session.commit()
                self.user = new_user
            except SQLAlchemyError as e:
                print(e)
                return None
            # parallel task to parse user page(have a delay between each call)

        session.close()
        return None

    def create_post_model(self):
        session = PostContainer.startSession()
        try:
            #title will check for uniqueness
            if session.query(Post).filter_by(title = self.title).first() is not None:
                new_post = Post.Post(
                    title=self.title,
                    link=self.url,
                    user=self.user,
                    created_on = datetime.datetime.now()
                )
                session.add(new_post)
                self.insert_post_subreddit(new_post)
                session.commit()
                self.post = new_post
        except Exception:
            pass

        finally:
            session.close()

    def insert_post_subreddit(self):
        session = PostContainer.startSession()

        subreddit = session.query(Sub.Subreddit).filter_by(name = self.subreddit).first()

        if subreddit != None:
            new_link = Sub.SubredditPostJoin(
                post = self.new_post,
                subreddit = subreddit
            )

            session.add(new_link)
            session.commit()

        else:
            new_subreddit = Sub.Subreddit(
                name = self.subreddit
            )

            new_link = Sub.SubredditPostJoin(
                post=self.new_post,
                subreddit=subreddit
            )

            session.add(new_subreddit)
            session.add(new_link)
            session.commit()


    def __repr__(self):
        return "<Post(id_counter = %s, author = %s, title= %s, url = %s, type = %s, comments_link= %s)>" % (
            PostContainer.id_counter, self.author, self.title, self.url, self.type, self.comments_link)
