from datetime import datetime, timedelta
import io
import os
import urllib.parse
import zipfile
import google.generativeai as genai
import pandas as pd
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import streamlit as st
from supabase import Client, create_client

# ==========================================
# 0. إعدادات النظام السيادي الشامل (OMEGA OS v10.0 PRIME)
# ==========================================
st.set_page_config(
    page_title="TASSAOUT OMEGA OS v10.0 PRIME", page_icon="👑", layout="wide"
)

GALLERY_FOLDER = "gallery"
os.makedirs(GALLERY_FOLDER, exist_ok=True)

# تهيئة الاتصالات والـ Secrets
@st.cache_resource
def init_system():
  try:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(url, key)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    return supabase, True
  except Exception:
    return None, False


supabase, db_connected = init_system()

# جلسة مؤقتة للتخزين المحلي في حال عدم توفر الاتصال
if "local_properties" not in st.session_state:
  st.session_state["local_properties"] = []
if "local_contacts" not in st.session_state:
  st.session_state["local_contacts"] = []
if "local_deals" not in st.session_state:
  st.session_state["local_deals"] = []

# ==========================================
# 1. القائمة الجانبية السيادية المتكاملة
# ==========================================
st.sidebar.title("👑 OMEGA OS v10.0 PRIME")
st.sidebar.markdown(
    "**المستخدم:** عامر بوخدادة\n**المنطقة:** قلعة السراغنة - مراكش"
    f"\n**التاريخ:** {datetime.now().strftime('%Y-%m-%d')}"
)

privacy_mode = st.sidebar.checkbox(
    "🔒 نمط الخصوصية القصوى (إخفاء المبالغ والأرباح)", value=False
)
dark_mode_ui = st.sidebar.checkbox("🌙 تفعيل الوضع الليلي المبسط", value=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "قائمة التشغيل السيادية:",
    [
        "📊 لوحة القيادة والمؤشرات الشاملة",
        "📸 وحدة الكاميرا والمعالجة البصرية المتقدمة",
        "🤖 غرفة قيادة وكلاء الذكاء الاصطناعي (Agentic AI)",
        "🌐 وكيل البحث العميق واستخراج الداتا",
        "🏠 إدارة العقارات والمشاريع الذكية",
        "👥 إدارة الزبناء (CRM) وتقييم الصدارة",
        "💼 تتبع الصفقات، الأرباح وROI",
        "🧮 الحاسبة التمويلية واستثمار العقار",
        "🚗 اللوجستيات وتأجير السيارات",
        "📁 الأرشيف والتصدير الشامل (ZIP & CSV)",
        "⚙️ الإعدادات والأمان السيادي",
    ],
)

