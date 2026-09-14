DROP TRIGGER IF EXISTS quota_old_update;
DROP TRIGGER IF EXISTS quota_new_update;
DROP TRIGGER IF EXISTS quota_old_insert;
ALTER TABLE accounts DROP COLUMN quota_limit;
