import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq
from groq import BadRequestError, AuthenticationError, APIConnectionError, APIStatusError

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
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        GROQ_MODELS_URL,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    return [
        item["id"]
        for item in data.get("data", [])
        if item.get("id")
    ]


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
        raise RuntimeError(
            "لم يتم العثور على أي نموذج نصي مناسب. "
            "تحقق من صلاحية مفتاح Groq ومن قائمة النماذج في حسابك."
        )

    for preferred_model in PREFERRED_MODELS:
        if preferred_model in valid_models:
            return preferred_model

    return valid_models[0]


def run_omega_agent(domain: str, project_description: str) -> dict:
    """تشغيل أدوار OMEGA وإرجاع خطة منظمة بصيغة JSON."""
    active_model = select_best_agent_model()

    system_prompt = """
أنت OMEGA Super Agentic AI، وكيل أعمال متعدد الأدوار.

تعمل في الوقت نفسه كالتالي:
- CEO: تحدد الرؤية، الأهداف، الأولويات، ومؤشرات النجاح.
- CTO: تقترح البنية التقنية، الأدوات، التكاملات، وخطة التنفيذ.
- COO: تنشئ إجراءات تشغيل واضحة، توزيع مهام، ومراحل التنفيذ.
- Copywriter: تكتب محتوى تسويقياً مقنعاً بالعربية.
- Closer: تنشئ رسالة واتساب مختصرة وقوية لتحويل العميل إلى إجراء.

قواعد مهمة:
1. أجب باللغة العربية الواضحة، مع استعمال الفرنسية عند الحاجة في أسماء الأدوات.
2. لا تدّعِ تنفيذ أي إجراء خارجي مثل إرسال واتساب أو نشر إعلان.
3. أعطِ نتائج عملية قابلة للتنفيذ.
4. خصص جميع الاقتراحات للمجال والمشروع المعطيين.
5. أرجع JSON صالحاً فقط، بدون Markdown أو شرح خارج JSON.

استعمل البنية التالية بالضبط:
{
  "ceo_plan": {
    "vision": "",
    "objectives": [],
    "priorities": [],
    "kpis": []
  },
  "cto_plan": {
    "recommended_stack": [],
    "automation_workflow": [],
    "implementation_steps": []
  },
  "coo_plan": {
    "operations": [],
    "timeline": [],
    "responsibilities": []
  },
  "marketing_copy": {
    "title": "",
    "short_ad": "",
    "long_ad": "",
    "cta": ""
  },
  "whatsapp_message": ""
}
""".strip()

    user_prompt = f"""
المجال المختار: {domain}

وصف المهمة أو المشروع:
{project_description}

أنشئ الآن الخطة الكاملة والمحتوى التسويقي ورسالة واتساب.
""".strip()

    try:
        completion = client.chat.completions.create(
            model=active_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=2500,
            response_format={"type": "json_object"},
        )

        raw_result = completion.choices[0].message.content

        try:
            result = json.loads(raw_result)
        except json.JSONDecodeError:
            result = {
                "raw_response": raw_result
            }

        return {
            "success": True,
            "active_model": active_model,
            "result": result
        }

    except BadRequestError as error:
        return {
            "success": False,
            "active_model": active_model,
            "error_type": "BAD_REQUEST",
            "message": "Groq رفض الطلب. تحقق من إعدادات النموذج والـ payload.",
            "details": str(error)
        }

    except AuthenticationError as error:
        return {
            "success": False,
            "active_model": active_model,
            "error_type": "AUTHENTICATION_ERROR",
            "message": "مفتاح GROQ_API_KEY غير صحيح أو منتهي الصلاحية.",
            "details": str(error)
        }

    except APIConnectionError as error:
        return {
            "success": False,
            "active_model": active_model,
            "error_type": "CONNECTION_ERROR",
            "message": "تعذر الاتصال بخوادم Groq. تحقق من الإنترنت.",
            "details": str(error)
        }

    except APIStatusError as error:
        return {
            "success": False,
            "active_model": active_model,
            "error_type": "GROQ_API_ERROR",
            "message": f"حدث خطأ من Groq برمز الحالة {error.status_code}.",
            "details": str(error)
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "active_model": None,
            "error_type": "MODELS_ENDPOINT_ERROR",
            "message": "تعذر جلب قائمة النماذج المتاحة من Groq.",
            "details": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "active_model": None,
            "error_type": "UNEXPECTED_ERROR",
            "message": "حدث خطأ غير متوقع.",
            "details": str(error)
        }


if __name__ == "__main__":
    domain = input("اختر المجال: ").strip()
    project_description = input("وصف المهمة / المشروع: ").strip()

    if not domain or not project_description:
        print("
❌ المرجو إدخال المجال ووصف المشروع.")
        raise SystemExit(1)

    print("
⏳ جارٍ اكتشاف أفضل نموذج متاح وتشغيل OMEGA...
")

    response = run_omega_agent(domain, project_description)

    if response["success"]:
        print(f"✅ النموذج التنفيذي المختار: {response['active_model']}
")
        print(json.dumps(
            response["result"],
            ensure_ascii=False,
            indent=2
        ))
    else:
        print(f"❌ نوع الخطأ: {response['error_type']}")
        print(f"❌ الرسالة: {response['message']}")
        print(f"🔎 التفاصيل: {response['details']}")
