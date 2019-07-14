import datetime

from sqlalchemy.exc import SQLAlchemyError
import logging
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
        session_maker = sessionmaker(bind=engine,expire_on_commit=False)
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

        user = session.query(User.User).filter_by(username=self.author).first()
        self.user = user

        if user is None:
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
                new_post = Post.Post(
                    title=self.title.strip(),
                    link=self.url,
                    user=self.user,
                    created_on = datetime.datetime.now()
                )
                session.add(new_post)
                session.commit()
                session.flush()
                self.post = new_post
        except Exception as e:
            logging.exception(e)

        finally:

            session.close()

    def insert_post_subreddit(self):

        if self.post is not None and self.post.id is not None:
            session = PostContainer.startSession()
            subreddit = session.query(Sub.Subreddit).filter_by(name=self.subreddit).first()

            if subreddit != None:
                new_link = Sub.SubredditPostJoin(
                    post = self.post,
                    subreddit = subreddit,
                    subreddit_name=self.subreddit

                )

                session.add(new_link)
                session.commit()

            else:
                new_subreddit = Sub.Subreddit(
                    name = self.subreddit
                )
                session.add(new_subreddit)
                session.commit()
                session.flush()

                new_link = Sub.SubredditPostJoin(
                    post=self.post,
                    subreddit=subreddit,
                    subreddit_name = self.subreddit
                )


                session.add(new_link)
                session.commit()
                session.close()




    # checks if there a post in the db with the same title created by the same user and posted in the same subreddit
    # other wise its probably a crosspost or repost
    def checkDuplicatePost(self):
        session = PostContainer.startSession()
        dupPost = session.query(Post.Post).filter_by(title = self.title).first()

        if dupPost is not None and dupPost.user.username == self.author:
            checkSubReddit = session.query(Sub.SubredditPostJoin).filter_by(post_id = dupPost.id).first()
            if checkSubReddit is not None:
                session.close()
                return True

        session.close()
        return False

    def __repr__(self):
        return "<Post(id_counter = %s, author = %s, title= %s, url = %s, type = %s, comments_link= %s)>" % (
            PostContainer.id_counter, self.author, self.title, self.url, self.type, self.comments_link)
