import streamlit as st
import requests
import json
import pandas as pd
import re

st.set_page_config(page_title="OMEGA & DANA K9 - مركز القيادة العقاري", page_icon="👑", layout="wide")

# ===== محرك الذكاء الاصطناعي (Groq) =====
def call_super_ai(prompt, agent_name, domain):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Real Estate Agent & Broker specialized in '{domain}' in Tissaout, Tamlalt, and El Kelaa des Sraghna region. "
        f"Think step by step. Provide professional, highly tailored, actionable real estate strategies, land offers, zoning details, and investment insights. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75,
        "max_tokens": 2000
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def send_whatsapp_alert(message):
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            return

        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message[:4096]}
        }
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        st.warning(f"تعذر إرسال إشعار الواتساب: {e}")

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        return call_super_ai(f"بصفتك CEO عقاري محترف، قم بإعداد دراسة السوق والعرض الاستثماري الشامل لهذا الطلب: {task}. حدد المواصفات، الفئة المستهدفة، الفرص الاستثمارية، وخطوات الإنجاز بمدينة تملالت.", "Super CEO Agent", self.domain)

    def cto(self, task):
        return call_super_ai(f"بصفتك خبير رقمي و تقني عقاري (CTO)، اقترح استراتيجية التسويق الرقمي المستهدفة (اعلانات منصات التواصل، Geo-targeting) لجذب المشترين والمستثمرين لـ: {task}", "Super CTO Agent", self.domain)

    def coo(self, task):
        return call_super_ai(f"بصفتك مدبر عمليات (COO)، ضع خطة عمل ميدانية دقيقة لتدبير المعاملات العقارية، الوثائق الإدارية (تحفيظ، تصميم التهيئة)، والتنسيق الميداني بخصوص: {task}", "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة الاستراتيجية: {plan}. اكتب 3 إعلانات عقارية استثنائية وجذابة جداً خاصة بـ (بقع سكنية وتجارية بتملالت) باللهجة المغربية والفصحى مع الأيقونات، الهاشتاقات، وتحديد رقم الواتساب للتواصل: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA TAMLALT REAL ESTATE\nطلب جديد: بقع سكنية وتجارية بتملالت\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان العقاري وإضافة محفزات الاستعجال FOMO، ضمانات الموثوقية القانونية، ودعوة قوية لاتخاذ القرار الشراعي فوراً: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة التطبيق الموحدة =====
st.title("👑 OMEGA & DANA K9 - عقارات تملالت وقلعة السراغنة")
st.caption("نظام الوكلاء الأذكياء ومحرك البحث الاستراتيجي للبقع السكنية والتجارية")

tab1, tab2 = st.tabs(["🚀 نظام الوكلاء (OMEGA Agents)", "🐕 أداة الصيد والبحث (DANA K9)"])

with tab1:
    domain = "العقار - تملالت وقلعة السراغنة"
    task = st.text_area("وصف الطلب أو العرض العقاري", value="مطلوب/عرض بقع سكنية وتجارية استراتيجية في تملالت للمستثمرين والخواص مع دراسة الفرص الاستثمارية")

    agent = SuperOmegaAgent(domain)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧠 دراسة الاستثمار العقاري (CEO)"):
            with st.spinner("جاري إعداد التحليل الاستراتيجي للبقع بتملالت..."):
                st.markdown(agent.ceo(task))
    with col2:
        if st.button("💻 الاستراتيجية الرقمية (CTO)"):
            with st.spinner("جاري صياغة استراتيجية استهداف المستثمرين..."):
                st.markdown(agent.cto(task))
    with col3:
        if st.button("📊 الخطة الميدانية والتحفيظ (COO)"):
            with st.spinner("جاري تجهيز الخطوات الميدانية والإدارية..."):
                st.markdown(agent.coo(task))

    if st.button("✍️ توليد الإعلان الاحترافي + إرسال واتساب"):
        with st.spinner("جاري صياغة الإعلانات القوية وتنبيه الواتساب..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم بنجاح!")
            st.markdown(final_ad)

with tab2:
    st.markdown("**القاعدة**: عطي الأمر و أنا ننفد.")
    command = st.text_area("🎯 عطي الأمر للبحث:", placeholder="مثال: بقع سكنية وتجارية للبيع في تملالت")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        do_phone = st.checkbox("استخرج الأرقام", value=True)
    with col_b:
        do_price = st.checkbox("استخرج الأثمنة", value=True)
    with col_c:
        do_excel = st.checkbox("صدر Excel", value=True)

    PHONE_REGEX = r'(\+212[67]\d{8}|0[67]\d{8})'
    PRICE_REGEX = r'(\d+[\s,]?\d*)\s*(درهم|dh|MAD)'

    if st.button("🚀 نفد أمر البحث الآن"):
        if command:
            query = f"{command} تملالت قلعة السراغنة المغرب"
            with st.spinner("🐕 DANA K9 كيصيد دابا..."):
                try:
                    from duckduckgo_search import DDGS
                    results = []
                    with DDGS() as ddgs:
                        res = ddgs.text(query, region="ma-ma", max_results=15)
                        for i, r in enumerate(res):
                            text = r.get('title', '') + " " + r.get('body', '')

                            phone = "غير متوفر"
                            if do_phone:
                                phones = re.findall(PHONE_REGEX, text)
                                if phones: phone = phones[0]

                            price = "غير محدد"
                            if do_price:
                                prices = re.findall(PRICE_REGEX, text)
                                if prices: price = f"{prices[0][0]} {prices[0][1]}"

                            results.append({
                                "م": i+1,
                                "النتيجة": r.get('title', ''),
                                "الوصف": r.get('body', '')[:180] + "...",
                                "الثمن": price,
                                "الهاتف": phone,
                                "الرابط": r.get('href', '')
                            })

                    if results:
                        df = pd.DataFrame(results)
                        st.success(f"تم التنفيذ. تم العثور على {len(df)} نتيجة")
                        st.dataframe(df, use_container_width=True, hide_index=True)

                        if do_excel:
                            csv = df.to_csv(index=False).encode('utf-8-sig')
                            st.download_button("📥 تحميل النتائج Excel", csv, "dana_k9_results.csv", "text/csv")
                    else:
                        st.warning("لم يتم العثور على نتائج مطابقة للأمر.")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء البحث: {e}")
        else:
            st.error("لم يتم إعطاء أي أمر للبحث.")
