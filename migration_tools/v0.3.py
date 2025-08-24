import sqlite3

import lib

con = sqlite3.connect(lib.get.database_path())
con.execute("""
ALTER TABLE members
ADD (
    sent_peeps INTEGER DEFAULT(0),
    received_peeps INTEGER DEFAULT (0)
)
""")