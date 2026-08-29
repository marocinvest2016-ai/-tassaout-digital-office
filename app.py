import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
import io
import gdown
import pandas as pd
import random
import base64

# إعداد الصفحة
st.set_page_config(page_title="وكالة تساوت للإنتاج الرقمي والخدمات", page_icon="⚙️", layout="wide")

# الاتصال بالخدمات عبر الأسرار
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

BRAND_WATERMARK_TEXT = "وكالة تساوت للانتاج الرقمي +212691897126"
BRAND_PHONE = "+212691897126"

# تحميل خط عربي بارز مع ضبط الحجم ليكون واضحاً وضخماً
@st.cache_resource
def load_ar_font():
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
        gdown.download(url, "Cairo-Bold.ttf", quiet=True)
        return ImageFont.truetype("Cairo-Bold.ttf", 42)
    except: 
        return ImageFont.load_default()

font_main = load_ar_font()

# مصفوفة الألوان والأنماط الفنية المتجددة
PROFESSIONAL_PALETTES = [
    {"bg": (15, 23, 42, 255), "glow": (59, 130, 246, 255), "text": (255, 255, 255, 255)},   # كحلي داكن
    {"bg": (127, 29, 29, 255), "glow": (254, 240, 138, 255), "text": (255, 255, 255, 255)}, # أحمر قرمزي فاخر
    {"bg": (6, 78, 59, 255), "glow": (167, 243, 208, 255), "text": (255, 255, 255, 255)},   # أخضر زمردي
    {"bg": (88, 28, 135, 255), "glow": (221, 214, 254, 255), "text": (255, 255, 255, 255)}, # بنفسجي ملكي
    {"bg": (10, 10, 10, 255), "glow": (245, 158, 11, 255), "text": (255, 255, 255, 255)},   # أسود فاحم مع ذهبي
]

