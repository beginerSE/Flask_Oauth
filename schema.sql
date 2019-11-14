CREATE TABLE user_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  user_screen TEXT NOT NULL,
  provider TEXT NOT NULL,
  user_token TEXT NOT NULL,
  user_secret TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);