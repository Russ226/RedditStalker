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

# create parser for user pages to find where they post


from bs4 import BeautifulSoup
import requests

entryPointsubreddit = 'https://old.reddit.com/r/the_donald/'
headers = {
    "user-agent": "ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36"
}


def get_reddit_posts(url):
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')
    # finds next page
    nextPage = soup.find('span', {'class', 'next-button'}).find('a')['href']
    posts = soup.findAll('div', {"class": "thing"})

    return posts, nextPage


def get_user_subreddit_posts(user = ""):
    url = 'https://old.reddit.com/user/' + user

    testUrl = "https://old.reddit.com/user/fox-mcleod"

    r = requests.get(testUrl, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    # soup.findAll('a', {"class": "Post__subredditLink"})[0]["href"]
    # next page for users
    #soup.find('div', {'class', 'ListingPagination'}).find('a')['href']
    #get all subreddit on the pages and next page for at least 10 pages

    #have a delay between a call to each page

#span class = next button for next url
