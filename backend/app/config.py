import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "").strip()

MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024
PDF_PREVIEW_LENGTH = 500
