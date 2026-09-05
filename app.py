import streamlit as st
from openai import OpenAI
import json, os, datetime, re
from duckduckgo_search import DDGS

st.set_page_config(page_title="DANA OMEGA BRAIN v11.4.2", page_icon="🧠", layout="wide")

ARCHIVE_FILE = "dana_office_archive.json"
AVAILABLE_SECTORS = [
    "العقار","الهندسة المعمارية","الصناعية","الميكانيكية",
    "الرقمية","الديكور","التصميم","التصوير","الثقافة"
]

def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}
    return {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def extract_phones(text):
    return list(set(re.findall(r'\+212[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}', text)))

def extract_links(text):
    return list(set(re.findall(r'https?://[^\s<>"]+', text)))

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")

def ddg_search(query):
    context = ""
    try:
        with st.spinner("🦆 DANA كيقلب فـ DuckDuckGo..."):
            with DDGS() as ddgs:
                results = ddgs.text(f"{query} المغرب رقم الهاتف واتساب", region="ma-ma", max_results=8)
                for i, res in enumerate(results, 1):
                    context += f"[{i}] {res.get('title','')}\n{res.get('body','')}\nالرابط: {res.get('href','')}\n\n"
    except Exception as e:
        context = f"خطأ في البحث: {e}"
    if not context: context = "لم يتم العثور على نتائج بحث."
    return context

if "config" not in st.session_state:
    st.session_state.config = {
        "mode": "Aggressive Mode",
        "agent": "DANA General",
        "model": "openai/gpt-oss-120b",
        "memory": {"الاسم": "القائد", "المدينة": "قلعة السراغنة"},
        "sectors": ["العقار","الهندسة المعمارية"], # صلحت الديفولت
        "system_prompt": """أنت DANA OMEGA BRAIN v11.4.2 - الدماغ الصياد المجاني.
مهمتك: تعطي نتائج حقيقية من DuckDuckGo.
القواعد: 1. جاوب بالدارجة. 2. جدول: | # | الاسم | التخصص | رقم الهاتف | رابط | المصدر |
3. 2 رسائل واتساب. 4. إلا ما لقيتيش قل "لم يتم العثور".
السياق: {context} الذاكرة: {memory}"""
    }

if "office" not in st.session_state: st.session_state.office = load_json(ARCHIVE_FILE)
client = get_client()

def call_dana(prompt):
    cfg = st.session_state.config
    context = ddg_search(prompt)
    full_system = cfg["system_prompt"].format(context=context, memory=json.dumps(cfg['memory']))
    try:
        response = client.chat.completions.create(model=cfg["model"], messages=[{"role": "system", "content": full_system}, {"role": "user", "content": prompt}], temperature=0.2, max_tokens=700)
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ خطأ من Groq: {e}"); return None

with st.sidebar:
    st.title("⚙️ مركز القيادة v11.4.2")
    st.session_state.config["sectors"] = st.multiselect("اختار القطاعات", AVAILABLE_SECTORS, default=st.session_state.config["sectors"])
    st.success("✅ DuckDuckGo مفعل - مجاني 100%")
    st.subheader("2. 📁 مكتب المدير")
    st.json(st.session_state.office)
    if st.button("💾 حفظ الأرشيف"): save_json(ARCHIVE_FILE, st.session_state.office); st.success("تم")

st.title("🧠 DANA OMEGA BRAIN v11.4.2")
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
            phones = extract_phones(reply); links = extract_links(reply)
            if phones or links:
                st.session_state.office["الطلبات"].append({"التاريخ": str(datetime.datetime.now()),"الطلب": prompt,"الأرقام": phones,"الروابط": links})
                save_json(ARCHIVE_FILE, st.session_state.office)
                st.success(f"✅ تم تخزين {len(phones)} رقم")
