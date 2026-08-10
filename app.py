from datetime import datetime
import io
import os
import urllib.parse
import zipfile
from PIL import Image, ImageEnhance
import streamlit as st

# 1. إعداد النظام السيادي بشاشة عريضة
st.set_page_config(
    page_title="TASSAOUT OMEGA OS", page_icon="👑", layout="wide"
)
GALLERY_FOLDER = "gallery"
os.makedirs(GALLERY_FOLDER, exist_ok=True)

# 2. قاعدة المعرفة والعروض المتاحة
CORE_DB = {
    "sectors": [
        "عقار",
        "سيارات",
        "خدمات",
        "تسويق",
        "فلاحة",
        "لوجستيك",
        "تعاونيات",
        "قطع غيار",
        "مواد إنشائية",
    ],
    "cities": ["مراكش", "قلعة السراغنة", "الدار البيضاء", "أكادير", "طنجة"],
    "tech": {
        "عقار": "Hasselblad X2D",
        "سيارات": "Sony A1",
        "فلاحة": "Phase One IQ4",
        "قطع غيار": "Canon R5",
        "مواد إنشائية": "DJI Drone + Sony A1",
        "عام": "Universal Sensor",
    },
    "listings": {
        "عقار": [
            "أرض فلاحية 5 هكتارات بقلعة السراغنة - محفيقة ومجهزة",
            "بقعة تجارية وسط مراكش - واجهة رئيسية",
        ],
        "سيارات": [
            "شاحنة نقل بضائع دولية - حالة ممتازة موديل حديث",
            "سيارة نفعية رباعية الدفع - صيانة دورية متميزة",
        ],
        "مواد إنشائية": [
            "مواد بناء وأسمنت وحديد تسليح - توريد مباشر بقلعة السراغنة",
            "معدات وتجهيزات الورش الكبرى",
        ],
        "فلاحة": [
            "تجهيز سقي بقطرة الماء لأنظمة الأراضي الكبرى",
            "معدات حراثة وتسميد رقمية متطورة",
        ],
    },
}

# 3. إعدادات الكاميرا والتوثيق البصري الفائق
ENVIRONMENT_PRESETS = {
    "عقار فخم": {
        "camera": "Hasselblad X2D",
        "sharpness": 2.2,
        "contrast": 1.6,
        "color": 1.3,
    },
    "قطع غيار/سيارات": {
        "camera": "Sony A1",
        "sharpness": 1.9,
        "contrast": 1.8,
        "color": 1.2,
    },
    "مواد إنشائية/ميدان": {
        "camera": "DJI Drone + Sony A1",
        "sharpness": 1.5,
        "contrast": 1.8,
        "color": 1.2,
    },
}

def apply_agentic_vision(image, preset):
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(preset["sharpness"])
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(preset["contrast"])
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(preset["color"])
    return image

