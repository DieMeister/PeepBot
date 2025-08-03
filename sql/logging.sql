CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY,
    timestamp VARCHAR(19) NOT NULL,
    type VARCHAR(5) NOT NULL,
    log_module VARCHAR(8) NOT NULL,
    description TEXT NOT NULL,
    execution_method VARCHAR(7)
);

CREATE TABLE commands (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    type VARCHAR(9) NOT NULL
);

CREATE TABLE extension_success (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    extension_name TEXT NOT NULL
);

CREATE TABLE extension_error (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    extension_name TEXT NOT NULL,
    reason TEXT NOT NULL
);

CREATE TABLE commands_synced (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    amount INTEGER NOT NULL
);

CREATE TABLE guild_join (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    guild_id INTEGER NOT NULL,
    guild_name TEXT NOT NULL
);

CREATE TABLE member_join (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL
);

CREATE TABLE configure_channel (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    channel_id INTEGER NOT NULL,
    channel_name TEXT NOT NULL
);

CREATE TABLE catch_peep (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    peep_amount INTEGER NOT NULL,
    random_integer INTEGER NOT NULL
);

CREATE TABLE psps_denied (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    reason TEXT NOT NULL
);

CREATE TABLE change_peep_message (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    message_type TEXT NOT NULL,
    old_message TEXT NOT NULL,
    new_message TEXT NOT NULL
);

CREATE TABLE help (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    type TEXT NOT NULL
);
