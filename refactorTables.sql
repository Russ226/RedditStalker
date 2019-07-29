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

ALTER TABLE `redditstalker`.`subredditscomementsjoin` 
RENAME TO  `redditstalker`.`subredditscommentsjoin` ;


ALTER TABLE redditstalker.subredditscommentsJoin
ADD COLUMN subreddit_name varchar(100) NOT NULL AFTER comment_id;


ALTER TABLE redditstalker.subredditsPostsJoin
CHANGE COLUMN subbredit_name subreddit_name VARCHAR(100) NOT NULL;

ALTER TABLE redditstalker.subredditsUsersJoin
CHANGE COLUMN subbredit_name subreddit_name VARCHAR(100) NOT NULL;

Alter Table redditstalker.comments
ADD Column link varchar(250) NOT NULL AFTER content;

Alter table redditstalker.comments
ADD column subreddit_id int Not Null after user_id,
Add Foreign Key (subreddit_id) REFERENCES subreddits(id);

SET foreign_key_checks = 1;

Alter table redditstalker.posts
ADD column subreddit_id int Not Null after user_id,
Add Foreign Key (subreddit_id) REFERENCES subreddits(id);