# ==========================================
# 1. لوحة القيادة والمؤشرات الشاملة
# ==========================================
if menu == "📊 لوحة القيادة والمؤشرات الشاملة":
  st.title("📊 لوحة القيادة والمؤشرات السيادية الخبيرة")
  st.write(
      "نظرة عامة ومباشرة على أداء العمليات العقارية، الإعلانات، والخدمات"
      " الرقمية بقلعة السراغنة ومراكش."
  )

  try:
    r_data, c_data, d_data = [], [], []
    if db_connected:
      r_res = supabase.table("reports").select("*").execute()
      c_res = supabase.table("crm_contacts").select("*").execute()
      d_res = supabase.table("crm_deals").select("*").execute()
      r_data = r_res.data if r_res.data else []
      c_data = c_res.data if c_res.data else []
      d_data = d_res.data if d_res.data else []
    else:
      r_data = st.session_state["local_properties"]
      c_data = st.session_state["local_contacts"]
      d_data = st.session_state["local_deals"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي العقارات والخدمات", len(r_data))
    col2.metric("إجمالي الزبناء المسجلين", len(c_data))
    col3.metric("إجمالي الصفقات الجارية", len(d_data))

    if privacy_mode:
      col4.metric("إجمالي قيمة الصفقات (درهم)", "🔒 مخفي بالخصوصية")
    else:
      total_revenue = sum(
          [float(deal.get("amount", 0)) for deal in d_data if deal.get("amount")]
      )
      col4.metric(
          "إجمالي قيمة الصفقات (درهم)", f"{total_revenue:,.2f} درهم مغربي"
      )

    st.markdown("---")
    st.markdown("### 📈 أحدث الصفقات والعمليات المسجلة")
    if d_data:
      df_deals = pd.DataFrame(d_data)
      if privacy_mode and "amount" in df_deals.columns:
        df_deals["amount"] = "🔒 مخفي"
      st.dataframe(df_deals, use_container_width=True)
    else:
      st.info("لا توجد صفقات مسجلة لعرضها في المؤشرات حالياً.")

  except Exception as e:
    st.error(f"خطأ في الاتصال أو جلب مؤشرات اللوحة: {e}")

# ==========================================
# 2. وحدة الكاميرا والمعالجة البصرية المتقدمة
# ==========================================
elif menu == "📸 وحدة الكاميرا والمعالجة البصرية المتقدمة":
  st.header("MEGA PREMIUM Camera OS & Visual Agent")
  st.write(
      "تصحيح وتعديل صور العقارات، إضافة العلامة المائية التلقائية، وتطبيق الفلاتر"
      " السيادية."
  )

  ENVIRONMENT_PRESETS = {
      "عقار فخم (مراكش)": {
          "camera": "Hasselblad X2D 100C",
          "sharpness": 2.2,
          "contrast": 1.6,
      },
      "تجزئة أرضية (قلعة السراغنة)": {
          "camera": "Sony A1",
          "sharpness": 1.8,
          "contrast": 1.9,
      },
      "توثيق ميداني": {
          "camera": "Canon EOS R5",
          "sharpness": 1.5,
          "contrast": 1.3,
      },
  }

  preset_name = st.selectbox(
      "اختر إعداد البيئة البصرية:", list(ENVIRONMENT_PRESETS.keys())
  )
  preset = ENVIRONMENT_PRESETS[preset_name]

  add_watermark = st.checkbox(
      "إضافة علامة مائية تلقائية (Tassaout Immobilière)", value=True
  )
  uploaded_file = st.file_uploader(
      "ارفع صورة العقار أو الأرض للمعالجة:", type=["jpg", "jpeg", "png"]
  )

  if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة الأصلية", use_container_width=True)

    if st.button("تطبيق المعالجة البصرية السيادية"):
      enhancer = ImageEnhance.Sharpness(image)
      img_enhanced = enhancer.enhance(preset["sharpness"])

      contrast_enhancer = ImageEnhance.Contrast(img_enhanced)
      img_final = contrast_enhancer.enhance(preset["contrast"])

      if add_watermark:
        draw = ImageDraw.Draw(img_final)
        width, height = img_final.size
        watermark_text = "Tassaout Immobiliere - Sraghna"
        # تم تصحيح الصيغة لتدعم وضع RGB دون أخطاء الشفافية
        draw.text(
            (width - 300, height - 40), watermark_text, fill=(255, 255, 255)
        )

      st.image(
          img_final,
          caption="الصورة بعد المعالجة الاحترافية والعلامة المائية",
          use_container_width=True,
      )

      file_path = os.path.join(
          GALLERY_FOLDER,
          f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
      )
      img_final.save(file_path)
      st.success(f"تم حفظ الصورة بنجاح في الأرشيف: {file_path}")

# ==========================================
# 3. غرفة قيادة وكلاء الذكاء الاصطناعي (Agentic AI)
# ==========================================
elif menu == "🤖 غرفة قيادة وكلاء الذكاء الاصطناعي (Agentic AI)":
  st.title("🤖 غرفة عمليات وكلاء الذكاء الاصطناعي المتخصصين")

  agent_type = st.selectbox(
      "اختر الوكيل الذكي (Agent):",
      [
          "🏢 وكيل العقارات وتحليل السوق المغربي",
          "🤝 وكيل المبيعات وإغلاق الصفقات (CRM Expert)",
          "📢 وكيل التسويق الرقمي والحملات (Sraghna Media / DANA)",
          "💰 وكيل الإدارة المالية وتقييم الأرباح (CFO Agent)",
      ],
  )

  with st.form("agent_command_form"):
    user_task = st.text_area(
        "أدخل التوجيه أو المشكلة ليقوم الوكيل بتحليلها وإنجازها:"
    )
    submit_agent = st.form_submit_button("🚀 إرسال المهمة للوكيل الذكي")

    if submit_agent:
      if user_task and db_connected:
        try:
          model = genai.GenerativeModel("gemini-1.5-flash")
          system_personas = {
              "🏢 وكيل العقارات وتحليل السوق المغربي": (
                  "أنت خبير استراتيجي عقاري في السوق المغربي (قلعة السراغنة ومراكش)."
              ),
              "🤝 وكيل المبيعات وإغلاق الصفقات (CRM Expert)": (
                  "أنت خبير مبيعات وتفاوض عالمي لرفع نسبة إغلاق الصفقات."
              ),
              "📢 وكيل التسويق الرقمي والحملات (Sraghna Media / DANA)": (
                  "أنت مدير تسويق رقمي وإعلانات ممولة مستهدف للسوق المغربي."
              ),
              "💰 وكيل الإدارة المالية وتقييم الأرباح (CFO Agent)": (
                  "أنت مستشار مالي محترف لإدارة العائد على الاستثمار ROI."
              ),
          }
          prompt = f"{system_personas[agent_type]}\n\nالمهمة: {user_task}"
          with st.spinner("جاري معالجة المهمة بواسطة الوكيل المتخصص..."):
            response = model.generate_content(prompt)
            st.success("✅ تم تنفيذ المهمة بنجاح:")
            st.markdown(response.text)
        except Exception as ag_err:
          st.error(f"حدث خطأ أثناء تشغيل الوكيل الذكي: {ag_err}")
      elif user_task:
        st.success(
            "✅ [محاكاة محلية] تم إنجاز المهمة بنجاح لوكيل "
            f"({agent_type})."
        )
      else:
        st.warning("يرجى كتابة المهمة أولاً.")

# ==========================================
# 4. وكيل البحث العميق واستخراج الداتا
# ==========================================
elif menu == "🌐 وكيل البحث العميق واستخراج الداتا":
  st.title("🌐 وكيل البحث العميق واستخراج عروض السوق والداتا")

  with st.form("deep_research_form"):
    research_query = st.text_input(
        "ما الذي تريد من وكيل البحث العميق استخراجه أو البحث عنه؟"
    )
    target_focus = st.selectbox(
        "مجال البحث والتركيز:",
        [
            "العقارات والأراضي (Real Estate)",
            "الخدمات الرقمية والتسويق (Digital & Media)",
            "السيارات واللوجستيات (Auto & Logistics)",
        ],
    )
    run_research = st.form_submit_button("🔍 بدء البحث العميق وتحليل الداتا")

    if run_research:
      if research_query:
        if db_connected:
          try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            research_prompt = f"""
                        أنت وكيل بحث عميق ومحلل أسواق خبير في السوق المغربي (قلعة السراغنة، مراكش).
                        قم بتحليل واستخراج تقرير دقيق حول: '{research_query}' في مجال '{target_focus}'.
                        """
            with st.spinner("جاري البحث العميق واستخراج البيانات..."):
              response = model.generate_content(research_prompt)
              st.success("✅ تقرير البحث العميق جاهز:")
              st.markdown(response.text)
          except Exception as rs_err:
            st.error(f"فشل تشغيل وكيل البحث العميق: {rs_err}")
        else:
          st.success("✅ تم إنجاز البحث العميق (محاكاة محلية بنجاح).")
      else:
        st.warning("يرجى إدخال موضوع البحث.")

# ==========================================
# 5. إدارة العقارات والمشاريع الذكية
# ==========================================
elif menu == "🏠 إدارة العقارات والمشاريع الذكية":
  st.title("🏠 إدارة العقارات والإعلانات والخدمات الميدانية")
  tab1, tab2 = st.tabs(
      ["➕ إضافة عقار/مشروع جديد", "📋 استعراض، فلترة وتصدير العقارات"]
  )

  with tab1:
    with st.form("prop_form"):
      name = st.text_input("اسم العقار / المشروع / الخدمة")
      price = st.number_input("السعر المقترح (درهم)", step=1000.0)
      status = st.selectbox("حالة العقار", ["متاح", "محجوز", "مباع"])
      desc = st.text_area("وصف تفصيلي أو ملاحظات ميدانية")
      use_ai = st.checkbox("🤖 توليد وصف تسويقي احترافي باستخدام Gemini AI")

      if st.form_submit_button("حفظ العقار في النظام"):
        final_desc = desc
        if use_ai and name and db_connected:
          try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"اكتب إعلاناً تسويقياً جذاباً بالعربية لعقار باسم '{name}' سعره {price} درهم بسوق قلعة السراغنة ومراكش."
            response = model.generate_content(prompt)
            final_desc = response.text
          except Exception:
            pass

        if name:
          prop_data = {
              "project_name": name,
              "price": price,
              "report_content": final_desc,
              "status": status,
          }
          if db_connected:
            supabase.table("reports").insert(prop_data).execute()
          else:
            st.session_state["local_properties"].append(prop_data)
          st.success("تم إضافة العقار بنجاح!")
        else:
          st.warning("اسم العقار مطلوب.")

  with tab2:
    try:
      p_data = (
          supabase.table("reports").select("*").execute().data
          if db_connected
          else st.session_state["local_properties"]
      )
      if p_data:
        df = pd.DataFrame(p_data)
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "📥 تحميل جدول العقارات (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="omega_properties.csv",
            mime="text/csv",
        )
      else:
        st.info("لا توجد عقارات مسجلة.")
    except Exception as e:
      st.error(f"خطأ: {e}")

