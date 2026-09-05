import streamlit as st
from openai import OpenAI
import json, os, datetime, re

st.set_page_config(page_title="DANA OMEGA BRAIN v11.2", page_icon="🧠", layout="wide")

# ========= 1. الأنظمة مصلحة =========
ARCHIVE_FILE = "dana_office_archive.json"
CLOUD_LIB_FILE = "dana_cloud_library.json"

def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}
    return {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def extract_phones(text):
    return re.findall(r'\+212[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}', text)

if "config" not in st.session_state:
    st.session_state.config = {
        "mode": "Aggressive Mode",
        "agent": "DANA General",
        "model": "openai/gpt-oss-120b", # تبدل لـ groq/compound باش يخف
        "memory": {"الاسم": "القائد", "المدينة": "قلعة السراغنة"},
        "sectors": ["العقار","الهندسة","الرقمية","التصميم"],
        "system_prompt": """أنت DANA OMEGA BRAIN v11.2 - الدماغ الجامع.
خبير فـ {sectors}. جاوب بالدارجة المغربية مباشر وحاد. بلا "آسف".
إلا تسول على منتوج/خدمة: جيب الاسم + التخصص + رقم الهاتف + الرابط.
خرج النتيجة فـ جدول. من بعد ولد 2 رسائل واتساب.
أي رقم هاتف خزنو فـ "مكتب المدير".
الذاكرة: {memory}"""
    }

if "office" not in st.session_state: st.session_state.office = load_json(ARCHIVE_FILE)
if "library" not in st.session_state: st.session_state.library = load_json(CLOUD_LIB_FILE)

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
client = get_client()

def call_dana(prompt):
    cfg = st.session_state.config
    # نقصنا الحجم باش نتفاداو 413
    full_system = cfg["system_prompt"].format(memory=json.dumps(cfg['memory']), sectors=", ".join(cfg['sectors'][:3]))

    try:
        with st.spinner("🧠 DANA كيبحث + كيصيد الأرقام..."):
            response = client.chat.completions.create(
                model=cfg["model"],
                messages=[{"role": "system", "content": full_system}, {"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=500 # كان 4096 و هو السبب
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ خطأ: {e}"); return None

# ========= 2. الواجهة =========
with st.sidebar:
    st.title("⚙️ مركز القيادة v11.2")

    st.subheader("1. القطاعات النشطة")
    st.session_state.config["sectors"] = st.multiselect(
        "اختار القطاعات",
        ["العقار","الهندسة المعمارية","الصناعية","الميكانيكية","الرقمية","الديكور","التصميم","التصوير","الثقافة"],
        default=st.session_state.config["sectors"]
    )

    st.subheader("2. 📁 مكتب المدير")
    st.json(st.session_state.office)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 حفظ"):
            save_json(ARCHIVE_FILE, st.session_state.office); st.success("تم")
    with col2:
        if st.button("🗑️ تفريغ"):
            st.session_state.office = {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}
            save_json(ARCHIVE_FILE, st.session_state.office); st.rerun()

    st.subheader("3. ☁️ المكتبة السحابية")
    new_doc = st.text_area("زيد معلومة/درس/عرض")
    if st.button("📚 تخزين"):
        st.session_state.library["الأرشيف"].append({"التاريخ": str(datetime.date.today()), "المحتوى": new_doc})
        save_json(CLOUD_LIB_FILE, st.session_state.library); st.success("تخزن")

st.title("🧠 DANA OMEGA BRAIN v11.2 - الدماغ الجامع")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("أمر DANA الصياد..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = call_dana(prompt)
        if reply:
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            phones = extract_phones(reply)
            if phones:
                st.session_state.office["الطلبات"].append({
                    "التاريخ": str(datetime.datetime.now()),
                    "الطلب": prompt,
                    "النتيجة": reply[:500], # نقصنا الحجم حتى هنا
                    "الأرقام": phones
                })
                save_json(ARCHIVE_FILE, st.session_state.office)
                st.success(f"✅ تم تخزين {len(phones)} رقم")
