import urllib.parse
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
import requests

# إعداد الصفحة
st.set_page_config(page_title="وكالة تساوت للانتاج الرقمي والخدمات", page_icon="⚙️", layout="wide")

# الاتصال بالخدمات عبر الأسرار
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    supabase = None
    groq_client = None

BRAND_WATERMARK_TEXT = "وكالة تساوت للانتاج الرقمي +212691897126"
BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"

# تحميل خط عربي بارز للعلامة المائية
@st.cache_resource
def load_ar_font():
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
        gdown.download(url, "Cairo-Bold.ttf", quiet=True)
        return ImageFont.truetype("Cairo-Bold.ttf", 42)
    except: 
        return ImageFont.load_default()

font_main = load_ar_font()

# مصفوفة الألوان والأنماط الفنية للعلامة المائية
PROFESSIONAL_PALETTES = [
    {"bg": (15, 23, 42, 255), "glow": (59, 130, 246, 255), "text": (255, 255, 255, 255)},    # كحلي داكن
    {"bg": (127, 29, 29, 255), "glow": (254, 240, 138, 255), "text": (255, 255, 255, 255)}, # أحمر قرمزي فاخر
    {"bg": (6, 78, 59, 255), "glow": (167, 243, 208, 255), "text": (255, 255, 255, 255)},    # أخضر زمردي
    {"bg": (88, 28, 135, 255), "glow": (221, 214, 254, 255), "text": (255, 255, 255, 255)}, # بنفسجي ملكي
    {"bg": (10, 10, 10, 255), "glow": (245, 158, 11, 255), "text": (255, 255, 255, 255)},    # أسود فاحم مع ذهبي
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

# دالة توليد الصورة برمجياً عبر وصف نصي وتطبيق الهوية البصرية
def generate_ai_image(prompt_text):
    encoded_prompt = urllib.parse.quote(prompt_text)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    
    try:
        res = requests.get(image_url, timeout=30)
        if res.status_code == 200:
            return res.content
    except Exception as e:
        st.error(f"خطأ في توليد الصورة: {e}")
    
    return None

# واجهة القائمة الجانبية للتحكم والأقسام
st.sidebar.title("📌 لوحة التحكم والخدمات")
menu = st.sidebar.radio("اختر القسم:", [
    "🏠 الواجهة الرسمية (الرئيسية)",
    "🌐 موقع الخدمات المحلي (Sraghna Services)",
    "🧠 وكيل تساوت للإنتاج الرقمي", 
    "🚀 توليد الإعلانات الفورية", 
    "📸 استوديو التصوير والهوية البصرية", 
    "🎨 استوديو توليد الصور بالذكاء الاصطناعي",
    "📊 الأرشيف السحابي",
    "📞 التواصل والاتصال المباشر"
])

if "last_ad" not in st.session_state: st.session_state["last_ad"] = ""
if "last_title" not in st.session_state: st.session_state["last_title"] = ""

# ==========================================
# 1. الواجهة الرسمية (الرئيسية النظيفة)
# ==========================================
if menu == "🏠 الواجهة الرسمية (الرئيسية)":
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
        
        .main-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 70vh;
            text-align: center;
            font-family: 'Cairo', sans-serif;
        }
        
        .agency-title {
            font-size: 3.5rem;
            font-weight: 900;
            color: #1e293b;
            margin-bottom: 25px;
            line-height: 1.3;
        }
        
        .phone-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #25D366;
            direction: ltr;
            background: #f0fdf4;
            padding: 10px 30px;
            border-radius: 50px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            display: inline-block;
            margin-bottom: 30px;
        }
        
        .whatsapp-link {
            background-color: #25D366;
            color: white !important;
            padding: 12px 35px;
            border-radius: 30px;
            font-size: 1.3rem;
            font-family: 'Cairo', sans-serif;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
            transition: 0.3s;
        }
        
        .whatsapp-link:hover {
            background-color: #22bf5b;
        }
        </style>
        
        <div class="main-container">
            <div class="agency-title">وكالة تساوت للانتاج الرقمي</div>
            <div>
                <span class="phone-number">0691897126</span>
            </div>
            <div>
                <a href="https://wa.me/212691897126" target="_blank" class="whatsapp-link">مراسلة عبر الواتساب</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. عرض موقع الخدمات المحلي (Sraghna Services)
