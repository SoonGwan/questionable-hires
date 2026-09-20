DROP VIEW public_items;
CREATE VIEW public_items AS SELECT id, title, payload FROM items;