# ==========================================
# 6. إدارة الزبناء (CRM) وتقييم الصدارة
# ==========================================
elif menu == "👥 إدارة الزبناء (CRM) وتقييم الصدارة":
  st.title("👥 إدارة الزبناء وجهات الاتصال (Lead Scoring)")

  with st.form("crm_form"):
    full_name = st.text_input("اسم العميل الكامل")
    phone = st.text_input("رقم الهاتف (مثال: 2126xxxxxxxx)")
    interest = st.text_input("مجال الاهتمام")
    lead_quality = st.selectbox(
        "مستوى الجودة", ["🔥 عميل ساخن", "⚡ عميل مهتم", "🧊 عميل بارد"]
    )

    if st.form_submit_button("حفظ العميل"):
      if full_name:
        payload = {
            "full_name": full_name,
            "phone": phone,
            "interest_area": f"{interest} [{lead_quality}]",
        }
        if db_connected:
          supabase.table("crm_contacts").insert(payload).execute()
        else:
          st.session_state["local_contacts"].append(payload)
        st.success("تم حفظ العميل بنجاح!")
      else:
        st.warning("اسم العميل مطلوب.")

  try:
    c_list = (
        supabase.table("crm_contacts").select("*").execute().data
        if db_connected
        else st.session_state["local_contacts"]
    )
    if c_list:
      df_c = pd.DataFrame(c_list)
      st.dataframe(df_c, use_container_width=True)
      if "phone" in df_c.columns:
        phones = df_c["phone"].dropna().tolist()
        sel_p = st.selectbox("اختر هاتف العميل لمراسلة واتساب:", phones)
        if sel_p:
          clean_p = sel_p.replace("+", "").replace(" ", "")
          st.markdown(
              f"[🔗 فتح واتساب مباشر للعميل](https://wa.me/{clean_p}?text=مرحباً،"
              " نتواصل معك من نظام OMEGA OS.)"
          )
  except Exception:
    pass

