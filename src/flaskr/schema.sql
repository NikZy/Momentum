DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS post;

CREATE TABLE bruker (
  brukerid INTEGER PRIMARY KEY AUTOINCREMENT,
  brukernavn TEXT UNIQUE NOT NULL,  passord TEXT NOT NULL,
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
  forfatter TEXT NOT NULL,
  laget DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tittel TEXT NOT NULL,
  brødtekst TEXT NOT NULL

CREATE TABLE tag(
  tagnavn TEXT PRIMARY KEY
);