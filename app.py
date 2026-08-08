import streamlit as st
from agent import TassaoutAgenticCore

# تشغيل جوهر النظام
core = TassaoutAgenticCore()
core.render_dashboard()
