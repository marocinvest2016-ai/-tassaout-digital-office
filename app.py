import streamlit as st
from openai import OpenAI
import json, os, datetime, re, requests

st.set_page_config(page_title="DANA OMEGA BRAIN v11.3", page_icon="🧠", layout="wide")

ARCHIVE_FILE = "dana_office_archive.json"
CLOUD_LIB_FILE = "dana_cloud_library.json"
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

# ========= 1. البحث الحقيقي فالويب =========
@st.cache_resource
def get_apis():
    groq_client = OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
    tavily_key = st.secrets.get("TAVILY_API_KEY", None)
    return groq_client, tavily_key

def tavily_search(query, tavily_key):
    if not tavily_key: return []
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": tavily_key,
        "query": query + " المغرب رقم الهاتف",
        "search_depth": "advanced",
        "max_results": 5,
        "include_answer": True
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")
            })
        return results
    except: return []

# ========= 2. الأنظمة =========
if "config" not in st.session_state:
    st.session_state.config = {
        "mode": "Aggressive Mode",
        "agent": "DANA General",
        "model": "openai/gpt-oss-120b",
        "memory": {"الاسم": "القائد", "المدينة": "قلعة السراغنة"},
        "sectors": AVAILABLE_SECTORS[:4],
        "system_prompt": """أنت DANA OMEGA BRAIN v11.3 - الدماغ الصياد العدواني.
مهمتك: تعطي نتائج حقيقية 100% من البحث أسفله.
القواعد:
1. جاوب بالدارجة المغربية مباشر وحاد. بلا "آسف".
2. خرج النتيجة دائما فـ جدول: | # | الاسم | التخصص | رقم الهاتف | رابط الأعمال |
3. من بعد الجدول ولد "2 رسالة واتساب واجدة" للتواصل.
4. إلا ما لقيتيش رقم قل "لم يتم العثور".

السياق من البحث الحقي:
{context}
الذاكرة: {memory}"""
    }

if "office" not in st.session_state: st.session_state.office = load_json(ARCHIVE_FILE)
if "library" not in st.session_state: st.session_state.library = load_json(CLOUD_LIB_FILE)

client, TAVILY_KEY = get_apis()

def call_dana(prompt):
    cfg = st.session_state.config

    # الخطوة 1: البحث الحقيقي
    search_results = tavily_search(prompt, TAVILY_KEY)
    context = ""
    if search_results:
        for i, res in enumerate(search_results, 1):
            context += f"[{i}] {res['title']}\n{res['content']}\nالرابط: {res['url']}\n\n"
    else:
        context = "لم يتم العثور على نتائج بحث. استعمل معلوماتك العامة."

    full_system = cfg["system_prompt"].format(context=context, memory=json.dumps(cfg['memory']), sectors=", ".join(cfg['sectors']))

    try:
        with st.spinner("🧠 DANA كيصيد فـ Google + LinkedIn + Avito..."):
            response = client.chat.completions.create(
                model=cfg["model"],
                messages=[{"role": "system", "content": full_system}, {"role": "user", "content": prompt}],
                temperature=0.3, # نقصناها باش تكون النتائج دقيقة
                max_tokens=500
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ خطأ من Groq: {e}"); return None

# ========= 3. الواجهة =========
with st.sidebar:
    st.title("⚙️ مركز القيادة v11.3")

    st.subheader("1. القطاعات النشطة")
    raw_default = st.session_state.config.get("sectors", [])
    if not isinstance(raw_default, list): raw_default = [raw_default] if raw_default else []
    safe_default = [s for s in raw_default if s in AVAILABLE_SECTORS] or AVAILABLE_SECTORS[:2]

    st.session_state.config["sectors"] = st.multiselect("اختار القطاعات", AVAILABLE_SECTORS, default=safe_default)

    if not TAVILY_KEY: st.warning("⚠️ زيد TAVILY_API_KEY فـ secrets باش يخدم البحث الحقيقي")
    else: st.success("✅ البحث الحقيقي مفعل")

    st.subheader("2. 📁 مكتب المدير")
    st.json(st.session_state.office)
    if st.button("💾 حفظ الأرشيف"): save_json(ARCHIVE_FILE, st.session_state.office); st.success("تم")

st.title("🧠 DANA OMEGA BRAIN v11.3 - الدماغ الصياد")

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
            links = extract_links(reply)
            if phones or links:
                st.session_state.office["الطلبات"].append({
                    "التاريخ": str(datetime.datetime.now()),
                    "الطلب": prompt,
                    "النتيجة": reply[:500],
                    "الأرقام": phones,
                    "الروابط": links
                })
                save_json(ARCHIVE_FILE, st.session_state.office)
                st.success(f"✅ تم تخزين {len(phones)} رقم و {len(links)} رابط")
