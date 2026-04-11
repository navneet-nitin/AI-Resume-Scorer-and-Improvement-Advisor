from app.config import MAX_PDF_SIZE_BYTES


def validate_pdf(file_name: str | None, file_bytes: bytes, content_type: str | None = None) -> None:
    normalized_content_type = (content_type or "").lower()

    if normalized_content_type.startswith("image/"):
        raise ValueError("IMAGE_FILE_UPLOADED")

    if not file_name or not file_name.lower().endswith(".pdf"):
        raise ValueError("INVALID_FILE_TYPE")

    if normalized_content_type and normalized_content_type not in {"application/pdf", "application/x-pdf"}:
        raise ValueError("INVALID_FILE_TYPE")

    if not file_bytes:
        raise ValueError("EMPTY_FILE")

    if len(file_bytes) > MAX_PDF_SIZE_BYTES:
        raise ValueError("FILE_TOO_LARGE")

    if not file_bytes.startswith(b"%PDF"):
        raise ValueError("INVALID_FILE_CONTENT")
