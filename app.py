import streamlit as st
import pandas as pd
import io
import datetime
from supabase import create_client

# إعداد الصفحة
st.set_page_config(page_title="Alpha Nexus Omega | Master Control", page_icon="⚡", layout="wide")

# الاتصال بـ Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_SERVICE_ROLE_KEY")

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("⚡ Alpha Nexus Omega — Master Command Center")
st.markdown("نظـام التحكم المركزي المتكامل لإدارة العقارات، الحملات الإعلانية، والسجلات الذكية.")

# التبويبات الرئيسية (Tabs) للوحة التحكم الكبرى
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📣 Instant Ads", 
    "🚀 Omega Queue", 
    "📊 Camera Logs", 
    "🛡️ Audit Trail", 
    "📁 Storage Media", 
    "⚙️ Config & Notifs",
    "🔔 الإشعارات",
    "🛠️ الإعدادات الديناميكية",
    "📥 التصدير السريع"
])

with tab1:
    st.subheader("إدارة نظام الإعلانات الفورية (Instant Ads)")
    with st.form("instant_ads_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            content = st.text_area("محتوى الإعلان (Content)")
        with col_b:
            message = st.text_area("الرسالة النهائية (Message)")
        source = st.text_input("المصدر", value="streamlit-agent")
        submitted = st.form_submit_button("🚀 حفظ الإعلان")
        
        if submitted:
            if not content.strip() or not message.strip():
                st.warning("⚠️ حقل الـ content والـ message مطلوبان.")
            else:
                try:
                    payload = {"content": content.strip(), "message": message.strip(), "source": source.strip()}
                    supabase.table("instant_ads").insert(payload).execute()
                    st.success("✅ تم حفظ الإعلان بنجاح وتجاوز قيود RLS عبر Service Role.")
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")

    st.markdown("---")
    st.subheader("📋 آخر الإعلانات المسجلة")
    try:
        ads_res = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(5).execute()
        if ads_res.data:
            st.dataframe(ads_res.data, width='stretch')
        else:
            st.info("لا توجد إعلانات.")
    except Exception as e:
        st.warning(f"تعذر الجلب: {e}")

with tab2:
    st.subheader("طابور الحملات والإعلانات (Omega Queue)")
    try:
        queue_res = supabase.table("alpha_nexus_omega_queue").select("*").order("created_at", desc=True).limit(10).execute()
        if queue_res.data:
            st.dataframe(queue_res.data, width='stretch')
        else:
            st.info("الطابور فارغ.")
    except Exception as e:
        st.warning(f"خطأ في الجلب: {e}")

with tab3:
    st.subheader("سجلات الكاميرا والعمليات (Omega Logs)")
    try:
        logs_res = supabase.table("tassaout_omega_logs").select("*").order("created_at", desc=True).limit(5).execute()
        if logs_res.data:
            st.dataframe(logs_res.data, width='stretch')
        else:
            st.info("لا توجد سجلات كاميرا.")
    except Exception as e:
        st.warning(f"خطأ: {e}")

with tab4:
    st.subheader("سجل التدقيق المركزي (Immutable Audit Trail)")
    try:
        audit_res = supabase.table("alpha_system_audit_logs").select("*").order("created_at", desc=True).limit(10).execute()
        if audit_res.data:
            st.dataframe(audit_res.data, width='stretch')
        else:
            st.info("لا توجد حركات مسجلة.")
    except Exception as e:
        st.warning(f"خطأ: {e}")

with tab5:
    st.subheader("إدارة رفع الملفات والوسائط السحابية (Private Storage & Signed URLs)")
    
    uploaded_file = st.file_uploader("اختر ملفاً للرفع:", type=["png", "jpg", "jpeg", "pdf", "mp4", "txt"])
    if uploaded_file is not None:
        if st.button("🚀 رفع للسحابة الآن"):
            try:
                path = f"admin_uploads/{uploaded_file.name}"
                supabase.storage.from_("tassaout-media").upload(
                    path=path, 
                    file=uploaded_file.getvalue(), 
                    file_options={"content-type": uploaded_file.type or "application/octet-stream"}
                )
                
                signed_url_res = supabase.storage.from_("tassaout-media").create_signed_url(path, 300)
                signed_url = None
                if isinstance(signed_url_res, dict):
                    signed_url = signed_url_res.get("signedURL") or signed_url_res.get("signedUrl") or signed_url_res.get("url")
                
                st.success("✅ تم الرفع وإنشاء الرابط الآمن بنجاح!")
                if signed_url:
                    st.code(signed_url)
            except Exception as e:
                st.error(f"❌ فشل الرفع: {e}")

    st.markdown("---")
    st.markdown("### 🧪 اختبار التخزين الآمن (Storage Test)")
    if st.button("🚀 تشخيص اختبار التخزين الفوري"):
        try:
            test_path = f"admin_uploads/test-{int(datetime.datetime.utcnow().timestamp())}.txt"
            supabase.storage.from_("tassaout-media").upload(
                path=test_path, 
                file=b"Alpha Nexus Storage Test Content", 
                file_options={"content-type": "text/plain"}
            )
            obj_check = supabase.table("storage.objects").select("name").eq("bucket_id", "tassaout-media").eq("name", test_path).maybe_single().execute()
            if obj_check.data:
                st.success(f"✅ تم التحقق من وجود الملف في قاعدة البيانات: {obj_check.data.get('name')}")
            else:
                st.warning("تم الرفع ولكن تعذر العثور على السجل في storage.objects مباشرة.")
        except Exception as e:
            st.error(f"❌ خطأ التشخيص: {e}")

with tab6:
    st.subheader("إعدادات المنظومة الأساسية")
    try:
        config_res = supabase.table("alpha_site_config").select("*").execute()
        if config_res.data:
            for row in config_res.data:
                st.text_input(f"الإعداد [{row['key']}]:", value=row['value'], disabled=True)
    except Exception as e:
        st.warning(f"خطأ: {e}")

with tab7:
    st.markdown("### 🔔 سجل الإشعارات الإدارية")
    try:
        notif_res = supabase.table("alpha_notifications").select("*").order("created_at", desc=True).limit(5).execute()
        if notif_res.data:
            st.dataframe(notif_res.data, width='stretch')
        else:
            st.info("لا توجد إشعارات جديدة.")
    except Exception as e:
        st.warning(f"تعذر جلب الإشعارات: {e}")

with tab8:
    st.markdown("### 🛠️ إدارة وتعديل إعدادات النظام الديناميكية")
    try:
        config_res = supabase.table("alpha_site_config").select("*").execute()
        if config_res.data:
            for row in config_res.data:
                new_val = st.text_input(f"تعديل [{row['key']}]:", value=row['value'], help=row['description'])
                if st.button(f"حفظ التعديل: {row['key']}", key=f"btn_{row['key']}"):
                    supabase.table("alpha_site_config").update({"value": new_val, "updated_at": "now()"}).eq("key", row['key']).execute()
                    st.success(f"✅ تم تحديث الإعداد {row['key']} بنجاح!")
        else:
            st.info("لا توجد إعدادات مسجلة.")
    except Exception as e:
        st.warning(f"تعذر جلب الإعدادات: {e}")

with tab9:
    st.markdown("### 📥 تصدير سجلات الحملات كملف CSV")
    if st.button("📥 تجهيز وتنزيل ملف CSV للحملات"):
        try:
            export_res = supabase.table("alpha_nexus_omega_queue").select("*").execute()
            if export_res.data:
                df = pd.DataFrame(export_res.data)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📂 اضغط هنا لتحميل الملف (CSV)",
                    data=csv_data,
                    file_name="alpha_nexus_campaigns_export.csv",
                    mime="text/csv",
                )
            else:
                st.warning("لا توجد بيانات لتصديرها.")
        except Exception as e:
            st.error(f"❌ فشل عملية التصدير: {e}")
