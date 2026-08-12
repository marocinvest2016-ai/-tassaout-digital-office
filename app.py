import streamlit as st
from supabase import create_client
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# 1. إعدادات الصفحة السيادية
st.set_page_config(
    page_title="👑 Alpha Core Nexus — Multi-Asset Sovereign AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 12px; padding: 10px; margin-bottom: 10px; }
    h1, h2, h3 { color: #f0f2f6; }
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
    except:
        return None

supabase = init_supabase()

def load_ads_from_db():
    if not supabase: return []
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data if res.data else []
    except:
        return []

# 3. توليد بطاقة بصرية محلية
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

# الشريط الجانبي
with st.sidebar:
    st.markdown('<div class="sovereign-badge">👑 ALPHA CORE NEXUS</div>', unsafe_allow_html=True)
    st.header("لوحة التحكم السيادية")
    st.info("النظام يعمل محلياً بكامل ميزات الرفع المتعدد والتفاعل.")
    
    selected_domain = st.selectbox(
        "اختر وضع التوجيه الذكي:",
        ["الوكيل الشامل (Auto-Router)", "وكيل الإعلانات العقارية", "وكيل التجارة والأعمال", "وكيل اللوجستيات والمشاريع"]
    )
    st.markdown("---")
    st.caption("📍 الموقع التشغيلي: قلعة السراغنة | المغرب")
    st.caption("📞 الخط الساخن: 0691897126")

# الواجهة الرئيسية
st.title("👑 Alpha Core Nexus — Multi-Image Sovereign Interface")
st.markdown("أهلاً بك يا سيدي الرئيس. غرفة العمليات جاهزة لاستقبال الأوامر ورفع **مجموعات الصور** دفعة واحدة.")

col_chat, col_view = st.columns([1.2, 1], gap="large")

with col_chat:
    st.subheader("🤖 غرفة عمليات الوكيل الذكي (رفع متعدد)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "أنا جاهز. يمكنك الآن رفع أكثر من صورة دفعة واحدة وسيقوم النظام بمعالجتها وعرضها في الشاشة التفاعلية."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message and message["images"]:
                cols = st.columns(len(message["images"]))
                for idx, img_file in enumerate(message["images"]):
                    with cols[idx]:
                        st.image(img_file, width=150)

    # ميزة الرفع المتعدد للصور (accept_multiple_files=True)
    uploaded_files = st.file_uploader(
        "📎 رفع متعدد للصور (يمكنك تحديد عدة صور معاً):", 
        type=["png", "jpg", "jpeg", "webp"], 
        accept_multiple_files=True,
        key="multi_uploader"
    )
    
    user_query = st.chat_input("اكتب أمرك السيادي هنا...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query, "images": uploaded_files})
        with st.chat_message("user"):
            st.markdown(user_query)
            if uploaded_files:
                cols = st.columns(len(uploaded_files))
                for idx, img_file in enumerate(uploaded_files):
                    with cols[idx]:
                        st.image(img_file, width=150)

        # المعالجة المحلية الذكية
        file_count = len(uploaded_files) if uploaded_files else 0
        agent_output = f"""⚡ **تقرير المعالجة السيادية المتعددة:**
تم تلقي الأمر: *"{user_query}"*
📸 **تم إرفاق ومعالجة {file_count} صورة بنجاح** عبر الشاشة التفاعلية المحلية.
✅ النظام يعمل باستقلالية تامة وبدون أي قيود خارجية.
---
#AlphaCoreNexus #MultiAsset #SovereignAI"""

        if supabase:
            try:
                supabase.table("instant_ads").insert({
                    "title": f"[متعدد الصور ({file_count})] {user_query[:20]}...",
                    "content": agent_output.strip()
                }).execute()
            except:
                pass

        st.session_state.messages.append({"role": "assistant", "content": agent_output.strip()})
        st.rerun()

with col_view:
    st.subheader("📋 الشاشة التفاعلية للوسائط والأرشيف")
    ads = load_ads_from_db()
    
    if not ads:
        st.info("لا توجد سجلات مسجلة حالياً.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} — {str(ad.get('created_at'))[:10]}"):
                st.write(ad.get('content'))
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    wa_link = f"https://wa.me/212691897126?text={urllib.parse.quote(ad.get('content'))}"
                    st.link_button("📲 نشر على الواتساب", wa_link, use_container_width=True)
                with col_btn2:
                    if st.button("🖼️ توليد بطاقة مصورة", key=f"btn_{ad.get('id')}", use_container_width=True):
                        img_buf = generate_ad_card(ad.get('title'), ad.get('content'))
                        st.image(img_buf, use_container_width=True)
                        st.download_button("⬇️ تحميل", img_buf, file_name="card.png", mime="image/png", key=f"dl_{ad.get('id')}", use_container_width=True)
