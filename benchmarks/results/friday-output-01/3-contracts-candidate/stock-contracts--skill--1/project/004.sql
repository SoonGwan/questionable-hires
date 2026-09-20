DROP VIEW legacy_stock;
CREATE VIEW legacy_stock AS SELECT sku, quantity AS units FROM stock;
