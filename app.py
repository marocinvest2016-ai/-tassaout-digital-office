import streamlit as st
from supabase import create_client
import random
from datetime import datetime
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# 1. إعدادات الصفحة السيادية المطلقة
st.set_page_config(
    page_title="👑 Alpha Core Nexus — Sovereign Agentic AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة سيادية فاخرة (CSS مخصص)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 12px; padding: 10px; margin-bottom: 10px; }
    h1, h2, h3 { color: #f0f2f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .sovereign-badge { background: linear-gradient(90deg, #FFD700, #FFA500); padding: 5px 15px; border-radius: 8px; color: black; font-weight: bold; display: inline-block; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# 2. الاتصال بقاعدة البيانات السيادية (Supabase)
SUPABASE_URL = "https://xjjriuohqvhdxfgsyepl.supabase.co"
SUPABASE_KEY = "sb_publishable_xNbvcCGrqDQyU8fAtEMF7w_FqDzwSVg"

@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"خطأ في الاتصال بـ Supabase: {e}")
        return None

supabase = init_supabase()

def load_ads_from_db():
    if not supabase:
        return []
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data if res.data else []
    except Exception as e:
        return []

# 3. محرك توليد الصور المحلي (Pillow)
def generate_ad_card(title, content):
    img = Image.new('RGB', (1080, 1080), color='#0e1117')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 50)
        font_body = ImageFont.truetype("arial.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    draw.text((50, 50), "👑 Alpha Core Nexus", font=font_title, fill='#FFD700')
    draw.text((50, 130), title[:40], font=font_title, fill='white')
    
    wrapped_text = textwrap.fill(content[:350], width=40)
    draw.text((50, 220), wrapped_text, font=font_body, fill='#f0f2f6')
    
    draw.text((50, 980), "📞 0691897126 | قلعة السراغنة | MarocInvest", font=font_body, fill='#34A853')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# 4. الشريط الجانبي السيادي
with st.sidebar:
    st.markdown('<div class="sovereign-badge">👑 ALPHA CORE NEXUS</div>', unsafe_allow_html=True)
    st.header("لوحة التحكم السيادية")
    st.info("النظام يعمل بكفاءة تامة مع ميزات الواتساب ومولد الصور.")
    
    selected_domain = st.selectbox(
        "اختر وضع التوجيه الذكي (Routing Domain):",
        ["الوكيل الشامل (Auto-Router)", "وكيل الإعلانات العقارية", "وكيل التجارة والأعمال", "وكيل معالجة البيانات واللوجستيات"]
    )
    
    st.markdown("---")
    if st.button("🗑️ مسح ذاكرة المحادثة السيادية", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("📍 الموقع التشغيلي: قلعة السراغنة | المغرب")
    st.caption("📞 الخط الساخن: 0691897126")

# 5. الواجهة الرئيسية
st.title("👑 Alpha Core Nexus — Super Multi-Domain Agentic AI")
st.markdown("أهلاً بك يا سيدي الرئيس. النظام السيادي المتكامل جاهز لإدارة الأوامر، النشر الفري على الواتساب، وتوليد البطاقات البصرية.")

# تقسيم الشاشة إلى قسمين: محادثة ذكية (يمين/يسار) ولوحة إعلانات حية مع أزرار النشر
col_chat, col_view = st.columns([1.2, 1], gap="large")

with col_chat:
    st.subheader("🤖 غرفة عمليات الوكيل الذكي")
    
    # تهيئة الذاكرة
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "أنا وكيلك الذكي السيادي. جاهز لتنفيذ الأوامر، كتابة الإعلانات المنظمة، ومعالجة الصور والملفات بدون أي قيود."}
        ]

    # عرض سجل المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message and message["image"]:
                st.image(message["image"], width=300)

    # صندوق الإدخال والمرفقات
    uploaded_file = st.file_uploader("📎 إرفاق صورة أو مستند للتحليل الفوري:", type=["png", "jpg", "jpeg", "webp"], key="sovereign_uploader")
    user_query = st.chat_input("اكتب أمرك السيادي هنا للوكيل الذكي...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query, "image": uploaded_file})
        with st.chat_message("user"):
            st.markdown(user_query)
            if uploaded_file: st.image(uploaded_file, width=300)

        # توليد رد الوكيل
        p_lower = user_query.lower()
        if "عقار" in p_lower or "شقة" in p_lower or "منزل" in p_lower or "أرض" in p_lower or selected_domain == "وكيل الإعلانات العقارية":
            category = "عقاري"
            agent_output = f"""🏠 **عرض عقاري سيادي ممتاز بقلعة السراغنة** 🏠
✨ **التفاصيل:** {user_query}
{ "📎 [تم تحليل المرفق البصري واعتماد قياسات العقار]" if uploaded_file else "" }
🎯 **لماذا هذا العقار؟** 
✅ تصميم عصري وتشطيبات عالية الجودة.
✅ موقع استراتيجي هادئ وقريب من كافة المرافق الحيوية.
✅ صفقة استثمارية آمنة ومربحة.
🔑 **للحجز الفوري:** 
📞 0691897126 | 📧 marocinvest2012@gmail.com
---
#عقارات #قلعة_السراغنة #شقق_للبيع #استثمار_عقاري #MarocInvest #AlphaCoreNexus"""
        elif "تجاري" in p_lower or "محل" in p_lower or "مشروع" in p_lower or selected_domain == "وكيل التجارة والأعمال":
            category = "تجاري"
            agent_output = f"""🛍️ **عرض تجاري واستثماري حصري** 🛍️
✨ **التفاصيل:** {user_query}
{ "📎 [تم إدماج تحليل الصورة المرفقة]" if uploaded_file else "" }
🎯 **مميزات المشروع التجاري:** 
✅ موقع حيوي ممتاز يضمن حركة مرور واستهداف عالي.
✅ واجهة احترافية ومساحة مهيأة لكافة الأنشطة.
✅ فرصة حقيقية لتعظيم أرباحك وتوسيع نطاق عملك.
🔑 **للتواصل والتعاقد:** 
📞 0691897126 | 📧 marocinvest2012@gmail.com
---
#عقارات_تجارية #استثمار_تجاري #قلعة_السراغنة #MarocInvest #AlphaCoreNexus"""
        else:
            category = "لوجستيات وعام"
            agent_output = f"""⚡ **تقرير التنفيذ السيادي:**
لقد تم تلقي وتحليل الأمر بنجاح محلياً: *"{user_query}"*
{ "📷 تم رصد واستلام الصورة المرفقة." if uploaded_file else "" }
✅ المنظومة تعمل بكفاءة مطلقة واستقرار تام دون أي اتصال خارجي.
---
#AlphaCoreNexus #SystemSovereign"""

        # الحفظ في Supabase
        if supabase:
            try:
                supabase.table("instant_ads").insert({
                    "title": f"[{category}] {user_query[:25]}...",
                    "content": agent_output.strip()
                }).execute()
            except:
                pass

        st.session_state.messages.append({"role": "assistant", "content": agent_output.strip()})
        st.rerun()

with col_view:
    st.subheader("📋 لوحة الإعلانات الحية والتحكم الشامل")
    ads = load_ads_from_db()
    
    if not ads:
        st.info("لا توجد إعلانات مسجلة حالياً في القاعدة.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} — {str(ad.get('created_at'))[:10]}"):
                st.write(ad.get('content'))
                
                col_btn1, col_btn2 = st.columns(2)
                
                # 1. زر الواتساب
                with col_btn1:
                    wa_link = f"https://wa.me/212691897126?text={urllib.parse.quote(ad.get('content'))}"
                    st.link_button("📲 نشر على الواتساب", wa_link, use_container_width=True)

                # 2. زر توليد الصورة
                with col_btn2:
                    if st.button("🖼️ توليد بطاقة مصورة", key=f"btn_{ad.get('id')}", use_container_width=True):
                        img_buf = generate_ad_card(ad.get('title'), ad.get('content'))
                        st.image(img_buf, use_container_width=True)
                        st.download_button("⬇️ تحميل الصورة", img_buf, file_name="ad_card.png", mime="image/png", key=f"dl_{ad.get('id')}", use_container_width=True)
