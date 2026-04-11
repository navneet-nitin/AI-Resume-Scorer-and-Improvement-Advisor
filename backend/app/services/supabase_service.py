import re
import uuid
from datetime import datetime, timezone

from supabase import create_client

from app.config import (
    PDF_PREVIEW_LENGTH,
    SUPABASE_BUCKET_NAME,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
)

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    supabase = None
else:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def _require_supabase():
    if supabase is None or not SUPABASE_BUCKET_NAME:
        print("SUPABASE ERROR: Missing configuration")
        raise ValueError("SUPABASE_NOT_CONFIGURED")
    return supabase


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", filename or "resume.pdf")
    sanitized = sanitized.strip("._") or "resume"
    if not sanitized.lower().endswith(".pdf"):
        sanitized = f"{sanitized}.pdf"
    return sanitized


def upload_pdf(file_bytes: bytes, filename: str) -> str:
    try:
        client = _require_supabase()
        file_id = str(uuid.uuid4())
        safe_filename = sanitize_filename(filename)
        file_path = f"resumes/{file_id}_{safe_filename}"

        client.storage.from_(SUPABASE_BUCKET_NAME).upload(
            file_path,
            file_bytes,
            {"content-type": "application/pdf", "x-upsert": "false"},
        )

        file_url = client.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(file_path)
        if not file_url:
            raise ValueError("FILE_UPLOAD_FAILED")

        return file_url

    except ValueError:
        raise
    except Exception as exc:
        print("UPLOAD ERROR:", str(exc))
        raise ValueError("FILE_UPLOAD_FAILED")


def insert_resume_record(file_url: str, preview_text: str, user_email: str | None = None) -> str:
    try:
        client = _require_supabase()
        data = {
            "file_url": file_url,
            "extracted_text_preview": preview_text[:PDF_PREVIEW_LENGTH],
            "user_email": user_email,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        response = client.table("resume_submissions").insert(data).execute()
        if not response.data:
            raise ValueError("DB_INSERT_FAILED")

        return response.data[0]["id"]

    except ValueError:
        raise
    except Exception as exc:
        print("DB INSERT ERROR:", str(exc))
        raise ValueError("DB_INSERT_FAILED")


def update_resume_result(submission_id: str, result: dict) -> None:
    try:
        client = _require_supabase()
        response = client.table("resume_submissions").update(
            {
                "overall_score": result.get("overall_score"),
                "grade": result.get("grade"),
                "full_result_json": result,
            }
        ).eq("id", submission_id).execute()

        if not response.data:
            raise ValueError("DB_UPDATE_FAILED")

    except ValueError:
        raise
    except Exception as exc:
        print("DB UPDATE ERROR:", str(exc))
        raise ValueError("DB_UPDATE_FAILED")
