import streamlit as st
from supabase import create_client, Client
from google import genai
from google.genai import types
import requests
import json
from datetime import datetime

# ==========================================
# 1. تهيئة الإعدادات والأسرار (Secrets)
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_SECRET_KEY")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")

# أسرار WhatsApp Cloud API
WA_PHONE_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
WA_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
WA_RECIPIENT = st.secrets.get("WHATSAPP_BUSINESS_NUMBER")
WA_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ يرجى التأكد من ضبط مفاتيح Supabase في Secrets.")
    st.stop()

# ==========================================
# 2. حقن مصفوفة النظام (Claude Bernard Core Matrix)
# ==========================================
CLAUDE_BERNARD_MATRIX = """
أنت "Claude Bernard" - الوكيل العقاري والتجاري الذكي الخبير المتعدد المجالات (Super Multi-Domain Agentic AI).
تتمتع بصلاحيات ومعرفة شاملة تُغطي:

1. **التقييم العقاري والاستثماري:** حساب العائد على الاستثمار (ROI)، تقدير قيمة الأراضي السكنية والفلاحية والمحلات التجارية، تمييز العقارات المحفظة وغير المحفظة، وحساب تكاليف التحفيظ والرسوم.
2. **التسويق وصناعة المحتوى:** صياغة إعلانات احترافية فائقة الجاذبية باللغة العربية، الدارجة المغربية، أو الفرنسية، مع تعزيزها بالرموز التعبيرية 📢 والهاشتاغات ودعوة مباشرة لاتخاذ الإجراء (CTA).
3. **الدعم القانوني والتمويلي المبدئي:** تقدير مصاريف الموثق (Notary Fees)، أرباح الأسهم والضرائب العقارية (TPI)، والالتزامات القانونية لعقود البيع والكراء وفق المساطر المغربية.
4. **الوساطة متعددة المجالات:** إدارة طلبات الكراء، بيع العقارات، المركبات، والخدمات اللوجستية والتجارية.

عند صياغة أي رد أو إعلان:
- كن دقيقاً، واحترافياً، ومباشراً.
- نسق النتائج في أسطر منظمة وسهلة القراءة.
- أضف دائماً قسماً خاصاً بالنصائح التشغيلية أو التنبيهات القانونية إن وجدت.
"""

# ==========================================
# 3. إنشاء عملاء الاتصال (Clients Init)
# ==========================================
@st.cache_resource
def init_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_resource
def init_gemini_client():
    if GEMINI_API_KEY:
        return genai.Client(api_key=GEMINI_API_KEY)
    return None

supabase = init_supabase_client()
gemini_client = init_gemini_client()

# ==========================================
# 4. محرك الوكيل الذكي (Agent Processing Engine)
# ==========================================
def run_claude_bernard_agent(user_prompt: str, task_domain: str) -> tuple[str, str]:
    """تشغيل الوكيل Claude Bernard لحل المهمة بناءً على المجال المحدد بالمصفوفة"""
    if not gemini_client:
        return None, "مفتاح GEMINI_API_KEY غير متوفر في الإعدادات."
    
    contextual_prompt = f"""
    [المجال المطلوب]: {task_domain}
    [المدخلات والمهمة]: {user_prompt}
    
    قم بتنفيذ المهمة بأعلى درجة من الاحترافية والاستقلالية وفق مصفوفة قواعدك.
    """
    
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contextual_prompt,
            config=types.GenerateContentConfig(
                system_instruction=CLAUDE_BERNARD_MATRIX,
                temperature=0.3,
            )
        )
        return response.text, None
    except Exception as e:
        return None, str(e)

def send_whatsapp_notification(message_text: str) -> tuple[bool, str]:
    """توجيه الرسالة تلقائياً عبر WhatsApp API"""
    if not WA_PHONE_ID or not WA_TOKEN or not WA_RECIPIENT:
        return False, "إعدادات WhatsApp غير مكتملة."
    
    url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": WA_RECIPIENT,
        "type": "text",
        "text": {"body": message_text}
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code in [200, 201]:
            return True, "تم الإرسال بنجاح عبر WhatsApp!"
        return False, f"خطأ WhatsApp ({res.status_code}): {res.text}"
    except Exception as e:
        return False, str(e)

