from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import PROMPT_TEXT_LIMIT
from app.services.gemini_service import analyze_with_gemini
from app.services.pdf_service import extract_text_from_pdf
from app.services.supabase_service import (
    insert_resume_record,
    update_resume_result,
    upload_pdf,
)
from app.utils.prompt_builder import build_prompt
from app.utils.validators import validate_pdf

router = APIRouter()


@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    user_email: str = Form(None),
):
    try:
        # 🔹 Read file
        file_bytes = await file.read()

        # 🔹 Step 1: Validate PDF
        validate_pdf(file.filename, file_bytes, file.content_type)

        # 🔹 Step 2: Upload PDF to Supabase Storage
        file_url = upload_pdf(file_bytes, file.filename or "resume.pdf")

        # 🔹 Step 3: Extract text
        extracted_text = extract_text_from_pdf(file_bytes)

        if not extracted_text or len(extracted_text.strip()) < 100:
            raise ValueError("TEXT_EXTRACTION_FAILED")

        # 🔹 Step 4: Trim text
        trimmed_text = extracted_text[:PROMPT_TEXT_LIMIT]

        # 🔹 Step 5: Insert initial DB record (IMPORTANT FIX)
        submission_id = insert_resume_record(
            file_url=file_url,
            preview_text=trimmed_text,
            user_email=user_email   # ✅ FIXED
        )

        # 🔹 Step 6: Build prompt
        prompt = build_prompt(trimmed_text)

        # 🔹 Step 7: Call Gemini
        result = analyze_with_gemini(prompt)

        # 🔹 Step 8: Update DB with result
        update_resume_result(submission_id, result)

        # 🔹 Step 9: Return response
        return {
            "submission_id": submission_id,
            "file_url": file_url,
            **result
        }

    except ValueError as exc:
        error_code = str(exc)
        print(f"ANALYZE RESUME VALUE ERROR: {error_code}")

        if error_code == "IMAGE_FILE_UPLOADED":
            raise HTTPException(status_code=400, detail="Upload a PDF, not an image.")
        if error_code in {"INVALID_FILE_TYPE", "INVALID_FILE_CONTENT"}:
            raise HTTPException(status_code=400, detail="Upload a valid PDF.")
        if error_code == "EMPTY_FILE":
            raise HTTPException(status_code=400, detail="The file is empty.")
        if error_code == "FILE_TOO_LARGE":
            raise HTTPException(status_code=400, detail="Upload a PDF up to 5MB.")
        if error_code == "TEXT_EXTRACTION_FAILED":
            raise HTTPException(status_code=422, detail="This PDF has no readable text. Upload a text-based PDF.")
        if error_code in {"AI_API_ERROR", "INVALID_JSON_FROM_AI", "INCOMPLETE_JSON_FROM_AI", "EMPTY_AI_RESPONSE"}:
            raise HTTPException(status_code=500, detail="Resume analysis failed. Please try again.")
        if error_code == "FILE_UPLOAD_FAILED":
            raise HTTPException(status_code=500, detail="Could not upload the PDF.")
        if error_code == "DB_INSERT_FAILED":
            raise HTTPException(status_code=500, detail="Could not create the submission.")
        if error_code == "DB_UPDATE_FAILED":
            raise HTTPException(status_code=500, detail="Could not save the analysis result.")
        if error_code == "SUPABASE_NOT_CONFIGURED":
            raise HTTPException(status_code=500, detail="Storage is not configured.")

        raise HTTPException(status_code=500, detail="Something went wrong.")

    except Exception as exc:
        print("UNEXPECTED ERROR:", repr(exc))
        raise HTTPException(status_code=500, detail="Something went wrong.")
