import sqlite3

import lib


# add columns to members table
database = sqlite3.connect(lib.get.database_path())
database.execute("""
ALTER TABLE members
ADD (
    sent_peeps INTEGER DEFAULT(0),
    received_peeps INTEGER DEFAULT (0)
)
""")
database.commit()
database.close()

# allow None as value for members_added in logging.guild_join
logging = sqlite3.connect(lib.get.log_path())
logging.executescript(lib.file.load_data("./v0.3.sql"))
logging.commit()
logging.close()
