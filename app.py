import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="Tassaout Immo & Media", page_icon="🏢", layout="wide")

# التصميم الموحد والأنماط البصرية
st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; font-family: Tahoma, sans-serif; }
    .prop-card { padding: 20px; border-radius: 12px; border: 1px solid #22c55e; margin-bottom: 20px; background-color: #0f3d24; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .badge-cat { background-color: #22c55e; color: #000; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 8px; }
    .stButton>button { background-color: #22c55e; color: #000; font-weight: bold; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #16a34a; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# ملف تخزين البيانات المحلي
DATA_FILE = "tassaout_interactive_ads.json"

def load_ads():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_ads(ads):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=4)

if 'ads_data' not in st.session_state:
    st.session_state.ads_data = load_ads()

# دالة تحميل الخدمات الرقمية والهندسية
def load_services():
    try:
        with open("services_tassaout_sraghna.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"services": [
            {"الخدمة": "التسويق الرقمي وإدارة الحملات", "الوصف": "إدارة الحملات الإعلانية الموجهة لعقارات ومشاريع قلعة السراغنة ومراكش."},
            {"الخدمة": "التصميم الهندسي والـ 3D", "الوصف": "إنشاء مجسمات معمارية وتصاميم ثلاثية الأبعاد احترافية."},
            {"الخدمة": "اللوجستيك والنقل", "الوصف": "خدمات نقل البضائع ومواد البناء بالمنطقة."}
        ]}

# تهيئة الـ Chat في session_state للوكيل الذكي
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "مرحباً بك! أنا مساعدك الذكي في Tassaout Immo & Media. اسألني عن أي عقار، خدمة، مواد بناء، أو اطلب المساعدة في اختيار العرض المناسب لك بقلعة السراغنة ومراكش."}
    ]

# التنقل بين الصفحات الرئيسية
if 'nav_mode' not in st.session_state: st.session_state.nav_mode = "المنصة الرئيسية"

col_n1, col_n2, col_n3, col_n4 = st.columns(4)
if col_n1.button("🏠 المنصة الرئيسية والعروض", use_container_width=True): st.session_state.nav_mode = "المنصة الرئيسية"
if col_n2.button("➕ إضافة إعلان جديد", use_container_width=True): st.session_state.nav_mode = "إضافة إعلان"
if col_n3.button("🛠️ الخدمات الرقمية والهندسية", use_container_width=True): st.session_state.nav_mode = "خدمات"
if col_n4.button("📞 تواصل مع عامر بوخدادة", use_container_width=True): st.session_state.nav_mode = "اتصال"

st.markdown("---")

# 1. صفحة المنصة الرئيسية وعرض الإعلانات مع الفلترة والوكيل الذكي
if st.session_state.nav_mode == "المنصة الرئيسية":
    st.title("🏢 Tassaout Immo & Media")
    st.markdown("<p style='color: #a3e635;'>منصة الإعلانات الذكية والخدمات الشاملة - قلعة السراغنة ومراكش</p>", unsafe_allow_html=True)
    
    # قسم الوكيل الذكي المتفاعل
    with st.expander("🤖 الوكيل الذكي المتفاعل (اضغط للتحدث والاستفسار)", expanded=True):
        for msg in st.session_state.chat_history:
            if msg["role"] == "assistant":
                st.markdown(f"<div style='background-color: #14532d; color: #4ade80; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-right: 3px solid #22c55e;'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #0f3d24; color: #f8fafc; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 3px solid #16a34a; text-align: left;'>👤 {msg['content']}</div>", unsafe_allow_html=True)
        
        user_query = st.text_input("اكتب طلبك أو استفسارك هنا...", key="user_agent_input")
        if st.button("إرسال للوكيل الذكي"):
            if user_query.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                q = user_query.lower()
                
                # منطق الرد الآلي
                if 'أرض' in q or 'فلاحية' in q or 'عقار' in q:
                    results = [ad for ad in st.session_state.ads_data if 'العقاري' in ad['category'] or 'أرض' in ad['title']]
                    if results:
                        ans = f"وجدت {len(results)} عرض عقاري مطابق. أحدثها: '{results[0]['title']}' بسعر {results[0]['price']} في {results[0]['location']}."
                    else:
                        ans = "عذراً، لا توجد عروض عقارية مطابقة حالياً، يمكنك إضافة عرض جديد من قائمة 'إضافة إعلان'."
                elif 'بناء' in q or 'إسمنت' in q or 'حديد' in q or 'مواد' in q:
                    results = [ad for ad in st.session_state.ads_data if 'مواد البناء' in ad['category']]
                    if results:
                        ans = f"متوفر لدينا في قسم مواد البناء: '{results[0]['title']}' - {results[0]['description']}."
                    else:
                        ans = "يمكننا توفير كافة مواد البناء بالجملة والتقسيط بجهة مراكش آسفي حسب طلبك."
                elif 'مراكش' in q or 'السراغنة' in q:
                    ans = "نحن نغطي مناطق قلعة السراغنة ومراكش بشكل أساسي في مجالات العقارات، مواد البناء، والهندسة الرقمية والتسويق."
                else:
                    ans = "يسعدنا تواصلك! يمكنك تصفح العروض أدناه أو التواصل معنا مباشرة عبر الواتساب."
                
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                st.rerun()

    st.markdown("### 📋 العروض والأنشطة المتاحة")
    
    # شريط الفلترة حسب القطاع
    filter_option = st.selectbox("فلترة حسب القطاع:", [
        "جميع العروض",
        "العقاري الفلاحي",
        "العقاري الصناعي والتجاري",
        "العقاري المهني والاستثماري",
        "بيع مواد البناء",
        "مكتب الدراسات والهندسة",
        "الهندسة الرقمية والتصوير",
        "التسويق العقاري والتجاري"
    ])
    
    # فلترة البيانات
    displayed_ads = st.session_state.ads_data
    if filter_option != "جميع العروض":
        displayed_ads = [ad for ad in st.session_state.ads_data if ad['category'] == filter_option]
    
    if not displayed_ads:
        st.info("لا توجد عروض مطابقة حالياً في هذا القسم. يمكنك إضافة عرض جديد.")
    else:
        cols = st.columns(3)
        for idx, ad in enumerate(displayed_ads):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="prop-card">
                    <span class="badge-cat">{ad.get('category', 'عام')}</span>
                    <h3 style="color: #4ade80; margin: 10px 0 5px 0;">{ad.get('title', '')}</h3>
                    <p style="font-size: 13px; color: #cbd5e1; margin: 3px 0;">📍 {ad.get('location', '')}</p>
                    <p style="font-size: 12px; color: #94a3b8; margin: 6px 0;">{ad.get('description', '')}</p>
                    <hr style="border-color: #14532d;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 15px; font-weight: bold; color: #4ade80;">{ad.get('price', '')}</span>
                        <a href="https://wa.me/212691897126" target="_blank" style="background-color: #16a34a; color: #fff; padding: 5px 10px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">تواصل معنا</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # عرض الصور المرفقة إن وجدت
                if ad.get('images'):
                    img_cols = st.columns(len(ad['images']) if len(ad['images']) <= 3 else 3)
                    for img_i, img_data in enumerate(ad['images']):
                        with img_cols[img_i % 3]:
                            st.image(img_data, use_container_width=True)
                
                # زر حذف العرض
                if st.button(f"حذف العرض #{idx}", key=f"del_{idx}"):
                    st.session_state.ads_data.remove(ad)
                    save_ads(st.session_state.ads_data)
                    st.rerun()

