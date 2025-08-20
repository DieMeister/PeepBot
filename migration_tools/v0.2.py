import sqlite3
import lib


con = sqlite3.connect(lib.get.database_path())

guild_db: list[tuple[int, str, str, str, str]] = []
channel_db: list[tuple[int, int]] = []
member_db: list[tuple[int, int, str, int]] = []

data = lib.load_data("../data.json")
for guild in data["guilds"]:
    guild_entry = (
        guild["guild_id"],
        guild["peep_success_massage"],
        guild["peep_scratch_massage"],
        guild["peep_no_peep_message"],
        guild["last_peep"]
    )
    if guild_entry not in guild_db:
        guild_db.append(guild_entry)
    for channel in guild["allowed_channel_ids"]:
        channel_entry = (
            channel,
            guild["guild_id"]
        )
        if channel_entry not in channel_db:
            channel_db.append(channel_entry)
    for member in guild["members"]:
        member_entry = (
            member["user_id"],
            guild["guild_id"],
            member["execute_psps_timestamp"],
            member["peep_count"]
        )
        if member_entry not in member_db:
            member_db.append(member_entry)

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

print(len(con.execute("""
SELECT * FROM members
""").fetchall()))
con.close()
