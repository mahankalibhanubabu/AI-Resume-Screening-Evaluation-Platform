"""
services/file_handler.py
------------------------
Handles all file-related operations:
 - Validation (extension, MIME type, size, magic bytes)
 - Sanitisation (UUID-based filename generation)
 - Persistence (saving to disk)
"""

import os
import uuid
import logging
from typing import Tuple

from fastapi import UploadFile, HTTPException, status

from config import (
    UPLOAD_DIR,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
)

logger = logging.getLogger(__name__)

# PDF magic bytes
_PDF_MAGIC = b"%PDF"


async def validate_and_save_resume(file: UploadFile) -> Tuple[str, str, bytes]:
    """
    Validates the uploaded resume and saves it to disk with a UUID filename.

    Args:
        file: The ``UploadFile`` object received from FastAPI.

    Returns:
        A tuple of ``(absolute_file_path, uuid_filename, raw_bytes)``.

    Raises:
        HTTPException 400: Invalid extension, MIME type, or file content.
        HTTPException 413: File exceeds the configured size limit.
    """
    original_name: str = file.filename or ""

    # ── 1. Extension check ────────────────────────────────────────────────
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{ext or 'unknown'}'. "
                "Only PDF resumes are accepted."
            ),
        )

    # ── 2. MIME-type check ────────────────────────────────────────────────
    content_type: str = file.content_type or ""
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid MIME type '{content_type}'. "
                "Only 'application/pdf' is accepted."
            ),
        )

    # ── 3. Read file into memory ──────────────────────────────────────────
    content: bytes = await file.read()

    # ── 4. Size check ─────────────────────────────────────────────────────
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit.",
        )

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # ── 5. Magic-bytes check (real PDF validation) ────────────────────────
    if not content.startswith(_PDF_MAGIC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid PDF document.",
        )

    # ── 6. Generate a safe, unique filename ───────────────────────────────
    safe_filename = f"{uuid.uuid4()}.pdf"

    # ── 7. Ensure upload directory exists ─────────────────────────────────
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    # ── 8. Persist to disk ────────────────────────────────────────────────
    with open(file_path, "wb") as fh:
        fh.write(content)

    logger.info(
        "Resume saved | original=%s | saved_as=%s | size=%d bytes",
        original_name,
        safe_filename,
        len(content),
    )

    return file_path, safe_filename, content
