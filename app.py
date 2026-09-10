import json
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Tassaout Méga Fort | OMEGA Super Agentic AI",
    page_icon="👑",
    layout="wide",
)


def call_super_ai(prompt, agent_name):
  """محرك الذكاء الاصطناعي الفائق - Groq + Llama 3.3"""
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
      f"You are {agent_name}, an elite Super Agentic AI powered by Meta Llama"
      " on Groq. Think step by step. Provide professional, highly tailored,"
      " ethical, and actionable strategies. Respond in Moroccan Arabic Darija"
      " + العربية الفصحى, with professional formatting, bullet points, emojis,"
      " and tables when needed."
  )

  payload = {
      "model": "llama-3.3-70b-versatile",
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

  def ceo(self):
    return call_super_ai(
        "ضع خطة استراتيجية شاملة وتنافسية متكاملة. عطيني SWOT + الميزة التنافسية"
        " + خطة 90 يوم",
        "Super CEO Agent",
    )

  def cto(self):
    return call_super_ai(
        "اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور"
        " الرقمي بدقة",
        "Super CTO Agent",
    )

  def coo(self):
    return call_super_ai(
        "ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة للعمليات",
        "Super COO Agent",
    )

  def run_autonomous_pipeline(self):
    plan = self.ceo()
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
    copy_prompt = (
        f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية احترافية وأخلاقية"
        " باللهجة المغربية والفصحى، مع تمييزها بـ '### الإعلان الأول'، '### الإعلان"
        " الثاني'، '### الإعلان الثالث'، ودعوة للاتصال برقم الواتساب:"
        f" {whatsapp_num}"
    )
    draft_ads = call_super_ai(copy_prompt, "Super Copywriter Agent")
    closer_prompt = (
        f"قم بتحسين الإعلانات الثلاثة وإضافة محفزات الاستعجال FOMO والضمانات"
        " الشفافة مع الحفاظ على نفس التسميات: {draft_ads}"
    )
    final_ads = call_super_ai(closer_prompt, "Super Closer Agent")
    send_whatsapp_alert(f"👑 Tassaout Méga Fort\n\n{final_ads}")
    return plan, final_ads


st.title("👑 Tassaout Méga Fort - OMEGA Super Agentic AI")
st.caption(
    "بدون قوائم منسدلة أو حقول نصية - 6 أزرار تشغيلية فورية عبر Groq Llama 3.3"
)

agent = SuperOmegaAgent()

if "results" not in st.session_state:
  st.session_state.results = None

# 6 أزرار تشغيلية موزعة بوضوح
col1, col2, col3 = st.columns(3)

with col1:
  btn_ceo = st.button("🧠 1. تحليل واستراتيجية CEO")
  btn_pipeline = st.button("🚀 4. تشغيل الحملة الكاملة + واتساب", type="primary")

with col2:
  btn_cto = st.button("💻 2. الاستراتيجية التقنية CTO")
  btn_whatsapp_test = st.button("💬 5. إرسال اختبار سريع للواتساب")

with col3:
  btn_coo = st.button("📊 3. الخطة التشغيلية COO")
  btn_reset = st.button("🔄 6. مسح النتائج")

if btn_ceo:
  with st.spinner("المدير التنفيذي يحلل الاستراتيجية..."):
    st.session_state.results = ("ceo", agent.ceo())

if btn_cto:
  with st.spinner("المدير التقني يجهز البنية..."):
    st.session_state.results = ("cto", agent.cto())

if btn_coo:
  with st.spinner("مدير العمليات يضبط الجدول..."):
    st.session_state.results = ("coo", agent.coo())

if btn_pipeline:
  with st.spinner(
      "الوكلاء يعملون في الخلفية (خطة + إعلانات موثوقة + واتساب)..."
  ):
    plan, final_ads = agent.run_autonomous_pipeline()
    st.session_state.results = ("pipeline", (plan, final_ads))
    st.success("تم تنفيذ المنطق وتوليد الحملة وإرسالها للواتساب بنجاح!")

if btn_whatsapp_test:
  with st.spinner("جاري إرسال رسالة تجريبية عبر الواتساب..."):
    send_whatsapp_alert(
        "👑 اختبار ناجح من منصة Tassaout Méga Fort عبر WhatsApp API!"
    )
    st.success("تم إرسال رسالة الواتساب بنجاح!")

if btn_reset:
  st.session_state.results = None
  st.rerun()

if st.session_state.results:
  res_type, res_data = st.session_state.results
  if res_type in ["ceo", "cto", "coo"]:
    st.markdown("---")
    st.subheader(f"📋 نتيجة تحليل الـ {res_type.upper()} الفائق")
    st.markdown(res_data)
    st.download_button(
        label=f"📥 تحميل تقرير {res_type.upper()} (.txt)",
        data=res_data,
        file_name=f"Tassaout_{res_type.upper()}_Report.txt",
        mime="text/plain",
    )
  elif res_type == "pipeline":
    plan, final_ads = res_data
    st.markdown("---")
    with st.expander("📋 معاينة الخطة الاستراتيجية الكاملة (CEO)"):
      st.markdown(plan)

    st.markdown("---")
    st.subheader("📢 البطاقات الإعلانية الملونة والموثوقة")
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
              label=f"📥 تحميل البطاقة الإعلانية رقم {idx} (.txt)",
              data=card_content,
              file_name=f"Tassaout_Mega_Fort_Ad_{idx}.txt",
              mime="text/plain",
              key=f"download_btn_{idx}",
          )
          st.markdown("<br>", unsafe_allow_html=True)
    else:
      with st.container():
        st.markdown(
            f"""
                <div style="background-color: #f8fafc; border-right: 6px solid #4F46E5; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.06);">
                    <h3 style="margin-top: 0; color: #1F2937;">🏷️ البطاقات الإعلانية</h3>
                    <div style="color: #374151; font-size: 16px; line-height: 1.7; white-space: pre-wrap;">{final_ads}</div>
                </div>
                """,
            unsafe_allow_html=True,
        )
        st.download_button(
            label="📥 تحميل الحملة الإعلانية كاملة (.txt)",
            data=final_ads,
            file_name="Tassaout_Mega_Fort_Campaign.txt",
            mime="text/plain",
            key="download_btn_all",
        )

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 15px; font-weight:"
    " bold;'>"
    "إنتاج السيد عامر بوخدادة | جهة مراكش آسفي | كل الحقوق محفوظة 2026 👑"
    "</div>",
    unsafe_allow_html=True,
)
