DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS forsideInnlegg;
DROP TABLE IF EXISTS tag;


CREATE TABLE bruker (
  brukerid INTEGER PRIMARY KEY AUTOINCREMENT,
  brukernavn TEXT UNIQUE NOT NULL,  
  passord TEXT NOT NULL,
  epost TEXT NOT NULL,
  type TEXT CHECK (type ='jobbsøker' OR type='startup' OR type='admin') DEFAULT 'jobbsøker',
  bilde TEXT IMAGE
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