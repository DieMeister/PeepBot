-- create reference from members.user_id to users.user_id
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
WHERE caught_peeps <> 0
    OR tries <> 0
    OR sent_peeps <> 0
    OR received_peeps <> 0;

DROP TABLE members;

ALTER TABLE new_table RENAME TO members;

-- delete users without any entry
DELETE FROM users
WHERE user_id NOT IN (
	SELECT user_id
	FROM members
);
