CREATE TABLE items(id INTEGER PRIMARY KEY, title TEXT NOT NULL, payload BLOB NOT NULL);
INSERT INTO items VALUES(1, '첫 항목', x'00ff'), (2, 'keep', x'');
CREATE VIEW public_items AS SELECT id, title AS label, payload FROM items;
