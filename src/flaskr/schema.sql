DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS post;

CREATE TABLE bruker (
  brukerid INTEGER PRIMARY KEY AUTOINCREMENT,
  brukernavn TEXT UNIQUE NOT NULL,
  passord TEXT NOT NULL,
  epost TEXT NOT NULL,
  bilde IMAGE
);

CREATE TABLE jobbsøker(
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
  tidligerejobber TEXT,
  kompetanse TEXT,
  cv TEXT,
  fødselsdato DATE NOT NULL
);

CREATE TABLE startup(
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
  beskrivelse TEXT NOT NULL,
  oppstartsdato DATE NOT NULL
);

CREATE TABLE forsideInnlegg (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES bruker(brukerid)
);