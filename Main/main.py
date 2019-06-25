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
    soup = Parser.get_soup_obj('https://old.reddit.com/r/the_donald/')
    posts, nextPage = Parser.get_reddit_posts(soup)

    ## create posts and users

    ## sleep

    ## go on to the next page(limit = 10)

    print(nextPage)


def create_entries(postContainers):
    for post in postContainers:
        post.create_user_model()
        post.create_post_model()


if __name__ == '__main__':
    main()
