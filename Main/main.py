from Main.Parser import Parser


# refactoring objectives:
#     - remove all mentions of comments
#     - create links for user pages
#


# cleans a posts with no comments
def cleanPost(link):
    if link.find('https://') == -1:
        return True

    return False

def main():
    # posts = Parser.get_reddit_posts('https://old.reddit.com/r/the_donald/')
    # for post in posts:
    #     print("data-url: " + post["data-url"])
    #     print("permalink: " + post["data-permalink"])

    Parser.get_user_subreddit_posts()



def create_entries(postContainers):
    for post in postContainers:
        post.create_user_model()
        post.create_post_model()


if __name__ == '__main__':
    main()
