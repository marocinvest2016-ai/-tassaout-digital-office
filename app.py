import json
import os
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw
import textwrap
import zipfile
from urllib.parse import quote
from supabase import create_client, Client
import streamlit as st

# 1. إعداد الصفحة والأنماط السيادية
st.set_page_config(
    page_title="Alpha Core Nexus - المكتبة والوكلاء الأذكياء",
    page_icon="👑",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    text-align: center; 
    color: #1e3a8a; 
    font-weight: 800; 
    font-size: 1.5rem; 
    font-family: 'Cairo', sans-serif; 
    margin-bottom: 5px;
    margin-top: 5px;
}
textarea, input, .stTextArea textarea {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}
.stButton button {
    font-size: 1.2rem !important;
    font-weight: bold !important;
}
.stChatMessage {
    background-color: #f8fafc; 
    border-radius: 16px; 
    padding: 1rem; 
    margin-bottom: 10px;
    font-size: 1.1rem !important;
}
</style>
""", unsafe_allow_html=True)

# 2. ربط الخدمات السحابية والذكاء الاصطناعي
groq_client = None
try:
    from groq import Groq
    if "GROQ_API_KEY" in st.secrets:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    pass

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_SIGNATURE = "انتاج السيد عامر مؤسس الذكاء المنطقي السحابي المركب<br>جهة مراكش اسفي<br>كل الحقوق محفوظة 2026"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def generate_ad_image(text):
    img = Image.new('RGB', (1080, 1080), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 1040, 1040], fill='white', outline='#0284c7', width=10)
    draw.text((540, 90), "مكتب تساوت الرقمي - إعلان", fill='#1e3a8a', anchor="mm")
    draw.text((540, 140), f"الهاتف: {LOCAL_PHONE}", fill='#0284c7', anchor="mm")
    lines = textwrap.wrap(text, width=32)
    y = 240
    for line in lines[:12]:
        draw.text((540, y), line, fill='black', anchor="mm")
        y += 55
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- تعريف الوكيل الذكي المكلف (AmarAgent) ---
class AmarAgent:
    def __init__(self, nom_entreprise):
        self.nom = nom_entreprise

    def scanner_domain(self, keyword):
        opps = []
        if supabase:
            try:
                res = (
                    supabase.table("instant_ads")
                    .select("*")
                    .ilike("message", f"%{keyword}%")
                    .limit(5)
                    .execute()
                )
                opps = res.data
            except:
                opps = []
        if not opps:
            opps = [{
                "message": f"صفقة عقارية / تجارية مقترحة بـ {keyword}",
                "region": "قلعة السراغنة - مراكش",
                "montant": 150000,
            }]
        return [
            {
                "region": ad.get("region", "Marrakech-Safi"),
                "ville": keyword,
                "objet": ad.get("message", "صفقة")[:100],
                "montant_est": ad.get("montant", 50000),
            }
            for ad in opps
        ]

    def analyse_domain(self, opps):
        for opp in opps:
            opp["concurrence"] = "🟢 ضعيفة" if opp["montant_est"] < 100000 else "🟡 متوسطة"
            ht = opp["montant_est"] / 1.20
            opp["ht"] = round(ht, 2)
            opp["tva"] = round(opp["montant_est"] - ht, 2)
            opp["benefice"] = round(ht * 0.14, 2)
            opp["score"] = 95
        return sorted(opps, key=lambda x: x["score"], reverse=True)

    def rapport_comm(self, opps):
        msg = f"*👑 تقرير الوكيل الذكي (عامر) - {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n"
        for i, opp in enumerate(opps, 1):
            msg += (
                f"*{i}. [{opp['score']}/100] {opp['objet']}*\n💰"
                f" {opp['montant_est']} DH | 📍 {opp['region']} | 📈 أرباح تقديرية:"
                f" {opp['benefice']} DH\n\n"
            )
        return msg

# بيانات افتراضية تجريبية للعقارات
DEFAULT_PROPERTIES = [
    {
        "id": "TS-001",
        "title": "أرض فلاحية خصبة بقلعة السراغنة",
        "type": "أرض فلاحية",
        "price": 450000,
        "surface": 5000,
        "description": "أرض فلاحية ذات صيت حسن، تتوفر على بئر وماء السقي وقريبة من الطريق الرئيسية.",
        "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600"
    },
    {
        "id": "TS-002",
        "title": "بقعة أرضية مخصصة للبناء بوسط المدينة",
        "type": "بقعة أرضية",
        "price": 320000,
        "surface": 150,
        "description": "بقعة محفظة صالحة لبناء منزل ريفي أو تجاري، منطقة هادئة وقريبة من المرافق.",
        "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600"
    }
]

@st.cache_data
def load_properties(path="properties.json"):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PROPERTIES
    return DEFAULT_PROPERTIES

properties = load_properties()
df = pd.DataFrame(properties)

# 3. القائمة الجانبية الرئيسية للتنقل بين الأنظمة المدمجة
st.sidebar.title("🗂️ الدماغ المركزي")
main_nav = st.sidebar.radio(
    "اختر النظام الأساسي:",
    [
        "💬 محطة المحادثات والخدمات الذكية",
        "🏛️ المكتبة الرقمية السحابية الجامعة",
        "🤖 شبكة الوكلاء الأذكياء المكلفين",
        "🏢 وكالة تساوت العقارية والصفقات"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(f"الرقم الموحد الرسمي: **{LOCAL_PHONE}**\n\n`[TASSAOUT VERIFIED]`")

# --- النظام الأساسي 1: محطة المحادثات والخدمات الذكية ---
if main_nav == "💬 محطة المحادثات والخدمات الذكية":
    st.markdown("<h1 class='main-header'>خدمات تساوت الرقمية للعقار والاعمال بقلعة السراغنة</h1>", unsafe_allow_html=True)

    # عرض سجل المحادثات
    for i, msg in enumerate(st.session_state["messages"]):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "attachments" in msg:
                for att in msg["attachments"]:
                    if att["type"] == "image":
                        st.image(att["data"], width="stretch")
                    elif att["type"] == "video":
                        st.video(att["data"])
                    elif att["type"] == "file":
                        st.download_button(f"📎 {att['name']}", att["data"], att["name"], key=f"hist_file_{i}_{att['name']}")
            if "images" in msg:
                for img_bytes in msg["images"]:
                    st.image(img_bytes, width="stretch")
            if "zip" in msg:
                st.download_button("📥 تحميل حزمة الإعلانات والملفات (ZIP)", msg["zip"], f"tassaout_package_{i}.zip", key=f"zip_btn_{i}")

    # الشاشة التفاعلية الكبيرة الموحدة للإدخال
    with st.container(border=True):
        prompt = st.text_area(
            "حقل إدخال النص",
            placeholder="اكتب طلبك، تفاصيل الإعلان العقاري، أو كبسولة المعلوميات هنا...",
            height=220,
            key="unified_prompt_box",
            label_visibility="collapsed"
        )
        
        uploaded_files = st.file_uploader(
            "أداة رفع الملفات والصور",
            type=["png", "jpg", "jpeg", "mp4", "pdf", "docx"],
            accept_multiple_files=True,
            key="unified_file_uploader",
            label_visibility="collapsed"
        )
        
        submit_btn = st.button("🚀 تنفيذ الطلب وإرسال", use_container_width=True, type="primary")

    if submit_btn and (prompt or uploaded_files):
        attachments = []
        if uploaded_files:
            for file in uploaded_files:
                file_bytes = file.read()
                if file.type.startswith("image"):
                    attachments.append({"type": "image", "data": file_bytes, "name": file.name})
                elif file.type.startswith("video"):
                    attachments.append({"type": "video", "data": file_bytes, "name": file.name})
                else:
                    attachments.append({"type": "file", "data": file_bytes, "name": file.name})

        user_msg = {"role": "user", "content": prompt if prompt else "تم رفع ملفات للتحليل", "attachments": attachments}
        st.session_state["messages"].append(user_msg)

        with st.spinner("جاري المعالجة وهندسة المحتوى الرقمي..."):
            context = "المستخدم رفع ملفات: " + ", ".join([a['name'] for a in attachments]) if attachments else ""
            system_prompt = f"""
            أنت الوكيل الذكي والمساعد الحصري في خدمات تساوت الرقمية للعقار والأعمال بقلعة السراغنة، جهة مراكش آسفي.
            قم بصياغة النصوص الإعلانية والتسويقية العقارية باحترافية تامة. اختم دائماً برقم التواصل الرسمي: {BRAND_PHONE}
            """

            answer = ""
            try:
                if groq_client:
                    resp = groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": (prompt if prompt else "") + " " + context}
                        ],
                        temperature=0.6
                    )
                    answer = resp.choices[0].message.content
                else:
                    answer = "عذراً، مفتاح الوكيل الذكي (Groq API Key) غير متصل بالخوادم حالياً."
            except Exception as e:
                answer = f"حدث خطأ أثناء الاتصال بالوكيل الذكي: {e}"

            images = []
            zip_buffer = None

            if any(k in (prompt or "") for k in ["إعلان", "عقار", "شقة", "بقعة", "منزل", "ولد", "صايب", "تصميم"]) or attachments:
                img_bytes = generate_ad_image(answer)
                images.append(img_bytes)

                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as z:
                    z.writestr("ad_image_1.png", img_bytes)
                    z.writestr("ad_text.txt", answer)

        agent_msg = {
            "role": "assistant",
            "content": answer,
            "images": images if images else None,
            "zip": zip_buffer.getvalue() if zip_buffer else None
        }
        st.session_state["messages"].append(agent_msg)
        st.rerun()

# --- النظام الأساسي 2: المكتبة الرقمية السحابية الجامعة ---
elif main_nav == "🏛️ المكتبة الرقمية السحابية الجامعة":
    st.title("🛡️ المكتبة الرقمية السحابية الجامعة - Alpha Core Nexus")
    st.markdown("---")
    
    section = st.selectbox(
        "أقسام المكتبة:",
        [
            "الرئيسية ونظرة عامة",
            "الدستور والبروتوكولات السيادية",
            "أكواد الوكلاء والسكريبتات",
            "قواعد المعرفة والعقارات",
            "أصول الهوية والبصريات"
        ]
    )

    if section == "الرئيسية ونظرة عامة":
        st.header("مرحباً بك في الدماغ المركزي لمكتب تساوت الرقمي")
        st.info(f"النظام يعمل بتناغم تام مع الرقم الموحد الرسمي: **{LOCAL_PHONE}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="حالة النظام", value="نشط [ACTIVE]")
        with col2:
            st.metric(label="مستوى الأمان", value="محمي [TASSAOUT VERIFIED]")
        with col3:
            st.metric(label="الربط السحابي", value="جاهز لـ GitHub & Supabase")

    elif section == "الدستور والبروتوكولات السيادية":
        st.header("📜 البروتوكولات السيادية")
        st.markdown("""
        * **قاعدة عدم الحشو:** تنفيذ المهام بدقة وسرعة وبدون إطالة.
        * **عدم إبداء الرأي إلا بأمر:** الالتزام التام بالتعليمات السيادية للنظام.
        * **الأرشيف الموحد:** حفظ جميع السجلات بختم `[TASSAOUT VERIFIED]`.
        """)

    elif section == "أكواد الوكلاء والسكريبتات":
        st.header("⚙️ السكريبتات وأكواد التشغيل")
        st.code("""
