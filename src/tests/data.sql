INSERT INTO bruker (brukernavn, passord, epost, bilde)
VALUES
  ("guns", '123','guns@gmail.com', 'url'),
  ('Sindre','321', 'min@mail.com', 'url2'),
  ('test', 'test', 'test@test.no', 'url'); /* mail funker ikke */

INSERT INTO frontpage_post (author, made, title, bodytext)
VALUES
  ('Sindre', '2018-01-14', 'Første post!', 'teeeest teeext');

INSERT INTO tag (tagname)
VALUES
  ('AI');
