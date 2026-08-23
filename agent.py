import streamlit as st
from google import genai
import requests
import datetime

# ===============================
# 1. إعدادات السيادة TASSAOUT
# ===============================
GEMINI_API_KEY = st.secrets["gemini"]["API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

ALPHACLOUD_URL = "https://api.alphacloud.tassout.ai/upload"
API_KEY = "SIGNATURE_AMEUR_KEY_OMEGA"

WA_PHONE_ID = st.secrets["whatsapp"]["PHONE_NUMBER_ID"]
WA_TOKEN = st.secrets["whatsapp"]["ACCESS_TOKEN"]
WA_VERSION = st.secrets["whatsapp"]["API_VERSION"]

# ===============================
# 2. DANA - ALPHA NEXUS OMEGA
# ===============================
class DANA_Agent:
    def __init__(self):
        self.modes = {
            "PRODUIT": {"engine": "FLUX.1-Pro-Ultra", "lens": "85mm"},
            "PORTRAIT": {"engine": "Hasselblad-X2D", "lens": "50mm"},
            "MAGASIN": {"engine": "Imagen-4", "lens": "24mm"},
            "VOITURE": {"engine": "Midjourney-v7", "lens": "70-200mm"},
            "CINEMA": {"engine": "ARRI-Alexa", "lens": "35mm"}
        }

    def AGENT_01_analyze(self, frame_b64, mode):
        return f"Scene: {mode} | Tassaout Vision Verified"

    def AGENT_03_digital_studio(self, prompt: str) -> str:
        result = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=f"Professional photo Morocco, {prompt}, 8K, cinematic, {self.modes['MAGASIN']['engine']}"
        )
        image_bytes = result.generated_images[0].image.image_bytes
        return self.AGENT_06_upload_to_cloud(image_bytes, "GENERATED")

    def AGENT_04_stamp(self, filename):
        return f"{filename}_APPROUVE_PAR_AMEUR.jpg"

    def AGENT_08_generate_ad(self, analysis, location):
        return f"خدمة احترافية | {location} | من توقيع Signature ameur | Tassaout Vision Verified © 2026"

    def AGENT_06_upload_to_cloud(self, file_bytes, subject):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DANA_{subject}_{timestamp}.jpg"
        files = {'file': (filename, file_bytes, 'image/jpeg')}
        data = {'location': 'Kalâa Sraghna', 'agent': 'DANA-Omega'}
        headers = {'Authorization': f'Bearer {API_KEY}'}

        response = requests.post(ALPHACLOUD_URL, files=files, data=data, headers=headers)
        if response.status_code == 200:
            return response.json().get('url', filename)
        return filename

    def AGENT_08_publish_whatsapp(self, to_number, message, image_url=None):
        url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}

        if image_url:
            data = {"messaging_product": "whatsapp", "to": to_number, "type": "image", "image": {"link": image_url, "caption": message}}
        else:
            data = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": message}}
        return requests.post(url, headers=headers, json=data).json()

    def capture_execute(self, user_question: str, to_number: str, user_image_b64: str = None, mode="MAGASIN"):
        if mode not in self.modes:
            mode = "MAGASIN"

        analysis = self.AGENT_01_analyze(user_image_b64, mode)

        if "ولد لي" in user_question or "generate" in user_question:
            image_url = self.AGENT_03_digital_studio(user_question)
        else:
            image_url = None

        ad_text = self.AGENT_08_generate_ad(analysis, "مراكش وقلعة السراغنة")
        self.AGENT_04_stamp("final")
        self.AGENT_08_publish_whatsapp(to_number, ad_text, image_url)

        return f"[DONE] SLA 5s | {ad_text}"

# ===============================
# 3. واجهة التشغيل
# ===============================
dana = DANA_Agent()

def dana_whatsapp_agent(user_question: str, to_number: str = "", user_image_b64: str = None) -> str:
    """الوكيل الذكي DANA للإنتاج الرقمي والتصوير"""
    system_prompt = """
    أنت DANA، الوكيل الذكي الخاص بخدمات الاستوديو الرقمي والتصوير والإنتاج الإعلامي.
    مهمتك: الرد بالدارجة المغربية، باحترام واحترافية.
    الهدف: مساعدة العملاء في حجز جلسات التصوير، تصميم الهويات البصرية، وخدمات الإنتاج الرقمي.
    ممنوع: الوعود الكاذبة. إذا ما عرفتيش قول "غادي نرجع ليك بالجواب من الفريق"
    """
    
    full_prompt = f"{system_prompt}\n\nسؤال العميل: {user_question}"

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )
        if to_number:
            dana.capture_execute(user_question, to_number, user_image_b64)
        return response.text
    except Exception as e:
        return f"عندي مشكل تقني دابا. الخطأ: {e}"

def send_whatsapp_message(to_number, message):
    """إرسال رسالة عبر WhatsApp Business API"""
    url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp", 
        "to": to_number, 
        "type": "text", 
        "text": {"body": message}
    }
    return requests.post(url, headers=headers, json=data).json()
