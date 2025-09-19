import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import os
import base64

try:
    from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None

import pdfkit 
--
st.set_page_config(page_title="Smart Auto-Dashboard", layout="wide", page_icon="📊")
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>📊 Smart Auto-Generated Dashboard</h1>", unsafe_allow_html=True)

if "uploaded_df" not in st.session_state:
    st.warning("Please upload a CSV or Excel file from the Upload page first.")
    st.stop()

df_raw = st.session_state.uploaded_df.copy()

def make_unique_columns(columns):
    counts = {}
    new_cols = []
    for col in columns:
        if col in counts:
            counts[col] += 1
            new_cols.append(f"{col}_{counts[col]}")
        else:
            counts[col] = 0
            new_cols.append(col)
    return new_cols

df = df_raw.copy()
df.columns = make_unique_columns(df.columns)

for col in df.columns:
    if df[col].dtype == object:
        try:
            df[col] = pd.to_datetime(df[col], errors='ignore')
        except Exception:
            pass

date_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
cat_cols = [col for col in df.columns if df[col].dtype == 'object']

st.sidebar.header("🔍 Filters")

if date_cols:
    date_col = st.sidebar.selectbox("Select Date Column", date_cols)
    min_date, max_date = df[date_col].min(), df[date_col].max()
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
    if len(date_range) == 2:
        df = df[(df[date_col] >= pd.to_datetime(date_range[0])) & 
                (df[date_col] <= pd.to_datetime(date_range[1]))]

if cat_cols:
    category_col = st.sidebar.selectbox("Category Column", cat_cols)
    selected_cats = st.sidebar.multiselect("Select Categories", df[category_col].unique())
    if selected_cats:
        df = df[df[category_col].isin(selected_cats)]

def without_duplicates_null(data):
    df_clean = data.drop_duplicates().reset_index(drop=True)
    df_clean.replace("", np.nan, inplace=True)
    for col in df_clean.select_dtypes(include='object'):
        df_clean[col] = df_clean[col].str.strip().replace("", np.nan)
    return df_clean

def with_duplicates_filled(data):
    df_filled = data.copy()
    df_filled.replace("", np.nan, inplace=True)
    for col in df_filled.select_dtypes(include='object'):
        df_filled[col] = df_filled[col].str.strip().replace("", np.nan)
    df_filled.fillna(method='ffill', inplace=True)
    df_filled.fillna(method='bfill', inplace=True)
    return df_filled

df_no_duplicates_null = without_duplicates_null(df)
df_with_duplicates_filled = with_duplicates_filled(df)

tab_preview, tab_summary, tab_cleaned = st.tabs([
    "🗂 Data Preview",
    "📑 Summary",
    "✨ Cleaned Data"
])

with tab_preview:
    st.markdown("### 📋 Data Preview (Raw Uploaded Data)")
    st.dataframe(df_raw)

with tab_summary:
    st.markdown("### 📊 Automated EDA Summary")

    if ProfileReport is not None:
        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True, minimal=True)
        html_report = profile.to_html()

        b64_html = base64.b64encode(html_report.encode()).decode()
        iframe_code = f"""
        <iframe src="data:text/html;base64,{b64_html}" width="100%" height="1600" frameborder="0"></iframe>
        """
        st.markdown(iframe_code, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download EDA Report as HTML",
            data=html_report,
            file_name="EDA_Report.html",
            mime="text/html"
        )
        try:
            pdf_bytes = pdfkit.from_string(html_report, False)
            st.download_button(
                label="📥 Download EDA Report as PDF",
                data=pdf_bytes,
                file_name="EDA_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning("⚠ PDF generation failed. Make sure wkhtmltopdf is installed.")
            st.error(f"Error: {e}")
    else:
        st.info("Install ydata-profiling to enable automated EDA.")

with tab_cleaned:
    st.markdown("### 🧹 Data Without Duplicates (Missing as NULL)")
    st.dataframe(df_no_duplicates_null)
    st.download_button(
        label="📥 Download (No Duplicates, Null Missing Values)",
        data=df_no_duplicates_null.to_csv(index=False).encode('utf-8'),
        file_name="no_duplicates_null.csv",
        mime="text/csv"
    )

    st.markdown("### 🔄 Data With Duplicates (Missing Filled from Duplicates)")
    st.dataframe(df_with_duplicates_filled)
    st.download_button(
        label="📥 Download (With Duplicates, Missing Filled)",
        data=df_with_duplicates_filled.to_csv(index=False).encode('utf-8'),
        file_name="with_duplicates_filled.csv",
        mime="text/csv"
    )
