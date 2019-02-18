DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS jobbsøker;
DROP TABLE IF EXISTS startup;
DROP TABLE IF EXISTS frontpage_post;
DROP TABLE IF EXISTS tag;


CREATE TABLE bruker (
  brukerid INTEGER PRIMARY KEY AUTOINCREMENT,
  brukernavn TEXT UNIQUE NOT NULL,  
  passord TEXT NOT NULL,
  epost TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type ='jobbsøker' OR type='startup' OR type='admin') DEFAULT 'jobbsøker',
  bilde IMAGE
);

CREATE TABLE jobbsøker (
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
  tidligerejobber TEXT,
  kompetanse TEXT,
  cv TEXT,
  fødselsdato DATE
);

CREATE TABLE startup (
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
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