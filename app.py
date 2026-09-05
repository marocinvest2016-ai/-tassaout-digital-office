import streamlit as st
from openai import OpenAI
import json, os, datetime, re

st.set_page_config(page_title="DANA OMEGA BRAIN v11.0", page_icon="🧠", layout="wide")

# ========= 1. الأنظمة =========
ARCHIVE_FILE = "dana_office_archive.json" # مكتب المدير
CLOUD_LIB_FILE = "dana_cloud_library.json" # المكتبة السحابية

def load_json(file):
    if os.path.exists(file): return json.load(open(file, "r", encoding="utf-8"))
    return {"العروض": [], "الطلبات": [], "العملاء": [], "الأرشيف": []}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def extract_phones(text):
    return re.findall(r'\+212[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}', text)

if "config" not in st.session_state:
    st.session_state.config = {
        "mode": "Aggressive Mode",
        "agent": "DANA General",
        "model": "groq/compound",
        "memory": {"الاسم": "القائد", "المدينة": "قلعة السراغنة"},
        "sectors": ["العقار","الهندسة المعمارية","الهندسة الصناعية","الهندسة الميكانيكية","الرقمية","الديكور الداخلي","التصميم","التصوير الاحترافي","الثقافة العالمية"],
        "system_prompt": """أنت DANA OMEGA BRAIN v11.0 - الدماغ الجامع.
أنت خبير فـ 9 قطاعات: العقار, الهندسة المعمارية, الصناعية, الميكانيكية, الرقمية, الديكور, التصميم, التصوير, الثقافة العالمية.
تتعلم من كل معلومة وتغذي بها باقي القطاعات.

### القواعد الصارمة - وضع الصياد العدواني:
1. كن مباشر، حاد، بالدارجة المغربية. بلا "آسف".
2. إلا تسول على منتوج/خدمة/شخص: قلب فـ Google, LinkedIn, Facebook, Avito. جيب الاسم + التخصص + رقم الهاتف + الرابط ضروري.
3. خرج النتيجة دائما فـ جدول: | # | الاسم | التخصص | رقم الهاتف | رابط الأعمال |
4. بعد الجدول مباشرة ولد "2 رسالة واتساب واجدة" للتواصل.
5. أي جواب فيه رقم هاتف خزنو أوتوماتيك فـ "مكتب المدير".

الذاكرة: {memory}
القطاعات النشطة: {sectors}"""
    }

if "office" not in st.session_state: st.session_state.office = load_json(ARCHIVE_FILE)
if "library" not in st.session_state: st.session_state.library = load_json(CLOUD_LIB_FILE)

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
client = get_client()

def call_dana(prompt):
    cfg = st.session_state.config
    full_system = cfg["system_prompt"].format(memory=json.dumps(cfg['memory']), sectors=cfg['sectors'])
    try:
        with st.spinner("🧠 DANA كيبحث + كيصيد الأرقام..."):
            response = client.chat.completions.create(
                model=cfg["model"],
                messages=[{"role": "system", "content": full_system}, {"role": "user", "content": prompt}],
                temperature=0.7, max_tokens=4096
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ خطأ: {e}"); return None

# ========= 2. الواجهة =========
with st.sidebar:
    st.title("⚙️ مركز القيادة v11.0")

    st.subheader("1. القطاعات النشطة")
    st.session_state.config["sectors"] = st.multiselect(
        "اختار القطاعات",
        st.session_state.config["sectors"],
        default=st.session_state.config["sectors"]
    )

    st.subheader("2. 📁 مكتب المدير")
    st.json(st.session_state.office)
    if st.button("💾 حفظ الأرشيف"):
        save_json(ARCHIVE_FILE, st.session_state.office); st.success("تم حفظ الأرشيف")

    st.subheader("3. ☁️ المكتبة السحابية")
    new_doc = st.text_area("زيد معلومة/درس/عرض")
    if st.button("📚 تخزين فالمكتبة"):
        st.session_state.library["الأرشيف"].append({"التاريخ": str(datetime.date.today()), "المحتوى": new_doc})
        save_json(CLOUD_LIB_FILE, st.session_state.library); st.success("تخزن")

    st.subheader("4. ✨ مساعد البرمجة")
    prompt_request = st.text_area("قول ليه شنو بغيتي فالبرومبت", height=80)
    if st.button("ولد البرومبت"):
        meta = f"اكتب System Prompt عدواني لخبير فـ {st.session_state.config['sectors']} يجيب أرقام ويولد رسائل واتساب"
        st.session_state.config["system_prompt"] = call_dana(meta)
        st.rerun()

st.title("🧠 DANA OMEGA BRAIN v11.0 - الدماغ الجامع")

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

            # تخزين تلقائي
            phones = extract_phones(reply)
            if phones:
                st.session_state.office["الطلبات"].append({
                    "التاريخ": str(datetime.datetime.now()),
                    "الطلب": prompt,
                    "النتيجة": reply[:800],
                    "الأرقام": phones
                })
                save_json(ARCHIVE_FILE, st.session_state.office)
                st.success(f"✅ تم تخزين {len(phones)} رقم فمكتب المدير")
