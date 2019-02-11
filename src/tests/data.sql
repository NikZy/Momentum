INSERT INTO bruker (brukerid, brukernavn, passord, epost, bilde)
VALUES
  (1, 'guns', '123','guns@gmail.com', 'url'),
  (2, 'Sindre','321', 'min@mail.com', 'url2');

INSERT INTO forsideInnlegg (id, forfatter, laget, tittel, brødtekst)
VALUES
  (1, 'Sindre', '2018-01-14', 'Første post!', 'teeeest teeext');
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

INSERT INTO tag (tagnavn)
VALUES
  ('AI');
