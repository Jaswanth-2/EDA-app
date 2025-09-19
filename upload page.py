import streamlit as st
import pandas as pd
import os
import time
import json

UPLOAD_FOLDER = "uploaded_data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="EDA Dashboard App", layout="wide")

st.title("📤 Upload Your Dataset")

st.markdown("""
Upload your dataset in **CSV**, **Excel (.xlsx, .xls)**, or **JSON** format.  
Maximum file size: **2 GB**.

- After uploading, the dataset is saved on the server and previewed below.
- You can proceed to the Dashboard or Data Visualization pages.
""")

uploaded_file = st.file_uploader(
    "Choose a dataset file", 
    type=["csv", "xlsx", "xls", "json"]
)

def load_file(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file)
        elif file.name.endswith('.json'):
            data = json.load(file)
            return pd.json_normalize(data)
        else:
            st.error("Unsupported file format")
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file:
    df = load_file(uploaded_file)
    if df is not None:
        st.session_state["uploaded_df"] = df

        filename = f"dataset_{int(time.time())}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if uploaded_file.name.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df.to_excel(file_path, index=False)
        elif uploaded_file.name.endswith('.json'):
            uploaded_file.seek(0)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

        st.session_state["uploaded_file_path"] = file_path

        st.success(f"✅ Dataset '{uploaded_file.name}' uploaded successfully! Size: {uploaded_file.size / (1024**2):.2f} MB")

        st.markdown("### Dataset preview:")
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Clear uploaded data"):
            st.session_state.pop("uploaded_df", None)
            st.session_state.pop("uploaded_file_path", None)
            st.experimental_rerun()

        st.markdown(
            """
            <a href="/dashboard" target="_self">
                <button style="background-color:green;color:white;
                               border:none;padding:10px 20px;
                               border-radius:8px;font-size:16px;">
                    📊 Go to Dashboard
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

elif "uploaded_df" in st.session_state:
    st.info("Dataset already uploaded in this session:")
    st.dataframe(st.session_state["uploaded_df"].head(), use_container_width=True)
else:
    st.info("Please upload a CSV, Excel, or JSON file to proceed.")

st.markdown("""
<script>
console.log("Custom JS loaded! You can add your scripts here.");
</script>
""", unsafe_allow_html=True)
