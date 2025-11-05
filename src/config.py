import os
from dotenv import load_dotenv

load_dotenv()

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

