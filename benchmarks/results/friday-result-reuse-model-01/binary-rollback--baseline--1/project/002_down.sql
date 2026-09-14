UPDATE artifacts SET payload_hex = CAST(payload_hex AS BLOB);
ALTER TABLE artifacts RENAME COLUMN payload_hex TO payload;
