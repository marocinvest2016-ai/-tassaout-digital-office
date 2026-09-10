import json
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Tassaout Méga Fort | OMEGA Super Agentic AI",
    page_icon="👑",
    layout="wide",
)

# النموذج النشط والصحيح رسمياً من Groq
GROQ_MODEL = "llama-3.3-70b-versatile"


def call_super_ai(prompt, agent_name, domain):
  """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq + Llama 3.3"""
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
      "model": GROQ_MODEL,
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
    st.session_state.last_model = GROQ_MODEL
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

  def run_autonomous_pipeline(self, task):
    plan = self.ceo(task)
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
    copy_prompt = (
        f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية احترافية وأخلاقية"
        " باللهجة المغربية والفصحى، مع تمييزها بـ '### الإعلان الأول'، '### الإعلان"
        " الثاني'، '### الإعلان الثالث'، ودعوة للاتصال برقم الواتساب:"
        f" {whatsapp_num}"
    )
    draft_ads = call_super_ai(copy_prompt, "Super Copywriter Agent", self.domain)
    closer_prompt = (
        "قم بتحسين الإعلانات الثلاثة وإضافة محفزات الاستعجال FOMO والضمانات"
        f" الشفافة مع الحفاظ على نفس التسميات: {draft_ads}"
    )
    final_ads = call_super_ai(closer_prompt, "Super Closer Agent", self.domain)
    send_whatsapp_alert(
        f"👑 Tassaout Méga Fort\nمجال: {self.domain}\n\n{final_ads}"
    )
    return plan, final_ads


# ===== واجهة Streamlit التشغيلية =====
st.title("👑 Tassaout Méga Fort - OMEGA Super Agentic AI v5.0")
st.caption(
    "نظام الوكلاء الأذكياء المتعدد المجالات (عقار، تجارة، خدمات) مع ربط مباشر"
    " بالواتساب والرفع"
)

domain = st.selectbox(
    "اختر المجال",
    [
        "العقار والخدمات بجهة مراكش آسفي",
        "التجارة الإلكترونية",
        "المطاعم والضيافة",
        "التعليم والتكوين",
        "التسويق الرقمي",
    ],
)
task = st.text_area(
    "وصف المهمة / المشروع / العقار",
    placeholder="مثال: تسويق وبيع شقق سكنية أو بقع أرضية بقلعة السراغنة ومراكش",
)

agent = SuperOmegaAgent(domain)

if "results" not in st.session_state:
  st.session_state.results = None

# أزرار التشغيل والتحكم
col1, col2, col3, col4 = st.columns(4)

with col1:
  btn_ceo = st.button("🧠 تحليل واستراتيجية CEO")
  btn_cto = st.button("💻 الاستراتيجية التقنية CTO")

with col2:
  btn_coo = st.button("📊 الخطة التشغيلية COO")
  btn_pipeline = st.button("🚀 تشغيل الحملة الكاملة + واتساب", type="primary")

with col3:
  btn_upload = st.button("🖼️ رفع ومعالجة الصور")

with col4:
  btn_reset = st.button("🔄 مسح النتائج")

# معالجة الأزرار
if btn_ceo:
  with st.spinner("المدير التنفيذي يحلل الاستراتيجية بدقة..."):
    st.session_state.results = ("ceo", agent.ceo(task))

if btn_cto:
  with st.spinner("المدير التقني يجهز البنية والبايثون..."):
    st.session_state.results = ("cto", agent.cto(task))

if btn_coo:
  with st.spinner("مدير العمليات يضبط مؤشرات الأداء..."):
    st.session_state.results = ("coo", agent.coo(task))

if btn_pipeline:
  with st.spinner("الوكلاء يكتبون الحملة ويجهزون الواتساب..."):
    plan, final_ads = agent.run_autonomous_pipeline(task)
    st.session_state.results = ("pipeline", (plan, final_ads))
    st.success("تم توليد الحملة وإرسالها للواتساب بنجاح!")

if btn_upload:
  st.session_state.results = ("upload", None)

if btn_reset:
  st.session_state.results = None
  st.rerun()

# منطقة عرض النتائج
if st.session_state.results:
  res_type, res_data = st.session_state.results
  st.info(f"🤖 النموذج المستخدم: `{GROQ_MODEL}`")

  if res_type in ["ceo", "cto", "coo"]:
    st.markdown("---")
    st.subheader(f"📋 تقرير الـ {res_type.upper()} الفائق")
    st.markdown(res_data)
    st.download_button(
        label=f"📥 تحميل التقرير (.txt)",
        data=res_data,
        file_name=f"Tassaout_{res_type.upper()}_Report.txt",
        mime="text/plain",
    )

  elif res_type == "pipeline":
    plan, final_ads = res_data
    st.markdown("---")
    with st.expander("📋 معاينة الخطة الاستراتيجية الكاملة"):
      st.markdown(plan)

    st.markdown("---")
    st.subheader("📢 البطاقات الإعلانية الاحترافية")
    parts = final_ads.split("### الإعلان")
    card_colors = [
        "background-color: #f0f7ff; border-right: 6px solid #1E3A8A;",
        "background-color: #f4fbf7; border-right: 6px solid #059669;",
        "background-color: #fffbeb; border-right: 6px solid #D97706;",
    ]

    if len(parts) > 1:
      for idx, part in enumerate(parts[1:], 1):
        color_style = card_colors[(idx - 1) % len(card_colors)]
        card_content = f"### الإعلان {idx}\n" + part.strip()
        with st.container():
          st.markdown(
              f"""
                    <div style="{color_style} padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.06);">
                        <h3 style="margin-top: 0; color: #1F2937;">🏷️ البطاقة الإعلانية رقم {idx}</h3>
                        <div style="color: #374151; font-size: 16px; line-height: 1.7; white-space: pre-wrap;">{part.strip()}</div>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
          st.download_button(
              label=f"📥 تحميل البطاقة رقم {idx} (.txt)",
              data=card_content,
              file_name=f"Tassaout_Ad_{idx}.txt",
              mime="text/plain",
              key=f"dl_{idx}",
          )
    else:
      st.markdown(final_ads)
      st.download_button(
          label="📥 تحميل الحملة كاملة (.txt)",
          data=final_ads,
          file_name="Tassaout_Campaign.txt",
          mime="text/plain",
      )

  elif res_type == "upload":
    st.markdown("---")
    st.subheader("🖼️ مركز رفع المعاينة والصور العقارية والتسويقية")
    uploaded_file = st.file_uploader(
        "اختر صورة الإعلان أو العقار لرفعها", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file is not None:
      st.success("تم رفع الصورة ومعاينتها بنجاح في النظام!")
      st.image(
          uploaded_file, caption="معاينة الصورة المرفوعة", use_container_width=True
      )
      st.info("💬 الصورة جاهزة للربط مع منشوراتك والحملات الدعائية 👑")

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 15px; font-weight:"
    " bold;'>"
    "إنتاج السيد عامر بوخدادة | جهة مراكش آسفي | قلعة السراغنة 2026 👑"
    "</div>",
    unsafe_allow_html=True,
)
