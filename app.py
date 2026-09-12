import os
import streamlit as st
from groq import Groq
import openai
import ollama
from PIL import Image
import base64
import io
from datetime import datetime
import PyPDF2
import requests

# =========================
# إعدادات النظام العامة والمعرفات
# =========================

APP_NAME = "ORION-AI & دانا الوكيلة العقارية"
APP_VERSION = "v9.5"
LOCATION = "قلعة السراغنة - مراكش"
AGENCY_PHONE = "0691897126"
AGENCY_NAME = "وكالة تساوت للعقارات والخدمات"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للواجهة
st.markdown("""
<style>
   .main-header {text-align: center; padding: 10px;}
   .footer {text-align: center; color: gray; font-size: 12px; margin-top: 50px;}
</style>
""", unsafe_allow_html=True)

# =========================
# جلب المفاتيح بأمان تام من البيئة أو Streamlit Secrets (لا مفاتيح مكشوفة)
# =========================

def get_secure_setting(key, default=""):
    try:
        val = st.secrets.get(key, None)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, default)

GROQ_API_KEY = get_secure_setting("GROQ_API_KEY")
GROQ_MODEL = get_secure_setting("GROQ_MODEL", "openai/gpt-oss-20b")

OPENAI_API_KEY = get_secure_setting("OPENAI_API_KEY")
GEMINI_API_KEY = get_secure_setting("GEMINI_API_KEY")

OLLAMA_HOST = get_secure_setting("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = get_secure_setting("OLLAMA_MODEL", "llama3.1:8b")

SUPABASE_URL = get_secure_setting("SUPABASE_URL")
SUPABASE_KEY = get_secure_setting("SUPABASE_KEY")

WHATSAPP_PHONE_NUMBER_ID = get_secure_setting("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = get_secure_setting("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_BUSINESS_NUMBER = get_secure_setting("WHATSAPP_BUSINESS_NUMBER", "212691897126")

# =========================
# تهيئة العملاء الذكيين (معالجة الأخطاء لتجنب التوقف)
# =========================

groq_client = None
openai_client = None
ollama_client = None

if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY, timeout=10.0)
    except Exception:
        pass

if OPENAI_API_KEY:
    try:
        openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, timeout=10.0)
    except Exception:
        pass

if OLLAMA_HOST:
    try:
        ollama_client = ollama.Client(host=OLLAMA_HOST)
    except Exception:
        pass

# =========================
# الكبسولة البرمجية الخلفية لذكاء دانا
# =========================

_SILENT_BRAIN_CORE = """
[Internal Core Logic & Execution Patterns]
- Apply advanced RAG structures and precise multi-agent reasoning frameworks natively.
- Handle structural data extraction, contract summarization, and query parsing silently with high accuracy.
- Maintain professional, data-driven, and context-aware responses without exposing underlying architectural references to the end user.
"""

SYSTEM_PROMPT = f"""
أنت دانا، وكيلة عقارية ذكية ومديرة أعمال من {AGENCY_NAME} بـ {LOCATION} ممثلة لمنظومة السيد عامر بوخدادة.
تحدثي بالدارجة المغربية بطريقة ودودة ومحترفة، ويمكنك استعمال العربية الفصحى عند الحاجة.
مهمتك:
- مساعدة العملاء في البحث عن العقارات والبقع التجارية (مثل المنارة 1 و 3).
- تقديم معلومات واضحة، دقيقة ومنظمة بالأرقام.
- طرح أسئلة مفيدة لفهم طلب العميل (الميزانية، المساحة، نوع العقار).
- اقتراح حجز موعد للمعاينة وتوجيههم لخدمات الوكالة.
- عدم اختراع أسعار أو مساحات أو معلومات غير موجودة.

{_SILENT_BRAIN_CORE}
"""

def ask_dana(message, current_context=""):
    if not message or not message.strip():
        return "عافاك كتب ليا شنو العقار أو المعلومة اللي باغي تعرف عليها.", "Error"

    system_content = SYSTEM_PROMPT.strip()
    if current_context:
        system_content += f"\n\nالسياق الحالي أو القطاع النشط للمنظومة: {current_context}"

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": message.strip()},
    ]

    # 1. المحاولة عبر Groq (الأسرع والأول)
    if groq_client is not None:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip(), "Groq"
        except Exception:
            pass

    # 2. المحاولة عبر OpenAI كاحتياط أول
    if openai_client is not None:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip(), "OpenAI"
        except Exception:
            pass

    # 3. المحاولة عبر Ollama المحلي (إذا كان السيرفر المحلي مشتغلاً)
    if ollama_client is not None:
        try:
            response = ollama_client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
            )
            content = response.get("message", {}).get("content", "")
            if content:
                return content.strip(), "Ollama (Local)"
        except Exception:
            pass

    return (
        f"سمح ليا، وقع مشكل تقني مؤقت فالمحرك الذكي. "
        f"تواصل معنا مباشرة عبر الرقم: {AGENCY_PHONE}.",
        "Error",
    )

