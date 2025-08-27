CREATE TABLE guilds (
    guild_id INTEGER,
    success_message VARCHAR(2000) DEFAULT('You got a peep!'),
    scratch_message VARCHAR(2000) Default('You got scratched.'),
    no_peep_message VARCHAR(2000) DEFAULT('No peep, L!'),
    last_peep VARCHAR(19) NOT NULL,
    log_channel_id INTEGER,
    PRIMARY KEY (guild_id)
)
WITHOUT ROWID;

CREATE TABLE members (
    user_id INTEGER,
    guild_id INTEGER REFERENCES guilds(guild_id),
    last_peep VARCHAR(19),
    caught_peeps INTEGER DEFAULT(0),
    tries INTEGER DEFAULT(0),
    sent_peeps INTEGER DEFAULT(0),
    received_peeps INTEGER DEFAULT(0),
    PRIMARY KEY (user_id, guild_id)
)
WITHOUT ROWID;

CREATE TABLE allowed_channels (
    channel_id INTEGER,
    guild_id INTEGER REFERENCES guilds(guild_id),
    PRIMARY KEY (channel_id)
)
WITHOUT ROWID;

CREATE TABLE role_assigning (
    role_id INTEGER,
    guild_id INTEGER REFERENCES guilds(guild_id),
    PRIMARY KEY (role_id)
)
WITHOUT ROWID;
