# make a request to a subreddit 
# parse the first two pages

# each post should include the following:
# 	title
# 	username
# 	date if possible 
# 		figure if post is a self post or image or link(might start if an easy subreddit be doing those checks)
#	link to the post with the comments
# 	comments
# 		username
# 		date?
# 		content
# 	usernames of everyone to create entries in db


from bs4 import BeautifulSoup
import requests

url = 'https://old.reddit.com/r/carporn/'
headers = {
    "user-agent": "ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36"
}


def get_reddit_posts(url):
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    posts = soup.findAll('div', {"class": "thing"})

    return posts


def get_comments(url):
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    comments = soup.findAll('div', {"class": "sitetable"})
    if len(comments) > 0:
        root_comments = comments[1].findAll('div', {"class": "thing"})

        return root_comments

    return None
