CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    stolen_peeps INTEGER
);

-- TODO add emotes to default psps messages
CREATE TABLE guilds (
    guild_id INTEGER,
    success_message VARCHAR(2000) DEFAULT('You got a peep!'), -- TODO make NOT NULL
    scratch_message VARCHAR(2000) Default('You got scratched.'), -- TODO make NOT NULL
    no_peep_message VARCHAR(2000) DEFAULT('No peep, L!'), -- TODO make NOT NULL
    last_peep VARCHAR(19) NOT NULL,
    log_channel_id INTEGER,
    PRIMARY KEY (guild_id)
)
WITHOUT ROWID;

CREATE TABLE members (
    user_id INTEGER REFERENCES users(user_id),
    guild_id INTEGER REFERENCES guilds(guild_id),
    last_peep VARCHAR(19), -- TODO make NOT NULL
    caught_peeps INTEGER DEFAULT(0),
    tries INTEGER DEFAULT(0), -- TODO make NOT NULL
    sent_peeps INTEGER DEFAULT(0), -- TODO make NOT NULL
    received_peeps INTEGER DEFAULT(0), -- TODO make NOT NULL
    PRIMARY KEY (user_id, guild_id)
)
WITHOUT ROWID;

-- TODO rename to psps_channel
CREATE TABLE allowed_channels (
    channel_id INTEGER,
    guild_id INTEGER REFERENCES guilds(guild_id), -- TODO make NOT NULL
    PRIMARY KEY (channel_id)
)
WITHOUT ROWID;

CREATE TABLE role_assigning (
    role_id INTEGER,
    guild_id INTEGER REFERENCES guilds(guild_id),
    PRIMARY KEY (role_id)
)
WITHOUT ROWID;
