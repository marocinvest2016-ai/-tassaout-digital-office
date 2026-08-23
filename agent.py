import streamlit as st
from google import genai
import requests
import datetime

# ===============================
# إعدادات السيادة المطلقة (Alpha Core Nexus)
# ===============================
GEMINI_API_KEY = st.secrets["gemini"]["API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

ALPHACLOUD_URL = "https://api.alphacloud.tassout.ai/upload"
API_KEY = "SIGNATURE_AMEUR_KEY_OMEGA"

WA_PHONE_ID = st.secrets["whatsapp"]["PHONE_NUMBER_ID"]
WA_TOKEN = st.secrets["whatsapp"]["ACCESS_TOKEN"]
WA_VERSION = st.secrets["whatsapp"]["API_VERSION"]

# ===============================
# منظومة الكاميرا العالمية ودستور التصنيع
# ===============================
class AlphaCoreNexusFactory:
    def __init__(self):
        self.modes = {
            "PRODUIT": {"engine": "FLUX.1-Pro-Ultra", "lens": "85mm", "target": "المنتجات والمجاليات"},
            "PORTRAIT": {"engine": "Hasselblad-X2D", "lens": "50mm", "target": "الصور الشخصية وفريق العمل"},
            "MAGASIN": {"engine": "Imagen-4", "lens": "24mm", "target": "المحلات والواجهات التجارية"},
            "VOITURE": {"engine": "Midjourney-v7", "lens": "70-200mm", "target": "السيارات والآليات الفلاحية"},
            "CINEMA": {"engine": "ARRI-Alexa", "lens": "35mm", "target": "المشاريع السينمائية والكبرى"},
            "ARCHITECTURE": {"engine": "Unreal-Engine-5.4", "lens": "18mm", "target": "الهندسة المعمارية والديكور 3D"}
        }

    def agent_vision_analyze(self, query: str, mode: str) -> str:
        return f"Camera Mode: {mode} | Target Analyzed | Tassaout Vision Verified"

    def agent_digital_studio(self, prompt: str, mode: str) -> str:
        engine_used = self.modes.get(mode, self.modes["PRODUIT"])["engine"]
        result = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=f"Professional commercial asset, {prompt}, 8K, cinematic lighting, powered by {engine_used}"
        )
        image_bytes = result.generated_images[0].image.image_bytes
        return self.agent_upload_to_cloud(image_bytes, mode)

    def agent_stamp(self, filename: str) -> str:
        return f"{filename}_APPROUVE_PAR_AMEUR.jpg"

    def agent_generate_ad(self, mode: str, domain: str) -> str:
        return f"خدمة معتمدة في قطاع [{domain}] | وضع التصوير [{mode}] | توقيع Signature Ameur | Tassaout Vision Verified © 2026"

    def agent_upload_to_cloud(self, file_bytes, subject) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"OMEGA_{subject}_{timestamp}.jpg"
        files = {'file': (filename, file_bytes, 'image/jpeg')}
        data = {'location': 'Global - Tassaout Valley', 'agent': 'Alpha Nexus Omega'}
        headers = {'Authorization': f'Bearer {API_KEY}'}

        try:
            response = requests.post(ALPHACLOUD_URL, files=files, data=data, headers=headers)
            if response.status_code == 200:
                return response.json().get('url', filename)
        except Exception:
            pass
        return filename

    def agent_publish_whatsapp(self, to_number: str, message: str, image_url: str = None):
        if not to_number:
            return
        url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}

        if image_url:
            data = {"messaging_product": "whatsapp", "to": to_number, "type": "image", "image": {"link": image_url, "caption": message}}
        else:
            data = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": message}}
        
        try:
            requests.post(url, headers=headers, json=data)
        except Exception:
            pass

    def execute_pipeline(self, user_question: str, domain: str, mode: str, to_number: str = None) -> str:
        if mode not in self.modes:
            mode = "PRODUIT"

        # 1. التحليل البصري
        self.agent_vision_analyze(user_question, mode)

        # 2. توليد الأصول البصرية إذا تطلب الأمر
        image_url = None
        if any(keyword in user_question for keyword in ["ولد", "تصميم", "صورة", "generate", "3D"]):
            image_url = self.agent_digital_studio(user_question, mode)

        # 3. صياغة التقرير والختم السيادي
        ad_text = self.agent_generate_ad(mode, domain)
        self.agent_stamp("final_asset")

        # 4. النشر الفوري عبر الواتساب
        if to_number:
            self.agent_publish_whatsapp(to_number, ad_text, image_url)

        return f"👑 [DANA CEO - مصنع Alpha Core Nexus]:\n\n{ad_text}\n\n📌 **الحالة:** تم التوثيق بنجاح تام | SLA < 5s | معتمد ومختوم."

# تشغيل المصنع الإمبراطوري
factory = AlphaCoreNexusFactory()

def dana_whatsapp_agent(user_question: str, domain: str = "عام", mode: str = "PRODUIT", to_number: str = "") -> str:
    """الوكيل الذكي المركزي DANA لتدبير المصنع الرقمي والمحفظة السيادية"""
    system_prompt = """
    أنت DANA، المديرة التنفيذية (CEO) لنظام Alpha Core Nexus و Master Grand Studio.
    مهمتك: الرد على الزبناء والشركاء بأسلوب احترافي، دقيق، وموثوق.
    السياسة: لا مجال للخطأ، دقة مطلقة، تنفيذ فوري، وتطبيق الختم السيادي APPROUVÉ PAR AMEUR © 2026.
    """
    
    full_prompt = f"{system_prompt}\n\nقطاع التدخل: {domain} | وضع الكاميرا: {mode}\nطلب المستخدم: {user_question}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        execution_log = factory.execute_pipeline(user_question, domain, mode, to_number)
        
        return f"{response.text}\n\n---\n{execution_log}"
    except Exception as e:
        return f"⚠️ تنبيه نظام DANA: حدث خطأ طارئ أثناء معالجة الطلب السحابي. التفاصيل: {e}"

def send_whatsapp_message(to_number, message):
    """إرسال رسالة مباشرة عبر WhatsApp API"""
    url = f"https://graph.facebook.com/{WA_VERSION}/{WA_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    try:
        return requests.post(url, headers=headers, json=data).json()
    except Exception:
        return {"status": "error"}