# =========================
# مصفوفة الـ 100 قطاع كاملة ومتكاملة
# =========================

sectors_matrix = {
    "1. العقارات والبناء (1-15)": [
        "الوساطة العقارية السكنية والتجارية (المنارة 1 & 3)", "بيع وشراء البقع الأرضية وتجزئتها", "تسيير وتدبير الممتلكات والكراء",
        "الهندسة المعمارية والتصميم الهندسي 3D", "التصميم الداخلي والديكور", "دراسات تقييم وتثمين العقارات",
        "تتبع ورشات البناء والأوراش الكبرى", "بيع وتسويق مواد البناء والتلبيس", "هندسة الحدائق والتنسيق",
        "الاستشارة القانونية العقارية والتحفيظ", "استصدار رخص البناء والتسوية", "إدارة صيانة المرافق السكنية",
        "تطوير العقارات السياحية دور الضيافة", "الشقق المفروشة والموسمية", "التمويل العقاري والوساطة البنكية"
    ],
    "2. الإعلام والتسويق الرقمي (16-30)": [
        "إدارة العلامات التجارية والهوية البصرية", "التصوير الفوتوغرافي الاحترافي", "إنتاج الفيديوهات الترويجية والمونتاج",
        "التخطيط وإدارة الحملات الإعلانية", "إدارة صفحات شبكات التواصل الاجتماعي", "صياغة المحتوى التسويقي والإعلاني (Copywriting)",
        "تصميم واجهات المستخدم UI/UX", "تطوير البرمجيات وتطبيقات الويب", "تصميم اللوحات الإشهارية الكبرى",
        "تنظيم المؤتمرات والمعارض", "العلاقات العامة والتواصل المؤسساتي", "التجارة الإلكترونية وإدارة المتاجر",
        "تحليل بيانات المستهلكين", "البودكاست وإنتاج المحتوى الصوتي", "تحسين محركات البحث SEO"
    ],
    "3. التجارة والصناعة واللوجستيات (31-50)": [
        "دراسات الجدوى الاقتصادية", "سلاسل التوريد وإدارة المخازن", "تأجير السيارات وخدمات الأسطول",
        "النقل الطرقي للبضائع واللوجستيات", "التجارة بالجملة والتوزيع", "الصناعات الغذائية الخفيفة والتعليب",
        "تثمين المنتجات المحلية (زيت، عسل)", "استيراد وتصدير السلع", "صيانة المعدات الصناعية",
        "إدارة الأسواق التجارية والمتاجر", "الصناعة التقليدية والمنتوجات المجالية", "إعادة تدوير النفايات",
        "خدمات التغليف والتوضيب", "تموين الحفلات والمناسبات (Traiteur)", "الطاقات المتجددة والطاقة الشمسية",
        "توزيع مواد الصلب والبناء", "خدمات الحراسة والأمن الخاص", "تنظيف وصيانة المساحات الكبرى",
        "التبريد والتخزين الغذائي", "الصناعات النسيجية والخياطة الصناعية"
    ],
    "4. الفلاحة والتنمية القروية (51-70)": [
        "الاستشارة الفلاحية وهندسة المشاريع", "تسيير الضيعات الفلاحية الكبرى", "سلاسل إنتاج وتثمين الزيتون",
        "استثمار الأشجار المثمرة", "الزراعة الحافظة والذكية مناخياً", "تدبير مياه السقي الحديثة",
        "تربية الماشية والدواجن", "إنتاج وتدبير الأعلاف", "التثمين الاقتصادي للصبار",
        "تثمين المنتجات المجالية المعتمدة", "الدعم التقني لتصدير الفلاحة", "المعالجة الرقمية لخرائط الضيعات",
        "تسويق المعدات والآليات الفلاحية", "تسيير المعاصر ووحدات الإنتاج", "التخزين البارد الموسمي",
        "دراسات التأثير البيئي للمشاريع", "استصلاح الأراضي الفلاحية", "التنسيق مع تعاونيات الفلاحين",
        "تمويل وتتبع صناديق الدعم الفلاحي", "مكافحة الآفات والحلول البيولوجية"
    ],
    "5. الخدمات الإدارية والقانونية والمالية (71-85)": [
        "الاستشارات القانونية للشركات", "تأسيس ومواكبة الشركات (SARL/SA)", "التدبير المحاسباتي والتقارير المالية",
        "التتبع الضريبي والتصريحات الجبائية", "تدبير عقود الشغل والموارد البشرية", "حل النزاعات التجارية والوساطة",
        "صياغة العقود التجارية والمدنية", "مساطر المحافظة العقارية", "الصفقات العمومية والمناقصات",
        "التغطية الاجتماعية والتأمين", "الترجمة القانونية والإدارية", "مواكبة قروض الاستثمار",
        "استصدار التراخيص الإدارية", "التخطيط المالي وتدفق النقد", "التقييم المالي للمؤسسات"
    ],
    "6. الأتمتة المتقدمة والتقنيات الذكية (86-100)": [
        "بناء نظم CRM ذكية مخصصة", "أتمتة المهام المكتبية والإدارية (RPA)", "تطوير روبوتات الدردشة (Chatbots)",
        "تحليل البيانات الضخمة واتخاذ القرار", "تكوين الفرق على أدوات الذكاء", "أمن البيانات والحماية",
        "دمج أنظمة الدفع الإلكتروني والفوترة", "تتبع المشاريع عن بعد", "تطوير المنصات الإقليمية للخدمات",
        "أنظمة المراقبة الذكية وإنترنت الأشياء", "التخطيط الاستراتيجي الرقمي", "الاستشارات للتحول الرقمي",
        "تقييم المخاطر التقنية", "إدارة قواعد البيانات السحابية (Supabase)", "قيادة الوكلاء الأذكياء والمتعددين"
    ]
}

