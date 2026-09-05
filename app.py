from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1", # هذا صحيح
)

response = client.chat.completions.create( # بدل responses بـ chat.completions
    model="openai/gpt-oss-120b", # 120b ماشي 20b
    messages=[
        {"role": "system", "content": "أنت مساعد ذكي"},
        {"role": "user", "content": "Explain the importance of fast language models"}
    ],
    temperature=0.7,
    max_tokens=1024
)
print(response.choices[0].message.content) # هادي طريقة القراءة فـ chat
