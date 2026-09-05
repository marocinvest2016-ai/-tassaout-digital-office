import json
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide"
)


# ===== 1. دالة اختيار النماذج (تلقائي + يدوي) =====
@st.cache_data
def get_available_groq_models(api_key):
  """كيجيب لائحة الموديلات المتاحة من المنصة"""
  if not api_key:
    return ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "groq/compound"]

  url = "https://api.groq.com/openai/v1/models"
  headers = {"Authorization": f"Bearer {api_key}"}
  try:
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    models = [m["id"] for m in res.json().get("data", [])]
    return models if models else ["llama-3.3-70b-versatile"]
  except:
    return [
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
        "qwen/qwen2.5-72b-instruct",
        "groq/compound",
    ]


def get_default_best_model(models_list):
  """كيختار أحسن موديل للعربية والدارجة تلقائيا كقيمة افتراضية"""
  priority = [
      "llama-3.3-70b-versatile",
      "openai/gpt-oss-120b",
      "qwen/qwen2.5-72b-instruct",
      "groq/compound",
  ]
  for preferred in priority:
    if preferred in models_list:
      return preferred
  return models_list[0] if models_list else "llama-3.3-70b-versatile"


# ===== 2. المحرك الرئيسي =====
def call_super_ai(prompt, agent_name, domain, model_name):
  url = "https://api.groq.com/openai/v1/chat/completions"
  api_key = st.secrets.get("GROQ_API_KEY", "")

  if not api_key:
    return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets"

  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json",
  }

  system_prompt = (
      f"You are {agent_name}, an elite Super Agentic AI specialized in"
      f" '{domain}' powered by advanced LLMs on Groq. Think step by step."
      " Provide professional, highly tailored, actionable strategies. Respond"
      " in Moroccan Arabic Darija + العربية الفصحى, with professional"
      " formatting, bullet points, emojis, and tables when needed."
  )

  payload = {
      "model": model_name,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt},
      ],
      "temperature": 0.75,
      "max_tokens": 3000,
  }

  try:
    res = requests.post(url, headers=headers, json=payload, timeout=120)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
  except Exception as e:
    return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"


# ===== 3. إرسال الواتساب =====
def send_whatsapp_alert(message):
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


# ===== 4. محرك توليد الفيديو الذكي =====
def generate_ai_video(prompt_text, domain, model_name):
  prompt = (
      f"قم بصياغة سيناريو إعلاني بصري احترافي (Storyboard) لمدة 3 دقائق"
      f" لمشروع في مجال '{domain}' بناءً على هذا الوصف: {prompt_text}."
      " اعطيني تفاصيل كل مشهد (Légende, Angle de caméra, Voix off) بالدارجة والعربية."
  )
  return call_super_ai(
      prompt, "Super Video Director Agent", domain, model_name
  )


class SuperOmegaAgent:

  def __init__(self, domain, model):
    self.domain = domain
    self.model = model

  def ceo(self, task):
    return call_super_ai(
        f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال"
        f" {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم",
        "Super CEO Agent",
        self.domain,
        self.model,
    )

  def cto(self, task):
    return call_super_ai(
        f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني،"
        f" واستهداف الجمهور الرقمي لـ: {task} في {self.domain}",
        "Super CTO Agent",
        self.domain,
        self.model,
    )

  def coo(self, task):
    return call_super_ai(
        f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة"
        f" لـ: {task} في {self.domain}",
        "Super COO Agent",
        self.domain,
        self.model,
    )

  def copywriter(self, plan):
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
    prompt = (
        f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة"
        " المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة"
        f" للاتصال برقم الواتساب: {whatsapp_num}"
    )
    ad = call_super_ai(
        prompt, "Super Copywriter Agent", self.domain, self.model
    )
    send_whatsapp_alert(
        f"👑 OMEGA SUPER AGENTIC v29.0\nالمجال والمشروع: {self.domain}\n\n{ad}"
    )
    return ad

  def closer(self, ad):
    prompt = (
        "قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات"
        f" لزيادة المبيعات: {ad}"
    )
    return call_super_ai(prompt, "Super Closer Agent", self.domain, self.model)


