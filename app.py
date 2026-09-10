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
  """محرك الذكاء الاصطناعي الفائق - Groq + Llama"""
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
      " professional, highly tailored, ethical, and actionable strategies."
      " Never generate fake reviews or false testimonials. Rely on real value,"
      " authentic guarantees, and transparent facts. Respond in Moroccan"
      " Arabic Darija + العربية الفصحى, with professional formatting, bullet"
      " points, emojis, and tables when needed."
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

  def __init__(self, domain):
    self.domain = domain if domain else "عام"

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

  def run_autonomous_pipeline(self, task):
    """المنطق الخلفي التلقائي: CEO يخطط -> Copywriter يصيغ 3 إعلانات أخلاقية -> Closer يحسنها بالمصداقية والـ FOMO الحقيقي"""
    plan = self.ceo(task)

    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
    copy_prompt = (
        f"بناءً على هذه الخطة الاستراتيجية: {plan}. اكتب بالضبط 3 إعلانات تسويقية"
        " احترافية وأخلاقية جذابة ومفصولة تماماً عن بعضها في مجال (تركيزك على: "
        f"{self.domain}). تجنب تماماً أي شهادات كاذبة أو وهمية، وركز على القيمة"
        " الحقيقية والشفافية. قم بتمييز كل إعلان بالعنوان التالي حرفياً: '###"
        " الإعلان الأول'، '### الإعلان الثاني'، '### الإعلان الثالث'."
        " استخدم اللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية،"
        f" هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
    )
    draft_ads = call_super_ai(
        copy_prompt, "Super Copywriter Agent", self.domain
    )

    closer_prompt = (
        f"قم بتحسين هذه الإعلانات الثلاثة وإضافة محفزات الاستعجال الحقيقية FOMO"
        " (مثل: محدودية العرض، الأسبقية) والضمانات المهنية والشفافة بعيداً عن أي"
        " مبالغات أو شهادات كاذبة. حافظ بحرفية تامة على تقسيم الإعلانات الثلاثة"
        " ونفس العناوين: '### الإعلان الأول'، '### الإعلان الثاني'، '### الإعلان"
        f" الثالث': {draft_ads}"
    )
    final_ads = call_super_ai(closer_prompt, "Super Closer Agent", self.domain)

    send_whatsapp_alert(
        f"👑 Tassaout Méga Fort\nالمجال: {self.domain}\n\n{final_ads}"
    )

    return plan, final_ads


# ===== واجهة Streamlit التفاعلية =====
st.title("👑 Tassaout Méga Fort")
st.caption(
    "OMEGA Super Agentic AI | المنصة السيادية المتقدمة للذكاء الاصطناعي والمصداقية"
    " التجارية"
)

# خانة كتابة المجال بشكل حر وفارغ
domain = st.text_input(
    "اكتب المجال المطلوب (بحرية تامة)",
    placeholder="مثال: تسويق عقاري، خدمات رقمية، تجارة...",
)
task = st.text_area(
    "وصف المهمة / المشروع",
    placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة",
)

agent = SuperOmegaAgent(domain)

col1, col2, col3 = st.columns(3)

with col1:
  if st.button("🧠 تحليل واستراتيجية CEO"):
    if task:
      with st.spinner("المدير التنفيذي يحلل المشروع في الخلفية..."):
        st.markdown(agent.ceo(task))
    else:
      st.warning("⚠️ أدخل وصف المهمة أولاً.")

with col2:
  if st.button("💻 الاستراتيجية التقنية CTO"):
    if task:
      with st.spinner("المدير التقني يجهز البنية في الخلفية..."):
        st.markdown(agent.cto(task))
    else:
      st.warning("⚠️ أدخل وصف المهمة أولاً.")

with col3:
  if st.button("📊 الخطة التشغيلية COO"):
    if task:
      with st.spinner("مدير العمليات يضبط الجدول في الخلفية..."):
        st.markdown(agent.coo(task))
    else:
      st.warning("⚠️ أدخل وصف المهمة أولاً.")

st.markdown("---")

if st.button(
    "🚀 تشغيل الوكلاء بالكامل (خطة + إعلانات أخلاقية موثوقة + واتساب)",
    type="primary",
):
  if task:
    with st.spinner(
        "الوكلاء الأذكياء يعملون في الخلفية بمصداقية تامة (CEO -> Copywriter ->"
        " Closer)..."
    ):
      plan, final_ads = agent.run_autonomous_pipeline(task)
      st.success("تم تنفيذ المنطق الخلفي وتوليد الحملة بنجاح!")

      with st.expander("📋 معاينة الخطة الاستراتيجية الكاملة (CEO)"):
        st.markdown(plan)

      st.markdown("---")
      st.subheader("📢 البطاقات الإعلانية الملونة والموثوقة")

      parts = final_ads.split("### الإعلان")
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

            # زر تحميل مباشر لكل بطاقة إعلانية على حدة
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
  else:
    st.warning("⚠️ الرجاء إدخال وصف المهمة أو المشروع أولاً.")

# ====================== تذييل الموقع ======================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 15px; font-weight:"
    " bold;'>"
    "إنتاج السيد عامر بوخدادة | جهة مراكش آسفي | كل الحقوق محفوظة 2026 👑"
    "</div>",
    unsafe_allow_html=True,
)
