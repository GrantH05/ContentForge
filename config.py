import os
from dotenv import load_dotenv

load_dotenv()

# ContentForge AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CONTENTFORGE_VERSION = "1.0.0"

BRAND_RULES = {
    "banned_words": ["fake", "guarantee", "100%", "miracle"],
    "tone": "professional, confident, enterprise-focused",
    "name": "ContentForge AI"
}
