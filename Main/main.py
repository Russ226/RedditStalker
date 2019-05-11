import Parser
import Parser_Containers as pc
import re


# cleans a posts with no comments
def cleanPost(link):
    if link.find('https://') == -1:
        return True

    return False


def main():
    posts = Parser.get_reddit_posts('https://old.reddit.com/r/carporn/')

    postContainers = []
    for post in posts:
        p = pc.PostContainer(post)

        if (cleanPost(p.comments_link)):
            postContainers.append(p)

    create_entries(postContainers)


def create_entries(postContainers):
    for post in postContainers:
        post.create_user_model()
        post.create_post_model()
        post.create_comment_model()


if __name__ == '__main__':
    main()
