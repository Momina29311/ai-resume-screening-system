from pathlib import Path
from datetime import datetime

def create_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def write_text(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")

def log_message(message: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")