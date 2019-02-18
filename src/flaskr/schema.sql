mailmailDROP TABLE IF EXISTS ;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS job_applicant;
DROP TABLE IF EXISTS startup;
DROP TABLE IF EXISTS frontpage_post;
DROP TABLE IF EXISTS tag;


CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  mail TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type ='job_applicant' OR type='startup' OR type='admin') DEFAULT 'job_applicant',
  image IMAGE
);

CREATE TABLE job_applicant (
  user_id INTEGER PRIMARY KEY REFERENCES user(user_id),
  former_jobs TEXT,
  kompetanse TEXT,
  cv TEXT,
  fødselsdato DATE
);

CREATE TABLE startup (
  user_id INTEGER PRIMARY KEY REFERENCES user(user_id),
  descriptiontext TEXT NOT NULL,
  startup_date DATE NOT NULL
);

CREATE TABLE frontpage_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author TEXT NOT NULL,
  made DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  bodytext TEXT NOT NULL
);

CREATE TABLE tag (
  tagname TEXT PRIMARY KEY
);
