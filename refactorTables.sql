ALTER TABLE redditstalker.posts 
 DROP COLUMN commentLink;

ALTER TABLE redditstalker.users 
DROP COLUMN email;

ALTER TABLE redditstalker.subredditspostsjoin
RENAME TO subredditsPostsJoin;

ALTER TABLE redditstalker.subredditsPostsJoin
ADD COLUMN subbredit_name varchar(100) NOT NULL AFTER post_id;

ALTER TABLE redditstalker.subredditsusersjoin
RENAME TO subredditsUsersJoin;

ALTER TABLE redditstalker.subredditsUsersJoin
ADD COLUMN subbredit_name varchar(100) NOT NULL AFTER user_id;


CREATE TABLE IF NOT EXISTS redditStalker.comments(
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  content LONGTEXT,
  created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(id),
  foreign key (user_id) REFERENCES users(id)
);



CREATE TABLE IF NOT EXISTS redditStalker.subredditscomementsJoin(
	id INT NOT NULL AUTO_INCREMENT,
	subreddit_id INT NOT NULL,
	comment_id INT NOT NULL,
	foreign key (comment_id) REFERENCES comments(id),
	foreign key (subreddit_id) REFERENCES subreddits(id),
    PRIMARY KEY(id)
);

ALTER TABLE redditstalker.subredditscommentsJoin
ADD COLUMN subbredit_name varchar(100) NOT NULL AFTER comment_id;