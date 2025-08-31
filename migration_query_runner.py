import sqlite3
import lib

version = "v0.3.1"

match version:
    case "v0.3.0":
        log_db = sqlite3.connect(lib.get.database_path())
        log_db.executescript(lib.file.load_data(f"./migration_queries/{version}/database.sql"))
        log_db.commit()
        log_db.close()

        logging = sqlite3.connect(lib.get.log_path())
        logging.executescript(lib.file.load_data(f"./migration_queries/{version}/logs.sql"))
        logging.commit()
        logging.close()
    case "v0.3.1":
        log_db = sqlite3.connect(lib.get.log_path())
        data_db = sqlite3.connect(lib.get.database_path())
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
