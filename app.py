import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة مشاريع البناء والعقار", layout="wide", page_icon="🏗️")

# تصميم الواجهة بمدخلات المشروع
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

# الحسابات المالية
contingency_amount = (construction_cost + architect_fees) * (contingency_rate / 100)
total_investment = land_price + construction_cost + architect_fees + contingency_amount

st.sidebar.markdown("### التوقعات المالية للبيع أو الاستثمار")
expected_selling_price = st.sidebar.number_input("القيمة التقديرية للبيع الإجمالي أو المداخيل (درهم)", min_value=100000, max_value=20000000, value=2200000, step=50000)

net_profit = expected_selling_price - total_investment
roi = (net_profit / total_investment) * 100 if total_investment > 0 else 0

# العرض الرئيسي في لوحة القيادة
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
st.success(f"النظام جاهز ومُحدث لتقييم **{project_name}**. يمكنك تعديل الأبيانات في الشريط الجانبي لتحديث الحسابات فورياً.")
