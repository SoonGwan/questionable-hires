ALTER TABLE artifacts RENAME COLUMN payload TO payload_hex;
UPDATE artifacts SET payload_hex = hex(payload_hex);
