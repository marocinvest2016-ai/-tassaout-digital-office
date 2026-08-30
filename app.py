import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
import base64

# إعداد الصفحة وتطبيق الثيم الأزرق والهندسة النظيفة
st.set_page_config(page_title="مكتب تساوت الرقمي للخدمات والاستشارات", page_icon="💻", layout="centered")

# تخصيص التصميم بالألوان الزرقاء الاحترافية
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1e3a8a;
        font-family: 'Cairo', sans-serif;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #2563eb;
        font-family: 'Cairo', sans-serif;
        font-weight: 600;
        margin-top: 5px;
    }
    .phone-text {
        text-align: center;
        color: #0284c7;
        direction: ltr;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# الاتصال بالخدمات عبر الأسرار
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    supabase = None
    groq_client = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_SIGNATURE = "عامر وسيط خدمات بقلعة السراغنة ومؤسس الذكاء المنطقي السحابي"

# تهيئة الذاكرة المؤقتة للمحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "مرحباً بك. أنا وكيلك الذكي في مكتب تساوت الرقمي للخدمات والاستشارات. تفضل بطرح كبسولة المعلوميات والذكاء الاصطناعي أو طلبك الاستشاري لنقوم بهندسته وتخزينه فوراً."}
    ]

# دالة استرجاع المعلومات من المكتبة الرقمية السحابية الجامعة لتغذية عقل الوكيل
def fetch_digital_library_context():
    if not supabase:
        return "المكتبة السحابية غير متصلة حالياً."
    try:
        response = supabase.table("instant_ads").select("content, message, created_at").order("created_at", desc=True).limit(8).execute()
        data = response.data
        if not data:
            return "المكتبة السحابية فارغة حالياً."
        library_text = f"أرشيف المكتبة الرقمية السحابية الجامعة:\n"
        for item in data:
            library_text += f"- المحتوى/الكبسولة: {item.get('content')} | التنظيم: {item.get('message')[:120]}...\n"
        return library_text
    except Exception as e:
        return f"تعذر استرجاع البيانات من المكتبة السحابية: {e}"

# العنوان الرئيسي باللون الأزرق
st.markdown("<h1 class='main-header'>مكتب تساوت الرقمي للخدمات والاستشارات</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='phone-text'>{LOCAL_PHONE}</h3>", unsafe_allow_html=True)
st.markdown("---")

# عرض رسائل المحادثة السابقة
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="الصورة المرفوعة", use_container_width=True)