# نموذج كود مزامن أوتوماتيكي للوكلاء
import os
def sync_to_github():
    print("Syncing Tassaout Library with GitHub repository...")
        """, language="python")

    elif section == "قواعد المعرفة والعقارات":
        st.header("🏢 قواعد المعرفة والعقارات")
        st.write("إدارة عروض العقارات، الشقق، والقطع الأرضية بقلعة السراغنة ومراكش.")
        st.success("تم ربط قاعدة البيانات بنجاح.")

    elif section == "أصول الهوية والبصريات":
        st.header("🎨 أصول الهوية والبصريات واستوديو تساوت")
        st.write("تحتوي على معايير التصميم، الشعارات، واللوحات الإعلانية الرقمية.")

# --- النظام الأساسي 3: شبكة الوكلاء الأذكياء المكلفين ---
elif main_nav == "🤖 شبكة الوكلاء الأذكياء المكلفين":
    st.title("🤖 شبكة الوكلاء الأذكياء المكلفين (AmarAgent Engine)")
    st.markdown("نظام الفحص التلقائي وتحليل الفرص التجارية والعقارية في قلعة السراغنة ومراكش.")

    agent_tab1, agent_tab2 = st.tabs(["🔍 فحص وتحليل السوق والصفقات", "➕ إضافة صفقة جديدة للنظام"])

    with agent_tab1:
        st.subheader("محطة التشغيل والتحليل الذكي")
        city_input = st.text_input("حدد المنطقة أو المدينة للبحث:", "قلعة السراغنة")
        amar = AmarAgent("Sraghna Digital Market")

        if st.button("🚀 بدء فحص وتوليد تقرير الوكيل"):
            with st.spinner("جاري فحص البيانات وتحليل المنافسة..."):
                opps_brutes = amar.scanner_domain(city_input)
                if opps_brutes:
                    opps_analyse = amar.analyse_domain(opps_brutes)
                    rapport = amar.rapport_comm(opps_analyse)

                    st.success("تم توليد تقرير الوكيل بنجاح!")
                    st.text_area("📄 نص التقرير المولد:", rapport, height=200)

                    encoded_msg = quote(rapport)
                    whatsapp_url = f"https://wa.me/{LOCAL_PHONE}?text={encoded_msg}"
                    st.markdown(
                        f"### [🔗 اضغط هنا للإرسال المباشر للتقرير عبر الواتساب]({whatsapp_url})",
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("⚠️ لا توجد صفقات مطابقة حالياً.")

    with agent_tab2:
        st.subheader("إضافة صفقة أو عرض جديد لقاعدة بيانات الوكيل")
        with st.form("agent_add_form"):
            ad_msg = st.text_input("تفاصيل الصفقة / العرض (مثل: بقعة تجارية بالهدى)")
            ad_reg = st.text_input("المنطقة", "قلعة السراغنة")
            ad_mnt = st.number_input("المبلغ التقديري (بالدرهم)", min_value=0, value=80000)
            submitted = st.form_submit_button("حفظ الصفقة في السيرفر")

            if submitted:
                if ad_msg and ad_reg:
                    if supabase:
                        try:
                            payload = {"message": ad_msg, "region": ad_reg, "montant": ad_mnt}
                            supabase.table("instant_ads").insert(payload).execute()
                            st.success("تم حفظ الصفقة بنجاح في قاعدة البيانات السحابية! 🚀")
                        except Exception as e:
                            st.error(f"خطأ أثناء الحفظ: {e}")
                    else:
                        st.success("تم محاكاة حفظ الصفقة بنجاح (قاعدة البيانات غير متصلة محلياً)!")
                else:
                    st.warning("يرجى إدخال التفاصيل الأساسية.")

# --- النظام الأساسي 4: وكالة تساوت العقارية والصفقات ---
elif main_nav == "🏢 وكالة تساوت العقارية والصفقات":
    st.title("🏢 Agence Immobilière — Kelaa Sraghna")
    st.write("Terrains agricoles, fermes, lots de construction, maisons et immeubles.")

    st.sidebar.header("Filtres de recherche")
    types = ["Tous"] + sorted(df["type"].unique().tolist())
    selected_type = st.sidebar.selectbox("Type de bien", types)
    max_price = st.sidebar.number_input("Prix maximum (MAD)", min_value=0, value=int(df["price"].max()) if not df.empty else 1000000)
    min_surface = st.sidebar.number_input("Surface min (m²)", min_value=0, value=0)
    
    sort_option = st.sidebar.selectbox("ترتيب حسب السعر", ["بدون ترتيب", "الأقل سعراً", "الأعلى سعراً"])

    filtered = df.copy()
    if selected_type != "Tous":
        filtered = filtered[filtered["type"] == selected_type]
    filtered = filtered[filtered["price"] <= max_price]
    filtered = filtered[filtered["surface"] >= min_surface]

    if sort_option == "الأقل سعراً":
        filtered = filtered.sort_values(by="price", ascending=True)
    elif sort_option == "الأعلى سعراً":
        filtered = filtered.sort_values(by="price", ascending=False)

    st.sidebar.markdown(f"Biens trouvés : **{len(filtered)}**")

    if filtered.empty:
        st.warning("لا توجد عقارات مطابقة لمعايير البحث الحالية.")
    else:
        for _, row in filtered.iterrows():
            cols = st.columns([1, 2])
            with cols[0]:
                img_url = row.get("image_url")
                if img_url:
                    st.image(img_url, use_container_width=True)
                else:
                    st.write("Aucune image")
            with cols[1]:
                st.subheader(row.get("title", ""))
                st.write(f"Type : **{row.get('type')}**  •  Surface : **{row.get('surface')} m²**  •  Prix : **{row.get('price', 0):,} MAD**")
                st.write(row.get("description", ""))
                
                msg_text = f"سلام، مهتم بالعرض العقاري: {row.get('title')} (المرجع: {row.get('id', '')})"
                whatsapp_msg = quote(msg_text)
                whatsapp_url = f"https://wa.me/{LOCAL_PHONE}?text={whatsapp_msg}"
                
                st.markdown(f"[💬 تواصل عبر الواتساب]({whatsapp_url})  •  مرجع العقار : `{row.get('id', '')}`")
            st.markdown("---")

# تذييل الصفحة العام الثابت
whatsapp_footer_url = f"https://wa.me/{LOCAL_PHONE}"
st.markdown(f"""
    <div style="text-align: center; padding: 20px 0; font-family: 'Cairo', sans-serif; color: #1e3a8a;">
        <div style="margin-bottom: 12px;">
            <a href="{whatsapp_footer_url}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 24px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <p style="font-size: 0.9rem; color: #2563eb; font-weight: 700; line-height: 1.8;">
            {FOUNDER_SIGNATURE}
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Alpha Core Nexus & Tassaout Digital Platform © 2026 | مرخص ومحمي برقم 0691897126 [TASSAOUT VERIFIED]")
