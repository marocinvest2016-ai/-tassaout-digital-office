# google_connector.py
import streamlit as st
from typing import Optional, Dict, Any

def get_google_sheets_data() -> Optional[Dict[str, Any]]:
    """
    يحاول يجيب البيانات من Google Sheets.
    إذا ما كانش Service Account أو الشيت، كيرجع None بدون ما يطيح.
    """
    try:
        # === حط هنا معلوماتك ===
        # 1. رفع ملف الـ Service Account JSON فـ secrets أو فـ المجلد
        # 2. أو استعمل st.secrets["gcp_service_account"]

        # مثال بسيط (غيرو حسب الشيت ديالك):
        # from google.oauth2.service_account import Credentials
        # import gspread
        # 
        # creds = Credentials.from_service_account_info(
        #     st.secrets["gcp_service_account"],
        #     scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        # )
        # client = gspread.authorize(creds)
        # sheet = client.open_by_key("SHEET_ID_هنا").sheet1
        # records = sheet.get_all_records()
        # return {"records": records}

        # حالياً: ما كاين والو → نرجع None
        return None

    except Exception as e:
        st.warning(f"⚠️ مقدرناش نوصلو لـ Google Sheets: {e}")
        return None


def calculate_roi_from_sheet(data: Optional[Dict[str, Any]]) -> Optional[Dict[str, float]]:
    """
    يحسب الإيرادات و ROI من البيانات.
    إذا ما كاينش بيانات، كيرجع None.
    """
    if not data or "records" not in data:
        return None

    try:
        total_revenue = 0.0
        total_cost = 0.0

        for row in data["records"]:
            # غير أسماء الأعمدة حسب الشيت ديالك
            revenue = float(row.get("إيرادات", row.get("revenue", 0)) or 0)
            cost = float(row.get("تكلفة", row.get("cost", 0)) or 0)
            total_revenue += revenue
            total_cost += cost

        avg_roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0.0

        return {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "avg_roi": avg_roi
        }
    except Exception as e:
        st.warning(f"⚠️ خطأ فـ حساب ROI: {e}")
        return None
