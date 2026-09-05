import json, os, requests, streamlit as st
from datetime import datetime
from duckduckgo_search import DDGS
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb # بديل FAISS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="DANA CORE v5.2", page_icon="👑", layout="wide")
MEMORY_FILE = "dana_brain_capsule.json"

def load_capsule():...
def save_capsule(data):...

if "capsule" not in st.session_state: st.session_state.capsule = load_capsule()
if "last_result" not in st.session_state: st.session_state.last_result = ""

# ===== 1. تصدير PDF =====
def export_to_pdf(text, title):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 12)
    y = height - 50
    c.drawString(30, y, f"تقرير: {title}")
    y -= 30
    for line in text.split('\n'):
        c.drawString(30, y, line[:90])
        y -= 20
        if y < 50: c.showPage(); y = height - 50
    c.save()
    buffer.seek(0)
    return buffer

# ===== 2. إرسال واتساب =====
def send_whatsapp(phone_number, message):...

# ===== 3. RAG مع ChromaDB - أخف من FAISS =====
@st.cache_resource
def load_db():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("dana_memory")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return collection, model

def ingest_docs(uploaded_files):
    collection, model = load_db()
    texts = []
    for pdf in uploaded_files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            if page.extract_text(): texts.append(page.extract_text())

    chunks = [t[i:i+1000] for t in texts for i in range(0, len(t), 800)]
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(embeddings=embeddings, documents=chunks, ids=ids)
    return len(chunks)

def rag_search(query, k=3):
    collection, model = load_db()
    q_emb = model.encode([query]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=k)
    return "\n---\n".join(results['documents'][0]) if results['documents'] else ""

# ===== 4. Web + Groq =====
def smart_web_search(query):...
def call_dana_brain(prompt, model_name):...

# ===== 5. الواجهة مع الأزرار =====
st.title("👑 DANA CORE v5.2 - مصلح للـ Cloud")
...
