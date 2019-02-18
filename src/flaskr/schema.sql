mailmailDROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS jobbsøker;
DROP TABLE IF EXISTS startup;
DROP TABLE IF EXISTS forsideInnlegg;
DROP TABLE IF EXISTS tag;


CREATE TABLE bruker (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  mail TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type ='jobbsøker' OR type='startup' OR type='admin') DEFAULT 'jobbsøker',
  image IMAGE
);

CREATE TABLE jobbsøker (
  user_id INTEGER PRIMARY KEY REFERENCES bruker(user_id),
  former_jobs TEXT,
  kompetanse TEXT,
  cv TEXT,
  fødselsdato DATE
);

CREATE TABLE startup (
  user_id INTEGER PRIMARY KEY REFERENCES bruker(user_id),
  beskrivelse TEXT NOT NULL,
  oppstartsdato DATE NOT NULL
);

CREATE TABLE forsideinnlegg (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  forfatter TEXT NOT NULL,
  laget DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tittel TEXT NOT NULL,
  brødtekst TEXT NOT NULL
);

CREATE TABLE tag (
  tagnavn TEXT PRIMARY KEY
);
