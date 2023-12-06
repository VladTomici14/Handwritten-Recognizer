# from http.client import HTTPException
from werkzeug.exceptions import HTTPException


def allowed_file(filename):
    file_extension = filename.split(".")[-1] in ("jpg", "jpeg", "png", "webp", "mp4", "mov", "avi")

    if not file_extension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")

