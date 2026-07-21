"""
main.py
-------
FastAPI application entry-point for the ATS Resume Analyzer.

Endpoints:
    GET  /health       → Health-check
    POST /api/analyze  → Accepts resume + metadata, triggers n8n, returns ATS JSON
"""

import logging

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import API_HOST, API_PORT, N8N_TIMEOUT_SECONDS, N8N_WEBHOOK_URL
from services.file_handler import validate_and_save_resume
from services.n8n_service import trigger_n8n_workflow

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ATS Resume Analyzer API",
    description=(
        "Accepts resume uploads, forwards them to the n8n AI workflow, "
        "and returns an ATS analysis report in JSON."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict to your domain in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="Health check")
async def health_check() -> dict:
    """Returns the running status of the API."""
    return {"status": "running", "service": "ATS Resume Analyzer API", "version": "2.0.0"}


def _validate_candidate_payload(full_name: str, email: str, linkedin: str) -> None:
    """Performs lightweight validation for the incoming analysis request."""
    if not full_name or not full_name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Full name is required.")

    if "@" not in email or "." not in email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid email address.")

    if not linkedin.startswith(("http://", "https://")) or "linkedin.com" not in linkedin.lower():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid LinkedIn URL.")


# ─────────────────────────────────────────────────────────────────────────────
# Main Analysis Endpoint
# ─────────────────────────────────────────────────────────────────────────────
@app.post(
    "/api/analyze",
    tags=["Analysis"],
    summary="Analyze a resume via the n8n AI workflow",
    response_description="ATS analysis report produced by the n8n Gemini workflow",
)
async def analyze_resume(
    full_name: str = Form(..., description="Candidate's full name"),
    email: str = Form(..., description="Candidate's email address"),
    linkedin: str = Form(..., description="Candidate's LinkedIn profile URL"),
    resume: UploadFile = File(..., description="Resume PDF file (max 5 MB)"),
) -> JSONResponse:
    """
    Accepts a resume PDF plus candidate metadata, validates everything,
    forwards the payload to the n8n webhook, and returns the structured
    ATS analysis produced by Gemini.
    """
    full_name = full_name.strip()
    email = email.strip()
    linkedin = linkedin.strip()
    logger.info("Incoming analysis request | name=%s | email=%s", full_name, email)

    try:
        _validate_candidate_payload(full_name, email, linkedin)
    except HTTPException:
        raise

    try:
        _, safe_filename, resume_bytes = await validate_and_save_resume(resume)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during file handling")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process the uploaded file. Please try again.",
        )

    if not N8N_WEBHOOK_URL:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The n8n webhook URL is not configured.",
        )

    try:
        result = await trigger_n8n_workflow(
            webhook_url=N8N_WEBHOOK_URL,
            timeout_seconds=N8N_TIMEOUT_SECONDS,
            full_name=full_name,
            email=email,
            linkedin=linkedin,
            resume_content=resume_bytes,
            resume_filename=safe_filename,
        )
    except httpx.TimeoutException:
        logger.error("n8n timed out for email=%s", email)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI analysis is taking longer than expected. Please try again in a moment.",
        ) from None
    except httpx.ConnectError:
        logger.error("Cannot connect to n8n at %s", N8N_WEBHOOK_URL)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The analysis service is currently unreachable. Ensure n8n is running and the webhook is active.",
        ) from None
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        logger.error("n8n HTTP error: %s", status_code)
        if status_code == 404:
            detail = "The n8n webhook path could not be found. Please activate the workflow and confirm the webhook URL."
        else:
            detail = f"Analysis service returned an error ({status_code})."
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail) from None
    except ValueError as exc:
        logger.error("n8n response parse error: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Received an unreadable response from the analysis service.",
        ) from None
    except Exception:
        logger.exception("Unexpected error during n8n workflow trigger")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        ) from None

    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": True, "data": result})


# ─────────────────────────────────────────────────────────────────────────────
# Dev Entry-Point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
        log_level="info",
    )