def call_gemini_rest(prompt_text, image_paths=None):
    # محاولة جلب المفتاح بأكثر من احتمال لضمان عدم فشل الاتصال
    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            api_key = st.secrets.get("gemini_api_key", "")
    except Exception:
        pass
        
    if not api_key:
        return "⚠️ تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في إعدادات الأسرار (Secrets) على المنصة السحابية."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    parts = [{"text": prompt_text}]
    
    if image_paths:
        import base64
        for img_p in image_paths:
            if os.path.exists(img_p):
                with open(img_p, "rb") as img_file:
                    encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_string
                        }
                    })

    payload = {
        "contents": [{
            "parts": parts
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ خطأ في المصادقة أو الاتصال (رمز الاستجابة: {response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ حدث خطأ تقني أثناء الإرسال: {e}"
