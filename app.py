from datetime import datetime
import io
import json
import os
import faiss
import numpy as np
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import requests
from sentence_transformers import SentenceTransformer
import streamlit as st

st.set_page_config(page_title="DANA CORE v5.1", page_icon="👑", layout="wide")
MEMORY_FILE = "dana_brain_capsule.json"


def load_capsule():
  if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {
      "identity": {"name": "DANA CORE", "role": "وكيل عقاري وتجاري سيادي"},
      "knowledge": [],
      "research": [],
  }


def save_capsule(data):
  with open(MEMORY_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


if "capsule" not in st.session_state:
  st.session_state.capsule = load_capsule()
if "last_result" not in st.session_state:
  st.session_state.last_result = ""


# ===== 1. تصدير PDF =====
def export_to_pdf(text, title):
  buffer = io.BytesIO()
  c = canvas.Canvas(buffer, pagesize=A4)
  width, height = A4
  c.setFont("Helvetica", 12)
  y = height - 50
  c.drawString(30, y, f"تقرير: {title}")
  y -= 30
  for line in text.split("\n"):
    c.drawString(30, y, line[:90])  # تقطيع السطور لتناسب العرض
    y -= 20
    if y < 50:
      c.showPage()
      y = height - 50
  c.save()
  buffer.seek(0)
  return buffer


# ===== 2. إرسال واتساب =====
def send_whatsapp(phone_number, message):
  token = st.secrets.get("WHATSAPP_TOKEN", "")
  phone_id = st.secrets.get("WHATSAPP_PHONE_ID", "")
  if not token or not phone_id:
    return "❌ ضع WHATSAPP_TOKEN و WHATSAPP_PHONE_ID في Secrets"

  url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }
  payload = {
      "messaging_product": "whatsapp",
      "to": phone_number,
      "type": "text",
      "text": {"body": message[:1000]},  # حد الواتساب للنص المرسل
  }
  try:
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    return (
        "✅ تم الإرسال للواتساب بنجاح"
        if res.status_code == 200
        else f"❌ خطأ: {res.text}"
    )
  except Exception as e:
    return f"❌ خطأ في الاتصال بالواتساب: {e}"


# ===== 3. RAG + Groq Engine =====
@st.cache_resource
def load_embedding_model():
  return SentenceTransformer("all-MiniLM-L6-v2")


def ingest_docs(uploaded_files):
  model = load_embedding_model()
  texts = []
  for pdf in uploaded_files:
    reader = PdfReader(pdf)
    for page in reader.pages:
      if page.extract_text():
        texts.append(page.extract_text())

  chunks = [t[i : i + 1000] for t in texts for i in range(0, len(t), 800)]
  if not chunks:
    return 0
  embeddings = model.encode(chunks)
  index = faiss.IndexFlatL2(embeddings.shape[1])
  index.add(np.array(embeddings))
  st.session_state.index, st.session_state.chunks = index, chunks
  return len(chunks)


def rag_search(query, k=3):
  if "index" not in st.session_state:
    return ""
  model = load_embedding_model()
  q_emb = model.encode([query])
  _, indices = st.session_state.index.search(np.array(q_emb), k)
  return "\n---\n".join([
      st.session_state.chunks[i]
      for i in indices[0]
      if i < len(st.session_state.chunks)
  ])


def call_dana_brain(prompt, model_name):
  api_key = st.secrets.get("GROQ_API_KEY", "")
  if not api_key:
    return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets"

  context = ""
  if "index" in st.session_state:
    rag = rag_search(prompt)
    if rag:
      context += "\n\nمعرفة مستخرجة من الملفات المرفوعة:\n" + rag

  identity = st.session_state.capsule["identity"]
  system_prompt = (
      f"أنت {identity['name']}. دورك: {identity['role']}. السياق الإضافي:"
      f" {context} . القواعد: فكر كـ CEO+CTO+COO. جاوب بالدارجة المغربية + العربية"
      " الفصحى. استعمل جداول، نقط واضحة، و Emojis."
  )

  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": model_name,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt},
      ],
      "temperature": 0.75,
      "max_tokens": 2000,
  }

  try:
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=90,
    )
    res.raise_for_status()
    result = res.json()["choices"][0]["message"]["content"]
    st.session_state.last_result = result
    return result
  except Exception as e:
    return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"


# ===== 4. واجهة Streamlit =====
st.title("👑 DANA CORE v5.1 - النواة السيادية (واتساب + PDF)")

with st.sidebar:
  st.header("⚙️ إعدادات الوكيل")
  st.text_input(
      "رقمك للواتساب",
      key="my_phone",
      placeholder="2126xxxxxxxx",
      value="212",
  )
  uploaded_files = st.file_uploader(
      "ارفع ملفات PDF للذاكرة", type="pdf", accept_multiple_files=True
  )
  if st.button("💉 حقن الملفات"):
    if uploaded_files:
      count = ingest_docs(uploaded_files)
      st.success(f"تم حقن {count} قطعة معلومات في ذاكرة الدماغ بنجاح!")
    else:
      st.warning("المرجو اختيار ملف PDF أولاً.")

task = st.text_area(
    "أعطي الأمر للوكيل:",
    height=130,
    placeholder=(
        "مثال: اقترح علي استراتيجية تسويق لـ 3 شقق بقلعة السراغنة مع محفزات"
        " البيع"
    ),
)

if st.button("🚀 فعّل DANA", use_container_width=True):
  if task.strip():
    with st.spinner("الدماغ السيادي يخطط، يحلل، ويصيغ التقرير..."):
      result = call_dana_brain(task, "llama-3.3-70b-versatile")
      st.markdown(result)
  else:
    st.warning("المرجو كتابة الأمر أو المهمة أولاً.")

# ===== 5. أزرار التصدير والإرسال الفوري =====
if st.session_state.last_result:
  st.markdown("---")
  col1, col2 = st.columns(2)
  with col1:
    pdf_file = export_to_pdf(st.session_state.last_result, task[:30])
    st.download_button(
        "📄 تحميل التقرير كملف PDF",
        data=pdf_file,
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        use_container_width=True,
    )
  with col2:
    if st.button("📲 إرسال التقرير للواتساب مباشرة", use_container_width=True):
      msg = f"*DANA CORE Report*\n\n{st.session_state.last_result[:900]}"
      status = send_whatsapp(st.session_state.my_phone, msg)
      if "✅" in status:
        st.success(status)
      else:
        st.error(status)
