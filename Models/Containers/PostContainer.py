import datetime
import Models.SQLModels.User as User
import Models.SQLModels.Post as Post
import Models.SQLModels.Subreddit as SR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# for now hard coding to carporn will change later
# data-domain = {self.carporn, i.reddit???}
class PostContainer:
    id_counter = 0

    @staticmethod
    def startSession():
        engine = create_engine('mysql+pymysql://root:Pen1992@@localhost/forumv1?charset=utf8', encoding='utf-8')
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session

    def __init__(self, post):

        self.title = post.findAll('p', {'class', 'title'})[0].findAll('a')[0].text
        self.author = post['data-author']
        self.type = post['data-domain']
        self.url = post['data-url']
        self.comments_link = 'reddit.com' + \
                             post.findAll('p', {'class', 'title'})[0].findAll('a', {'data-event-action', "title"})[0][
                                 'href']
        self.id = 0

        PostContainer.id_counter += 1

    def create_user_model(self):
        session = PostContainer.startSession()

        user = session.query(User).filter_by(username=self.author).first()

        if user is None:
            new_user = User.User(
                username=self.author,
                email=self.author + '@email.com',
                password='123456',
                created_on = datetime.datetime.now()
            )
            session.add(new_user)
            session.commit()
            session.close()
            return None

        session.close()

    def create_post_model(self):
        self.comments_link = "https://old." + self.comments_link
        session = PostContainer.startSession()
        try:
            if self.type is not "self.carporn":
                user = session.query(User).filter_by(username=self.author).first()
                new_post = Post.Post(
                    title=self.title,
                    link=self.url,
                    user=user,
                    created_on = datetime.datetime.now()
                )
                session.add(new_post)
                session.commit()
                self.id = new_post.id
        except Exception:
            pass

        finally:
            session.close()

    def __repr__(self):
        return "<Post(id_counter = %s, author = %s, title= %s, url = %s, type = %s, comments_link= %s)>" % (
            PostContainer.id_counter, self.author, self.title, self.url, self.type, self.comments_link)
