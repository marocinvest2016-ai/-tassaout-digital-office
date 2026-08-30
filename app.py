import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
from urllib.parse import quote
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

# تهيئة الذاكرة المؤقتة للمحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "مرحباً بك يا Mr. Ameur. أنا وكيلك الذكي في وكالة تساوت للإنتاج الرقمي والخدمات. كيف يمكنني مساعدتك اليوم في الإعلانات، العقارات، توليد الأفكار، أو تحليل الصور؟"}
    ]

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1e293b;'>وكالة تساوت للانتاج الرقمي والخدمات</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #25D366; direction: ltr;'>{LOCAL_PHONE}</h3>", unsafe_allow_html=True)
st.markdown("---")

# عرض رسائل المحادثة السابقة
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="الصورة المعالجة / المرفوعة", use_container_width=True)

# نافذة الإدخال التفاعلية الموحدة (تشبه Gemini مع علامة + لتحميل الصور)
col_input, col_plus = st.columns([10, 1])

with col_plus:
    # زر علامة + لتحميل الصور بطريقة تفاعلية مدمجة
    uploaded_file = st.file_uploader("➕", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="chat_image_upload")

user_prompt = st.chat_input("اكتب طلبك هنا (توليد إعلان، استشارة عقارية، صياغة برومبت، أو طلب تحليل صورة)...")

if user_prompt or uploaded_file:
    # معالجة المدخلات من المستخدم
    current_user_msg = user_prompt if user_prompt else "قم بتحليل هذه الصورة واقترح رؤية تسويقية لها."
    
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

    # معالجة الرد عبر عقل الوكيل الذكي (Groq)
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير والتنفيذ بواسطة وكيل تساوت الذكي..."):
            ai_reply = ""
            
            try:
                if img_bytes:
                    b64_image = base64.b64encode(img_bytes).decode("utf-8")
                    vision_response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"أنت وكيل ذكي لمحترف الإنتاج الرقمي Mr. Ameur. قم بتحليل الطلب والصورة بدقة واقترح أفضل صيغة تسويقية ورقمية للخدمة مع تضمين رقم الواتساب {BRAND_PHONE}. طلب المستخدم: {current_user_msg}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                            ]
                        }],
                        temperature=0.6
                    )
                    ai_reply = vision_response.choices[0].message.content
                else:
                    system_instructions = (
                        f"أنت المساعد الذكي الحصري لـ Mr. Ameur في 'وكالة تساوت للانتاج الرقمي والخدمات' بقلعة السراغنة ومراكش. "
                        f"تتعامل مع مجالات العقارات (شقق، بقع، أراضي، فيلات)، الخدمات الرقمية، النقل واللوجستيك (Marrakech World Auto Services و Sraghna Media Trans). "
                        f"قمصاغة إعلانات احترافية أو إجابات دقيقة ومباشرة، مع ختم الردود دائماً برقم الواتساب الرسمي: {BRAND_PHONE}."
                    )
                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": system_instructions},
                            {"role": "user", "content": current_user_msg}
                        ],
                        temperature=0.6
                    )
                    ai_reply = response.choices[0].message.content
            except Exception as e:
                ai_reply = f"عذراً، حدث خطأ في معالجة الطلب: {e}. رقم التواصل الدائم هو {BRAND_PHONE}."

            st.markdown(ai_reply)
            
            # حفظ الإعلان أو النتيجة في الأرشيف السحابي تلقائياً إذا كان نص إعلان
            if supabase and ("إعلان" in current_user_msg or "عروض" in ai_reply):
                try:
                    supabase.table("instant_ads").insert({
                        "category": "الوكيل الذكي العام",
                        "city": "قلعة السراغنة ومراكش",
                        "content": current_user_msg[:50],
                        "message": ai_reply,
                        "price": 0,
                        "source": "Tassaout-AI-Agent",
                        "created_at": datetime.now(timezone.utc).isoformat()
                    }).execute()
                except:
                    pass

    # حفظ الرد في سجل المحادثة
    agent_msg_dict = {"role": "assistant", "content": ai_reply}
    if img_bytes:
        agent_msg_dict["image"] = img_bytes
    st.session_state["messages"].append(agent_msg_dict)

# ==========================================
# تذييل الصفحة (Footer)
# ==========================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 10px 0; font-family: 'Cairo', sans-serif; color: #64748b;">
        <p style="font-size: 1.1rem; font-weight: bold; color: #1e293b; margin-bottom: 3px;">وكالة تساوت للانتاج الرقمي والخدمات</p>
        <p style="font-size: 1rem; color: #3b82f6; margin-bottom: 3px;">Mr. Ameur</p>
        <p style="font-size: 0.9rem;">جميع الحقوق محفوظة © 2026</p>
    </div>
""", unsafe_allow_html=True)
