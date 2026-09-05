import json
import os
import urllib.parse
import requests
import streamlit as st

st.set_page_config(
    page_title="OMEGA Super Agentic AI", 
    page_icon="👑", 
    layout="wide"
)

# رقم الواتساب المعتمد
DEFAULT_WHATSAPP = "+212691897126"

# تحسين مظهر الخطوط والاتجاه للغة العربية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"], div, p, h1, h2, h3, h4, span, label, input, select, textarea, button {
        font-family: 'Cairo', sans-serif !important;
        text-align: right;
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)


def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq + Llama"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # محاولة جلب المفتاح من Secrets أو من المتغيرات البيئية أو من حقل الإدخال
    api_key = ""
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "") or st.session_state.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit أو في الشريط الجانبي."

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' "
        "powered by Meta Llama on Groq. Think step by step. Provide professional, "
        "highly tailored, actionable strategies. Respond in Moroccan Arabic Darija + العربية الفصحى, "
        "with professional formatting, bullet points, emojis, and tables when needed."
    )

    # استخدام الموديل الأحدث llama-3.3-70b-versatile مع بديل سريع لتجنب أي 400 Bad Request
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

    last_error = ""
    for model_name in models_to_try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.75,
            "max_tokens": 2048,
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=90)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
            else:
                # استخراج رسالة الخطأ الدقيقة لتوضيح السبب
                try:
                    err_json = res.json()
                    last_error = err_json.get("error", {}).get("message", res.text)
                except Exception:
                    last_error = f"Status {res.status_code}: {res.text}"
        except Exception as e:
            last_error = str(e)

    return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {last_error}"


def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب API الرسمي مع حماية ضد الانهيار"""
    try:
        phone_id = ""
        access_token = ""
        target_number = ""
        version = "v20.0"

        try:
            phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
            access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
            target_number = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", DEFAULT_WHATSAPP)
            version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")
        except Exception:
            pass

        if not all([phone_id, access_token, target_number]):
            return

        target_number = str(target_number).replace("+", "").replace(" ", "").strip()
        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token.strip()}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message[:4096]},
        }
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        st.warning(f"تعذر إرسال إشعار الواتساب التلقائي: {e}")


class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        return call_super_ai(
            f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم",
            "Super CEO Agent",
            self.domain,
        )

    def cto(self, task):
        return call_super_ai(
            f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}",
            "Super CTO Agent",
            self.domain,
        )

    def coo(self, task):
        return call_super_ai(
            f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}",
            "Super COO Agent",
            self.domain,
        )

    def copywriter(self, plan):
        whatsapp_num = DEFAULT_WHATSAPP
        try:
            whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", DEFAULT_WHATSAPP)
        except Exception:
            pass

        prompt = (
            f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        )
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(
            f"👑 OMEGA SUPER AGENTIC v4.1\nمهمة جديدة في مجال: {self.domain}\n\n{ad}"
        )
        return ad

    def closer(self, ad):
        prompt = (
            f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        )
        return call_super_ai(prompt, "Super Closer Agent", self.domain)


# ===== الشريط الجانبي (Sidebar) =====
with st.sidebar:
    st.markdown("### 👑 إعدادات المنظومة")
    whatsapp_display = DEFAULT_WHATSAPP
    try:
        whatsapp_display = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", DEFAULT_WHATSAPP)
    except Exception:
        pass

    st.info(f"📞 رقم الواتساب المعتمد: `{whatsapp_display}`")

    # خيار لإدخال المفتاح مباشرة إن لم يكن متوفراً في secrets
    custom_key = st.text_input(
        "مفتاح GROQ_API_KEY (اختياري):",
        type="password",
        value=st.session_state.get("GROQ_API_KEY", ""),
        help="يمكنك وضع المفتاح هنا مباشرة أو وضعه في Streamlit Secrets."
    )
    if custom_key:
        st.session_state["GROQ_API_KEY"] = custom_key

    st.caption("✅ الموديل المعتمد: `llama-3.3-70b-versatile`")


# ===== واجهة Streamlit الرئيسية =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq")

domain = st.selectbox(
    "اختر المجال",
    ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"],
)

task = st.text_area(
    "وصف المهمة / المشروع",
    value="Appartements à vendre sur kelaa sraghna",
    placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة",
    height=90
)

agent = SuperOmegaAgent(domain)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 خطة CEO", use_container_width=True):
        if not task.strip():
            st.warning("يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("المدير التنفيذي كيخدم..."):
                st.markdown(agent.ceo(task))

with col2:
    if st.button("💻 خطة CTO", use_container_width=True):
        if not task.strip():
            st.warning("يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("المدير التقني كيخدم..."):
                st.markdown(agent.cto(task))

with col3:
    if st.button("📊 خطة COO", use_container_width=True):
        if not task.strip():
            st.warning("يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("مدير العمليات كيخدم..."):
                st.markdown(agent.coo(task))

st.divider()

if st.button("✍️ إنشاء إعلان + إرسال واتساب", use_container_width=True, type="primary"):
    if not task.strip():
        st.warning("يرجى إدخال وصف المهمة أولاً.")
    else:
        with st.spinner("الكاتب كيكتب الإعلان والخبير كيغلق الصفقة..."):
            plan = agent.ceo(task)
            
            # التحقق إذا كانت استجابة الـ CEO خطأ
            if plan.startswith("❌ خطأ"):
                st.error(plan)
            else:
                ad = agent.copywriter(plan)
                final_ad = agent.closer(ad)

                st.success("تم بنجاح وإعداد الإعلان التسويقي النهائي!")
                st.markdown("### ✍️ الإعلان التسويقي النهائي + FOMO")
                st.markdown(final_ad)

                # زر سريع للمحادثة والمشاركة عبر الواتساب بنقرة واحدة
                target_wa = whatsapp_display.replace("+", "").replace(" ", "").strip()
                encoded_msg = urllib.parse.quote(final_ad[:1500])
                wa_direct_url = f"https://wa.me/{target_wa}?text={encoded_msg}"

                st.markdown(f"""
                <div style="background-color:#25D366; padding:12px 18px; border-radius:12px; text-align:center; margin-top:15px;">
                    <a href="{wa_direct_url}" target="_blank" style="color:white; font-weight:bold; text-decoration:none; font-size:16px;">
                        📲 فتح ومشاركة الإعلان مباشرة على واتساب ({whatsapp_display})
                    </a>
                </div>
                """, unsafe_allow_html=True)
