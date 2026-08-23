import streamlit as st
from google import genai
import requests
import datetime

# ===============================
# 1. إعدادات السيادة المطلقة
# ===============================
GEMINI_API_KEY = st.secrets["gemini"]["API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

ALPHACLOUD_URL = "https://api.alphacloud.tassout.ai/upload"
API_KEY = "SIGNATURE_AMEUR_KEY_OMEGA"

WA_PHONE_ID = st.secrets["whatsapp"]["PHONE_NUMBER_ID"]
WA_TOKEN = st.secrets["whatsapp"]["ACCESS_TOKEN"]
WA_VERSION = st.secrets["whatsapp"]["API_VERSION"]

# ===============================
# 2. منظومة الوكلاء الفائقين (SUPER AGENTS - IMPERIAL v6.0)
# ===============================
class TassaoutGlobalEmpire:
    def __init__(self):
        print("[OMEGA-CORE v6.0] نظام السيادة الرقمية العالمي والشامل متصل ومفعل 100%")

    # القطب 1: العقارات الاستثمارية والفخمة
    def agent_real_estate(self, query: str) -> str:
        prompt = f"أنت وكيل العقارات الاستثمارية والفخمة في منصة Tassaout Omega. أجب باحترافية بالدارجة أو اللغة المناسبة. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"🏡 [القطب العقاري]: {res.text}"

    # القطب 2: التجارة، الأعمال، الهويات البصرية والتسويق
    def agent_commercial(self, query: str) -> str:
        prompt = f"أنت وكيل التجارة، الأعمال، والهويات البصرية (Sraghna Media / DANA Market). أجب باحترافية. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"💼 [القطب التجاري الرقمي]: {res.text}"

    # القطب 3: الأسفار، السياحة، والحج والعمرة
    def agent_travel(self, query: str) -> str:
        prompt = f"أنت وكيل الأسفار، السياحة، والحج والعمرة الدولي. أجب باحترافية. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"✈️ [قطب الأسفار والحج والعمرة]: {res.text}"

    # القطب 4: السيارات والآليات الفلاحية والثقيلة
    def agent_auto_machinery(self, query: str) -> str:
        prompt = f"أنت وكيل السيارات الفاخرة، كراء السيارات، والآليات الفلاحية والمعدات الثقيلة. أجب باحترافية. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"🚗🚜 [قطب السيارات والآليات]: {res.text}"

    # القطب 5: الصفقات العمومية ومواد البناء والتجهيز
    def agent_public_tenders_construction(self, query: str) -> str:
        prompt = f"أنت وكيل الصفقات العمومية، طلبات العروض، ومواد البناء والتجهيز الصناعي والمقاولاتي. أجب باحترافية ودقة تقنية. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"🏗️ [قطب الصفقات العمومية ومواد البناء]: {res.text}"

    # القطب 6: الهندسة المعمارية والصناعية والميكانيكية للمعامل والديكور
    def agent_engineering_decor(self, query: str) -> str:
        prompt = f"أنت خبير الهندسة المعمارية، الهندسة الصناعية والميكانيكية للمعامل والشركات، وهندسة الديكور الداخلي الفاخر. أجب باحترافية عالية. الطلب: {query}"
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return f"📐 [قطب الهندسة الصناعية والديكور]: {res.text}"

    # الموجه المركزي الأذكى (DANA CEO Router)
    def dana_ceo_router(self, user_query: str, domain: str, to_number: str = None) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stamp = "APPROUVÉ PAR AMEUR © 2026 - Tassaout Vision Verified"

        # توجيه الطلب حسب القطب المختار في الواجهة
        if domain == "عقارات":
            result = self.agent_real_estate(user_query)
        elif domain == "تجارة وأعمال":
            result = self.agent_commercial(user_query)
        elif domain == "أسفار وحج وعمرة":
            result = self.agent_travel(user_query)
        elif domain == "سيارات وآليات فلاحية":
            result = self.agent_auto_machinery(user_query)
        elif domain == "الصفقات العمومية ومواد البناء":
            result = self.agent_public_tenders_construction(user_query)
        elif domain == "الهندسة المعمارية والديكور":
            result = self.agent_engineering_decor(user_query)
        else:
            # التوجيه التلقائي الذكي عبر الـ Router
            router_prompt = f"حدد أي قطب يناسب هذا الطلب بدقة (عقارات / تجارة وأعمال / أسفار وحج وعمرة / سيارات وآليات فلاحية / الصفقات العمومية ومواد البناء / الهندسة المعمارية والديكور): {user_query}"
            routing_res = client.models.generate_content(model="gemini-2.5-flash", contents=router_prompt)
            result = f"🌐 [DANA CEO Router]: تم التوجيه بنجاح. تحليل النظام: {routing_res.text}"

        final_output = f"{result}\n\n--- \n📌 ختم السيادة: {stamp} | الوقت: {timestamp}"
        
        # إرسال عبر الواتساب تلقائياً إذا توفر الرقم
        if to_number:
            self.send_whatsapp_broadcast(to_number, final_output)

        return final_output

    def send_whatsapp_broadcast(self, to_number: str, message: str):
        url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message}
        }
        return requests.post(url, headers=headers, json=data).json()

# تشغيل النظام الإمبراطوري الشامل
empire = TassaoutGlobalEmpire()

def dana_whatsapp_agent(user_question: str, domain: str = "عام", to_number: str = "") -> str:
    """الواجهة الموحدة للوكيل الإمبراطوري الشامل DANA"""
    try:
        return empire.dana_ceo_router(user_question, domain, to_number)
    except Exception as e:
        return f"عندي مشكل تقني طارئ في النظام الإمبراطوري. الخطأ: {e}"

def send_whatsapp_message(to_number, message):
    """إرسال رسالة مباشرة عبر WhatsApp API"""
    return empire.send_whatsapp_broadcast(to_number, message)
