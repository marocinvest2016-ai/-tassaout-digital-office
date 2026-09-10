import streamlit as st
import requests
import json

# قائمة نماذج Groq محدثة مع fallback تلقائي
GROQ_MODELS = [
    "llama-3.1-8b-instant",        # أساسي: سريع ومستقر 100%
    "llama-3.2-11b-vision-preview", # بديل: أقوى شوية
    "llama-3.3-70b-versatile",      # قوي جداً (إذا كان متاح لحسابك)
]

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق مع نظام Fallback وتتبع النموذج الناجح"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Meta Llama on Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    last_error = None
    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.75,
            "max_completion_tokens": 2000
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=90)
            
            # معالجة أخطاء النموذج غير المتاح
            if res.status_code == 404:
                last_error = f"⚠️ النموذج {model} غير موجود (404). جاري تجربة البديل..."
                continue
            elif res.status_code == 400:
                last_error = f"⚠️ النموذج {model} غير صالح (400). جاري تجربة البديل..."
                continue
            elif res.status_code == 429:
                last_error = f"⏳ تجاوزت حد الطلبات (429) على {model}. جاري تجربة البديل..."
                continue
            
            # أي خطأ آخر
            res.raise_for_status()
            
            # تسجيل النموذج الناجح في الجلسة
            st.session_state.last_model_used = model
            st.session_state.last_model_status = "✅ نجح"
            
            return res.json()['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            last_error = f"⏱️ انتهت مهلة الاتصال بالنموذج {model} (90 ثانية). جاري تجربة البديل..."
            continue
        except Exception as e:
            last_error = f"❌ خطأ في الاتصال (النموذج {model}): {type(e).__name__} - {str(e)}"
            continue

    # إذا فشل كل النماذج
    st.session_state.last_model_status = "❌ فشل"
    return f"❌ تعذر الاتصال بجميع النماذج المتاحة.\n\nآخر خطأ: {last_error}"

def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب API"""
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            st.warning("⚠️ إعدادات WhatsApp غير مكتملة في Secrets")
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
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code != 200:
            st.warning(f"⚠️ فشل إرسال WhatsApp: HTTP {res.status_code}")
    except Exception as e:
        st.warning(f"⚠️ تعذر إرسال إشعار الواتساب: {type(e).__name__} - {str(e)}")

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = (
            f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}.\n\n"
            f"المطلوب:\n"
            f"1. تحليل SWOT مفصّل (نقاط القوة، الضعف، الفرص، التهديدات)\n"
            f"2. الميزة التنافسية الأساسية (Unique Value Proposition)\n"
            f"3. خطة تنفيذية لمدة 90 يوم (30-60-90) مع معالم رئيسية\n"
            f"4. مؤشرات الأداء الرئيسية (KPIs) المقترحة\n\n"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super CEO Agent", self.domain)

    def cto(self, task):
        prompt = (
            f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}.\n\n"
            f"المطلوب:\n"
            f"1. البنية التقنية المقترحة (Tech Stack: Frontend, Backend, Database, APIs)\n"
            f"2. أدوات التشغيل والأتمتة (Automation Tools, CI/CD, Monitoring)\n"
            f"3. استراتيجية استهداف الجمهور الرقمي (Digital Audience Targeting)\n"
            f"4. خطة أمان وحماية البيانات الأساسية\n\n"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super CTO Agent", self.domain)

    def coo(self, task):
        prompt = (
            f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}.\n\n"
            f"المطلوب:\n"
            f"1. هيكل الفريق والموارد البشرية المطلوبة\n"
            f"2. الجدولة الزمنية التفصيلية (Gantt-style timeline)\n"
            f"3. مؤشرات الأداء الرئيسية (KPIs) لكل مرحلة\n"
            f"4. إدارة المخاطر وخطة طوارئ\n\n"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = (
            f"بناءً على هذه الخطة الاستراتيجية:\n\n{plan}\n\n"
            f"اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى، مع:\n"
            f"• عنوان قوي (Headline) يلفت الانتباه\n"
            f"• نص إعلاني مقنع (Body Copy) يبرز الفوائد والحلول\n"
            f"• دعوة واضحة للعمل (CTA) مع رقم الواتساب: {whatsapp_num}\n"
            f"• هاشتاقات مناسبة (3-5 هاشتاقات)\n"
            f"• أيقونات وإيموجيز لجذب الانتباه\n\n"
            f"الإعلانات تكون مناسبة لـ Facebook, Instagram, WhatsApp Status."
        )
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        
        # إرسال إشعار WhatsApp
        alert_msg = (
            f"👑 OMEGA SUPER AGENTIC v4.5\n"
            f"📂 المجال: {self.domain}\n"
            f"🤖 النموذج المستخدم: {st.session_state.get('last_model_used', 'غير محدد')}\n\n"
            f"📝 نص الإعلان:\n{ad[:1500]}..."  # أول 1500 حرف فقط
        )
        send_whatsapp_alert(alert_msg)
        
        return ad

    def closer(self, ad):
        prompt = (
            f"قم بتحسين نص هذا الإعلان لزيادة المبيعات والتحويلات:\n\n{ad}\n\n"
            f"أضف العناصر التالية:\n"
            f"1. محفزات الاستعجال (FOMO): عرض محدود، وقت محدود، كمية محدودة\n"
            f"2. ضمان قوي (Money-back Guarantee أو ضمان الرضا)\n"
            f"3. شهادات عملاء (Testimonials) واقعية ومقنعة\n"
            f"4. أسئلة شائعة (FAQ) قصيرة تجاوب على اعتراضات الزبون\n"
            f"5. دعوة أقوى للعمل (Stronger CTA) مع شعور بالاستعجال\n\n"
            f"حافظ على اللهجة المغربية + العربية الفصحى، والتنسيق الأصلي."
        )
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

    def full_pipeline(self, task):
        """تشغيل الخط الكامل: CEO → CTO → COO → Copywriter → Closer"""
        with st.spinner("🧠 جاري تحليل المهمة..."):
            ceo_plan = self.ceo(task)
        
        with st.spinner("⚙️ جاري وضع الاستراتيجية التقنية..."):
            cto_plan = self.cto(task)
        
        with st.spinner("📋 جاري وضع الخطة التنفيذية..."):
            coo_plan = self.coo(task)
        
        combined_plan = f"=== خطة CEO ===\n{ceo_plan}\n\n=== خطة CTO ===\n{cto_plan}\n\n=== خطة COO ===\n{coo_plan}"
        
        with st.spinner("✍️ جاري كتابة الإعلانات..."):
            ad = self.copywriter(combined_plan)
        
        with st.spinner("🔥 جاري تحسين الإعلان لزيادة المبيعات..."):
            final_ad = self.closer(ad)
        
        return {
            "ceo": ceo_plan,
            "cto": cto_plan,
            "coo": coo_plan,
            "ad_original": ad,
            "ad_final": final_ad,
            "model_used": st.session_state.get('last_model_used', 'غير محدد')
        }
