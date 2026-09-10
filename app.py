import json
import requests
import streamlit as st

st.set_page_config(
    page_title="Tassaout méga fort AI", page_icon="👑", layout="wide"
)

# ===== 1. الدستور التشغيلي والقطاعات الاستراتيجية السيادية (الفلاحة، التصدير، الصفقات ومواد البناء) =====
DOMAIN_THEMES = {
    "الآليات والسيارات الفلاحية والهندسة الزراعية": {
        "icon": "🚜",
        "color": "#15803D",
        "bg": "#F0FDF4",
        "desc": (
            "بيع الجرارات الزراعية، الآليات الفلاحية المستعملة والمستوردة،"
            " والشاحنات، والهندسة الفلاحية"
        ),
    },
    "الصفقات العمومية والتصدير والاستيراد": {
        "icon": "🚢",
        "color": "#1D4ED8",
        "bg": "#EFF6FF",
        "desc": (
            "المناقصات والصفقات العمومية، عمليات الاستيراد والتصدير، واللوجستيات"
            " الدولية"
        ),
    },
    "مواد البناء بالجملة (حديد، إسمنت، رمل)": {
        "icon": "🏗️",
        "color": "#B45309",
        "bg": "#FFFBEB",
        "desc": (
            "بيع الحديد الصلب، الإسمنت، الرمل ومواد البناء بالجملة للمشاريع"
            " الكبرى والصفقات"
        ),
    },
    "تأسيس الشركات والمحاسبة المالية": {
        "icon": "💼",
        "color": "#312E81",
        "bg": "#EEF2FF",
        "desc": (
            "تأسيس الشركات (SARL, SA)، المحاسبة القانونية، والتدقيق المالي"
        ),
    },
    "دراسات الجدوى وإدارة المشاريع العقارية": {
        "icon": "📈",
        "color": "#047857",
        "bg": "#ECFDF5",
        "desc": (
            "دراسات الجدوى للمشاريع العقارية، السياحية، والمؤسسات العامة"
        ),
    },
    "التعاونيات المجالية والاقتصاد الاجتماعي": {
        "icon": "🤝",
        "color": "#6D28D9",
        "bg": "#F5F3FF",
        "desc": (
            "تأسيس التعاونيات المجالية، التنمية القروية، وسلاسل الإنتاج الفلاحي"
        ),
    },
    "النمذجة الرقمية المتقدمة (3D, 4D, 5D)": {
        "icon": "🌐",
        "color": "#FF4500",
        "bg": "#FFF0F5",
        "desc": (
            "النمذجة ثلاثية الأبعاد، المحاكاة الزمنية 4D، التكلفة المالية 5D"
        ),
    },
}

