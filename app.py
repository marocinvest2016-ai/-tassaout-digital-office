import urllib.parse
import streamlit as st
from agent import TassaoutAgenticCore

# إعدادات الصفحة
st.set_page_config(
    page_title="سراغنة العقارية | المنصة الرقمية المتكاملة",
    page_icon="🏢",
    layout="wide",
)

# إنشاء كائن الوكيل الذكي
agent = TassaoutAgenticCore()

# شريط التنقل الجانبي للخدمات الرئيسية
st.sidebar.title("📌 القائمة الرئيسية")
selected_tab = st.sidebar.radio(
    "اختر القسم المطلوب:",
    [
        "🤖 الوكيل الذكي (الدردشة)",
        "📋 عروض العقارات، الفلاحية والأعمال",
        "📸 شاشة تحميل وتوثيق الصور",
        "💬 التواصل المباشر (واتساب)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    f"📍 {agent.commercial_name}\n\nإدارة العمليات بقلعة السراغنة ومراكش."
)

# --- القسم الأول: الوكيل الذكي (الدردشة) ---
if selected_tab == "🤖 الوكيل الذكي (الدردشة)":
  st.title(f"🏢 {agent.commercial_name}")
  st.subheader("🤖 المساعد الذكي للعمليات والعقارات")
  st.markdown("---")

  if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            f"أهلاً بك في {agent.commercial_name}. أنا جاهز لإدارة الاستفسارات"
            " العقارية واللوجستية. كيف يمكنني خدمتك اليوم؟"
        ),
    }]

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input(
      "اطرح سؤالك أو استفسارك هنا (عقارات، أراضي فلاحية، أعمال)..."
  ):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      if "فلاح" in prompt or "أرض" in prompt or "بقعة" in prompt:
        response = (
            "نوفر عروضاً للأراضي الفلاحية والبقع الاستثمارية بقلعة السراغنة"
            " ومحيطها بمعايير دقيقة."
        )
      elif "شحن" in prompt or "لوجستيك" in prompt:
        response = (
            "نتابع مسارات الشحن واللوجستيك وسلاسل الإمداد بدقة تامة."
        )
      else:
        response = (
            f"تم استلام طلبك بنجاح في {agent.commercial_name}. نعمل على"
            " توفير أفضل الخدمات العقارية والتجارية لك."
        )

      st.markdown(response)
      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )

# --- القسم الثاني: عروض العقارات، الفلاحية والأعمال ---
elif selected_tab == "📋 عروض العقارات، الفلاحية والأعمال":
  st.title("🏡 عروض العقارات، الأراضي الفلاحية والأعمال")
  st.markdown("استعرض أحدث السجلات والفرص المتاحة ضمن منظومة تساوت:")
  st.markdown("---")

  col1, col2 = st.columns(2)

  with col1:
    st.header("🌾 القطاع العقاري والفلاحي")
    for item in agent.real_estate_listings:
      with st.expander(f"📍 {item['title']} | {item['category']}"):
        st.write(item["details"])

  with col2:
    st.header("🚚 الأعمال واللوجستيك")
    for log in agent.logistics_routes:
      with st.expander(f"🚛 {log['route']} - {log['schedule']}"):
        st.write(log["details"])

# --- القسم الثالث: شاشة تحميل وتوثيق الصور ---
elif selected_tab == "📸 شاشة تحميل وتوثيق الصور":
  st.title("📸 نظام رفع وتوثيق الصور الميدانية")
  st.markdown(
      "قم برفع الصور الخاصة بالعقارات، الأراضي، أو التوثيق الميداني لتخزينها"
      " ومعالجتها:"
  )
  st.markdown("---")

  uploaded_file = st.file_uploader(
      "اختر صورة للرفع (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"]
  )

  if uploaded_file is not None:
    st.success("تم رفع الصورة بنجاح وتوجيهها لنظام المعالجة الميدانية!")
    # تم التحديث هنا لاستخدام المعامل الجديد use_container_width
    st.image(
        uploaded_file,
        caption="معاينة الصورة المرفوعة",
        use_container_width=True,
    )
    st.write(
        "📌 **حالة التوثيق:** جاهزة للأرشفة والربط بملفات العقار أو التنسيق"
        " الميداني."
    )

# --- القسم الرابع: رابط التواصل مع الواتساب ---
elif selected_tab == "💬 التواصل المباشر (واتساب)":
  st.title("💬 خدمة العملاء والتواصل المباشر")
  st.markdown(
      "للتواصل الفوري مع إدارة المكتب أو طلب استشارة عقارية وتجارية عاجلة:"
  )
  st.markdown("---")

  whatsapp_number = "212691897126"
  whatsapp_text = (
      "مرحباً، أهلاً بك في سراغنة العقارية. أود الاستفسار عن العروض المتاحة."
  )
  whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(whatsapp_text)}"

  st.markdown(
      f"""
        <div style="text-align: center; padding: 30px; background-color: #f0f2f6; border-radius: 10px;">
            <h3>جاهز للتواصل الفوري؟</h3>
            <p>انقر على الزر أدناه لمراسلتنا مباشرة عبر تطبيق الواتساب:</p>
            <a href="{whatsapp_url}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 12px 24px; font-size: 18px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    💬 التواصل عبر الواتساب الآن
                </button>
            </a>
        </div>
        """,
      unsafe_allow_html=True,
  )
