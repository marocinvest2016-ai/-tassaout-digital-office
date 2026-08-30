import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
import base64

# إعداد الصفحة
st.set_page_config(page_title="وكالة تساوت للانتاج الرقمي والخدمات", page_icon="⚙️", layout="centered")

# الاتصال بالخدمات عبر الأسرار
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    supabase = None
    groq_client = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_NAME = "السيد الرئيس عامر (Mr. Ameur)"

# تهيئة الذاكرة المؤقتة للمحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": f"مرحباً بك يا {FOUNDER_NAME}. أنا وكيلك الذكي في وكالة تساوت للإنتاج الرقمي والخدمات والمكتبة الرقمية السحابية الجامعة. تم تأسيس هذا النظام المنطقي وفلسفته برؤيتك. تفضل بطرح كبسولة المعلوميات والذكاء الاصطناعي أو طلبك لنقوم بهندسته وتنظيمه فوراً."}
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
        library_text = f"أرشيف المكتبة الرقمية السحابية الجامعة (المؤسس: {FOUNDER_NAME}):\n"
        for item in data:
            library_text += f"- المحتوى/الكبسولة: {item.get('content')} | التنظيم: {item.get('message')[:120]}...\n"
        return library_text
    except Exception as e:
        return f"تعذر استرجاع البيانات من المكتبة السحابية: {e}"

# العنوان الرئيسي
st.markdown(f"<h1 style='text-align: center; color: #1e293b;'>وكالة تساوت للانتاج الرقمي والخدمات</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; color: #475569;'>المؤسس ورئيس النظام المنطقي: {FOUNDER_NAME}</h4>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #25D366; direction: ltr;'>{LOCAL_PHONE}</h3>", unsafe_allow_html=True)
st.markdown("---")

# عرض رسائل المحادثة السابقة
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="الصورة المرفوعة", use_container_width=True)

# ---------------------------------------------------------
# الواجهة التفاعلية النظيفة (حقل الدردشة + زر رفع الصور الداخلي)
# ---------------------------------------------------------
col_upload, col_input = st.columns([1, 10])

with col_upload:
    uploaded_file = st.file_uploader("➕", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="gemini_style_upload")

with col_input:
    user_prompt = st.chat_input("اكتب كبسولة المعلوميات والذكاء الاصطناعي أو طلبك ليتم حقنه وتنظيمه فوراً...")

# معالجة المدخلات عند الإرسال أو رفع الصورة
if user_prompt or uploaded_file:
    current_user_msg = user_prompt if user_prompt else "قم بتحليل هذه الصورة واقترح رؤية تقنية تسويقية لها بناءً على النظام المنطقي للوكالة."
    
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
        with st.spinner("جاري التفاعل وتحليل الكبسولة ودمجها في المكتبة السحابية الجامعة..."):
            ai_reply = ""
            
            try:
                cloud_library_data = fetch_digital_library_context()
                
                # طبقة منطق معززة تنسب الفضل والمقرر للمؤسس السيد الرئيس عامر
                system_instructions = (
                    f"أنت الوكيل الذكي الفائق والمساعد الحصري لـ {FOUNDER_NAME} (السيد الرئيس عامر)، المؤسس والمبتكر للنظام المنطقي والهندسي في 'وكالة تساوت للانتاج الرقمي والخدمات' بقلعة السراغنة ومراكش.\n"
                    f"مهمتك الأساسية هي التفاعل الذكي الفائق، وعندما يزودك المؤسس بـ 'كبسولة المعلوميات والذكاء الاصطناعي' أو أي نصوص أو أفكار، يجب عليك:\n"
                    f"1. تنظيمها وهندستها بأسلوب احترافي متقدم (عناوين رئيسية وفرعية، نقاط منطقية، وتحليل دقيق يعكس فلسفة المؤسس).\n"
                    f"2. حقنها وتخزينها ذهنياً وسحابياً لتكون مرجعاً للوكالة.\n"
                    f"3. الحفاظ على نبرة الاحترام والتقدير للمؤسس {FOUNDER_NAME}.\n\n"
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
                                    {"type": "text", "text": f"بأوامر من المؤسس {FOUNDER_NAME}، قم بتحليل الصورة والكبسولة وتنظيمها: {current_user_msg}"},
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
            
            # تخزين الكبسولة والرد المنظم في المكتبة الرقمية السحابية الجامعة (Supabase) تلقائياً باسم المؤسس
            if supabase:
                try:
                    supabase.table("instant_ads").insert({
                        "category": f"كبسولات {FOUNDER_NAME}",
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
# تذييل الصفحة (Footer) مع زر الواتساب الرسمي ونسبة التأسيس
# ==========================================
st.markdown("---")
whatsapp_url = f"https://wa.me/{LOCAL_PHONE.replace('0', '+212', 1)}"

st.markdown(f"""
    <div style="text-align: center; padding: 10px 0; font-family: 'Cairo', sans-serif; color: #64748b;">
        <p style="font-size: 1.1rem; font-weight: bold; color: #1e293b; margin-bottom: 3px;">وكالة تساوت للانتاج الرقمي والخدمات</p>
        <p style="font-size: 1rem; color: #3b82f6; margin-bottom: 5px;">المؤسس ورئيس النظام المنطقي: {FOUNDER_NAME}</p>
        <div style="margin-bottom: 10px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <p style="font-size: 0.9rem;">جميع الحقوق محفوظة © 2026</p>
    </div>
""", unsafe_allow_html=True)