# 2. صفحة إضافة إعلان جديد
elif st.session_state.nav_mode == "إضافة إعلان":
    st.title("➕ إضافة عرض أو إعلان جديد")
    st.write("أدخل تفاصيل الإعلان والبيانات مع إمكانية إرفاق الصور من الاستوديو بعدد غير محدود.")
    
    with st.form("new_ad_form"):
        title = st.text_input("عنوان العرض", placeholder="مثال: أرض فلاحية مجهزة للبيع")
        category = st.selectbox("القطاع أو الفئة", [
            "العقاري الفلاحي",
            "العقاري الصناعي والتجاري",
            "العقاري المهني والاستثماري",
            "بيع مواد البناء",
            "مكتب الدراسات والهندسة",
            "الهندسة الرقمية والتصوير",
            "التسويق العقاري والتجاري"
        ])
        location = st.text_input("الموقع", placeholder="مثال: قلعة السراغنة / مراكش")
        price = st.text_input("السعر أو التكلفة", placeholder="مثال: 1,200,000 DH")
        uploaded_files = st.file_uploader("تحميل الصور (عدد غير محدود)", accept_multiple_files=True, type=["png", "jpeg", "jpg", "webp"])
        description = st.text_area("التفاصيل والوصف", placeholder="اكتب تفاصيل الإعلان هنا...")
        
        submitted = st.form_submit_button("نشر العرض فوراً")
        if submitted:
            if title and location and price and description:
                images_list = []
                if uploaded_files:
                    for file in uploaded_files:
                        bytes_data = file.read()
                        encoded_img = base64.b64encode(bytes_data).decode("utf-8")
                        images_list.append(f"data:image/jpeg;base64,{encoded_img}")
                
                new_ad = {
                    "title": title,
                    "category": category,
                    "location": location,
                    "price": price,
                    "description": description,
                    "images": images_list
                }
                
                st.session_state.ads_data.insert(0, new_ad)
                save_ads(st.session_state.ads_data)
                st.success("تم نشر العرض بنجاح!")
            else:
                st.error("الرجاء ملء الحقول الإجبارية.")

# 3. صفحة الخدمات الرقمية والهندسية
elif st.session_state.nav_mode == "خدمات":
    st.title("🛠️ خدماتنا الرقمية والهندسية")
    services_data = load_services()
    for s in services_data.get("services", []):
        with st.expander(f"✨ {s.get('الخدمة', 'خدمة')}"):
            st.write(s.get('الوصف', ''))

# 4. صفحة الاتصال
elif st.session_state.nav_mode == "اتصال":
    st.title("📞 تواصل مع عامر بوخدادة")
    st.success("الهاتف/واتساب: 0691897126")
    st.markdown("[اضغط هنا للمحادثة المباشرة عبر الواتساب](https://wa.me/212691897126)")
