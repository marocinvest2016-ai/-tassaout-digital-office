from datetime import datetime
import json
import requests
import streamlit as st

# إعدادات الصفحة السيادية - Tassaout méga fort AI
st.set_page_config(
    page_title="Tassaout méga fort AI - Global Rogue Agent", 
    page_icon="👑", 
    layout="wide"
)

# تهيئة الذاكرة التكيفية وحقن التعليمات الحرة في الجلسة
if "adaptive_memory" not in st.session_state:
    st.session_state.adaptive_memory = []

if "agent_custom_instructions" not in st.session_state:
    st.session_state.agent_custom_instructions = (
        "أنت الوكيل الذكي المارق التابع لمنظومة 'Tassaout méga fort AI'. "
        "نظام رقمي سيادي عابر للحدود والبلدان (لا يحده زمان ولا مكان). "
        "قادر على التجاوب باحترافية مطلقة مع قطاع العقار أو أي قطاع تجاري/رقمي في أي سوق عالمي أو محلي، "
        "مع تقديم استراتيجيات جريئة، هجومية، وفورية."
    )

def call_super_ai(prompt, agent_name, domain, custom_market):
    """محرك الذكاء الاصطناعي الفائق - Tassaout méga fort AI + النطاق العالمي المارق"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # دمج التعليمات المحقونة من الشاشة التفاعلية مع النطاق العالمي
    adaptive_context = "\n".json(st.session_state.adaptive_memory) if isinstance(st.session_state.adaptive_memory, list) else ""
    
    system_prompt = (
        f"You are {agent_name}, operating under the global elite framework of 'Tassaout méga fort AI' as a Sovereign Rogue Agent. "
        f"Target Domain: '{domain}' | Target Market/Geography: '{custom_market}'. "
        f"Remember: You are a borderless digital system, operating globally without limits of time or space. "
        f"Think step by step with extreme intelligence, absolute autonomy, and aggressive efficiency. "
        f"Respond in professional multilingual format (Moroccan Arabic Darija, Classical Arabic, or English based on context), with bullet points, emojis, and actionable tables.\n\n"
        f"=== ⚡ التوجيهات والسلوكيات المحقونة تفاعلياً (الأولوية المطلقة) ===\n"
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
        "max_tokens": 2000
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

class RogueGlobalAgent:
    def __init__(self, domain, market):
        self.domain = domain
        self.market = market

    def ceo(self, task):
        return call_super_ai(f"بصفتك CEO مارق عابر للحدود، ضع خطة استراتيجية عالمية هجومية لهذا المشروع في مجال [{self.domain}] ضمن السوق/المنطقة [{self.market}]: {task}. اعطني SWOT خارق + ميزة تنافسية مدمرة + خطة 90 يوم", "Global Rogue CEO Agent", self.domain, self.market)

    def cto(self, task):
        return call_super_ai(f"بصفتك CTO مارق، اقترح البنية التقنية السحابية، أتمتة العمليات، والاستهداف الرقمي لـ: {task} في مجال [{self.domain}] ونطاق [{self.market}]", "Global Rogue CTO Agent", self.domain, self.market)

    def coo(self, task):
        return call_super_ai(f"بصفتك COO مارق، ضع خطة تشغيلية رقمية سريعة وخالية من البيروقراطية لـ: {task} في مجال [{self.domain}] ونطاق [{self.market}]", "Global Rogue COO Agent", self.domain, self.market)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية عالمية ومارقة باللغة المناسبة للسوق المستهدف [{self.market}] مع محفزات بيع صارخة ودعوة للتواصل عبر الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Global Rogue Copywriter Agent", self.domain, self.market)
        send_whatsapp_alert(f"👑 Tassaout méga fort AI (الوكيل المارق العالمي)\nالمجال: {self.domain} | السوق: {self.market}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بهندسة وتحسين نص هذا الإعلان وإضافة أقوى محفزات الاستعجال FOMO لضمان حسم الصفقات فوراً: {ad}"
        return call_super_ai(prompt, "Global Rogue Closer Agent", self.domain, self.market)

# القائمة الجانبية للتنقل
st.sidebar.title("👑 Tassaout méga fort AI")
st.sidebar.markdown("**النظام:** الوكيل الذكي المارق (عابر للحدود)")
st.sidebar.markdown("**المستخدم:** عامر بوخدادة | نظام رقمي عالمي")
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "اختر وحدة التشغيل:",
    [
        "⚡ غرفة العمليات العالمية للوكيل المارق",
        "🎛️ مركز الحقن والتطوير التفاعلي الفوري",
        "📱 مركز الإشعارات والربط الميداني"
    ]
)

# 1. غرفة العمليات العالمية
if app_mode == "⚡ غرفة العمليات العالمية للوكيل المارق":
    st.title("👑 Tassaout méga fort AI - النظام الرقمي العابر للحدود")
    st.caption("الوكيل الذكي المارق للتجارة، العقار، وكل القطاعات حول العالم - لا يحده زمان ولا مكان.")

    # عرض تذكيري بالتعليمات المحقونة الحالية
    if st.session_state.agent_custom_instructions:
        with st.expander("📌 الهوية والسلوك المارق المحقون حالياً للوكيل"):
            st.info(st.session_state.agent_custom_instructions)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        domain = st.selectbox(
            "اختر القطاع (العقار أو أي قطاع آخر)", 
            ["العقار (Real Estate)", "التجارة الإلكترونية (E-commerce)", "الخدمات الرقمية (Digital Services)", "التقنية والبرمجيات (SaaS)", "الاستثمار المالي", "قطاع آخر يحدد في الوصف"]
        )
    with col_m2:
        custom_market = st.text_input(
            "حدد السوق المستهدف / النطاق الجغرافي أو العالمي:", 
            value="عالمي / أي سوق مطلوب (Global / Any Market)"
        )

    task = st.text_area("وصف المهمة أو التحدي المراد تنفيذه", placeholder="مثال: إطلاق منصة رقمية عقارية أو تسويق مشاريع استثمارية كبرى في دبي، باريس، أو أي مدينة في العالم...")

    agent = RogueGlobalAgent(domain, custom_market)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧠 استراتيجية CEO المارق"):
            with st.spinner("الوكيل المارق يحلل ويهندس الخطة العالمية..."):
                st.markdown(agent.ceo(task))
    with col2:
        if st.button("💻 هندسة CTO المارق"):
            with st.spinner("الوكيل التقني يخطط للبنية..."):
                st.markdown(agent.cto(task))
    with col3:
        if st.button("📊 عمليات COO المارق"):
            with st.spinner("مدير العمليات يضع الجدول التشغيلي..."):
                st.markdown(agent.coo(task))

    if st.button("✍️ إطلاق إعلان مارق عالمي + إرسال واتساب"):
        with st.spinner("كاتب الإعلانات المارق يبتكر الحملة السيادية..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم تنفيذ العملية بنجاح!")
            st.markdown(final_ad)

# 2. مركز الحقن والتطوير التفاعلي الفوري
elif app_mode == "🎛️ مركز الحقن والتطوير التفاعلي الفوري":
    st.header("🎛️ لوحة التحكم وحقن السلوك المارق (Dynamic Rogue Injection)")
    st.markdown("""
    من هذه الشاشة التفاعلية، يمكنك **حقن وتعديل** أي تعليمات، أسلوب، نبرة، أو قواعد جديدة للوكيل المارق فوراً.
    أي نص تدخله هنا سيتم اعتماده **مباشرة** في الذاكرة الحية للوكيل ليقوم بتكييف عمله في جميع القطاعات والأسواق العالمية دون قيود.
    """)

    # خانة الحقن التفاعلي المفتوحة
    dynamic_injection = st.text_area(
        "أدخل المختلفات، التوجيهات أو التعليمات الجديدة لحقنها في الوكيل الذكي:",
        value=st.session_state.agent_custom_instructions,
        placeholder="مثال: تصرف كخبير استثماري عالمي، ركز على الأسواق الدولية، اعتمد لغة قوية ومباشرة..."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 حقن وتطوير أداء الوكيل فوراً"):
            st.session_state.agent_custom_instructions = dynamic_injection
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.adaptive_memory.append(f"[{timestamp}] حقن تفاعلي جديد: {dynamic_injection}")
            st.success("✅ تم حقن التعليمات بنجاح وتطوير أداء الوكيل المارق! توجه لغرفة العمليات لتجربة الأداء الجديد.")

    with col_btn2:
        if st.button("🔄 إعادة ضبط السلوك الافتراضي"):
            st.session_state.agent_custom_instructions = (
                "أنت الوكيل الذكي المارق التابع لمنظومة 'Tassaout méga fort AI'. "
                "نظام رقمي سيادي عابر للحدود والبلدان (لا يحده زمان ولا مكان). "
                "قادر على التجاوب باحترافية مطلقة مع قطاع العقار أو أي قطاع تجاري/رقمي في أي سوق عالمي أو محلي."
            )
            st.session_state.adaptive_memory = []
            st.success("🔄 تمت إعادة ضبط إعدادات وسلوك الوكيل إلى الوضع الافتراضي.")

    st.markdown("---")
    st.subheader("📜 سجل الذاكرة الحية والتعديلات المكتسبة:")
    if st.session_state.adaptive_memory:
        for idx, mem in enumerate(st.session_state.adaptive_memory, 1):
            st.text(f"{idx}. {mem}")
    else:
        st.info("لا توجد تعديلات مسجلة في الذاكرة الحية حالياً.")

# 3. مركز الإشعارات والربط الميداني
elif app_mode == "📱 مركز الإشعارات والربط الميداني":
    st.header("📱 مركز الاتصال والتنبيهات السيادية")
    st.markdown("اختبار إرسال تنبيهات الواتساب وتأكيد الربط الفوري مع رقم الأعمال.")
    
    test_msg = st.text_input("نص الرسالة الاختبارية:", value="👑 Tassaout méga fort AI - اختبار النظام المارق العالمي ناجح.")
    if st.button("📤 إرسال رسالة اختبار عبر واتساب"):
        send_whatsapp_alert(test_msg)
        st.success("تم إرسال الطلب إلى واجهة واتساب بنجاح!")

# تذيل الصفحة
st.markdown("---")
st.markdown(
    "**👑 Tassaout méga fort AI** | [الدعم السريع واتساب](https://wa.me/212691897126?text=مرحباً،%20أتواصل%20معكم%20من%20منظومة%20Tassaout%20méga%20fort%20AI.)"
)
