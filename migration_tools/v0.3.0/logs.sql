CREATE TABLE new_table (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    guild_id INTEGER NOT NULL,
    guild_name TEXT NOT NULL,
    members_total INTEGER NOT NULL,
    members_added INTEGER
);
INSERT INTO new_table (
    log_id,
    guild_id,
    guild_name,
    members_total,
    members_added
)
SELECT
    log_id,
    guild_id,
    guild_name,
    members_total,
    members_added
FROM guild_join;
DROP TABLE guild_join;
ALTER TABLE new_table RENAME TO guild_join;

ALTER TABLE help ADD category TEXT;

CREATE TABLE peep_transfer(
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    peep_amount INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    sender_peeps INTEGER,
    receiver_peeps INTEGER
);