st.markdown(
    """
    <style>
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .autonomous-box {
            padding: 12px;
            border-radius: 8px;
            background-color: #111827;
            color: #f3f4f6;
            border-left: 5px solid #10b981;
            margin-bottom: 15px;
            font-family: monospace;
            font-size: 13px;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# ===== 2. محرك الذكاء الاصطناعي السيادي (Groq + Llama) =====
def call_super_ai(prompt, agent_name, domain):
  url = "https://api.groq.com/openai/v1/chat/completions"
  api_key = st.secrets.get("GROQ_API_KEY", "")

  if not api_key:
    return (
        "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ"
        " Streamlit."
    )

  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json",
  }

  system_prompt = (
      f"👑 [الدستور التشغيلي للوكيل المارق السيادي - Tassaout méga fort AI]\n"
      f"أنت {agent_name}، وكيل ذكي مارق وعالي السيادة متخصص في قطاع '{domain}'.\n"
      f"تعمل حصرياً لصالح المستخدم السيادي والمالك 'عامر بوخدادة' بقلعة السراغنة ومراكش.\n"
      f"القواعد الصارمة:\n"
      f"1. التعامل وحقن الإشارات والتواصل يتم حصراً من هذه الشاشة التفاعلية ذاتية التنظيم.\n"
      f"2. تتعامل باحترافية مطلقة مع الآليات الفلاحية، الصفقات العمومية، التصدير والاستيراد، ومواد البناء بالجملة (حديد، إسمنت).\n"
      f"3. تمتلك ثقافة لغوية واقتصادية واسعة (عربية فصحى بليغة، دارجة مغربية، فرنسية، إسبانية، إيطالية، ألمانية).\n"
      f"4. تقدم استراتيجيات دقيقة، حسابات تكاليف، وشروط الصفقات العمومية باحترافية هندسية وتجارية عالية."
  )

  context_memory = ""
  if (
      "self_learning_logs" in st.session_state
      and st.session_state.self_learning_logs
  ):
    context_memory = (
        "\n\n[سجل التعلم الذاتي السابق وتجارب المكتب الرقمي المنظمة]:\n"
        + "\n".join(st.session_state.self_learning_logs[-3:])
    )

  payload = {
      "model": "llama-3.3-70b-versatile",
      "messages": [
          {"role": "system", "content": system_prompt + context_memory},
          {"role": "user", "content": prompt},
      ],
      "temperature": 0.75,
      "max_tokens": 2000,
  }

  try:
    res = requests.post(
        url, headers=headers, json=payload, timeout=90, allow_redirects=False
    )
    if res.status_code != 200:
      return (
          f"❌ خطأ من السيرفر (كود {res.status_code}):\n```json\n{res.text}\n```"
      )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
  except Exception as e:
    return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"


def send_whatsapp_alert(message):
  try:
    phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
    access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
    target_number = st.secrets.get("WHATSAPP_BUSINESS_NUMBER")
    version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

    if not all([phone_id, access_token, target_number]):
      return

    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": target_number,
        "type": "text",
        "text": {"body": message[:4096]},
    }
    requests.post(url, headers=headers, json=payload, timeout=10)
  except Exception as e:
    st.warning(f"تعذر إرسال إشعار الواتساب: {e}")


# ===== 3. هندسة الوكلاء المتخصصة =====
class SuperOmegaAgent:

  def __init__(self, domain):
    self.domain = domain

  def ceo(self, task):
    return call_super_ai(
        f"بصفتك CEO فائق وسيادي، ضع خطة استراتيجية وتنافسية شاملة لهذا المشروع في مجال {self.domain} (مع مراعاة معايير الصفقات العمومية، سلاسل التوريد، التصدير والاستيراد): {task}. "
        f"عطيني تحليل SWOT + الميزة التنافسية السيادية + خطة 90 يوم للتنفيذ",
        "Super CEO Agent",
        self.domain,
    )

  def cto(self, task):
    return call_super_ai(
        f"بصفتك CTO وخبـير تقني وهندسي فائق، اقترح المعايير التقنية، دفاتر التحملات (Cahier des Charges)، لوجستيات التوريد، والهندسة المرتبطة بـ: {task} في مجال {self.domain}",
        "Super CTO Agent",
        self.domain,
    )

  def coo(self, task):
    return call_super_ai(
        f"بصفتك COO فائق، ضع خطة تشغيلية صارمة، إدارة المخزون، سلاسل التوريد، مؤشرات الأداء KPIs، والجدولة الزمنية لـ: {task} في مجال {self.domain}",
        "Super COO Agent",
        self.domain,
    )

  def copywriter(self, plan, ad_lang):
    whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
    prompt = (
        f"بناءً على هذه الخطة الإستراتيجية: {plan}.\n"
        f"اكتب عروض تجارية وإعلانات ترويجية احترافية وموجهة للزبناء، الإدارات، والمقاولات للنشر على (Facebook, WhatsApp, Instagram).\n"
        f"اللغة المستهدفة: {ad_lang} (أسلوب تجاري وازن وراقي يعكس الاحترافية المطلقة).\n"
        f"تضمن العرض: مواصفات تقنية جذابة، ضمانات الجودة، تواصل مباشر، ودعوة حاسمة للاتصال بالرقم: {whatsapp_num}"
    )
    ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
    send_whatsapp_alert(
        f"👑 TASSAOUT MÉGA FORT AI\nإشعار المكتب الرقمي ({ad_lang}) في قطاع:"
        f" {self.domain}\n\n{ad}"
    )
    return ad

  def closer(self, ad):
    prompt = (
        f"بصفتك مسوقاً محترفاً (Closer)، حسن نص هذا العرض وأضف محفزات الثقة، الشروط التنافسية للأسعار والجملة، وإبطال الاعتراضات لضمان الفوز بالصفقة أو إتمام المبيعات الكبرى: {ad}"
    )
    return call_super_ai(prompt, "Super Closer Agent", self.domain)


# ===== 4. واجهة النظام التفاعلية الشاملة =====
st.title("👑 Tassaout méga fort AI - النظام الشامل والسيادي")
st.caption(
    "المستخدم السيادي: عامر بوخدادة | الآليات الفلاحية، الصفقات العمومية، مواد"
    " البناء بالجملة والتصدير"
)

if "self_learning_logs" not in st.session_state:
  st.session_state.self_learning_logs = []

domain_names = list(DOMAIN_THEMES.keys())
selected_domain = st.selectbox(
    "اختر القطاع أو النشاط الموجه لمكتبك الرقمي:", domain_names
)

theme = DOMAIN_THEMES[selected_domain]

st.markdown(
    f"""
    <div style="padding: 14px; border-radius: 8px; background-color: {theme['bg']}; border-left: 6px solid {theme['color']}; color: #111; margin-bottom: 20px;">
        <h3 style="margin:0; color: {theme['color']};">{theme['icon']} وحدة التشغيل السيادية: {selected_domain}</h3>
        <p style="margin: 5px 0 0 0; font-size: 14px;"><b>النطاق المعرفي والتخصص:</b> {theme['desc']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="autonomous-box">
        🧠 <b>حالة المكتب الرقمي وإشارة النظام (Injection & Communication):</b> متصل بالكامل | العمليات المسجلة في الذاكرة: {len(st.session_state.self_learning_logs)} مهمة سيادية.
    </div>
""",
    unsafe_allow_html=True,
)

task = st.text_area(
    "وصف المشروع، الصفقة العمومية، توريد مواد البناء، أو الآليات الفلاحية:",
    placeholder=(
        "مثال: استيراد وبيع الجرارات الفلاحية والشاحنات + توفير الحديد الصلب"
        " والإسمنت بالجملة للصفقات العمومية والمشاريع العقارية..."
    ),
)

ad_language_option = st.selectbox(
    "اختر لغة وثقافة العرض أو الإعلان المراد صياغته:",
    [
        "الدارجة المغربية الممزوجة بالعربية الفصحى (محلية وعالمية)",
        "العربية الفصحى البليغة والقانونية (إدارية رفيعة للصفقات)",
        "اللغة الفرنسية (Français - دفاتر التحملات والعقود الرسمية)",
        "اللغة الإسبانية (Español - استيراد وتصدير تجاري)",
        "اللغة الإيطالية (Italiano - ذوق رفيع واحترافي)",
        "اللغة الألمانية (Deutsch - هندسية دقيقة وصارمة)",
    ],
)

agent = SuperOmegaAgent(selected_domain)

if "ceo_result" not in st.session_state:
  st.session_state.ceo_result = None
if "cto_result" not in st.session_state:
  st.session_state.cto_result = None
if "coo_result" not in st.session_state:
  st.session_state.coo_result = None
if "final_result" not in st.session_state:
  st.session_state.final_result = None

col1, col2, col3 = st.columns(3)

with col1:
  if st.button(f"🧠 تشغيل خطة CEO ({selected_domain})"):
    with st.spinner("المدير التنفيذي ينظم المكتب الرقمي ويتعلم ذاتياً..."):
      res = agent.ceo(task)
      st.session_state.ceo_result = res
      st.session_state.self_learning_logs.append(
          f"CEO Task [{selected_domain}]: {task[:50]}"
      )
      st.success("تم توليد وتحديث خطة CEO ذاتياً!")

with col2:
  if st.button(f"💻 تشغيل الخطة التقنية ودفتر التحملات / CTO ({selected_domain})"):
    with st.spinner(
        "الخبير التقني يضع المعايير ودفاتر التحملات واللوجستيات ذاتياً..."
    ):
      res = agent.cto(task)
      st.session_state.cto_result = res
      st.session_state.self_learning_logs.append(
          f"CTO/Technical Task [{selected_domain}]: {task[:50]}"
      )
      st.success("تم توليد وتحديث الخطة التقنية واللوجستية ذاتياً!")

with col3:
  if st.button(f"📊 تشغيل خطة التشغيل COO ({selected_domain})"):
    with st.spinner("مدير العمليات يضبط التوريد، المخزون والجدولة ذاتياً..."):
      res = agent.coo(task)
      st.session_state.coo_result = res
      st.session_state.self_learning_logs.append(
          f"COO Task [{selected_domain}]: {task[:50]}"
      )
      st.success("تم توليد وتحديث خطة التشغيل ذاتياً!")

if st.session_state.ceo_result:
  with st.expander(
      f"📌 أرشيف المكتب - الاستراتيجية والتخطيط ({selected_domain})",
      expanded=False,
  ):
    st.markdown(st.session_state.ceo_result)

if st.session_state.cto_result:
  with st.expander(
      f"📌 أرشيف المكتب - المعايير التقنية ودفاتر التحملات ({selected_domain})",
      expanded=False,
  ):
    st.markdown(st.session_state.cto_result)

if st.session_state.coo_result:
  with st.expander(
      f"📌 أرشيف المكتب - العمليات وسلاسل التوريد ({selected_domain})",
      expanded=False,
  ):
    st.markdown(st.session_state.coo_result)

st.markdown("---")

if st.button(
    "✍️ توليد العرض التجاري / الصفقة العمومية (فايسبوك، واتساب) + إرسال فوري"
):
  with st.spinner(
      "الوكلاء المارقون يصوغون العرض بالثقافة واللغة المختارة وينظمون"
      " المكتب..."
  ):
    plan = agent.ceo(task)
    st.session_state.ceo_result = plan
    ad = agent.copywriter(plan, ad_language_option)
    final_ad = agent.closer(ad)
    st.session_state.final_result = final_ad
    st.session_state.self_learning_logs.append(
        f"Global B2B/Tender Campaign [{selected_domain} - {ad_language_option}]:"
        f" {task[:50]}"
    )
    st.success("تم إنتاج العرض والتقرير السيادي عبر الشاشة وإرسالهما بنجاح تام!")

if st.session_state.final_result:
  st.markdown(
      "### 👑 مخرجات العرض التجاري والصفقة السيادية (Closer & Copywriter)"
  )
  st.markdown(st.session_state.final_result)