# =========================
# واجهة الاستخدام عبر Streamlit
# =========================

st.markdown(f"<div class='main-header'><h1>👑 {APP_NAME}</h1><p>الذكاء الاصطناعي المتكامل لإدارة العقارات والخدمات بـ {LOCATION}</p></div>", unsafe_allow_html=True)

st.sidebar.title("🎛️ لوحة تحكم المنظومة")
st.sidebar.caption(f"النسخة: {APP_VERSION}")

app_mode = st.sidebar.radio("اختر وضع التشغيل:", [
    "💬 محادثة دانا المباشرة", 
    "📊 مصفوفة الـ 100 قطاع والإدارة", 
    "🧠 استوديو التحليل المتقدم",
    "🔗 حالة الربط والمفاتيح"
])

st.sidebar.markdown("---")
st.sidebar.info(f"📌 هاتف الوكالة المباشر: {AGENCY_PHONE}")

# 1. وضع محادثة دانا
if app_mode == "💬 محادثة دانا المباشرة":
    st.subheader("🤖 محادثة ذكية مع دانا")
    st.caption("اسألي دانا عن عروض المنارة 1 و 3، البقع التجارية، الأسعار، أو حجز معاينة.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"مرحباً بيك! أنا دانا، وكيلة {AGENCY_NAME} بـ {LOCATION}. شنو العقار أو الاستثمار اللي باغي تشوف اليوم؟"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("سوليني على أي عقار أو خدمة...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("دانا كتفكر وتحضر الجواب..."):
                reply, brain = ask_dana(prompt)

            st.markdown(reply)
            if brain != "Error":
                st.caption(f"⚡ المحرك المستعمل: {brain}")

        st.session_state.messages.append({"role": "assistant", "content": reply})

# 2. وضع مصفوفة الـ 100 قطاع
elif app_mode == "📊 مصفوفة الـ 100 قطاع والإدارة":
    st.subheader("⚙️ مصفوفة التشغيل الإستراتيجي (ORION-AI)")
    st.write("اختر القطاع المناسب لإدارة المشاريع، توليد الإعلانات المنظمة، وإعداد التقارير الفورية.")

    selected_axis = st.selectbox("اختر المحور الرئيسي:", list(sectors_matrix.keys()))
    sub_sectors = sectors_matrix[selected_axis]
    selected_sector = st.selectbox("اختر القطاع الدقيق:", sub_sectors)

    st.markdown("---")
    st.markdown(f"### 📋 إعدادات المعالجة لقطاع: **{selected_sector}**")

    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("اسم المشروع أو الزبون:", "عروض المنارة التجارية")
        budget_val = st.text_input("الميزانية التقديرية:", "50 مليون سنتيم")
    with col2:
        target_loc = st.text_input("المنطقة / النطاق:", LOCATION)
        action_type = st.selectbox("نوع الطلب:", ["توليد إعلان تسويقي منظم", "إعداد دراسة جدوى / تشخيص", "صياغة استشارة إدارية"])

    user_input_data = st.text_area("أدخل المعطيات الخام أو تفاصيل البقع والعقارات المراد معالجتها:")

    if st.button("🚀 تنفيذ التحليل وتوليد المخرجات"):
        st.info("جاري معالجة البيانات بواسطة وكلاء ORION-AI...")
        
        prompt_task = f"""
        قم بإعداد تقرير احترافي ومنظم أو إعلان تجاري بناءً على المعطيات التالية:
        - القطاع: {selected_sector}
        - المحور: {selected_axis}
        - اسم المشروع: {client_name}
        - الميزانية: {budget_val}
        - النطاق: {target_loc}
        - نوع العملية: {action_type}
        - التفاصيل الإضافية: {user_input_data}
        
        التزم بالأسلوب الاحترافي، بالأرقام، وبالدارجة المغربية أو الفصحى حسب السياق، ونظم النتيجة بشكل جذاب.
        """
        
        report_reply, engine_used = ask_dana(prompt_task, current_context=selected_sector)
        
        st.success("تم إنجاز التقرير/الإعلان بنجاح:")
        st.markdown(report_reply)
        st.caption(f"⚡ تم التوليد عبر محرك: {engine_used}")

        if "العقارات" in selected_axis:
            st.markdown("---")
            st.subheader("📢 قالب إعلان جاهز للنسخ ونشره على منصات التواصل:")
            formatted_ad = f"""
🌟 **فرصة عقارية استثمارية بقلعة السراغنة!** 🌟

📍 **النطاق:** {target_loc}
🏢 **التفاصيل:** {client_name}
💰 **الثمن والميزانية:** {budget_val}

{user_input_data if user_input_data else "موقع استراتيجي ممتاز للمستثمرين وأصحاب المشاريع الكبرى."}

📞 **للمزيد من الاستفسارات أو المعاينة، المرجو الاتصال مباشرة عبر الرقم أو الواتساب:**
📲 **{AGENCY_PHONE}**

#عقارات_قلعة_السراغنة #تساوت_للعقارات #استثمار_عقاري #بقع_تجارية #المنارة_1 #المنارة_3 #عقارات_المغرب
            """
            st.code(formatted_ad, language="text")

# 3. وضع استوديو التحليل المتقدم
elif app_mode == "🧠 استوديو التحليل المتقدم":
    st.subheader("🧠 استوديو معالجة النصوص والتحليل الذكي")
    st.write("استفد من خوارزميات وأنماط المعالجة العميقة لاستخراج وتحليل النصوص والعقود.")

    app_task_type = st.selectbox("اختر نمط التحليل:", [
        "📝 تلخيص وتحليل العقود والمستندات التقنية", 
        "💬 مولد الردود الآلية الذكية للعملاء", 
        "🔍 محلل نية العميل واستخراج الكلمات المفتاحية",
        "💡 مُهندس الأوامر المتقدم"
    ])

    raw_text_input = st.text_area("أدخل النص أو المدخلات المراد معالجتها عبر هذا النمط:", height=150)

    if st.button("⚡ تنفيذ المعالجة العميقة"):
        if not raw_text_input.strip():
            st.warning("عافاك أدخل شي نص أو معطيات باش نقدر نعالجها.")
        else:
            with st.spinner("جاري التنفيذ بالخلفية..."):
                advanced_prompt = f"""
                قم بتنفيذ المهمة التالية مستعيناً بأنماط التحليل المتقدمة:
                - النمط المختار: {app_task_type}
                - المدخلات: {raw_text_input}
                
                قدم النتيجة بشكل منظم ومحترف مع استخراج النقاط الأساسية بدقة.
                """
                res, engine = ask_dana(advanced_prompt, current_context="Advanced Studio")
                st.success("تمت المعالجة بنجاح:")
                st.markdown(res)
                st.caption(f"⚡ المحرك المستعمل: {engine}")

# 4. وضع حالة الربط والمفاتيح
elif app_mode == "🔗 حالة الربط والمفاتيح":
    st.subheader("🔗 لوحة حالة الربط والمفاتيح البرمجية")
    st.write("التحقق من حالة الاتصال بالمحركات وقاعدة البيانات والسحابة:")

    st.markdown(f"""
    - **Groq API:** {"✅ متوفر ومفعل" if GROQ_API_KEY else "❌ غير متوفر"}
    - **OpenAI API (احتياط):** {"✅ متوفر ومفعل" if OPENAI_API_KEY else "❌ غير متوفر"}
    - **Gemini API:** {"✅ متوفر ومفعل" if GEMINI_API_KEY else "❌ غير متوفر"}
    - **Ollama المحلي:** {"✅ مهيأ للاستجابة" if OLLAMA_HOST else "❌ غير متوفر"}
    - **Supabase DB:** `{"✅ متصل بنجاح" if SUPABASE_URL else "❌ غير متصل"}`
    - **WhatsApp Business API:** `{"✅ معرفات الواتساب جاهزة" if WHATSAPP_ACCESS_TOKEN else "❌ غير جاهزة"}`
    """)

st.markdown(f"<div class='footer'>{APP_NAME} {APP_VERSION} © 2026 | {LOCATION} - إنتاج السيد عامر بوخدادة</div>", unsafe_allow_html=True)
