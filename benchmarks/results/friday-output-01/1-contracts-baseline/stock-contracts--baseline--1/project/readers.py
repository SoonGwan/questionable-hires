OLD = 'SELECT sku, units FROM legacy_stock ORDER BY sku'
NEW = 'SELECT sku, quantity-reserved AS units FROM stock ORDER BY sku'