# ===== 5. واجهة Streamlit & Sidebar Control =====
st.title("👑 OMEGA Super Agentic AI - V12 NEXUS")
st.caption(
    "نظام الوكلاء الأذكياء المفتوح لكافة القطاعات مع التحكم في النماذج"
)

api_key = st.secrets.get("GROQ_API_KEY", "")
available_models = get_available_groq_models(api_key)
default_model = get_default_best_model(available_models)

# إعدادات الـ Sidebar لاختيار الموديل يدوياً أو تركها تلقائية
st.sidebar.header("⚙️ إعدادات المحرك (Model Nexus)")
mode_selection = st.sidebar.radio(
    "طريقة اختيار الموديل:", ["تلقائي (Auto-Model الذكي)", "اختيار يدوي"]
)

if mode_selection == "تلقائي (Auto-Model الذكي)":
  selected_model = default_model
  st.sidebar.success(f"المحرك النشط (تلقائي): `{selected_model}` ⚡")
else:
  selected_model = st.sidebar.selectbox(
      "اختر الموديل يدوياً:",
      available_models,
      index=(
          available_models.index(default_model)
          if default_model in available_models
          else 0
      ),
  )
  st.sidebar.info(f"المحرك النشط (يدوي): `{selected_model}` 🎯")

# حقل حر مفتوح لإدخال أي مجال أو قطاع دون قيود
domain = st.text_input(
    "حدد المجال أو القطاع (مثال: العقار، التجارة الرقمية، اللوجستيك، الفلاحة...)",
    placeholder="أدخل المجال هنا...",
)
task = st.text_area(
    "وصف المهمة / المشروع",
    placeholder="مثال: تسويق وبناء منصة رقمية لبيع بقع أرضية بقلعة السراغنة",
)

if "result_title" not in st.session_state:
  st.session_state.result_title = ""
if "result_content" not in st.session_state:
  st.session_state.result_content = ""

if domain and task:
  agent = SuperOmegaAgent(domain, selected_model)

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    if st.button("🧠 خطة CEO", use_container_width=True):
      with st.spinner("المدير التنفيذي كيخدم..."):
        st.session_state.result_title = f"🧠 خطة المدير التنفيذي (CEO) - {domain}"
        st.session_state.result_content = agent.ceo(task)
  with col2:
    if st.button("💻 خطة CTO", use_container_width=True):
      with st.spinner("المدير التقني كيخدم..."):
        st.session_state.result_title = (
            f"💻 الاستراتيجية التقنية (CTO) - {domain}"
        )
        st.session_state.result_content = agent.cto(task)
  with col3:
    if st.button("📊 خطة COO", use_container_width=True):
      with st.spinner("مدير العمليات كيخدم..."):
        st.session_state.result_title = f"📊 خطة العمليات (COO) - {domain}"
        st.session_state.result_content = agent.coo(task)
  with col4:
    if st.button("🎬 توليد فيديو", use_container_width=True):
      with st.spinner("مخرج الفيديو الذكي كيوجد الستوري بورد..."):
        st.session_state.result_title = (
            f"🎬 سيناريو فيديو احترافي (3 دقائق) - {domain}"
        )
        st.session_state.result_content = generate_ai_video(
            task, domain, selected_model
        )

  if st.button("✍️ إنشاء إعلان + إرسال واتساب", use_container_width=True):
    with st.spinner("الكاتب والكلوزر كيوجدوا الإعلان بالدارجة..."):
      plan = agent.ceo(task)
      ad = agent.copywriter(plan)
      final_ad = agent.closer(ad)
      st.session_state.result_title = f"✍️ الإعلان التسويقي النهائي + FOMO"
      st.session_state.result_content = final_ad
      st.success("تم بنجاح وإرسال الإشعار للواتساب!")
else:
  st.info("المرجو ملء خانة 'المجال' وخانة 'وصف المهمة' لتفعيل أزرار الوكلاء.")

if st.session_state.result_content:
  st.markdown("---")
  st.subheader(st.session_state.result_title)
  st.markdown(st.session_state.result_content)
