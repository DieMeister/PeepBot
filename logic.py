import datetime
from datetime import datetime as dt

def log(message: str, module: str) -> None:
    timestamp = dt.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{timestamp}] [{module:8}] {message}")