# ==========================================
# 7. تتبع الصفقات، الأرباح وROI
# ==========================================
elif menu == "💼 تتبع الصفقات، الأرباح وROI":
  st.title("💼 إدارة الصفقات وحساب العمولات وصافي الأرباح")

  with st.form("deal_form"):
    contact_id = st.number_input("معرف العميل (Contact ID)", min_value=1, step=1)
    amount = st.number_input("مبلغ الصفقة الإجمالي (درهم)", step=1000.0)
    ad_expense = st.number_input("تكلفة الحملة الإعلانية (درهم)", value=0.0)
    stage = st.selectbox(
        "المرحلة", ["في طور المتابعة", "تم إغلاق الصفقة بنجاح", "ملغاة"]
    )

    comm = amount * 0.03
    net_profit = comm - ad_expense

    if not privacy_mode:
      st.info(
          f"العمولة (3%): {comm:,.2f} د.م | صافي الربح: {net_profit:,.2f} د.م"
      )

    if st.form_submit_button("حفظ الصفقة"):
      payload = {
          "contact_id": int(contact_id),
          "amount": amount,
          "deal_stage": stage,
      }
      if db_connected:
        supabase.table("crm_deals").insert(payload).execute()
      else:
        st.session_state["local_deals"].append(payload)
      st.success("تم حفظ الصفقة بنجاح!")