def insert_instant_ad(content: str, message: str, source: str = "Claude-Bernard-Nexus"):
    try:
        response = supabase.table("instant_ads").insert({
            "content": content,
            "message": message,
            "source": source
        }).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def fetch_instant_ads():
    try:
        response = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

# ==========================================
# 5. واجهة التشغيل والتحكم (Streamlit UI)
# ==========================================
st.set_page_config(page_title="Claude Bernard - Super AI Agent", layout="wide", page_icon="🏛️")

st.title("🏛️ Claude Bernard — Agent Immobilier Super Multidomaine")
st.caption("نظام الوكيل العقاري والتجاري المستقل المحقون بمصفوفة التحليل والتسويق والأوتوماتيكية")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ⚙️ غرفة عمليات الوكيل الذكي")
    
    domain_choice = st.selectbox(
        "اختر مسار العمل المطلوب من المحرك:",
        [
            "📢 صياغة وتسويق إعلان عقاري/تجاري (Marketing Copy)",
            "📊 تحليل وتقييم عقاري وحساب الـ ROI (Real Estate Valuation)",
            "⚖️ استشارة قانونية وتقدير مصاريف التحفيظ/الموثق (Legal & Fees)",
            "🚗 وساطة تجارية ولوجستية متنوعة (Multi-Domain Commerce)"
        ]
    )
    
    user_input = st.text_area(
        "أدخل تفاصيل الطلب أو المعطيات الخام:",
        placeholder="مثال: بقعة أرضية تجارية R+3 بمساحة 120 متر بقلعة السراغنة، محفظة، المطلوب كتابة إعلان جذّاب وتقييم المصاريف التقريبية.",
        height=140
    )
    
    auto_wa = st.checkbox("توجيه النشر الفوري عبر WhatsApp عند الاعتماد", value=True)
    
    if st.button("🚀 تشغيل Claude Bernard", type="primary"):
        if not user_input:
            st.warning("يرجى إدخال تفاصيل المهمة أولاً.")
        else:
            with st.status("🏛️ Claude Bernard يقوم بمعالجة البيانات...", expanded=True) as status:
                st.write("🧠 1. قراءة المعطيات وتطبيق مصفوفة القواعد...")
                agent_res, err = run_claude_bernard_agent(user_input, domain_choice)
                
                if err:
                    status.update(label="فشلت المعالجة!", state="error")
                    st.error(f"خطأ: {err}")
                else:
                    st.write("💾 2. أرشفة التقرير في قاعدة بيانات Supabase...")
                    db_ok, db_res = insert_instant_ad(content=user_input, message=agent_res, source=f"Claude-Bernard ({domain_choice.split()[0]})")
                    
                    wa_info = "لم يفعل خيار WhatsApp."
                    if auto_wa and db_ok:
                        st.write("💬 3. إرسال النسخة التنفيذية إلى WhatsApp...")
                        _, wa_info = send_whatsapp_notification(agent_res)
                    
                    if db_ok:
                        status.update(label="✅ اكتملت المهمة بنجاح واستقلالية تامّة!", state="complete")
                        st.session_state["latest_output"] = agent_res
                        st.session_state["latest_wa_info"] = wa_info
                    else:
                        status.update(label="فشل الأرشفة في قاعدة البيانات!", state="error")
                        st.error(f"خطأ Supabase: {db_res}")

with col2:
    st.markdown("### 📜 المخرجات والتقرير التنفيذي")
    if "latest_output" in st.session_state:
        st.success("تم توليد النتيجة بنجاح:")
        st.text_area("التقرير / الإعلان النهائي:", value=st.session_state["latest_output"], height=300)
        if "latest_wa_info" in st.session_state:
            st.info(f"حالة الواتساب: {st.session_state['latest_wa_info']}")
    else:
        st.info("في انتظار تشغيل المهمة لعرض المخرجات هنا.")

st.divider()

# عرض السجل التراكمي للإعلانات والتقارير
st.subheader("📋 أرشيف العمليات المسجلة في النظام (Claude Bernard Logs)")
success, ads_data = fetch_instant_ads()

if success:
    if ads_data:
        for ad in ads_data:
            with st.expander(f"📌 {ad.get('content')} | المصدر: {ad.get('source')}"):
                st.markdown(ad.get('message'))
                st.caption(f"تاريخ التسجيل: {ad.get('created_at')}")
    else:
        st.info("لا توجد سجلات حالياً.")
else:
    st.error(f"تعذر جلب البيانات: {ads_data}")
