import sqlite3

import lib
from lib import config
from lib.utils import load_file

version = "v0.4.0"

match version:
    case "v0.3.0":
        log_db = sqlite3.connect(config.data_db_path())
        log_db.executescript(load_file(f"./migration_queries/{version}/database.sql"))
        log_db.commit()
        log_db.close()

        logging = sqlite3.connect(lib.get.log_path())
        logging.executescript(load_file(f"./migration_queries/{version}/logs.sql"))
        logging.commit()
        logging.close()
    case "v0.3.1":
        log_db = sqlite3.connect(lib.get.log_path())
        data_db = sqlite3.connect(config.data_db_path())
        data_db.execute("""
        UPDATE members
        SET
            received_peeps = 0,
            sent_peeps = 0
        """)
        data_db.commit()

        transfers = log_db.execute("""
        SELECT log_id, peep_amount, recipient_id
        FROM peep_transfer
        """).fetchall()

        for i in transfers:
            log_id: int
            amount: int
            recipient: int
            guild: int
            sender: int
            received_peeps: int
            sent_peeps: int

            log_id, amount, recipient = i
            guild, sender = log_db.execute("""
            SELECT guild_id, user_id
            FROM commands
            WHERE log_id = ?
            """, (log_id,)).fetchone()

            received_peeps = data_db.execute("""
            SELECT received_peeps
            FROM members
            WHERE guild_id = ?
            AND user_id = ?
            """, (guild, recipient)).fetchone()[0]

            sent_peeps = data_db.execute("""
            SELECT sent_peeps
            FROM members
            WHERE guild_id = ?
            AND user_id = ?
            """, (guild, sender)).fetchone()[0]

            data_db.execute("""
            UPDATE members
            SET received_peeps = ?
            WHERE guild_id = ?
            AND user_id = ?
            """, ((received_peeps + amount), guild, recipient))
            data_db.commit()

            data_db.execute("""
            UPDATE members
            SET sent_peeps = ?
            WHERE guild_id = ?
            AND user_id = ?
            """, ((sent_peeps + amount), guild, sender))
            data_db.commit()
        data_db.close()
        log_db.close()
    case "v0.4.0":
        data_db = sqlite3.connect(config.data_db_path())
        # Create users table
        data_db.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            stolen_peeps INTEGER
        )""")
        data_db.commit()

        # get all user ids
        members = data_db.execute("""
        SELECT user_id
        FROM members
        """).fetchall()
        users = []
        for i in members:
            user_id = i[0]
            if (user_id,) not in users:
                users.append((user_id,))
        # add users to database
        data_db.executemany("""
        INSERT INTO users (user_id)
        VALUES (?)
        """, users)
        data_db.commit()

        # alter members table to reference users table
        data_db.executescript(load_file("./migration_queries/v0.4.0/data_db.sql"))
        data_db.commit()

        # add logging table
        log_db = sqlite3.connect(config.log_db_path())
        log_db.executescript(load_file("./migration_queries/v0.4.0/log_db.sql"))
        log_db.commit()
        log_db.close()