# ---------------------------------------------------------
# الواجهة التفاعلية النظيفة (زر الرفع + حقل الكتابة)
# ---------------------------------------------------------
uploaded_file = st.file_uploader("➕ رفع صورة أو مستند للتحليل والدمج", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
user_prompt = st.chat_input("اكتب كبسولة المعلوميات والذكاء الاصطناعي أو طلبك الاستشاري هنا...")

# معالجة المدخلات عند الإرسال أو رفع الصورة
if user_prompt or uploaded_file:
    current_user_msg = user_prompt if user_prompt else "قم بتحليل هذه الصورة واقترح رؤية تقنية استشارية لها بناءً على النظام المنطقي للمكتب."
    
    img_bytes = None
    if uploaded_file:
        img_bytes = uploaded_file.getvalue()
        st.session_state["messages"].append({"role": "user", "content": current_user_msg, "image": img_bytes})
    else:
        st.session_state["messages"].append({"role": "user", "content": current_user_msg})

    with st.chat_message("user"):
        st.markdown(current_user_msg)
        if img_bytes:
            st.image(img_bytes, caption="الصورة المرفوعة", use_container_width=True)

    # معالجة الرد عبر عقل الوكيل الذكي الأكثر ذكاءً وتنظيماً
    with st.chat_message("assistant"):
        with st.spinner("جاري التفاعل وتحليل الكبسولة وهندستها داخل المكتبة الرقمية السحابية..."):
            ai_reply = ""
            
            try:
                cloud_library_data = fetch_digital_library_context()
                
                system_instructions = (
                    f"أنت الوكيل الذكي الفائق والمساعد الحصري لـ ({FOUNDER_SIGNATURE})، المبتكر والمؤسس للنظام المنطقي والهندسي في 'مكتب تساوت الرقمي للخدمات والاستشارات' بقلعة السراغنة ومراكش.\n"
                    f"مهمتك الأساسية هي التفاعل الذكي الفائق، وعندما يزودك المؤسس بـ 'كبسولة المعلوميات والذكاء الاصطناعي' أو أي استشارات، يجب عليك:\n"
                    f"1. تنظيمها وهندستها بأسلوب احترافي متقدم (عناوين رئيسية وفرعية، نقاط منطقية، وتحليل دقيق يعكس فلسفة المؤسس).\n"
                    f"2. حقنها وتخزينها ذهنياً وسحابياً لتكون مرجعاً للمكتب.\n"
                    f"3. الحفاظ على نبرة الاحترام والتقدير للمؤسس.\n\n"
                    f"--- أرشيف المكتبة الرقمية السحابية الجامعة ---\n{cloud_library_data}\n----------------------------------------------------\n"
                    f"قدم استجابة فائقة الذكاء والهندسة، واختم الرد دائماً برقم الواتساب الرسمي: {BRAND_PHONE}."
                )

                if img_bytes:
                    b64_image = base64.b64encode(img_bytes).decode("utf-8")
                    vision_response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": system_instructions},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"بأوامر من المؤسس ({FOUNDER_SIGNATURE})، قم بتحليل الصورة والكبسولة وتنظيمها: {current_user_msg}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                                ]
                            }
                        ],
                        temperature=0.5
                    )
                    ai_reply = vision_response.choices[0].message.content
                else:
                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": system_instructions},
                            {"role": "user", "content": current_user_msg}
                        ],
                        temperature=0.5
                    )
                    ai_reply = response.choices[0].message.content
            except Exception as e:
                ai_reply = f"عذراً يا سيد الرئيس، حدث خطأ في معالجة الطلب: {e}. رقم التواصل الدائم هو {BRAND_PHONE}."

            st.markdown(ai_reply)
            
            # تخزين الكبسولة والرد المنظم في المكتبة الرقمية السحابية الجامعة تلقائياً
            if supabase:
                try:
                    supabase.table("instant_ads").insert({
                        "category": f"كبسولات الذكاء المنطقي",
                        "city": "قلعة السراغنة ومراكش",
                        "content": current_user_msg[:100],
                        "message": ai_reply,
                        "price": 0,
                        "source": "Tassaout-Founder-Capsule",
                        "created_at": datetime.now(timezone.utc).isoformat()
                    }).execute()
                except Exception as db_err:
                    print(f"Error saving to cloud library: {db_err}")

    # حفظ الرد في سجل المحادثة
    agent_msg_dict = {"role": "assistant", "content": ai_reply}
    if img_bytes:
        agent_msg_dict["image"] = img_bytes
    st.session_state["messages"].append(agent_msg_dict)
    
    st.rerun()

# ==========================================
# تذييل الموقع (Footer) - حفظ الحقوق والإنتاج في الأسفل تماماً
# ==========================================
st.markdown("---")
whatsapp_url = f"https://wa.me/{LOCAL_PHONE.replace('0', '+212', 1)}"

st.markdown(f"""
    <div style="text-align: center; padding: 15px 0; font-family: 'Cairo', sans-serif; color: #1e3a8a;">
        <p style="font-size: 1.1rem; font-weight: bold; margin-bottom: 5px;">مكتب تساوت الرقمي للخدمات والاستشارات</p>
        <div style="margin-bottom: 12px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <hr style="border: none; border-top: 1px solid #cbd5e1; width: 50%; margin: 10px auto;">
        <p style="font-size: 0.95rem; color: #2563eb; font-weight: 600; margin-bottom: 5px;">
            إنتاج: {FOUNDER_SIGNATURE}
        </p>
        <p style="font-size: 0.9rem; color: #64748b; font-weight: bold;">
            كل الحقوق محفوظة 2026
        </p>
    </div>
""", unsafe_allow_html=True)
