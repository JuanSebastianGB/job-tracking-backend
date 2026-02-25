import random
import string
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from app.config import settings


def get_upload_path() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR).resolve()
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

    extension = Path(upload_file.filename).suffix if upload_file.filename else ""

    unique_filename = f"{timestamp}_{random_suffix}{extension}"

    dest_path = Path(destination_dir) / unique_filename
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, "wb") as f:
        content = upload_file.file.read()
        f.write(content)

    return unique_filename
