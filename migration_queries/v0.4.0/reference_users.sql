CREATE TABLE new_table (
    user_id INTEGER REFERENCES users(user_id),
    guild_id INTEGER REFERENCES guilds(guild_id),
    last_peep VARCHAR(19),
    caught_peeps INTEGER DEFAULT(0),
    tries INTEGER DEFAULT(0),
    sent_peeps INTEGER DEFAULT(0),
    received_peeps INTEGER DEFAULT(0),
    PRIMARY KEY (user_id, guild_id)
);

INSERT INTO new_table (
    user_id,
    guild_id,
    last_peep,
    caught_peeps,
    tries,
    sent_peeps,
    received_peeps
)
SELECT
    user_id,
    guild_id,
    last_peep,
    caught_peeps,
    tries,
    sent_peeps,
    received_peeps
FROM members
WHERE caught_peeps = 0
    AND tries = 0
    AND sent_peeps = 0
    AND received_peeps = 0;

DROP TABLE members;

ALTER TABLE new_table RENAME TO members;
