ALTER TABLE stock ADD COLUMN reserved INTEGER NOT NULL DEFAULT 0;
DROP VIEW legacy_stock;
CREATE VIEW legacy_stock AS SELECT sku, quantity-reserved AS units FROM stock;
