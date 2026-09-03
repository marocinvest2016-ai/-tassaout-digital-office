import streamlit as st
import requests
import json
from PIL import Image

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

def call_super_ai(prompt, agent_name):
    """محرك الذكاء الاصطناعي الفائق عبر Groq باستخدام Llama"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    if not prompt or not prompt.strip():
        return "❌ خطأ: نص المهمة فارغ. يرجى إدخال تفاصيل المشروع أولاً."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI powered by Meta Llama on Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75,
        "max_tokens": 3000
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as err:
        return f"❌ خطأ من خادم Groq: {err.response.status_code} - {err.response.text}"
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

class SuperOmegaAgent:
    def ceo(self, task):
        return call_super_ai(f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذه المهمة أو المشروع: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم", "Super CEO Agent")

    def cto(self, task):
        return call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task}", "Super CTO Agent")

    def coo(self, task):
        return call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task}", "Super COO Agent")

    def copywriter(self, plan):
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات."
        return call_super_ai(prompt, "Super Copywriter Agent")

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent")

# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI (Groq Powered)")
st.caption("CEO + CTO + COO + Copywriter + Closer مدعوم بأحدث موديلات Llama عبر Groq")

# وصف المهمة بحرية تامة (بدون خانة عنوان أو مجال)
task = st.text_area("وصف المهمة / المشروع", placeholder="اكتب مشروعك أو مهمتك مباشرة هنا بحرية تامة...")

# زر لتحميل الصور المتعددة ومعاينتها
st.subheader("🖼️ رفع الصور المرفقة للمشروع (اختياري)")
uploaded_files = st.file_uploader("اختر الصور (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"تم تحميل {len(uploaded_files)} صورة بنجاح:")
    cols = st.columns(min(len(uploaded_files), 4))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        with cols[i % 4]:
            st.image(img, caption=file.name, use_container_width=True)

agent = SuperOmegaAgent()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 خطة CEO"):
        if task.strip():
            with st.spinner("المدير التنفيذي كيخدم عبر Groq..."):
                st.markdown(agent.ceo(task))
        else:
            st.warning("⚠️ المرجو كتابة وصف المهمة أولاً.")

with col2:
    if st.button("💻 خطة CTO"):
        if task.strip():
            with st.spinner("المدير التقني كيخدم عبر Groq..."):
                st.markdown(agent.cto(task))
        else:
            st.warning("⚠️ المرجو كتابة وصف المهمة أولاً.")

with col3:
    if st.button("📊 خطة COO"):
        if task.strip():
            with st.spinner("مدير العمليات كيخدم عبر Groq..."):
                st.markdown(agent.coo(task))
        else:
            st.warning("⚠️ المرجو كتابة وصف المهمة أولاً.")

st.markdown("---")

if st.button("✍️ إنشاء إعلان تسويقي محترف"):
    if task.strip():
        with st.spinner("الكاتب والمغلق كيخدمو على الإعلان عبر Groq..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم توليد الإعلان بنجاح!")
            st.markdown(final_ad)
    else:
        st.warning("⚠️ المرجو كتابة وصف المهمة أولاً.")
