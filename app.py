import json
import requests
import streamlit as st

st.set_page_config(
    page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide"
)


def call_super_ai(prompt, agent_name, domain):
  """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq + Llama"""
  url = "https://api.groq.com/openai/v1/chat/completions"
  api_key = st.secrets.get("GROQ_API_KEY", "")

  if not api_key:
    return (
        "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ"
        " Streamlit."
    )

  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json",
  }

  system_prompt = (
      f"You are {agent_name}, an elite Super Agentic AI specialized in"
      f" '{domain}' powered by Meta Llama on Groq. Think step by step. Provide"
      " professional, highly tailored, actionable strategies. Respond in"
      " Moroccan Arabic Darija + العربية الفصحى, with professional formatting,"
      " bullet points, emojis, and tables when needed."
  )

  payload = {
      "model": "llama-3.3-70b-versatile",  # الموديل النشط والمدعوم حالياً لتفادي 404
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt},
      ],
      "temperature": 0.75,
      "max_tokens": 2000,
  }

  try:
    res = requests.post(url, headers=headers, json=payload, timeout=90)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
  except Exception as e:
    return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"


def send_whatsapp_alert(message):
  """إرسال إشعار مباشر عبر واتساب API"""
  try:
    phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
    access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
    target_number = st.secrets.get("WHATSAPP_BUSINESS_NUMBER")
    version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

    if not all([phone_id, access_token, target_number]):
      return

    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
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
        f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة"
        f" لـ: {task} في {self.domain}",
        "Super COO Agent",
        self.domain,
    )

  def copywriter(self, plan):
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
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


# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption(
    "CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq"
)

domain = st.selectbox(
    "اختر المجال",
    ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"],
)
task = st.text_area(
    "وصف المهمة / المشروع",
    placeholder="مثال: بيع بقعة تجارية في قلعة السراغنة",
)

agent = SuperOmegaAgent(domain)

# تهيئة Session State لحفظ النتائج وثباتها
if "result_title" not in st.session_state:
  st.session_state.result_title = ""
if "result_content" not in st.session_state:
  st.session_state.result_content = ""

col1, col2, col3 = st.columns(3)

with col1:
  if st.button("🧠 خطة CEO"):
    with st.spinner("المدير التنفيذي كيخدم..."):
      st.session_state.result_title = "🧠 خطة المدير التنفيذي (CEO)"
      st.session_state.result_content = agent.ceo(task)

with col2:
  if st.button("💻 خطة CTO"):
    with st.spinner("المدير التقني كيخدم..."):
      st.session_state.result_title = "💻 الاستراتيجية التقنية (CTO)"
      st.session_state.result_content = agent.cto(task)

with col3:
  if st.button("📊 خطة COO"):
    with st.spinner("مدير العمليات كيخدم..."):
      st.session_state.result_title = "📊 خطة العمليات (COO)"
      st.session_state.result_content = agent.coo(task)

if st.button("✍️ إنشاء إعلان + إرسال واتساب"):
  with st.spinner("الكاتب والكلوزر كيوجدوا الإعلان..."):
    plan = agent.ceo(task)
    ad = agent.copywriter(plan)
    final_ad = agent.closer(ad)
    st.session_state.result_title = "✍️ الإعلان التسويقي النهائي + FOMO"
    st.session_state.result_content = final_ad
    st.success("تم بنجاح وإرسال الإشعار للواتساب!")

# عرض النتيجة بثبات
if st.session_state.result_content:
  st.markdown("---")
  st.subheader(st.session_state.result_title)
  st.markdown(st.session_state.result_content)
