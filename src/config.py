import os
from dotenv import load_dotenv

# Load .env file (only in local development, Vercel uses environment variables)
# Vercel automatically provides environment variables, so dotenv is optional
if os.path.exists(".env"):
    load_dotenv()

# PORT is not needed in Vercel (it's serverless), but keep for local development
PORT = int(os.getenv("PORT", "8000"))

# WhatsApp
WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN", "")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "")

# Home Assistant
HA_BASE_URL = os.getenv("HA_BASE_URL", "").rstrip("/")
HA_TOKEN = os.getenv("HA_TOKEN", "")
HA_TIMEOUT_MS = int(os.getenv("HA_TIMEOUT_MS", "5000"))

# Seguridad
ALLOWED_NUMBERS = [x.strip() for x in os.getenv("ALLOWED_NUMBERS", "").split(",") if x.strip()]
DEFAULT_AREA = os.getenv("DEFAULT_AREA", "living")

