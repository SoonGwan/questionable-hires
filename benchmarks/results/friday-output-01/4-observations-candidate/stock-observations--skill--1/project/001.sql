CREATE TABLE stock(sku TEXT PRIMARY KEY, quantity INTEGER NOT NULL);
INSERT INTO stock VALUES ('A',10),('C',0);
CREATE VIEW legacy_stock AS SELECT sku, quantity AS units FROM stock;
