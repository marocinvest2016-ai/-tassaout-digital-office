# الصورة الرسمية للـ Python
FROM python:3.11-slim

# تحديث النظام وتثبيت الأدوات الأساسية (curl, git)
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# تثبيت Meta CLI الرسمي
RUN curl -fsS https://dev.meta.ai/install.sh | bash
ENV PATH="/root/.local/bin:$PATH"

# تحديد مجلد العمل
WORKDIR /app

# نسخ المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات المشروع
COPY . .

# فتح البورتات الخاصة بـ Streamlit (8501) و Flask (5000)
EXPOSE 8501 5000

# أمر التشغيل المتزامن لـ Streamlit و Flask عبر Gunicorn
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & gunicorn -w 1 -b 0.0.0.0:5000 app:app_webhook
