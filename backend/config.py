"""
config.py
---------
Centralised configuration loader.
All runtime settings are read from environment variables (or a .env file).
Never hardcode URLs, secrets, or paths here.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env file located next to this file (backend/.env)
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)

# ---------------------------------------------------------------------------
# n8n Webhook
# ---------------------------------------------------------------------------
N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "").strip()
if not N8N_WEBHOOK_URL:
    logger.warning("N8N_WEBHOOK_URL is not configured. Set it in the environment or backend/.env.")

# ---------------------------------------------------------------------------
# File Upload Settings
# ---------------------------------------------------------------------------
MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_EXTENSIONS: frozenset = frozenset({".pdf"})
ALLOWED_MIME_TYPES: frozenset = frozenset({"application/pdf"})

# Absolute path to the uploads directory
UPLOAD_DIR: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "uploads"
)

# ---------------------------------------------------------------------------
# API Settings
# ---------------------------------------------------------------------------
API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
API_PORT: int = int(os.getenv("API_PORT", "8000"))

# ---------------------------------------------------------------------------
# n8n Timeout (seconds) — AI analysis can be slow
# ---------------------------------------------------------------------------
N8N_TIMEOUT_SECONDS: float = float(os.getenv("N8N_TIMEOUT_SECONDS", "180"))