def add_artistic_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    w, h = img.size
    
    palette = random.choice(PROFESSIONAL_PALETTES)
    bar_height = 130
    
    bar_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_bar = ImageDraw.Draw(bar_layer)
    draw_bar.rectangle([0, h - bar_height, w, h], fill=palette["bg"])
    
    text_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw_txt = ImageDraw.Draw(text_layer)
    
    try:
        bbox = font_main.getbbox(BRAND_WATERMARK_TEXT)
        text_w = bbox[2] - bbox[0]
    except:
        text_w = len(BRAND_WATERMARK_TEXT) * 15
        
    x_pos = (w - text_w) // 2
    if x_pos < 20: 
        x_pos = 20
        
    y_pos = h - (bar_height // 2) - 22
    
    draw_txt.text((x_pos + 2, y_pos + 2), BRAND_WATERMARK_TEXT, font=font_main, fill=(0, 0, 0, 255))
    draw_txt.text((x_pos, y_pos), BRAND_WATERMARK_TEXT, font=font_main, fill=palette["text"])
    
    combined = Image.alpha_composite(img, bar_layer)
    final_img = Image.alpha_composite(combined, text_layer)
    
    buf = io.BytesIO()
    final_img.convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# واجهة القائمة الجانبية (شاملة أقسام موقع الخدمات وساتس تساوت)
st.sidebar.title("📌 منصة تساوت المتكاملة")
menu = st.sidebar.radio("اختر القسم:", [
    "🌐 عرض موقع الخدمات المحلي (Sraghna Services)",
    "🧠 وكيل تساوت للإنتاج الرقمي", 
    "🚀 توليد الإعلانات الفورية", 
    "📸 استوديو التصوير والهوية البصرية", 
    "📊 الأرشيف السحابي",
    "📞 التواصل والاتصال المباشر"
])

if "last_ad" not in st.session_state: st.session_state["last_ad"] = ""
if "last_title" not in st.session_state: st.session_state["last_title"] = ""

# ==========================================
# 1. عرض موقع الخدمات المحلي (مدمج من مستودع Sraghna-services-)
# ==========================================
if menu == "🌐 عرض موقع الخدمات المحلي (Sraghna Services)":
    st.subheader("🌐 منصة Sraghna Services - قلعة السراغنة ومراكش")
    st.markdown("مرحباً بك في الواجهة المدمجة الخاصة بخدماتك الرقمية والعقارية ونقل البضائع. يمكنك معاينة الأقسام أدناه:")
    
    tab1, tab2, tab3 = st.tabs(["🏠 العقارات والاستثمار", "💻 الخدمات الرقمية", "🚚 النقل والسيارات"])
    
    with tab1:
        st.markdown("### قطاع العقارات والأراضي")
        st.info("نقدم عروضاً حصرية لشقق سكنية، بقع أرضية، وفيلات بقلعة السراغنة ومراكش.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("- **شقق العصر الحديث:** تشطيبات رفيعة المستوى.")
            st.markdown("- **بقع تجارية:** مواقع استراتيجية للاستثمار.")
        with c2:
            st.markdown("- **أراضي فلاحية:** مساحات مختلفة وموثقة.")
            st.markdown("- **فيلات راقية:** بضواحي قلعة السراغنة ومراكش.")

    with tab2:
        st.markdown("### الخدمات الرقمية وتسويق الوسائط")
        st.write("إدارة الحملات الإعلانية، تصميم الهوية البصرية، وإنشاء اللوحات الرقمية.")
        st.markdown("- **Sraghna Media:** إنتاج مرئي وتسويق رقمي متكامل.")
        st.markdown("- **DANA Digital Market:** حلول تسويق إلكتروني مبتكرة.")

    with tab3:
        st.markdown("### خدمات النقل اللوجستي وتأجير السيارات")
        st.markdown("- **Marrakech World Auto Services:** أسطول سيارات متاح للتأجير.")
        st.markdown("- **Sraghna Media Trans:** خدمات نقل البضائع واللوجستيات بآمان وسرعة.")

# ==========================================
# 2. وكيل تساوت للإنتاج الرقمي
# ==========================================
elif menu == "🧠 وكيل تساوت للإنتاج الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي")
    user_task = st.text_area("أدخل المهمة أو الاستشارة:", height=150)
    if st.button("⚡ تنفيذ المهمة", type="primary"):
        if user_task:
            with st.spinner("جاري المعالجة بواسطة الذكاء الاصطناعي..."):
                try:
                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{"role": "user", "content": user_task}],
                        temperature=0.6
                    )
                    result = response.choices[0].message.content
                except:
                    result = "❌ تعذر الاتصال بنموذج الذكاء الاصطناعي حالياً."
                
                st.session_state["last_ad"] = result
                st.markdown("### 📊 نتيجة التحليل أو الرد:")
                st.markdown(result)
                
                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    st.download_button("📄 تحميل التقرير (ملف)", result, "tassaout_report.txt", use_container_width=True)
                with col_w2:
                    wa_url = f"https://wa.me/?text={quote(result)}"
                    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; font-weight:bold; cursor:pointer;">📲 إرسال عبر الواتساب</button></a>', unsafe_allow_html=True)

