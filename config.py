# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "output"
LOGS_FOLDER = BASE_DIR / "logs"

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

ATS_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.3,
    "education": 0.2,
    "keywords": 0.1,
}

LOG_LEVEL = "INFO"
LOG_FILE = LOGS_FOLDER / "app.log"