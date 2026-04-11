import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:
            page_text = []

            for page in document:
                text = page.get_text("text").strip()
                if text:
                    page_text.append(text)

        extracted_text = "\n\n".join(page_text).strip()
        if not extracted_text:
            raise ValueError("TEXT_EXTRACTION_FAILED")

        alpha_numeric_count = sum(char.isalnum() for char in extracted_text)
        if alpha_numeric_count < 80:
            raise ValueError("TEXT_EXTRACTION_FAILED")

        return extracted_text

    except ValueError:
        raise
    except Exception as e:
        print(f"PDF EXTRACTION ERROR: {e!r}")
        raise ValueError("TEXT_EXTRACTION_FAILED")
