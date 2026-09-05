import json
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide"
)

DEFAULT_WHATSAPP = "+212691897126"

# تنسيق الخط العربي واتجاه الصفحة
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"], div, p, h1, h2, h3, h4, span, label, input, select, textarea, button {
        font-family: 'Cairo', sans-serif !important;
        text-align: right;
        direction: rtl;
    }
</style>
""",
    unsafe_allow_html=True,
)


def call_super_ai(prompt, agent_name, domain):
  url = "https://api.groq.com/openai/v1/chat/completions"

  api_key = ""
  try:
    api_key = st.secrets.get("GROQ_API_KEY", "")
  except Exception:
    pass

  if not api_key:
    api_key = os.environ.get("GROQ_API_KEY", "") or st.session_state.get(
        "GROQ_API_KEY", ""
    )

  if not api_key:
    return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets أو الشريط الجانبي."

  headers = {
      "Authorization": f"Bearer {api_key.strip()}",
      "Content-Type": "application/json",
  }

  system_prompt = (
      f"You are {agent_name}, an elite Super Agentic AI specialized in"
      f" '{domain}' powered by Meta Llama on Groq. Think step by step. Provide"
      " professional, highly tailored, actionable strategies. Respond in"
      " Moroccan Arabic Darija + العربية الفصحى, with professional formatting,"
      " bullet points, emojis, and tables when needed."
  )

  # النماذج المعتمدة والنشطة حالياً على Groq
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
        "max_tokens": 2000,
    }

    try:
      res = requests.post(url, headers=headers, json=payload, timeout=90)
      if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
      else:
        try:
          err_json = res.json()
          last_error = err_json.get("error", {}).get("message", res.text)
        except Exception:
          last_error = f"Status {res.status_code}: {res.text}"
    except Exception as e:
      last_error = str(e)

  return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {last_error}"


def send_whatsapp_alert(message):
  try:
    phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "")
    access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "")
    target_number = st.secrets.get(
        "WHATSAPP_BUSINESS_NUMBER", DEFAULT_WHATSAPP
    )
    version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

    if not all([phone_id, access_token, target_number]):
      return

    target_number = (
        str(target_number).replace("+", "").replace(" ", "").strip()
    )
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
    st.warning(f"تعذر إرسال إشعار الواتساب: {e}")


class SuperOmegaAgent:

  def __init__(self, domain):
    self.domain = domain

  def ceo(self, task):
    return call_super_ai(
        f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال"
        f" {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم",
        "Super CEO Agent",
        self.domain,
    )

  def cto(self, task):
    return call_super_ai(
        f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني،"
        f" واستهداف الجمهور الرقمي لـ: {task} في {self.domain}",
        "Super CTO Agent",
        self.domain,
    )

  def coo(self, task):
    return call_super_ai(
        f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية"
        f" دقيقة لـ: {task} في {self.domain}",
        "Super COO Agent",
        self.domain,
    )

  def copywriter(self, plan):
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", DEFAULT_WHATSAPP)
    prompt = (
        f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة"
        " المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة"
        f" للاتصال برقم الواتساب: {whatsapp_num}"
    )
    ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
    send_whatsapp_alert(
        f"👑 OMEGA SUPER AGENTIC v4.1\nمهمة جديدة في مجال:"
        f" {self.domain}\n\n{ad}"
    )
    return ad

  def closer(self, ad):
    prompt = (
        "قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات"
        f" لزيادة المبيعات: {ad}"
    )
    return call_super_ai(prompt, "Super Closer Agent", self.domain)


# الشريط الجانبي
with st.sidebar:
  st.markdown("### 👑 إعدادات المنظومة")
  custom_key = st.text_input(
      "مفتاح GROQ_API_KEY (اختياري):",
      type="password",
      value=st.session_state.get("GROQ_API_KEY", ""),
  )
  if custom_key:
    st.session_state["GROQ_API_KEY"] = custom_key
  st.caption("✅ الموديل: `llama-3.3-70b-versatile`")

# الواجهة الرئيسية
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq")

domain = st.selectbox(
    "اختر المجال",
    ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"],
)
task = st.text_area(
    "وصف المهمة / المشروع",
    value="Appartements à vendre sur kelaa sraghna",
    height=90,
)

agent = SuperOmegaAgent(domain)

col1, col2, col3 = st.columns(3)
with col1:
  if st.button("🧠 خطة CEO", use_container_width=True):
    with st.spinner("المدير التنفيذي كيخدم..."):
      st.markdown(agent.ceo(task))
with col2:
  if st.button("💻 خطة CTO", use_container_width=True):
    with st.spinner("المدير التقني كيخدم..."):
      st.markdown(agent.cto(task))
with col3:
  if st.button("📊 خطة COO", use_container_width=True):
    with st.spinner("مدير العمليات كيخدم..."):
      st.markdown(agent.coo(task))

st.divider()

if st.button(
    "✍️ إنشاء إعلان + إرسال واتساب", use_container_width=True, type="primary"
):
  with st.spinner("الكاتب كيكتب الإعلان..."):
    plan = agent.ceo(task)
    if plan.startswith("❌ خطأ"):
      st.error(plan)
    else:
      ad = agent.copywriter(plan)
      final_ad = agent.closer(ad)
      st.success("تم بنجاح!")
      st.markdown(final_ad)
