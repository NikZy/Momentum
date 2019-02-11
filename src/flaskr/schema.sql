DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS jobbsoker;
DROP TABLE IF EXISTS startup;
DROP TABLE IF EXISTS forsideinnlegg;
DROP TABLE IF EXISTS tag;

CREATE TABLE bruker (
  brukerid INTEGER PRIMARY KEY AUTOINCREMENT,
  brukernavn TEXT UNIQUE NOT NULL,  
  passord TEXT NOT NULL,
  epost TEXT NOT NULL,
  bilde IMAGE
);

CREATE TABLE jobbsoker (
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
  tidligerejobber TEXT,
  kompetanse TEXT,
  cv TEXT,
  fødselsdato DATE NOT NULL
);

CREATE TABLE startup (
  brukerid INTEGER PRIMARY KEY REFERENCES bruker(brukerid),
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