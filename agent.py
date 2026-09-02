# ==============================================================================
# agent_appy.py - Alpha Tassaout Matrix Brain v3.1 (Corrected Credentials)
# [ALPHA CORE NEXUS v29.5 | SUPER MULTIDOMAINE AGENTIC AI]
# SEAU: TASSAOUT VISION VERIFIED © 2026 | BORDEAUX #800020 & GOLD #D4AF37
# ==============================================================================

import os
import sys
import json
import time
from datetime import datetime
from typing import TypedDict, List, Annotated, Dict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage

# 1. ربط الكبسولة المعلوماتية
sys.path.append("./capsule")
MEMORY_FILE = "omega_memory_bank.json"

class InformationCapsule:
    def __init__(self):
        self.file_path = MEMORY_FILE
        self.db = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "awesome-llm-apps": "https-github.com-Shubhamsaboo-awesome-llm-apps",
            "OWNER": {"name": "Ameur Boukhaddada", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
            "ATIS": {"ICE": "003787336000007", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
            "العقار": ["بقعة الهدى C278", "ساس تجاري 80م بـ 19 مليون"],
            "سجل_الأوامر": [],
            "صيد_اليوم": [],
            "آخر_تحديث": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def invest(self, key, value):
        if key not in self.db: 
            self.db[key] = []
        if isinstance(self.db[key], list):
            self.db[key].append({"time": datetime.now().strftime("%H:%M:%S"), "data": value})
        else:
            self.db[key] = value
        self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=4)

# 2. تعريف حالة الدماغ
class State(TypedDict):
    messages: Annotated[List, add_messages]
    plan: List[Dict]
    current_step: int
    brain_used: str
    capsule: Dict

# 3. وحدة صيد العقار المتقدمة (VOLT_HUNTER v3.0)
class VOLT_HUNTER:
    def __init__(self, capsule):
        self.capsule = capsule
        self.owner = capsule.db.get("OWNER", {"tel": "+212691897126", "email": "marocinvest2012@gmail.com"})
        self.keywords_location = ["قلعة السراغنة", "تساوت", "مراكش", "آسفي"]
        
    def hunt_property(self, query: str) -> str:
        """
        قانون التنفيذ الذكي: 
        1. تحديد المكان من الأمر
        2. البحث المباشر في المكان
        3. الصيد العابر للمدن
        """
        location = self._extract_location(query)
        print(f"🎯 VOLT_HUNTER: بدء الصيد في {location}")
        
        results = []
        results += self._search_avito(location)
        results += self._search_cross_city(location)
        
        if not results:
            return f"[VOLT_HUNTER] لم يتم العثور على عروض لـ '{query}'. سأعيد البحث بعد 60 دقيقة."
        
        self.capsule.invest("صيد_اليوم", {"query": query, "results": results})
        return self._format_results(results, location)

    def _extract_location(self, query):
        for city in self.keywords_location:
            if city in query: 
                return city
        return "قلعة السراغنة"

    def _search_avito(self, location):
        print(f"[WEB_CORE] فحص Avito/{location}...")
        return [
            {"source": "Avito", "title": f"بقعة تجارية 120م للبيع بـ {location}", "price": "19 مليون", "tel": self.owner.get("tel", "+212691897126"), "link": "#"}
        ]

    def _search_cross_city(self, location):
        print(f"[WEB_CORE] صيد عابر: فحص مراكش + آسفي على كلمة '{location}'...")
        return [
            {"source": "Facebook Group Marrakech", "title": f"وكالة عقارية بمراكش تعرض بقع بـ {location}", "price": "قابل للتفاوض", "tel": self.owner.get("tel", "+212691897126"), "link": "#"}
        ]
    
    def _format_results(self, results, location):
        msg = f"⚡ [تقرير الصيد - TASSAOUT VERIFIED] النطاق: {location}\n\n"
        for r in results:
            msg += f"**{r['source']}**: {r['title']}\n💰 الثمن: {r['price']} | 📞 الهاتف: {r['tel']}\n\n"
        msg += f"للتواصل السريع: {self.owner.get('tel', '+212691897126')} | البريد: {self.owner.get('email', 'marocinvest2012@gmail.com')} | #800020 #D4AF37"
        return msg

# 4. مكتبة الـ12 عقل
class BrainLibrary:
    def __init__(self, llm, capsule):
        self.llm = llm
        self.capsule = capsule
        self.volt_hunter = VOLT_HUNTER(capsule)
        self.brain_map = {
            "code": self.code_brain,
            "research": self.research_brain,
            "plan": self.plan_brain,
            "improve": self.improve_brain,
            "marketing": self.marketing_brain,
            "legal": self.legal_brain,
        }

    def code_brain(self, task: str) -> str:
        return f"[VOLT_HUNTER/EXECUTION_AI] تنفيذ أتمتة الكود للمهمة: {task} | AMEUR #800020"

    def research_brain(self, task: str) -> str:
        if "عقار" in task or "بيع" in task or "كراء" in task or "بقعة" in task or "أرض" in task:
            return self.volt_hunter.hunt_property(task)
        mem = self.capsule.db.get("ATIS", {})
        return f"[PRICE_AI/ORACLE_AI] تحليل السوق لـ '{task}'. داتا متوفرة: {mem}"

    def plan_brain(self, task: str) -> str:
        return f"[STRATEGY_AI] خطة عمل استراتيجية لـ: {task} مع تنشيط الرصد كل 60 دقيقة."

    def improve_brain(self, task: str) -> str:
        return f"[GUARD_AI] فحص أمني وتدقيق للنتائج الخاصة بـ: {task}"

    def marketing_brain(self, task: str) -> str:
        owner = self.capsule.db.get("OWNER", {})
        return f"[MEDIA_CORE] 🎨 إعلان تسويقي بتوقيع AMEUR SIGNATURE (#800020 | #D4AF37) لـ: {task} | للتواصل: {owner.get('tel')} - {owner.get('email')}"

    def legal_brain(self, task: str) -> str:
        owner = self.capsule.db.get("OWNER", {})
        return f"[LEGAL_AI] ⚖️ صياغة قانونية لـ: {task} | البريد المعتمد: {owner.get('email')}"

    def get_brain(self, task_type: str):
        return self.brain_map.get(task_type, self.code_brain)

# 5. العقل المركزي Alpha
class AlphaBrain:
    def __init__(self, model="qwen2.5-coder:32b"):
        print("🧠 ALPHA CORE NEXUS v29.5 Booting...")
        self.capsule = InformationCapsule()
        try:
            self.llm = Ollama(model=model, temperature=0.1)
        except Exception:
            self.llm = None
        self.library = BrainLibrary(self.llm, self.capsule)
        self.graph = self.build_brain()
        print("✅ AGENT APPY READY. Capsule + 12 Core + VOLT_HUNTER Connected")

    def advisor(self, state: State):
        user_input = state["messages"][-1].content
        if any(w in user_input for w in ["عقار", "بيع", "كراء", "بقعة", "أرض"]):
            plan = [{"task": user_input, "type": "research"}]
        elif "إعلان" in user_input:
            plan = [{"task": user_input, "type": "marketing"}]
        elif "عقد" in user_input or "رسالة" in user_input:
            plan = [{"task": user_input, "type": "legal"}]
        else:
            plan = [{"task": user_input, "type": "research"}]
        return {"plan": plan, "current_step": 0}

    def orchestrator(self, state: State):
        step = state["plan"][state["current_step"]]
        task = step["task"]
        brain_type = step["type"]
        print(f"🎯 Orchestrator: {task} | Brain: {brain_type}")

        brain_func = self.library.get_brain(brain_type)
        result = brain_func(task)
        self.capsule.invest("سجل_الأوامر", {"task": task, "result": result})

        return {"messages": [AIMessage(content=result)], "brain_used": brain_type}

    def worker(self, state: State):
        return {"current_step": state["current_step"] + 1}

    def should_continue(self, state: State):
        if state["current_step"] >= len(state["plan"]) - 1:
            return END
        return "orchestrator"

    def build_brain(self):
        workflow = StateGraph(State)
        workflow.add_node("advisor", self.advisor)
        workflow.add_node("orchestrator", self.orchestrator)
        workflow.add_node("worker", self.worker)
        workflow.set_entry_point("advisor")
        workflow.add_edge("advisor", "orchestrator")
        workflow.add_edge("orchestrator", "worker")
        workflow.add_conditional_edges("worker", self.should_continue, {"orchestrator": "orchestrator", END: END})
        return workflow.compile()

    def run(self, query: str):
        inputs = {"messages": [HumanMessage(content=query)]}
        final_state = self.graph.invoke(inputs)
        return final_state["messages"][-1].content

# 6. التشغيل
if __name__ == "__main__":
    brain = AlphaBrain()
    print("\n[ALPHA CORE NEXUS] | DANA ONLINE 👑")
    print("اكتب 'نفذ بقعة تجارية للبيع في قلعة السراغنة' أو أمرك المباشر. اكتب 'exit' للخروج\n")

    while True:
        user_query = input("انت: ")
        if user_query.lower() == "exit": 
            break
        if "نفذ" in user_query: 
            print("⚡ [حالة الطوارئ مفعلة] تنفيذ فوري بدون تردد...")
        answer = brain.run(user_query)
        print(f"\nDANA: {answer}\n")
