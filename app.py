import streamlit as st
import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# إعداد الصفحة
st.set_page_config(
    page_title="👑 OMEGA AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #888;
        margin-bottom: 3rem;
    }
    .button-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-top: 3rem;
    }
    .stButton > button {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1.5rem 3rem;
        border-radius: 1rem;
        height: 80px;
    }
    .status-box {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        font-size: 1rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<h1 class="main-header">👑 OMEGA AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">وكيل أعمال ذكي متكامل</p>', unsafe_allow_html=True)

# مفتاح API (مخفي)
if "GROQ_API_KEY" in os.environ:
    groq_api_key = os.environ["GROQ_API_KEY"]
else:
    groq_api_key = st.text_input("🔑 Groq API Key", type="password", value="", key="api_key_input", label_visibility="collapsed")

# System Prompt (مخفي في دماغ الوكيل)
SYSTEM_PROMPT = """
أنت OMEGA Super Agentic AI، وكيل أعمال ذكي.

تعمل كـ CEO + CTO + COO + Copywriter + Closer في نفس الوقت.

أرجع JSON بهذه البنية:
{
  "ceo_plan": {"vision": "", "objectives": [], "priorities": [], "kpis": []},
  "cto_plan": {"recommended_stack": [], "automation_workflow": [], "implementation_steps": []},
  "coo_plan": {"operations": [], "timeline": [], "responsibilities": []},
  "marketing_copy": {"title": "", "short_ad": "", "long_ad": "", "cta": ""},
  "whatsapp_message": "",
  "generated_images": [{"description": "", "prompt": "", "style": ""}]
}
""".strip()

# زر التشغيل الرئيسي
if st.button("🚀 تشغيل OMEGA", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("❌ أدخل مفتاح Groq API")
        st.stop()
    
    logger.info("بدء OMEGA...")
    
    # تهيئة العميل
    client = Groq(api_key=groq_api_key)
    
    with st.spinner("🧠 جاري التفكير..."):
        try:
            # جلب النماذج
            GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json",
            }
            
            response = requests.get(GROQ_MODELS_URL, headers=headers, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            all_models = [item["id"] for item in data.get("data", []) if item.get("id")]
            
            # تصفية النماذج
            EXCLUDED_KEYWORDS = [
                "prompt-guard", "llama-guard", "safeguard", "moderation",
                "whisper", "speech", "tts", "audio", "transcription", "vision",
            ]
            
            valid_models = [
                model for model in all_models
                if not any(kw in model.lower() for kw in EXCLUDED_KEYWORDS)
            ]
            
            if not valid_models:
                st.error("❌ لم يتم العثور على نماذج صالحة")
                st.stop()
            
            # اختيار النموذج
            PREFERRED_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
            active_model = None
            for preferred in PREFERRED_MODELS:
                if preferred in valid_models:
                    active_model = preferred
                    break
            
            if not active_model:
                active_model = valid_models[0]
            
            # استدعاء API
            completion = client.chat.completions.create(
                model=active_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": "أنشئ خطة أعمال متكاملة لمشروع جديد"}
                ],
                temperature=0.7,
                max_completion_tokens=2500,
                response_format={"type": "json_object"},
            )
            
            raw_result = completion.choices[0].message.content
            result = json.loads(raw_result)
            
            # حفظ في session state
            st.session_state.omega_result = result
            st.session_state.omega_timestamp = datetime.now().isoformat()
            
            logger.info("اكتمل OMEGA بنجاح")
            st.success("✅ تم إنشاء الخطة بنجاح!")
            
            # حفظ في ملف
            os.makedirs("omega_results", exist_ok=True)
            output_file = f"omega_results/omega_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            st.info(f"💾 حُفظ في: {output_file}")
        
        except Exception as e:
            logger.error(f"خطأ: {e}", exc_info=True)
            st.error(f"❌ خطأ: {str(e)}")

# عرض حالة آخر تشغيل
if "omega_timestamp" in st.session_state:
    timestamp = st.session_state.omega_timestamp
    st.markdown(f'<div class="status-box">🕐 آخر تشغيل: {timestamp[:19]}</div>', unsafe_allow_html=True)

# الأزرار دائمًا متاحة
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# زر تحميل الصور
if "omega_result" in st.session_state:
    result = st.session_state.omega_result
    images = result.get("generated_images", [])
    
    if images:
        images_text = "

".join([
            f"🖼️ صورة {i}
"
            f"الوصف: {img.get('description', 'N/A')}
"
            f"Prompt: {img.get('prompt', 'N/A')}
"
            f"Style: {img.get('style', 'N/A')}"
            for i, img in enumerate(images, 1)
        ])
        
        st.download_button(
            label="📥 تحميل الصور",
            data=images_text,
            file_name=f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.download_button(
            label="📥 تحميل الصور",
            data="لا توجد صور في هذه الجلسة

شغّل OMEGA لإنشاء صور جديدة",
            file_name=f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
else:
    st.download_button(
        label="📥 تحميل الصور",
        data="لا توجد صور بعد

اضغط على 'تشغيل OMEGA' أولاً",
        file_name=f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# زر واتساب
if "omega_result" in st.session_state:
    result = st.session_state.omega_result
    whatsapp_msg = result.get("whatsapp_message", "")
    
    if whatsapp_msg:
        st.download_button(
            label="📱 رسالة واتساب",
            data=whatsapp_msg,
            file_name=f"whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.download_button(
            label="📱 رسالة واتساب",
            data="لا توجد رسالة واتساب

شغّل OMEGA لإنشاء رسالة",
            file_name=f"whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
else:
    st.download_button(
        label="📱 رسالة واتساب",
        data="لا توجد رسالة بعد

اضغط على 'تشغيل OMEGA' أولاً",
        file_name=f"whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# التذييل
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888; margin-top: 3rem;">👑 OMEGA AI | يعمل على Groq 🚀</p>', unsafe_allow_html=True)