# ==========================================
# 3. توليد الإعلانات الفورية
# ==========================================
elif menu == "🚀 توليد الإعلانات الفورية":
    st.subheader("🚀 قسم توليد الإعلانات الفورية")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("التصنيف:", ["عقارات", "هندسة وديكور", "خدمات رقمية", "نقل ولوجستيك"])
        title = st.text_input("عنوان المشروع:", "شقق عصرية للبيع بقلعة السراغنة")
    with col2:
        city = st.text_input("المدينة / الموقع:", "قلعة السراغنة")
        price = st.text_input("السعر أو الميزانية:", "ابتداءً من 40 مليون سنتيم")
        
    details = st.text_area("تفاصيل إضافية:", "الطابق الأول، تشطيبات عالية الجودة، مساحات واسعة.")
    st.session_state["last_title"] = title

    if st.button("⚡ توليد الإعلان وحفظه", type="primary", use_container_width=True):
        prompt = f"اكتب إعلان تسويقي احترافي: التصنيف {category}, العنوان {title}, الموقع {city}, السعر {price}, التفاصيل {details}. اختمه برقم الهاتف {BRAND_PHONE}"
        with st.spinner("جاري صياغة الإعلان..."):
            try:
                response = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6
                )
                ad_text = response.choices[0].message.content
            except:
                ad_text = f"🔥 عرض حصري: {title} بمدينة {city}. للتواصل: {BRAND_PHONE}"

            st.session_state["last_ad"] = ad_text

        st.text_area("النص المتولد:", st.session_state["last_ad"], height=200)
        
        whatsapp_url = f"https://wa.me/?text={quote(ad_text)}"
        st.markdown(f"### 📲 [مشاركة مباشرة للإعلان عبر الواتساب]({whatsapp_url})")

        try:
            supabase.table("instant_ads").insert({
                "category": category,
                "city": city,
                "content": title,
                "message": ad_text,
                "price": 0,
                "source": "Sraghna-Services-Integrated",
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            st.success("✅ تم حفظ الإعلان سحابياً في جدول instant_ads!")
        except Exception as e:
            st.error(f"خطأ في الحفظ: {e}")

# ==========================================
# 4. استوديو التصوير والهوية البصرية
# ==========================================
elif menu == "📸 استوديو التصوير والهوية البصرية":
    st.subheader("📸 استوديو التصوير وتحليل الهوية البصرية عبر Groq")
    st.info("الوكيل الذكي يحلل محتوى الصورة، ويقوم بتطبيق العلامة المائية البارزة والواضحة بمنتصف الشريط السفلي.")

    uploaded_files = st.file_uploader("اختر الصور (رفع متعدد)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown("---")
        for idx, f in enumerate(uploaded_files):
            f_bytes = f.getvalue()
            
            with st.spinner(f"جاري معالجة الصورة رقم ({idx+1}) بالهوية البصرية وتطبيق العلامة المائية الواضحة..."):
                try:
                    b64_image = base64.b64encode(f_bytes).decode("utf-8")
                    vision_response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "قيم هذه الصورة باختصار واقترح رؤية تسويقية لها."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                            ]
                        }],
                        temperature=0.5
                    )
                    ai_analysis = vision_response.choices[0].message.content
                except:
                    ai_analysis = "صورة احترافية جاهزة للعرض والتسويق الرقمي."

            processed_bytes = add_artistic_watermark(f_bytes)
            
            col_img, col_info = st.columns([2, 1])
            with col_img:
                st.image(processed_bytes, caption=f"صورة مطورة ومعالجة رقم ({idx+1})", width=350)
            with col_info:
                st.markdown(f"**💡 رؤية المصور الذكي:**")
                st.write(ai_analysis)
                st.download_button(
                    label=f"📥 تحميل الصورة {idx+1}",
                    data=processed_bytes,
                    file_name=f"tassaout_brand_vision_{idx+1}.jpg",
                    mime="image/jpeg",
                    key=f"dl_img_{idx}"
                )

# ==========================================
# 5. الأرشيف السحابي
# ==========================================
elif menu == "📊 الأرشيف السحابي":
    st.subheader("📊 الأرشيف السحابي (قاعدة بيانات instant_ads)")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(50).execute()
        if ads_data.data:
            st.dataframe(pd.DataFrame(ads_data.data), use_container_width=True)
            st.metric("إجمالي السجلات والأرشيف", len(ads_data.data))
        else:
            st.info("لا توجد سجلات حالياً في الأرشيف.")
    except Exception as e:
        st.error(f"خطأ في جلب الأرشيف: {e}")

# ==========================================
# 6. التواصل والاتصال المباشر
# ==========================================
elif menu == "📞 التواصل والاتصال المباشر":
    st.subheader("📞 مركز الاتصال والخدمات")
    st.metric("رقم الواتساب الرسمي للوكالة", BRAND_PHONE)
    
    whatsapp_direct = f"https://wa.me/{BRAND_PHONE.replace('+', '')}"
    st.markdown(f"### 🟢 [اضغط هنا لبدء محادثة واتساب فورية]({whatsapp_direct})")
    st.markdown("---")
    st.write("📍 **الموقع:** قلعة السراغنة ومراكش، المملكة المغربية.")
