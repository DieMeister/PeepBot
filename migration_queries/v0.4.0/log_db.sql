CREATE TABLE user_join (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    user_id INTEGER NOT NULL
);

CREATE TABLE rank_command (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    rank_user_id INTEGER
);

CREATE TABLE give_peeps (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    amount INTEGER NOT NULL,
    member_guild_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL
);

-- support invalid str and int inputs
ALTER TABLE invalid_input RENAME TO invalid_str_input;
CREATE TABLE invalid_int_input (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    input INTEGER NOT NUL
);

-- log which prefix was used to execute a command
ALTER TABLE commands
ADD COLUMN prefix VARCHAR(4);

CREATE TABLE remove_peeps (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    old_total INTEGER NOT NULL,
    amount_removed INTEGER NOT NULL,
    member_guild_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL
);