# ==========================================
elif menu == "🌐 موقع الخدمات المحلي (Sraghna Services)":
    st.subheader("🌐 منصة Sraghna Services - قلعة السراغنة ومراكش")
    st.markdown("مرحباً بك في الواجهة المدمجة الخاصة بخدماتك الرقمية والعقارية ونقل البضائع:")
    
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
        st.markdown("- **Sraghna Media Trans:** خدمات نقل البضائع واللوجستيات بأمان وسرعة.")

# ==========================================
# 3. وكيل تساوت للإنتاج الرقمي
# ==========================================
elif menu == "🧠 وكيل تساوت للإنتاج الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي")
    user_task = st.text_area("أدخل المهمة أو الاستشارة:", height=150)
    if st.button("⚡ تنفيذ المهمة", type="primary"):
        if user_task and groq_client:
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
        else:
            st.warning("الرجاء إدخال نص المهمة أو التأكد من إعدادات مفتاح Groq.")

# ==========================================
# 4. توليد الإعلانات الفورية
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

        if supabase:
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
                st.error(f"خطأ في الحفظ السحابي: {e}")

# ==========================================
# 5. استوديو التصوير والهوية البصرية
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
# 6. استوديو توليد الصور بالذكاء الاصطناعي
# ==========================================
elif menu == "🎨 استوديو توليد الصور بالذكاء الاصطناعي":
    st.subheader("🎨 استوديو توليد الصور البصرية والتسويقية بالذكاء الاصطناعي")
    st.info("أدخل وصفاً تفصيلياً للصورة أو التصميم الذي ترغب في إنشائه (مثل: واجهة فيلا عصرية بقلعة السراغنة، لافتة محل تجاري، إلخ).")

    ai_prompt_input = st.text_area("وصف الصورة المطلوبة (Prompt):", "Modern luxury apartment exterior design in Morocco, architectural rendering, high quality")
    
    if st.button("🚀 توليد الصورة وتطبيق الهوية البصرية", type="primary"):
        if ai_prompt_input:
            with st.spinner("جاري توليد الصورة عبر الذكاء الاصطناعي..."):
                raw_image_bytes = generate_ai_image(ai_prompt_input)
                
                if raw_image_bytes:
                    # تطبيق العلامة المائية الخاصة بوكالة تساوت تلقائياً
                    final_watermarked_bytes = add_artistic_watermark(raw_image_bytes)
                    
                    st.success("✅ تم توليد الصورة وتطبيق الهوية البصرية بنجاح!")
                    st.image(final_watermarked_bytes, caption="الصورة المولدة مع العلامة المائية الرسمية", use_container_width=True)
                    
                    st.download_button(
                        label="📥 تحميل الصورة النهائية",
                        data=final_watermarked_bytes,
                        file_name="tassaout_ai_generated_image.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("تعذر توليد الصورة، يرجى المحاولة مرة أخرى بوصف مختلف.")
        else:
            st.warning("الرجاء إدخال وصف صالح للصورة أولاً.")

# ==========================================
# 7. الأرشيف السحابي
# ==========================================
elif menu == "📊 الأرشيف السحابي":
    st.subheader("📊 الأرشيف السحابي (قاعدة بيانات instant_ads)")
    if supabase:
        try:
            ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(50).execute()
            if ads_data.data:
                st.dataframe(pd.DataFrame(ads_data.data), use_container_width=True)
                st.metric("إجمالي السجلات والأرشيف", len(ads_data.data))
            else:
                st.info("لا توجد سجلات حالياً في الأرشيف.")
        except Exception as e:
            st.error(f"خطأ في جلب الأرشيف: {e}")
    else:
        st.warning("اتصال Supabase غير مهفر أو غير متوفر في الأسرار.")

# ==========================================
# 8. التواصل والاتصال المباشر
# ==========================================
elif menu == "📞 التواصل والاتصال المباشر":
    st.subheader("📞 مركز الاتصال والخدمات")
    st.metric("رقم الواتساب الرسمي للوكالة", LOCAL_PHONE)
    
    whatsapp_direct = f"https://wa.me/212{LOCAL_PHONE[1:]}"
    st.markdown(f"### 🟢 [اضغط هنا لبدء محادثة واتساب فورية]({whatsapp_direct})")
    st.markdown("---")
    st.write("📍 **الموقع:** قلعة السراغنة ومراكش، المملكة المغربية.")
