

CREATE TABLE IF NOT EXISTS redditStalker.users(
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(id),
  UNIQUE KEY user(username, email, password)
);

CREATE TABLE IF NOT EXISTS redditStalker.posts(
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  link VARCHAR(255),
  text_post TEXT,
  title VARCHAR(255) NOT NULL,
  created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(id),
  foreign key (user_id) REFERENCES users(id)
);

#CREATE TABLE IF NOT EXISTS redditStalker.comments(
  #id INT NOT NULL AUTO_INCREMENT,
 # user_id INT NOT NULL,
 # post_id INT NOT NULL,
 # comment_id INT,
 # reply BIT NULL,
 # post TEXT,
 # created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 # PRIMARY KEY(id),
  #foreign key (user_id) REFERENCES users(id),
  #foreign key (post_id) REFERENCES posts(id),
  #foreign key (comment_id) REFERENCES comments(id)
#);

CREATE TABLE IF NOT EXISTS redditStalker.subreddits(
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS redditStalker.subredditsPostsJoin(
	id INT NOT NULL AUTO_INCREMENT,
	subreddit_id INT NOT NULL,
	post_id INT NOT NULL,
	foreign key (post_id) REFERENCES posts(id),
	foreign key (subreddit_id) REFERENCES subreddits(id),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS redditStalker.subredditsUsersJoin(
	id INT NOT NULL AUTO_INCREMENT,
	subreddit_id INT NOT NULL,
	user_id INT NOT NULL,
	foreign key (user_id) REFERENCES users(id),
	foreign key (subreddit_id) REFERENCES subreddits(id),
    PRIMARY KEY(id)
);