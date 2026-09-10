# google_connector.py
import streamlit as st
import pandas as pd
import json
from google.oauth2.service_account import Credentials
import gspread

def get_google_sheets_data():
    """قراءة البيانات مباشرة من ملف Excel / Google Sheets المرتبط عبر Google Drive API"""
    try:
        service_account_str = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
        file_id = st.secrets.get("GOOGLE_DRIVE_FILE_ID", "")

        if not service_account_str or not file_id:
            st.warning("⚠️ إعدادات Google Drive أو Service Account غير مكتملة في Secrets")
            return None

        # تحليل JSON الخاص بحساب الخدمة
        service_account_info = json.loads(service_account_str)
        
        # تحديد النطاقات (Scopes) المطلوبة
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # المصادقة
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(creds)

        # فتح الملف بواسطة ID
        sheet = client.open_by_key(file_id).sheet1
        data = sheet.get_all_records()
        
        return pd.DataFrame(data)

    except Exception as e:
        st.warning(f"⚠️ خطأ في الاتصال بـ Google Drive / Sheets: {type(e).__name__} - {str(e)}")
        return None

def calculate_roi_from_sheet(df):
    """حساب ROI ومؤشرات مالية من بيانات Excel"""
    try:
        # تأكد من وجود الأعمدة المطلوبة
        required_cols = ['revenue', 'expenses', 'budget']
        if not all(col in df.columns for col in required_cols):
            return None
        
        # حساب ROI
        df['roi'] = ((df['revenue'] - df['expenses']) / df['expenses'].replace(0, 1)) * 100
        df['profit'] = df['revenue'] - df['expenses']
        df['margin'] = (df['profit'] / df['revenue'].replace(0, 1)) * 100
        
        # إحصائيات عامة
        total_revenue = df['revenue'].sum()
        total_expenses = df['expenses'].sum()
        total_profit = total_revenue - total_expenses
        avg_roi = df['roi'].mean()
        
        return {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'total_profit': total_profit,
            'avg_roi': avg_roi,
            'df_enriched': df
        }
    except Exception as e:
        st.warning(f"⚠️ خطأ في حساب ROI: {type(e).__name__} - {str(e)}")
        return None
