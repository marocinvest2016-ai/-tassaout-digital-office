import json
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Tassaout Méga Fort | OMEGA Super Agentic AI",
    page_icon="👑",
    layout="wide",
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
      "model": "llama-3.3-70b-versatile",  # تم تحديث اسم الموديل ليتوافق تماماً مع المعايير الحديثة لمنصة Groq وتجنب خطأ 400
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
        f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack"
        f" تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}",
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
        f"بناءً على هذه الخطة: {plan}. اكتب بالضبط 3 إعلانات تسويقية جذابة"
        " ومفصولة تماماً عن بعضها. قم بتتمييز كل إعلان بالعنوان التالي حرفياً:"
        " '### الإعلان الأول'، '### الإعلان الثاني'، '### الإعلان الثالث'."
        " استخدم اللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية،"
        f" هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
    )
    ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
    send_whatsapp_alert(
        f"👑 Tassaout Méga Fort\nمهمة جديدة في مجال: {self.domain}\n\n{ad}"
    )
    return ad

  def closer(self, ad):
    prompt = (
        f"قم بتحسين هذه الإعلانات الثلاثة وإضافة محفزات الاستعجال FOMO + ضمان +"
        " شهادات لزيادة المبيعات. يجب أن تحافظ بحرفية تامة على تقسيم الإعلانات"
        " الثلاثة وتستخدم نفس العناوين بانتظام: '### الإعلان الأول'، '### الإعلان"
        f" الثاني'، '### الإعلان الثالث': {ad}"
    )
    return call_super_ai(prompt, "Super Closer Agent", self.domain)


# ===== واجهة Streamlit =====
st.title("👑 Tassaout Méga Fort")
st.caption(
    "OMEGA Super Agentic AI | CEO + CTO + COO + Copywriter + Closer في وكيل"
    " واحد يخدم على Groq"
)

domain = st.selectbox(
    "اختر المجال",
    ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"],
)
task = st.text_area(
    "وصف المهمة / المشروع",
    placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة",
)

agent = SuperOmegaAgent(domain)

col1, col2, col3 = st.columns(3)

with col1:
  if st.button("🧠 خطة CEO"):
    with st.spinner("المدير التنفيذي كيخدم..."):
      st.markdown(agent.ceo(task))
with col2:
  if st.button("💻 خطة CTO"):
    with st.spinner("المدير التقني كيخدم..."):
      st.markdown(agent.cto(task))
with col3:
  if st.button("📊 خطة COO"):
    with st.spinner("مدير العمليات كيخدم..."):
      st.markdown(agent.coo(task))

if st.button("✍️ إنشاء إعلان + إرسال واتساب"):
  with st.spinner("الكاتب والكلوزر كيخدمو على الإعلانات..."):
    plan = agent.ceo(task)
    ad = agent.copywriter(plan)
    final_ad = agent.closer(ad)
    st.success("تم توليد الإعلانات وإرسالها بنجاح!")

    st.markdown("---")
    st.subheader("📢 البطاقات الإعلانية الملونة والسيادية")

    parts = final_ad.split("### الإعلان")
    card_colors = [
        "background-color: #f0f7ff; border-right: 6px solid #1E3A8A;",  # أزرق
        "background-color: #f4fbf7; border-right: 6px solid #059669;",  # أخضر
        (
            "background-color: #fffbeb; border-right: 6px solid #D97706;"
        ),  # أصفر ذهبي
    ]

    if len(parts) > 1:
      for idx, part in enumerate(parts[1:], 1):
        color_style = card_colors[(idx - 1) % len(card_colors)]
        with st.container():
          st.markdown(
              f"""
                    <div style="{color_style} padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <h3 style="margin-top: 0; color: #1F2937;">🏷️ البطاقة الإعلانية رقم {idx}</h3>
                        <div style="color: #374151; font-size: 16px; line-height: 1.6;">
                            {part}
                        </div>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
    else:
      with st.container():
        st.markdown(
            f"""
                <div style="background-color: #f8fafc; border-right: 6px solid #4F46E5; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h3 style="margin-top: 0; color: #1F2937;">🏷️ البطاقات الإعلانية</h3>
                    <div style="color: #374151; font-size: 16px; line-height: 1.6;">
                        {final_ad}
                    </div>
                </div>
                """,
            unsafe_allow_html=True,
        )

# ====================== تذييل الموقع ======================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 15px; font-weight:"
    " bold;'>"
    "إنتاج السيد عامر بوخدادة | جهة مراكش آسفي | كل الحقوق محفوظة 2026 👑"
    "</div>",
    unsafe_allow_html=True,
)
