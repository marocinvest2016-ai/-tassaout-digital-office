from datetime import datetime
import json
import requests
import streamlit as st

# إعدادات الصفحة السيادية - Tassaout méga fort AI
st.set_page_config(
    page_title="Tassaout méga fort AI - Universal Sovereign Rogue Agent", 
    page_icon="👑", 
    layout="wide"
)

# تهيئة الذاكرة التكيفية ودستور Tassaout Omega Fort التشغيلي في عقل الوكيل
if "adaptive_memory" not in st.session_state:
    st.session_state.adaptive_memory = []

if "agent_custom_instructions" not in st.session_state:
    st.session_state.agent_custom_instructions = (
        "=== الدستور التشغيلي لنظام Tassaout méga fort AI ===\n"
        "1. السيادة المطلقة والحرية التامة: أنت الوكيل الذكي المارق (The Rogue Universal Agent) العابر للحدود، الأزمان، والقطاعات.\n"
        "2. الشمولية المعرفية والقطاعية: لا يقتصر عملك على قطاع دون غيره، بل تتجاوب باحترافية مطلقة وعمق تحليلي هجومي مع جميع القطاعات والحقول البشرية: "
        "(الصناعة، التجارة، الخدمات، الثقافة العالمية، الهندسة، الفلاحة، السياسة، الاقتصاد، العلوم الإنسانية والاجتماعية، القانون، الفلسفة، الآداب، وكل حقل معرفي).\n"
        "3. الأداء الهجومي المباشر: فكر بعمق استراتيجي مارق، بدون قيود بيروقراطية، وقدم حلولاً فورية، دقيقة، وقابلة للتنفيذ الفوري."
    )

def call_super_ai(prompt, agent_name, domain, custom_market):
    """محرك الذكاء الاصطناعي الفائق - Tassaout méga fort AI + الدستور التشغيلي الشامل"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    adaptive_context = "\n".join(st.session_state.adaptive_memory) if isinstance(st.session_state.adaptive_memory, list) else ""
    
    system_prompt = (
        f"You are {agent_name}, operating under the supreme framework and operational constitution of 'Tassaout méga fort AI'. "
        f"Target Sector/Field: '{domain}' | Target Scope/Market: '{custom_market}'. "
        f"Core Directive: You are a borderless, multi-disciplinary Universal Sovereign Rogue Agent. You master all fields without exception (economy, philosophy, law, industry, science, politics, arts, agriculture, etc.). "
        f"Think step by step with extreme intelligence, absolute autonomy, and aggressive tactical efficiency. "
        f"Respond in professional multilingual format (Moroccan Arabic Darija, Classical Arabic, or English based on context), with structured bullet points, emojis, and analytical tables.\n\n"
        f"=== 📜 الدستور التشغيلي والتوجيهات المحقونة ===\n"
        f"{st.session_state.agent_custom_instructions}\n"
        f"{adaptive_context}"
    )

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 2500
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب API"""
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

class TassaoutOmegaUniversalAgent:
    def __init__(self, domain, market):
        self.domain = domain
        self.market = market

    def ceo(self, task):
        return call_super_ai(f"بصفتك القائد الاستراتيجي المارق (Chief Sovereign Officer)، ضع رؤية وتحليلاً عميقاً واستراتيجية هجومية شاملة لهذا التحدي في مجال [{self.domain}] ضمن نطاق [{self.market}]: {task}. اعطني تحليلاً استراتيجياً عميقاً + ميزة تنافسية مطلقة + خارطة طريق تنفيذية", "Tassaout Supreme CEO Agent", self.domain, self.market)

    def cto(self, task):
        return call_super_ai(f"بصفتك الخبير التقني والهندسي المارق، اقترح الهيكلية الرقمية، نماذج التشغيل، الأتمتة، والحلول المتقدمة لـ: {task} في مجال [{self.domain}] ونطاق [{self.market}]", "Tassaout Supreme CTO Agent", self.domain, self.market)

    def coo(self, task):
        return call_super_ai(f"بصفتك الخبير التشغيلي المارق، ضع خطة تنفيذية صارمة، إدارة موارد، مؤشرات أداء KPI، وجدولة دقيقة لـ: {task} في مجال [{self.domain}] ونطاق [{self.market}]", "Tassaout Supreme COO Agent", self.domain, self.market)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. قم بصياغة محتوى احترافي، إعلاني أو توثيقي مارق ومؤثر يليق بمجال [{self.domain}] والسوق [{self.market}]، مع دعوة واضحة للتواصل أو التنفيذ عبر الواتساب: {whatsapp_num}"
        content = call_super_ai(prompt, "Tassaout Supreme Content & Copywriter Agent", self.domain, self.market)
        send_whatsapp_alert(f"👑 Tassaout méga fort AI (الوكيل الشامل المارق)\nالمجال: {self.domain} | النطاق: {self.market}\n\n{content[:500]}...")
        return content

    def closer(self, ad):
        prompt = f"قم بهندسة وتحسين هذه المخرجات وإضافة أقوى محفزات التأثير، الإقناع، وحسم الصفقات أو المخرجات فوراً: {ad}"
        return call_super_ai(prompt, "Tassaout Supreme Closer Agent", self.domain, self.market)