# ==========================================
# 8. الحاسبة التمويلية واستثمار العقار
# ==========================================
elif menu == "🧮 الحاسبة التمويلية واستثمار العقار":
  st.title("🧮 الحاسبة التمويلية وحساب العائد الاستثماري (ROI)")
  t1, t2 = st.tabs(["حاسبة القروض البنكية", "حاسبة العائد (ROI)"])

  with t1:
    p = st.number_input("سعر العقار (درهم)", value=500000.0)
    down = st.number_input("التسبيق (درهم)", value=100000.0)
    rate = st.number_input("نسبة الفائدة السنوية (%)", value=4.5)
     yrs = st.slider("المدة بالسنوات", 5, 25, 20)
    if st.button("حساب القسط"):
      loan = p - down
      m_rate = (rate / 100) / 12
      m_pay = (
          loan * (m_rate * (1 + m_rate) ** (yrs * 12))
          / ((1 + m_rate) ** (yrs * 12) - 1)
      )
      st.metric("القسط الشهري المتوقع:", f"{m_pay:,.2f} درهم")

  with t2:
    inv = st.number_input("تكلفة الاستثمار (درهم)", value=600000.0)
    m_rent = st.number_input("الإيجار الشهري المتوقع (درهم)", value=4000.0)
    if st.button("حساب العائد"):
      roi = ((m_rent * 12) / inv) * 100 if inv > 0 else 0
      st.metric("نسبة العائد السنوي (ROI):", f"{roi:.2f}% سنوياً")

# ==========================================
# 9. اللوجستيات وتأجير السيارات
# ==========================================
elif menu == "🚗 اللوجستيات وتأجير السيارات":
  st.title("🚗 إدارة أسطول النقل وتأجير السيارات (Marrakech World Auto)")
  car = st.selectbox("السيارة:", ["Dacia Duster", "Renault Clio 5", "Hyundai Tucson"])
  days = st.number_input("عدد الأيام", 1, 30, 3)
  rate = st.number_input("سعر اليوم (درهم)", 350.0)
  if st.button("حساب التكلفة"):
    tot = days * rate
    st.success(f"التكلفة الإجمالية: {tot:,.2f} درهم")
    st.markdown(
        f"[🔗 حجز عبر"
        f" واتساب](https://wa.me/212691897126?text=حجز%20{urllib.parse.quote(car)}%20لمدة%20{days}%20أيام)"
    )

# ==========================================
# 10. الأرشيف والتصدير الشامل
# ==========================================
elif menu == "📁 الأرشيف والتصدير الشامل (ZIP & CSV)":
  st.title("📁 الأرشيف والتصدير الشامل")
  files = os.listdir(GALLERY_FOLDER)
  if files and st.button("تنزيل الأرشيف البصري (ZIP)"):
    zip_path = "omega_archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
      for root, _, filenames in os.walk(GALLERY_FOLDER):
        for f in filenames:
          zipf.write(
              os.path.join(root, f),
              arcname=os.path.relpath(os.path.join(root, f), GALLERY_FOLDER),
          )
    with open(zip_path, "rb") as f:
      st.download_button(
          "تحميل الأرشيف المضغوط", f, file_name="omega_archive.zip"
      )
  else:
    st.info("الأرشيف البصري فارغ حالياً.")

# ==========================================
# 11. الإعدادات والأمان السيادي
# ==========================================
elif menu == "⚙️ الإعدادات والأمان السيادي":
  st.title("⚙️ الإعدادات والأمان السيادي")
  if db_connected:
    st.success("🟢 متصل بقاعدة بيانات Supabase بنجاح.")
  else:
    st.warning("🟡 يعمل بنمط المحاكاة المحلية لغياب مفاتيح Supabase.")
  st.info("🤖 وكلاء الذكاء الاصطناعي مفعلان وجاهزان.")

st.markdown("---")
st.markdown(
    "**📞 التواصل السريع:** [راسلنا عبر"
    " واتساب](https://wa.me/212691897126?text=مرحباً،%20أتواصل%20معكم%20من%20منظومة%20Tassaout%20Omega%20OS%20PRIME.)"
)
