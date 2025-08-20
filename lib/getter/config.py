data: dict

def developer() -> list:
    return data["people"]["developer"]


def vip() -> list:
    return data["people"]["vip"]


def vup() -> list:
    return data["people"]["vup"]


def embed_color() -> int:
    return data["embed_color"]


def database_path() -> str:
    return data["file_paths"]["database"]


def database_backup_path() -> str:
    return data["file_paths"]["database_saves"]


def log_path() -> str:
    return data["file_paths"]["logs"]


def datetime_format() -> str:
    return data["datetime_formats"]["datetime"]


def discord_dt_format() -> str:
    return data["datetime_formats"]["discord"]


def date_format() -> str:
    return data["datetime_formats"]["date"]


def database_query() -> str:
    return data["sql_table_queries"]["database"]


def log_query() -> str:
    return data["sql_table_queries"]["logs"]


def thieves() -> dict:
    return data["people"]["thieves"]


def log_channel_missing() -> str:
    return data["messages"]["log_channel_missing"]
