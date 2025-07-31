import lib


def developer() -> list:
    return lib.config["people"]["developer"]


def vip() -> list:
    return lib.config["people"]["vip"]


def vup() -> list:
    return lib.config["people"]["vup"]


def embed_color() -> int:
    return lib.config["embed_color"]


def database_path() -> str:
    return lib.config["file_paths"]["database"]


def database_backup_path() -> str:
    return lib.config["file_paths"]["database_saves"]


def log_path() -> str:
    return lib.config["file_paths"]["logs"]


def datetime_format() -> str:
    return lib.config["datetime_formats"]["datetime"]


def date_format() -> str:
    return lib.config["datetime_formats"]["date"]