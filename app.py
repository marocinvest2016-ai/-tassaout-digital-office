import streamlit as st
from supabase import create_client, Client
import ollama
from duckduckgo_search import DDGS

# 1. إعدادات النظام السيادي
st.set_page_config(page_title="OMEGA OS - Sovereign Edition", layout="wide")

# الربط الآمن مع Supabase
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("👑 OMEGA OS - Sovereign Edition")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("الوحدة السيادية", [
    "رصد الميدان", 
    "مصنع الإعلانات التسويقية 📢", 
    "الوكيل الذكي المحلي (بدون API)", 
    "الأرشيف والتقارير"
])

# ==========================================
# الوحدة 1: رصد الميدان
# ==========================================
if menu == "رصد الميدان":
    st.header("📊 سجل بيانات الميدان")
    p_name = st.text_input("اسم المشروع/الورش")
    p_content = st.text_area("محتوى التقرير أو التحديث")
    if st.button("حفظ في السحابة السيادية"):
        if p_name and p_content:
            supabase.table("reports").insert({"project_name": p_name, "report_content": p_content, "report_type": "ورش"}).execute()
            st.success("تم الحفظ!")

# ==========================================
# الوحدة 2: مصنع الإعلانات الذكي (Ollama المحلي)
# ==========================================
elif menu == "مصنع الإعلانات التسويقية 📢":
    st.header("📢 مصنع صياغة الإعلانات (محلي بالكامل)")
    col1, col2 = st.columns(2)
    with col1:
        p_type = st.selectbox("نوع العقار:", ["أرض فلاحية", "فيرمة", "بقعة سكنية", "شقة"])
        loc = st.text_input("الموقع:", value="قلعة السراغنة")
    with col2:
        price = st.text_input("السعر:", value="تحديد بعد المعاينة")
        features = st.text_area("المميزات:")
    
    if st.button("توليد إعلان ذكي"):
        with st.spinner("الوكيل المحلي (Ollama) يكتب الإعلان..."):
            prompt = f"اكتب إعلان عقاري احترافي باللهجة المغربية الجذابة للعقار: {p_type} في {loc}، السعر: {price}، المميزات: {features}. انتهِ برقم الهاتف 0691897126 ورابط يوتيوب Studio Tassaout."
            res = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
            ad = res['message']['content']
            st.markdown(ad)
            supabase.table("instant_ads").insert({"content": p_type, "message": ad}).execute()
            st.success("تم الحفظ في القاعدة!")

# ==========================================
# الوحدة 3: الوكيل الذكي المحلي (Ollama + DuckDuckGo)
# ==========================================
elif menu == "الوكيل الذكي المحلي (بدون API)":
    st.header("🌐 الوكيل السيادي المطلق [محلي 100%]")
    q = st.text_input("اسأل الوكيل عن أي شيء:")
    if st.button("تنفيذ المهمة"):
        with st.spinner("البحث في الويب والمعالجة محلياً عبر Ollama..."):
            with DDGS() as ddgs:
                res = list(ddgs.text(q, max_results=3))
            ctx = "\n".join([r['body'] for r in res])
            ans = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': f"السؤال: {q}\nالمعلومات: {ctx}\nأجب بالعربية:"}])
            st.markdown(ans['message']['content'])
            supabase.table("reports").insert({"project_name": "بحث ذكي محلي", "report_content": ans['message']['content'], "report_type": "بحث"}).execute()

# ==========================================
# الوحدة 4: الأرشيف والتقارير (بدون أخطاء PDF)
# ==========================================
elif menu == "الأرشيف والتقارير":
    st.header("📁 الأرشيف السيادي")
    data = supabase.table("reports").select("*").order("created_at", desc=True).execute().data
    if data:
        for r in data:
            with st.expander(f"📌 {r.get('project_name', 'بدون عنوان')} ({r.get('created_at', '')})"):
                content = r.get('report_content', '')
                st.text_area("محتوى التقرير المؤرشف:", value=content, height=150, key=f"txt_{r.get('id')}")
                st.info("💡 يمكنك نسخ النص مباشرة واستخدامه في واتساب أو أي منصة دون مشاكل.")
    else:
        st.info("لا توجد تقارير مسجلة في الأرشيف حالياً.")
