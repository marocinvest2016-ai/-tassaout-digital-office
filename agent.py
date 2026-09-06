import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from groq import BadRequestError, AuthenticationError, APIConnectionError, APIStatusError

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omega_agent.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"

if not GROQ_API_KEY:
    raise RuntimeError(
        "لم يتم العثور على GROQ_API_KEY. أضفه داخل ملف .env ثم أعد التشغيل."
    )

client = Groq(api_key=GROQ_API_KEY)

EXCLUDED_KEYWORDS = [
    "prompt-guard",
    "llama-guard",
    "safeguard",
    "moderation",
    "whisper",
    "speech",
    "tts",
    "audio",
    "transcription",
    "vision",
]

PREFERRED_MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "llama-3.1-8b-instant",
]


def get_active_models() -> list[str]:
    """يجلب قائمة النماذج المتاحة فعلياً في حساب Groq."""
    logger.info("جاري جلب قائمة النماذج من Groq...")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            GROQ_MODELS_URL,
            headers=headers,
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        models = [
            item["id"]
            for item in data.get("data", [])
            if item.get("id")
        ]
        
        logger.info(f"تم العثور على {len(models)} نموذج متاح")
        return models
    
    except requests.RequestException as e:
        logger.error(f"فشل جلب النماذج: {e}")
        raise


def is_valid_agent_model(model_id: str) -> bool:
    """يستبعد نماذج الحماية والتصنيف والصوت."""
    model_name = model_id.lower()
    return not any(
        keyword in model_name
        for keyword in EXCLUDED_KEYWORDS
    )


def select_best_agent_model() -> str:
    """
    يختار أفضل نموذج توليدي متاح.
    لا يختار Prompt Guard كنموذج رئيسي تحت أي ظرف.
    """
    all_models = get_active_models()

    valid_models = [
        model
        for model in all_models
        if is_valid_agent_model(model)
    ]

    if not valid_models:
        logger.error("لم يتم العثور على أي نموذج نصي مناسب")
        raise RuntimeError(
            "لم يتم العثور على أي نموذج نصي مناسب.