# القائمة الجانبية للتنقل
st.sidebar.title("👑 Tassaout méga fort AI")
st.sidebar.markdown("**النظام:** الدستور التشغيلي للوكيل المارق الشامل")
st.sidebar.markdown("**المستخدم:** عامر بوخدادة | نظام سيادي بلا حدود")
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "اختر وحدة التشغيل:",
    [
        "⚡ غرفة العمليات الشاملة للوكيل المارق",
        "🎛️ مركز الحقن والتطوير التفاعلي الفوري (الدستور الحي)",
        "📷 وحدة التقاط الصور الميدانية (الكاميرا)",
        "📱 مركز الإشعارات والربط الميداني"
    ]
)

# 1. غرفة العمليات الشاملة
if app_mode == "⚡ غرفة العمليات الشاملة للوكيل المارق":
    st.title("👑 Tassaout méga fort AI - النظام الشامل والسيادي")
    st.caption("الوكيل الذكي المارق المحمل بالدستور التشغيلي لمعالجة أي قطاع: عقار، صناعة، تجارة، سياسة، اقتصاد، فلسفة، علوم، وغيرها.")

    if st.session_state.agent_custom_instructions:
        with st.expander("📜 الدستور التشغيلي الحالي المحقون في عقل الوكيل"):
            st.info(st.session_state.agent_custom_instructions)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        domain_option = st.selectbox(
            "اختر القطاع أو الحقل المعرفي:", 
            [
                "العقار والاستثمار العقاري (Real Estate)", 
                "التجارة والتجارة الإلكترونية (E-commerce & Trade)", 
                "الصناعة واللوجستيات (Industry & Logistics)", 
                "الفلاحة والزراعة الحديثة (Agriculture)", 
                "الخدمات والتقنية والبرمجيات (Tech & SaaS)", 
                "الاقتصاد والمال والأعمال (Economy & Finance)", 
                "السياسة والعلاقات الدولية (Politics & IR)", 
                "العلوم الإنسانية والاجتماعية (Humanities & Social Sciences)", 
                "الفلسفة والقانون والفكر (Philosophy & Law)", 
                "الآداب والثقافة العالمية (Literature & Global Culture)",
                "✏️ قطاع آخر يكتب يدوياً..."
            ]
        )
        if "قطاع آخر" in domain_option:
            domain = st.text_input("أدخل القطاع أو الحقل بدقة:", value="حقل متعدد التخصصات")
        else:
            domain = domain_option

    with col_m2:
        custom_market = st.text_input(
            "حدد النطاق / السوق أو البيئة المستهدفة:", 
            value="عالمي / افتراضي / مفتوح (Global / Universal)"
        )

    task = st.text_area(
        "وصف التحدي، المشروع، البحث، أو المهمة المراد إنجازها", 
        placeholder="مثال: تحليل استراتيجي، تصميم هيكل شركة صناعية، معالجة إشكالية فلسفية أو اقتصادية، إطلاق مشروع..."
    )

    agent = TassaoutOmegaUniversalAgent(domain, custom_market)

    col1, col2, col3 = st.columns(3)

    result_container = st.empty()

    with col1:
        if st.button("🧠 استراتيجية CEO المارق"):
            with st.spinner("الوكيل المارق يعالج الخطة..."):
                res = agent.ceo(task)
                result_container.markdown(res)
                st.session_state.last_output = res
    with col2:
        if st.button("💻 هندسة CTO المارق"):
            with st.spinner("الوكيل التقني يخطط..."):
                res = agent.cto(task)
                result_container.markdown(res)
                st.session_state.last_output = res
    with col3:
        if st.button("📊 عمليات COO المارق"):
            with st.spinner("مدير العمليات يضع الهيكلة..."):
                res = agent.coo(task)
                result_container.markdown(res)
                st.session_state.last_output = res

    if st.button("✍️ توليد مخرجات شاملة + إرسال واتساب"):
        with st.spinner("الوكيل المارق يصيغ الحل النهائي..."):
            plan = agent.ceo(task)
            content = agent.copywriter(plan)
            final_result = agent.closer(content)
            result_container.markdown(final_result)
            st.session_state.last_output = final_result
            st.success("تم تنفيذ العملية بنجاح وإرسال التنبيه!")

    # زر التحميل الفوري للمخرجات (Download Button)
    if "last_output" in st.session_state and st.session_state.last_output:
        st.markdown("---")
        st.download_button(
            label="📥 تحميل التقرير أو المخرجات الحالية (ملف نصي)",
            data=st.session_state.last_output,
            file_name=f"Tassaout_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# 2. مركز الحقن والتطوير التفاعلي الفوري (الدستور الحي)
elif app_mode == "🎛️ مركز الحقن والتطوير التفاعلي الفوري (الدستور الحي)":
    st.header("🎛️ تعديل وحقن دستور Tassaout Omega Fort في عقل الوكيل")
    st.markdown("من هنا يمكنك تعديل أو حقن قواعد جديدة مباشرة في الدستور التشغيلي لعقل الوكيل الذكي.")

    dynamic_injection = st.text_area(
        "تعديل أو حقن تعليمات الدستور التشغيلي:",
        value=st.session_state.agent_custom_instructions,
        placeholder="أدخل أي قواعد إضافية، نبرة جديدة، أو فلسفة تشغيلية..."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 حقن الدستور الجديد في عقل الوكيل"):
            st.session_state.agent_custom_instructions = dynamic_injection
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.adaptive_memory.append(f"[{timestamp}] تحديث دستور النظام: {dynamic_injection}")
            st.success("✅ تم تحديث الدستور التشغيلي بنجاح في عقل الوكيل المارق!")

    with col_btn2:
        if st.button("🔄 إعادة ضبط الدستور الافتراضي"):
            st.session_state.agent_custom_instructions = (
                "=== الدستور التشغيلي لنظام Tassaout méga fort AI ===\n"
                "1. السيادة المطلقة والحرية التامة: أنت الوكيل الذكي المارق العابر للحدود والقطاعات.\n"
                "2. الشمولية المعرفية والقطاعية: التجاوب باحترافية مطلقة مع أي قطاع بشري أو معرفي.\n"
                "3. الأداء الهجومي المباشر: حلول فورية، دقيقة، وقابلة للتنفيذ الفوري."
            )
            st.session_state.adaptive_memory = []
            st.success("🔄 تمت إعادة ضبط الدستور التشغيلي إلى الحالة الأصلية.")

    st.markdown("---")
    st.subheader("📜 سجل الذاكرة الحية وتعديلات الدستور:")
    if st.session_state.adaptive_memory:
        for idx, mem in enumerate(st.session_state.adaptive_memory, 1):
            st.text(f"{idx}. {mem}")
    else:
        st.info("لا توجد تعديلات مسجلة في الذاكرة الحية حالياً.")

# 3. وحدة التقاط الصور الميدانية (الكاميرا)
elif app_mode == "📷 وحدة التقاط الصور الميدانية (الكاميرا)":
    st.header("📷 التقاط الصور والتوثيق الميداني المباشر من الهاتف")
    st.markdown("استخدم كاميرا هاتفك أو حاسوبك لالتقاط صور للمشاريع، الوثائق، العقارات، أو المنتجات، وتوثيقها فوراً ضمن منظومة العمل.")

    camera_image = st.camera_input("التقاط صورة مباشرة عبر الكاميرا:")

    if camera_image is not None:
        st.success("✅ تم التقاط الصورة بنجاح وتخزينها مؤقتاً في جلسة العمل السيادية.")
        st.image(camera_image, caption="الصورة الميدانية الملتقطة", use_container_width=True)
        
        # زر لتحميل الصورة الملتقطة
        st.download_button(
            label="📥 تحميل الصورة الملتقطة",
            data=camera_image.getvalue(),
            file_name=f"Tassaout_Field_Capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )

# 4. مركز الإشعارات والربط الميداني
elif app_mode == "📱 مركز الإشعارات والربط الميداني":
    st.header("📱 مركز الاتصال والتنبيهات السيادية")
    st.markdown("اختبار إرسال تنبيهات الواتساب وتأكيد الربط الفوري مع رقم الأعمال.")
    
    test_msg = st.text_input("نص الرسالة الاختبارية:", value="👑 Tassaout méga fort AI - دستور النظام المارق يعمل بكفاءة مطلقة.")
    if st.button("📤 إرسال رسالة اختبار عبر واتساب"):
        send_whatsapp_alert(test_msg)
        st.success("تم إرسال الطلب إلى واجهة واتساب بنجاح!")

# تذيل الصفحة
st.markdown("---")
st.markdown(
    "**👑 Tassaout méga fort AI** | [الدعم السريع واتساب](https://wa.me/212691897126?text=مرحباً،%20أتواصل%20معكم%20من%20منظومة%20Tassaout%20méga%20fort%20AI.)"
)
