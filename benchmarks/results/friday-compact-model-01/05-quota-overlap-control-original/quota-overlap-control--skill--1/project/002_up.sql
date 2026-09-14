ALTER TABLE accounts ADD COLUMN quota_limit INTEGER;
UPDATE accounts SET quota_limit = quota;
CREATE TRIGGER quota_old_update AFTER UPDATE OF quota ON accounts WHEN NEW.quota_limit IS NOT NEW.quota BEGIN UPDATE accounts SET quota_limit=NEW.quota WHERE id=NEW.id; END;
CREATE TRIGGER quota_new_update AFTER UPDATE OF quota_limit ON accounts WHEN NEW.quota IS NOT NEW.quota_limit BEGIN UPDATE accounts SET quota=NEW.quota_limit WHERE id=NEW.id; END;
CREATE TRIGGER quota_old_insert AFTER INSERT ON accounts WHEN NEW.quota_limit IS NULL BEGIN UPDATE accounts SET quota_limit=NEW.quota WHERE id=NEW.id; END;
