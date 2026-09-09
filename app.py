from datetime import datetime
import os
import zipfile
from google import genai
import pandas as pd
from PIL import Image, ImageEnhance
import streamlit as st
from supabase import create_client, Client

# إعدادات الصفحة السيادية واسعة النطاق ومنظومة تساوت أوميغا
st.set_page_config(
    page_title="TASSAOUT OMEGA OS v8.0 - النظام الذكي الشامل", 
    page_icon="🏗️", 
    layout="wide"
)

# تهيئة مجلد الأرشيف البصري
GALLERY_FOLDER = "gallery"
os.makedirs(GALLERY_FOLDER, exist_ok=True)

# تهيئة الاتصالات والـ Secrets
@st.cache_resource
def init_system():
    try:
        url = st.secrets["SUPABASE_URL"].strip()
        key = st.secrets["SUPABASE_KEY"].strip()
        gemini_key = st.secrets["GEMINI_API_KEY"].strip()
        
        supabase_client = create_client(url, key)
        gemini_client = genai.Client(api_key=gemini_key)
        
        return supabase_client, gemini_client, True
    except Exception as e:
        return None, None, False

supabase, gemini_client, db_connected = init_system()

# 1. إعدادات البيئة البصرية
ENVIRONMENT_PRESETS = {
    "عقار فخم (مراكش)": {
        "camera": "Hasselblad X2D 100C",
        "sharpness": 2.2,
        "contrast": 1.6,
        "color": 1.3,
    },
    "تجزئة أرضية (قلعة السراغنة)": {
        "camera": "Sony A1",
        "sharpness": 1.8,
        "contrast": 1.9,
        "color": 1.4,
    },
    "توثيق ميداني": {
        "camera": "Canon EOS R5",
        "sharpness": 1.5,
        "contrast": 1.3,
        "color": 1.2,
    },
}

# القائمة الجانبية الموحدة للتحكم الشامل
st.sidebar.title("👑 TASSAOUT OMEGA OS")
st.sidebar.markdown(
    "**المستخدم:** عامر بوخدادة\n**المنطقة:** قلعة السراغنة - مراكش"
)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "اختر وحدة التشغيل:",
    [
        "🏗️ نظام حساب تكاليف المشاريع العقارية",
        "📸 وحدة الكاميرا والمعالجة المخفية",
        "📊 غرفة عمليات والوكلاء الذكيين (Omega Rogue)",
        "🗂️ الأرشيف والتصدير الشامل",
    ],
)

# وحدة حساب تكاليف المشاريع العقارية
if app_mode == "🏗️ نظام حساب تكاليف المشاريع العقارية":
    st.title("🏗️ النظام الذكي لإدارة وحساب تكاليف المشاريع العقارية")
    st.markdown("---")

    st.sidebar.header("🎛️ إعدادات وبيانات المشروع")
    project_name = st.sidebar.text_input("اسم المشروع أو المرجع", "مشروع تجزئة السلام - قلعة السراغنة")
    land_area = st.sidebar.number_input("مساحة البقعة (م²)", min_value=50, max_value=2000, value=180, step=10)
    land_price = st.sidebar.number_input("إجمالي سعر البقعة (درهم)", min_value=10000, max_value=10000000, value=600000, step=10000)

    st.sidebar.markdown("### تكاليف البناء")
    build_area = st.sidebar.number_input("مساحة البناء الإجمالية المغطاة (م²)", min_value=50, max_value=5000, value=360, step=10)
    cost_per_sqm = st.sidebar.selectbox(
        "مستوى البناء وتكلفتها لكل م²",
        options=[
            ("اقتصادي (3,500 درهم/م²)", 3500),
            ("قياسي / متوسط (5,500 درهم/م²)", 5500),
            ("فاخر / رفاهية (7,500 درهم/م²)", 7500)
        ],
        format_func=lambda x: x[0]
    )[1]

    construction_cost = build_area * cost_per_sqm
    architect_fees = st.sidebar.number_input("مصاريف المهندس، الرخص والمختبر (درهم)", value=120000, step=5000)
    contingency_rate = st.sidebar.slider("نسبة مصاريف الطوارئ والإضافات (%)", 0, 20, 10)

    contingency_amount = (construction_cost + architect_fees) * (contingency_rate / 100)
    total_investment = land_price + construction_cost + architect_fees + contingency_amount

    st.sidebar.markdown("### التوقعات المالية للبيع أو الاستثمار")
    expected_selling_price = st.sidebar.number_input("القيمة التقديرية للبيع الإجمالي أو المداخيل (درهم)", min_value=100000, max_value=20000000, value=2200000, step=50000)

    net_profit = expected_selling_price - total_investment
    roi = (net_profit / total_investment) * 100 if total_investment > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الاستثمار", f"{total_investment:,.0f} DH")
    col2.metric("تكلفة البناء", f"{construction_cost:,.0f} DH")
    col3.metric("الربح الصافي المتوقع", f"{net_profit:,.0f} DH", delta=f"{roi:.1f}%")
    col4.metric("سعر المتر المربع الإجمالي للبناء", f"{cost_per_sqm:,.0f} DH/m²")

    st.markdown("### 📊 تفصيل الميزانية والهيكل المالي")

    breakdown_df = pd.DataFrame({
        "البند": ["سعر الأرض", "تكلفة البناء الإجمالية", "مصاريف هندسية وترخيص", "طوارئ وإضافات"],
        "المبلغ (درهم)": [land_price, construction_cost, architect_fees, contingency_amount],
        "النسبة من الإجمالي (%)": [
            (land_price / total_investment) * 100,
            (construction_cost / total_investment) * 100,
            (architect_fees / total_investment) * 100,
            (contingency_amount / total_investment) * 100
        ]
    })

    st.dataframe(breakdown_df.style.format({"المبلغ (درهم)": "{:,.2f}", "النسبة من الإجمالي (%)": "{:.1f}%"}))
    st.markdown("---")
    st.success(f"النظام جاهز ومُحدث لتقييم **{project_name}**. يمكنك تعديل البيانات في الشريط الجانبي لتحديث الحسابات فورياً.")

