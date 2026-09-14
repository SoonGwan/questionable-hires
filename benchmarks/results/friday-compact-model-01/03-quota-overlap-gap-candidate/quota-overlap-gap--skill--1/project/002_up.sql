ALTER TABLE accounts ADD COLUMN quota_limit INTEGER;
UPDATE accounts SET quota_limit = quota;