def save_to_gallery(image, env_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{GALLERY_FOLDER}/MEGA_{timestamp}_{env_name.replace(' ', '_')}.jpg"
    image.save(filename, quality=95)
    return filename

# 4. قوالب التقارير الاحترافية والمؤسساتية
xl_templates = {
    "عقار": lambda city, gear, details: (
        f"--- 👑 مكتب تساوت الرقمي العقار والأعمال بقلعة السراغنة 👑 ---\n"
        f"[ TASSAOUT OMEGA PREMIUM - 100MP PRO-GRADE ]\n\n"
        f"القطاع: عقار | المدينة: {city}\n"
        f"النمط البصري: Dark/Cinematic\n\n"
        f"📢 الإعلان الترويجي:\n"
        f"العرض المعني: {details}\n"
        f"caméra tassaout méga go\n\n"
        f"📸 التوثيق البصري:\n"
        f"- تقنية التوثيق: {gear}\n"
        f"- المعالجة: 100MP Super-Resolution\n"
        f"- التوازن البصري: Dark/Cinematic Mode Optimized\n"
        f"--------------------------------------------------\n"
        f"✒️ التوقيع الرسمي: Ameur signature\n"
        f"⚡ نظام TASSAOUT OMEGA OS"
    ),
    "مواد إنشائية": lambda city, gear, details: (
        f"--- 👑 مكتب تساوت الرقمي العقار والأعمال بقلعة السراغنة 👑 ---\n"
        f"[ TASSAOUT OMEGA PREMIUM - 100MP PRO-GRADE ]\n\n"
        f"القطاع: مواد إنشائية | المدينة: {city}\n"
        f"النمط البصري: Dark/Cinematic\n\n"
        f"📢 الإعلان الترويجي:\n"
        f"العرض المعني: {details}\n"
        f"caméra tassaout méga go\n\n"
        f"📸 التوثيق البصري:\n"
        f"- تقنية التوثيق: {gear}\n"
        f"- المعالجة: 100MP Super-Resolution\n"
        f"- التوازن البصري: Dark/Cinematic Mode Optimized\n"
        f"--------------------------------------------------\n"
        f"✒️ التوقيع الرسمي: Ameur signature\n"
        f"⚡ نظام TASSAOUT OMEGA OS"
    ),
}

# 5. حالة النظام
if "last_action" not in st.session_state:
    st.session_state["last_action"] = "System Idle - Monitoring All Sectors..."

# 6. واجهة المستخدم المركزية
st.title("👑 TASSAOUT OMEGA OS | Field Agent v3.0")
st.sidebar.success("System Status: Online & Secured ✅")
st.sidebar.metric("الصور المؤرشفة ميدانياً", len(os.listdir(GALLERY_FOLDER)))

tab1, tab2, tab3 = st.tabs([
    "📸 الكاميرا والتوثيق الشامل", 
    "🧠 شاشة تفاعل الوكيل وإرسال التقارير", 
    "📦 الأرشيف والتحميل"
])

with tab1:
    st.subheader("📷 مركز التصوير والتوثيق الميداني العالي")
    col1, col2 = st.columns(2)
    with col1:
        selected_env = st.selectbox("اختر بيئة التصوير:", list(ENVIRONMENT_PRESETS.keys()))
    with col2:
        selected_sector = st.selectbox("اختر القطاع:", CORE_DB["sectors"])

    current_preset = ENVIRONMENT_PRESETS.get(selected_env, list(ENVIRONMENT_PRESETS.values())[0])

    photo = st.camera_input("التقط المشهد بوضوح تام (الكاميرا مفعلة)", key="mega_cam_screen")

    if photo:
        raw_image = Image.open(photo)
        processed_image = apply_agentic_vision(raw_image, current_preset)
        image_path = save_to_gallery(processed_image, selected_env)
        st.image(
            processed_image,
            caption=f"✅ تم التوثيق بنجاح عبر عدسة {current_preset['camera']}",
            use_container_width=True,
        )
        st.success("تم حفظ الصورة في الأرشيف الميداني تلقائياً.")

with tab2:
    st.subheader("🧠 شاشة التفاعل المباشر مع الوكيل (TASSAOUT MEGA GO)")

    active_sector = st.selectbox("استعراض العروض المسجلة في النظام:", CORE_DB["sectors"], key="sec_view")
    available_items = CORE_DB["listings"].get(active_sector, ["عروض عامة متوفرة في النظام للتطوير والتسويق"])
    selected_item = st.selectbox("اختر العنصر للعمل عليه:", available_items)

    user_input = st.text_area(
        "أدخل تعليماتك للوكيل (أو الكود السري):",
        value=f"caméra tassaout méga go {active_sector} قلعة السراغنة - {selected_item}",
        height=100,
    )

    if st.button("🚀 تنفيذ أمر الوكيل وتجهيز التقرير"):
        city = next((c for c in CORE_DB["cities"] if c in user_input), "قلعة السراغنة")
        gear = CORE_DB["tech"].get(active_sector, "Universal Sensor")

        generator = xl_templates.get(
            active_sector,
            lambda c, g, d: (
                f"--- 👑 مكتب تساوت الرقمي العقار والأعمال بقلعة السراغنة 👑 ---\n"
                f"[ TASSAOUT OMEGA PREMIUM - 100MP PRO-GRADE ]\n\n"
                f"القطاع: {active_sector} | المدينة: {c}\n"
                f"النمط البصري: Dark/Cinematic\n\n"
                f"📢 الإعلان الترويجي:\n"
                f"العرض: {d}\n"
                f"caméra tassaout méga go\n\n"
                f"📸 التوثيق البصري:\n"
                f"- التوثيق: {g}\n"
                f"- المعالجة: 100MP Super-Resolution\n"
                f"--------------------------------------------------\n"
                f"✒️ التوقيع الرسمي: Ameur signature\n"
                f"⚡ نظام TASSAOUT OMEGA OS"
            ),
        )
        report_text = generator(city, gear, selected_item)
        st.session_state["last_action"] = report_text

        st.success("🎯 تم توليد التقرير المؤسساتي بنجاح بواسطة الوكيل!")
        st.code(report_text, language="markdown")

        whatsapp_number = "212691897126"
        encoded_text = urllib.parse.quote(report_text)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_text}"
        st.link_button("📱 اضغط هنا لإرسال التقرير فوراً عبر الواتساب", whatsapp_url)

with tab3:
    st.subheader("📦 الأرشيف الذكي والتحميل")
    st.write("جميع الصور والتقارير الميدانية تُحفظ هنا بشكل منظم.")
    if st.button("📦 توليد وتحميل حزمة الأرشيف الكاملة (ZIP)"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in os.listdir(GALLERY_FOLDER):
                zip_file.write(os.path.join(GALLERY_FOLDER, file), file)
        st.download_button(
            "⬇️ تحميل الأرشيف البرمجي والميداني الآن",
            data=zip_buffer.getvalue(),
            file_name=f"ARCHIVE_TASSAOUT_{datetime.now().strftime('%Y-%m-%d')}.zip",
        )
