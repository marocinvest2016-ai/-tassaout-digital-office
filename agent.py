import os
import streamlit as st

class TassaoutAgenticCore:
    def __init__(self):
        self.office_name = "مكتب تساوت الرقمي | العقار والأعمال بقلعة السراغنة"
        self.commercial_name = "Sraghna Immobilière"

    def render_dashboard(self):
        st.title(f"👑 {self.office_name}")
        st.subheader(f"النظام السيادي المتقدم للأتمتة والاعلانات - {self.commercial_name}")
        st.success("تم تشغيل النظام السيادي بنجاح واستقرار تام.")

if __name__ == "__main__":
    core = TassaoutAgenticCore()
    core.render_dashboard()
