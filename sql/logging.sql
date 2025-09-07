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
    type VARCHAR(9) NOT NULL,
    prefix VARCHAR(4)
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
    guild_name TEXT NOT NULL,
    members_total INTEGER NOT NULL,
    members_added INTEGER
);

CREATE TABLE member_join (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL
);

CREATE TABLE user_join (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    user_id INTEGER NOT NULL
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

CREATE TABLE steal_peep(
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    moderator TEXT NOT NULL,
    emote TEXT NOT NULL
);

CREATE TABLE help (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    type TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE adding_role_to_list (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    role_id INTEGER NOT NULL,
    reason TEXT
);

CREATE TABLE assigning_role (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    role_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    reason TEXT
);

CREATE TABLE invalid_str_input (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    input TEXT NOT NULL
);

CREATE TABLE invalid_int_input (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    input INTEGER NOT NULL
);

CREATE TABLE log_channel (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    channel_id INTEGER NOT NULL
);

CREATE TABLE peep_transfer(
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    peep_amount INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    sender_peeps INTEGER,
    receiver_peeps INTEGER
);

CREATE TABLE rank_command(
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    rank_user_id INTEGER
);

CREATE TABLE give_peeps (
    log_id INTEGER PRIMARY KEY REFERENCES logs(log_id),
    amount INTEGER NOT NULL,
    member_guild_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL
);
