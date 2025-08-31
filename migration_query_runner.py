import sqlite3
import lib

version = "v0.3.0"

database = sqlite3.connect(lib.get.database_path())
database.executescript(lib.file.load_data(f"./migration_queries/{version}/database.sql"))
database.commit()
database.close()

logging = sqlite3.connect(lib.get.log_path())
logging.executescript(lib.file.load_data(f"./migration_queries/{version}/logs.sql"))
logging.commit()
logging.close()
