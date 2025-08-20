import sqlite3
import lib


con = sqlite3.connect(lib.get.database_path())

guild_db: list[tuple[int, str, str, str, str]] = []
channel_db: list[tuple[int, int]] = []
member_db: list[tuple[int, int, str, int]] = []

data = lib.load_data("test_data.json")
for guild in data["guilds"]:
    guild_db.append((
        guild["guild_id"],
        guild["peep_success_massage"],
        guild["peep_scratch_massage"],
        guild["peep_no_peep_message"],
        guild["last_peep"]
    ))
    for channel in guild["allowed_channel_ids"]:
        channel_db.append((
            channel,
            guild["guild_id"]
        ))
    for member in guild["members"]:
        member_db.append((
            member["user_id"],
            guild["guild_id"],
            member["execute_psps_timestamp"],
            member["peep_count"]
        ))

con.executemany("""
INSERT INTO guilds(guild_id, success_message, scratch_message, no_peep_message, last_peep)
VALUES(?,?,?,?,?)
""", guild_db)
con.executemany("""
INSERT INTO members (user_id, guild_id, last_peep, caught_peeps)
VALUES(?,?,?,?)
""", member_db)
con.executemany("""
INSERT INTO allowed_channels (channel_id, guild_id)
VALUES(?,?)
""", channel_db)

con.commit()
con.close()
