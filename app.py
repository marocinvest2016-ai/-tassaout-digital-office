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
st.set_page_config(page_title="وكالة تساوت للإنتاج الرقمي", page_icon="⚙️", layout="wide")

# الاتصال بالخدمات عبر الأسرار
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

BRAND_WATERMARK_TEXT = "وكالة تساوت للانتاج الرقمي +212691897126"
BRAND_PHONE = "+212691897126"

# تحميل خط عربي بارز وكبير
@st.cache_resource
def load_ar_font():
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
        gdown.download(url, "Cairo-Bold.ttf", quiet=True)
        return ImageFont.truetype("Cairo-Bold.ttf", 45)
    except: 
        return ImageFont.load_default()

font_main = load_ar_font()

# لوحات الألوان الفنية الاحترافية لتوليد الهوية البصرية المتجددة
PROFESSIONAL_PALETTES = [
    {"bg": (15, 23, 42, 230), "text": (251, 191, 36, 255)},   # كحلي عميق مع ذهبي ملكي
    {"bg": (127, 29, 29, 230), "text": (254, 240, 138, 255)},  # أحمر قرمزي فاخر مع أصفر فاتح
    {"bg": (6, 78, 59, 230), "text": (167, 243, 208, 255)},    # أخضر زمردي مع نعناعي ساطع
    {"bg": (88, 28, 135, 230), "text": (221, 214, 254, 255)},  # بنفسجي ملكي مع لافندر
    {"bg": (24, 24, 27, 240), "text": (244, 244, 245, 255)},   # أسود فحمي فخم مع أبيض ناصع
    {"bg": (120, 53, 15, 230), "text": (254, 215, 170, 255)},   # بني نحاسي دافئ مع بيج برونزي
]

def add_artistic_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    w, h = img.size
    
    # اختيار لوحة ألوان عشوائية ومتجددة لكل صورة
    palette = random.choice(PROFESSIONAL_PALETTES)
    
    # شريط أسفلي عريض وواضح لتثبيت العلامة المائية
    bar_height = 110
    draw.rectangle([0, h - bar_height, w, h], fill=palette["bg"])
    
    # كتابة النص الموحد باللون الاحترافي المتجدد
    draw.text((25, h - 80), BRAND_WATERMARK_TEXT, font=font_main, fill=palette["text"])
    
    buf = io.BytesIO()
    Image.alpha_composite(img, txt).convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# واجهة القائمة الجانبية (الأزرار الرئيسية)
st.sidebar.title("📌 واجهة تساوت التفاعلية")
menu = st.sidebar.radio("اختر القسم:", [
    "🧠 وكيل تساوت للإنتاج الرقمي", 
    "🚀 توليد الإعلانات الفورية", 
    "📸 استوديو التصوير والهوية البصرية (Groq Vision)", 
    "📊 الأرشيف السحابي",
    "📞 رقم الواتساب والتحميل اليدوي"
])

if "last_ad" not in st.session_state: st.session_state["last_ad"] = ""
if "last_title" not in st.session_state: st.session_state["last_title"] = ""

# ==========================================
# 1. وكيل تساوت للإنتاج الرقمي
# ==========================================
if menu == "🧠 وكيل تساوت للإنتاج الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي")
    st.write("مرحباً بك في المساعد الذكي الخاص بالوكالة. اطرح أي مهمة استراتيجية أو تسويقية:")
    
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
                    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; font-weight:bold; cursor:pointer;">📲 إرسال التقرير عبر الواتساب</button></a>', unsafe_allow_html=True)

# ==========================================
# 2. توليد الإعلانات الفورية
# ==========================================
elif menu == "🚀 توليد الإعلانات الفورية":
    st.subheader("🚀 قسم توليد الإعلانات الفورية")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("التصنيف:", ["عقارات", "هندسة وديكور", "خدمات رقمية", "أخرى"])
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
                "source": "Tassaout-Interface",
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            st.success("✅ تم حفظ الإعلان سحابياً في جدول instant_ads!")
        except Exception as e:
            st.error(f"خطأ في الحفظ: {e}")

# ==========================================
# 3. استوديو التصوير والهوية البصرية (Groq Vision)
# ==========================================
elif menu == "📸 استوديو التصوير والهوية البصرية (Groq Vision)":
    st.subheader("📸 استوديو التصوير وتحليل الهوية البصرية عبر Groq")
    st.info("الوكيل الذكي يحلل محتوى الصورة بصرياً، ويقوم بتطوير هويتها البصرية وتطبيق علامة مائية بارزة وملونة بشكل فني فريد لكل صورة.")

    uploaded_files = st.file_uploader("اختر الصور (رفع متعدد)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown("---")
        for idx, f in enumerate(uploaded_files):
            f_bytes = f.getvalue()
            
            # تحليل الصورة عبر نموذج الرؤية في Groq (Groq Vision)
            with st.spinner(f"جاري قيام الوكيل بتحليل وتطوير الهوية البصرية للصورة رقم ({idx+1}) عبر Groq..."):
                try:
                    b64_image = base64.b64encode(f_bytes).decode("utf-8")
                    vision_response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "قم بتقييم هذه الصورة الفوتوغرافية بإيجاز واقترح استراتيجية هوية بصرية تسويقية لها في جملة واحدة."},
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
                st.markdown(f"**💡 رؤية المصور الذكي (Groq):**")
                st.write(ai_analysis)
                st.download_button(
                    label=f"📥 تحميل الصورة {idx+1}",
                    data=processed_bytes,
                    file_name=f"tassaout_brand_vision_{idx+1}.jpg",
                    mime="image/jpeg",
                    key=f"dl_img_{idx}"
                )

# ==========================================
# 4. الأرشيف السحابي
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
# 5. رقم الواتساب للتحميل اليدوي
# ==========================================
elif menu == "📞 رقم الواتساب والتحميل اليدوي":
    st.subheader("📞 مركز الاتصال والتحميل اليدوي عبر الواتساب")
    st.write("يمكنك التواصل المباشر أو نسخ بيانات الواتساب الرسمية للوكالة:")
    
    st.metric("رقم الواتساب الرسمي للوكالة", BRAND_PHONE)
    
    whatsapp_direct = f"https://wa.me/{BRAND_PHONE.replace('+', '')}"
    st.markdown(f"### 🟢 [اضغط هنا لبدء محادثة واتساب فورية]({whatsapp_direct})")
    
    st.markdown("---")
    st.write("💡 **تعليمات التحميل اليدوي:**")
    st.markdown("1. توجه إلى **استوديو التصوير والهوية البصرية** للاستفادة من التحليل الذكي وتوليد الألوان المتجددة.")
    st.markdown("2. انسخ آخر إعلان تم توليده من قسم **توليد الإعلانات الفورية**.")
    st.markdown("3. أرسل الصورة والنص يدوياً عبر رقم الواتساب الخاص بالوكالة أو للعملاء مباشرة.")
