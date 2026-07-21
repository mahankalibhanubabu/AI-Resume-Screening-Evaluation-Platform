"""
services/n8n_service.py
-----------------------
Async service layer that triggers the n8n ATS Resume Analyzer webhook.

Responsibilities:
 - Build a multipart/form-data payload (full_name, email, linkedin, resume PDF)
 - POST to the configured N8N_WEBHOOK_URL
 - Parse and normalise the JSON response
 - Translate every possible failure into a clear, typed exception
"""

import logging
from typing import Any, Dict

import httpx

logger = logging.getLogger(__name__)


async def trigger_n8n_workflow(
    *,
    webhook_url: str,
    timeout_seconds: float,
    full_name: str,
    email: str,
    linkedin: str,
    resume_content: bytes,
    resume_filename: str,
) -> Dict[str, Any]:
    """
    Sends candidate data and resume to the n8n webhook and returns the
    ATS analysis JSON produced by the workflow.
    """
    if not webhook_url:
        raise ValueError("N8N_WEBHOOK_URL is not configured.")

    timeout = httpx.Timeout(timeout_seconds)
    files = {
        "resume": (resume_filename, resume_content, "application/pdf"),
    }
    data = {
        "full_name": full_name,
        "email": email,
        "linkedin": linkedin,
    }

    logger.info(
        "→ Triggering n8n | url=%s | candidate=%s | email=%s",
        webhook_url,
        full_name,
        email,
    )

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(webhook_url, files=files, data=data)
    except httpx.TimeoutException:
        logger.error("n8n workflow timed out for candidate=%s", full_name)
        raise
    except httpx.ConnectError as exc:
        logger.error("Unable to connect to n8n at %s", webhook_url)
        raise httpx.ConnectError("Unable to connect to the n8n webhook.") from exc
    except httpx.RequestError as exc:
        logger.exception("Network error while contacting n8n")
        raise httpx.ConnectError("Unable to reach the n8n webhook.") from exc

    response.raise_for_status()

    try:
        result: Any = response.json()
    except Exception as exc:
        preview = response.text[:300]
        logger.error("Non-JSON response from n8n: %s", preview)
        raise ValueError(f"n8n returned an unreadable response: {preview}") from exc

    if isinstance(result, list):
        if not result:
            raise ValueError("n8n returned an empty response array.")
        result = result[0]

    if isinstance(result, dict) and "json" in result:
        result = result["json"]

    if not isinstance(result, dict):
        raise ValueError(f"Unexpected response shape from n8n: {type(result).__name__}")

    logger.info(
        "✓ n8n workflow complete | candidate=%s | ats_score=%s",
        result.get("candidate_name", "unknown"),
        result.get("ats_score", "N/A"),
    )

    return result