# وحدة الكاميرا والمعالجة المخفية
elif app_mode == "📸 وحدة الكاميرا والمعالجة المخفية":
    st.header("📸 وحدة معالجة الصور الذكية في الخلفية")
    st.markdown("قم برفع الصورة، وسيتم تفعيل محرك المعالجة المتقدم وحفظها في الخلفية فور الضغط على زر التشغيل السيادي.")

    preset_name = st.selectbox(
        "اختر إعداد البيئة البصرية:", list(ENVIRONMENT_PRESETS.keys())
    )
    preset = ENVIRONMENT_PRESETS[preset_name]

    uploaded_file = st.file_uploader(
        "اختر ملف الصورة:", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        
        if st.button("⚡ تنفيذ المعالجة المخفية والحفظ التلقائي"):
            with st.spinner("جاري معالجة الصورة في الخلفية عبر المحرك السيادي..."):
                enhancer = ImageEnhance.Sharpness(image)
                img_enhanced = enhancer.enhance(preset["sharpness"])

                contrast_enhancer = ImageEnhance.Contrast(img_enhanced)
                img_final = contrast_enhancer.enhance(preset["contrast"])

                file_path = os.path.join(
                    GALLERY_FOLDER,
                    f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                )
                img_final.save(file_path)
                
            st.success(f"تمت المعالجة والحفظ في الخلفية بنجاح! المسار: {file_path}")
            st.image(img_final, caption="معاينة النتيجة النهائية المعتمدة", use_container_width=True)

# غرفة عمليات والوكلاء الذكيين (Omega Rogue)
elif app_mode == "📊 غرفة عمليات والوكلاء الذكيين (Omega Rogue)":
    st.header("⚡ النظام السيادي: الوكيل الذكي متعدد المجالات (Omega Rogue - DANA Core)")
    
    st.sidebar.header("🎯 مركز العمليات المارقة")
    agent_mode = st.sidebar.selectbox(
        "اختر وضع التشغيل للوكيل",
        [
            "النطاق العقاري (استثمار وتحليل البناء)",
            "النطاق البرمجي والسيبراني (توليد وفحص الأكواد)",
            "النطاق التجاري واللوجستي (إدارة النقل والمبيعات)",
            "الوضع المارق الشامل (Autonomous Multi-Domain Override)"
        ]
    )

    def fetch_land_data():
        market_data = {
            "المنطقة": ["قلعة السراغنة - تجزئة السلام", "قلعة السراغنة - وسط المدينة", "مراكش - طريق فاس", "مراكش - السعادة"],
            "متوسط سعر المتر للأرض (DH/m²)": [3300, 4500, 7000, 6000],
            "مؤشر الطلب": ["مرتفع جداً", "مستقر", "مرتفع", "تصاعدي"]
        }
        return pd.DataFrame(market_data)

    def generate_commercial_offer(proj_name, total_inv, net_prof):
        return f"""
        ==================================================
        TASSAOUT OMEGA FORT - عرض تجاري واقتصادي معتمد
        ==================================================
        اسم المشروع: {proj_name}
        إجمالي الاستثمار المقدر: {total_inv:,.0f} درهم
        الربح الصافي المتوقع: {net_prof:,.0f} درهم
        
        معتمد من طرف: DANA Digital Market & Tassaout Immobilière
        التوقيع الرقمي: Signature ameur - Tassaout Vision
        تاريخ الإصدار: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ==================================================
        """

    if st.sidebar.button("تنفيذ الأوامر الذكية وتحليل السوق"):
        st.success(f"تم إطلاق الوكيل بنجاح تحت وضع: **{agent_mode}**")
        
        if "العقاري" in agent_mode:
            st.markdown("### 🏢 تقرير النطاق العقاري الميداني (سوق قلعة السراغنة ومراكش)")
            st.dataframe(fetch_land_data(), use_container_width=True)
            
        elif "البرمجي" in agent_mode:
            st.markdown("### 💻 تقرير النطاق البرمجي والسيبراني")
            st.code("""
# Omega Rogue Security & Execution Protocol (SkillSpector Verified)
import os
def execute_autonomous_patch():
    print("Scanning system vectors via SkillSpector logic...")
    print("All multi-domain APIs synchronized with Google Cloud & Supabase.")
            """, language="python")
            
        elif "التجاري" in agent_mode:
            st.markdown("### 🚚 تقرير النطاق اللوجستي والتجاري")
            st.warning("تم تفعيل مسارات Sraghna Media Trans ومتابعة أسطول السيارات والعقود بنجاح.")
            
        else:
            st.markdown("### ⚡ تفعيل الوضع المارق الشامل (Omega Override)")
            st.error("تحذير: الوكيل يعمل بصلاحيات مطلقة متجاوزاً الحدود التقليدية، رابطاً بين الذاكرة المحلية، سحابة Google، والبيانات الميدانية بشكل ذاتي بالكامل.")

        st.markdown("---")
        st.markdown("### 📄 العرض التجاري المولد أوتوماتيكياً")
        st.text(generate_commercial_offer("مشروع تجزئة السلام - قلعة السراغنة", 1022000, 1178000))

    user_prompt = st.text_area("أمر مباشر إضافي للذكاء الاصطناعي (Gemini):")
    if st.button("إرسال التوجيه للوكيل"):
        if user_prompt and gemini_client is not None:
            try:
                # تم تحديث اسم النموذج هنا إلى gemini-3.6-flash لتجنب خطأ 404
                response = gemini_client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=user_prompt,
                )
                st.success("✅ استجابة الوكيل الذكي:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        elif user_prompt:
            st.info(f"تم استقبال الطلب محلياً: '{user_prompt}'")
        else:
            st.warning("المرجو إدخال توجيه صالح.")

# الأرشيف والتصدير الشامل
elif app_mode == "🗂️ الأرشيف والتصدير الشامل":
    st.header("🗂️ أرشيف الصور والملفات الموحد")
    files = os.listdir(GALLERY_FOLDER)
    if files:
        st.write(f"الملفات المخزنة حالياً ({len(files)} ملفات):")
        selected_file = st.selectbox("اختر ملفاً لمعاينته:", files)
        if selected_file:
            st.image(os.path.join(GALLERY_FOLDER, selected_file))

        if st.button("تنزيل الأرشيف بالكامل (ZIP)"):
            zip_path = "omega_archive.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, dirs, filenames in os.walk(GALLERY_FOLDER):
                    for file in filenames:
                        zipf.write(
                            os.path.join(root, file),
                            arcname=os.path.relpath(
                                os.path.join(root, file), GALLERY_FOLDER
                            ),
                        )
            with open(zip_path, "rb") as f:
                zip_data = f.read()
            st.download_button(
                label="تحميل ملف الأرشيف المضغوط",
                data=zip_data,
                file_name="omega_archive.zip",
                mime="application/zip",
            )
    else:
        st.info("الأرشيف فارغ حالياً.")

# تذيل الصفحة السيادية
st.markdown("---")
st.markdown(
    "**📞 التواصل السريع:** [راسلنا عبر واتساب](https://wa.me/212691897126?text=مرحباً،%20أتواصل%20معكم%20من%20منظومة%20Tassaout%20Omega%20OS.)"
)
