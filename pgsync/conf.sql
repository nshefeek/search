ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 10;
-- set this value to the number of tables you want to load into elastic