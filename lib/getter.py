config: dict

def developer() -> list:
    return config["people"]["developer"]


def vip() -> list:
    return config["people"]["vip"]


def vup() -> list:
    return config["people"]["vup"]


def embed_color() -> int:
    return config["embed_color"]


def database_path() -> str:
    return config["file_paths"]["database"]


def database_backup_path() -> str:
    return config["file_paths"]["database_saves"]


def log_path() -> str:
    return config["file_paths"]["logs"]


def datetime_format() -> str:
    return config["datetime_formats"]["datetime"]


def date_format() -> str:
    return config["datetime_formats"]["date"]


def database_query() -> str:
    return config["sql_table_queries"]["database"]


def log_query() -> str:
    return config["sql_table_queries"]["logs"]