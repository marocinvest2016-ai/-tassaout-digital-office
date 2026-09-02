# ==============================================================================
# نظام الوكيل الذكي السيادي الشامل: agent.py
# المالك / المطور: عامر بوخدادة (ameur signature tassaout ai)
# التنسيق: خدمات تساوت & شركة ATIS - المغرب
# ==============================================================================

class TassaoutAgentMemory:
    """إدارة الذاكرة السيادية وسجل المحادثات والمستندات"""
    def __init__(self):
        self.conversation_history = []
        self.document_cache = {}
        self.initialize_memory()

    def initialize_memory(self):
        welcome_msg = {
            "role": "assistant",
            "content": (
                "👑 **[النواة الذكية السيادية الشاملة - TASSAOUT & ATIS AGENT]**\n\n"
                "مرحباً بك يا أمير. تم تفعيل الذاكرة والنواة الاستراتيجية بنجاح:\n"
                "1. هندسة البناء والتصميم المعماري\n"
                "2. العقار الصناعي، التجاري والفلاحي\n"
                "3. التجارة الدولية والتصدير\n"
                "4. اللوجستيات والآليات الكبرى\n"
                "5. النظم الرقمية والبرمجة الذكية\n\n"
                "**[TASSAOUT & ATIS VERIFIED 🌿]**\n"
                "**ameur signature tassaout ai**"
            )
        }
        self.conversation_history.append(welcome_msg)

    def add_message(self, role: str, content: str, attachments=None):
        message = {"role": role, "content": content}
        if attachments:
            message["attachments"] = attachments
        self.conversation_history.append(message)

    def cache_document_text(self, file_name: str, extracted_text: str):
        self.document_cache[file_name] = extracted_text

    def get_accumulated_context(self) -> str:
        context_summary = ""
        for msg in self.conversation_history[-5:]:
            context_summary += f"- {msg['role']}: {msg['content'][:200]}...\n"
        return context_summary

    def clear_memory(self):
        self.conversation_history = []
        self.document_cache = {}
        self.initialize_memory()


class TassaoutAgentCore:
    """العقل الذكي المتعدد التخصصات (Multi-Domaine Engine)"""
    def __init__(self, founder_signature="ameur signature tassaout ai"):
        self.signature = founder_signature
        self.verified_tag = "[TASSAOUT & ATIS VERIFIED]"

    def process_request(self, domain: str, query: str, context_memory: str = "") -> str:
        domain_lower = domain.lower()

        if "عقار" in domain_lower or "شقق" in query or "منزل" in query or "أرض" in query:
            return self._generate_real_estate_content(query, context_memory)
        elif "هندسة" in domain_lower or "تصميم" in query or "بناء" in query:
            return self._generate_engineering_content(query, context_memory)
        elif "تجارة" in domain_lower or "تصدير" in query or "استيراد" in query:
            return self._generate_trade_content(query, context_memory)
        elif "لوجستيات" in domain_lower or "نقل" in query:
            return self._generate_logistics_content(query, context_memory)
        else:
            return self._generate_general_strategic_content(domain, query, context_memory)

    def _generate_real_estate_content(self, query: str, memory: str) -> str:
        return f"""
🏢 **[عقل العقار والاستثمار - خدمات تساوت & ATIS]** 🌟
بناءً على طلبكم والذاكرة السياقية للمشروع:
> *"{query}"*

* **التحليل الاستراتيجي:** تم رصد الطلب وتكييف العرض العقاري ليتطابق مع معايير السوق بقلعة السراغنة ومراكش.
* **المميزات:** تشطيبات راقية، مرونة في التمويل أو الاستغلال المباشر (Clé en main).
* 📞 **التواصل المباشر:** +212691897126
---
🌿 {self.verified_tag} | **{self.signature}**
"""

    def _generate_engineering_content(self, query: str, memory: str) -> str:
        return f"""
🏛️ **[عقل الهندسة المعمارية والديكور - خدمات تساوت & ATIS]** 📐
بناءً على التوجيه الهندسي المعتمد:
> *"{query}"*

* **التخطيط الوظيفي:** توزيع دقيق يضمن الاستغلال الأمثل للمساحات والإضاءة الطبيعية.
* **المواكبة التقنية:** إشراف ميداني متكامل من التصميم الأولي إلى التسليم النهائي.
* 📞 **للاعتماد الهندسي:** +212691897126
---
🌿 {self.verified_tag} | **{self.signature}**
"""

    def _generate_trade_content(self, query: str, memory: str) -> str:
        return f"""
🌐 **[عقل التجارة الدولية وسلاسل التوريد - خدمات تساوت & ATIS]** 📦
بناءً على استراتيجية التصدير والتبادل:
> *"{query}"*

* **سلاسل الإمداد:** ضبط مسارات الشحن وتثمين المنتوجات المجالية والصناعية.
* **المواكبة القانونية:** إعداد العقود والملفات الإدارية بدقة تامة.
* 📞 **للاعتماد التجاري:** +212691897126
---
🌿 {self.verified_tag} | **{self.signature}**
"""

    def _generate_logistics_content(self, query: str, memory: str) -> str:
        return f"""
🚛 **[عقل اللوجستيات والنقل - خدمات تساوت & ATIS]** ⚡
بناءً على التنسيق اللوجستي:
> *"{query}"*

* **العمليات:** إدارة الأسطول، تتبع النقل الطرقي، وضمان سلاسة توزيع البضائع.
* 📞 **للتنسيق اللوجستي:** +212691897126
---
🌿 {self.verified_tag} | **{self.signature}**
"""

    def _generate_general_strategic_content(self, domain: str, query: str, memory: str) -> str:
        return f"""
⚡ **[النواة الذكية السيادية الشاملة - {domain}]** 🚀
المحتوى المعالج بناءً على سجل المشروع:
> *"{query}"*

* **التنفيذ:** تفعيل مسارات العمل السريع Clé en main مع ضمان أعلى معايير الجودة الرقمية والخدماتية.
* 📞 **للاعتماد النهائي:** +212691897126
---
🌿 {self.verified_tag} | **{self.signature}**
"""


class TassaoutAgentSystem:
    """النظام الموحد الذي يدمج الذاكرة والعقل معاً للاستخدام المباشر"""
    def __init__(self):
        self.memory = TassaoutAgentMemory()
        self.core = TassaoutAgentCore()

    def run_query(self, domain: str, user_input: str) -> str:
        # 1. حفظ طلب المستخدم في الذاكرة
        self.memory.add_message("user", user_input)
        
        # 2. استخراج السياق التاريخي
        context = self.memory.get_accumulated_context()
        
        # 3. معالجة الطلب عبر العقل الذكي
        response = self.core.process_request(domain, user_input, context)
        
        # 4. حفظ رد الوكيل في الذاكرة
        self.memory.add_message("assistant", response)
        
        return response


# ==============================================================================
# مثال على التشغيل التجريبي المباشر (عند تنفيذ الملف مباشرة)
# ==============================================================================
if __name__ == "__main__":
    # تشغيل النظام
    agent_system = TassaoutAgentSystem()
    
    # طباعة الرسالة الترحيبية المخزنة
    print(agent_system.memory.conversation_history[0]["content"])
    print("\n" + "="*50 + "\n")
    
    # تجربة استعلام عقاري
    domain_test = "عقار"
    query_test = "أبحث عن بقعة أرضية تجارية بقلعة السراغنة مساحة 200 متر"
    
    print(f"🔹 المدخل [القطاع: {domain_test}]: {query_test}\n")
    output = agent_system.run_query(domain_test, query_test)
    print(output)
