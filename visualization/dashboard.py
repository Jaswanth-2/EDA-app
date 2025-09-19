import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Auto-Dashboard", layout="wide", page_icon="📊")

# Load Roboto font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------- LANGUAGE SELECTOR ----------
languages = {
    "English": {
        "title": "📊 Smart Auto-Generated Dashboard",
        "filters": "🔍 Filters",
        "metrics": "📌 Key Metrics",
        "insights": "📈 Quick Insights",
        "warning": "⚠ Please upload a dataset first from the Upload page."
    },
    "Hindi": {
        "title": "📊 स्मार्ट ऑटो-जनरेटेड डैशबोर्ड",
        "filters": "🔍 फ़िल्टर",
        "metrics": "📌 मुख्य मेट्रिक्स",
        "insights": "📈 त्वरित जानकारी",
        "warning": "⚠ कृपया पहले अपलोड पेज से डेटा सेट अपलोड करें।"
    }
}

selected_lang = st.sidebar.selectbox("🌐 Select Language", list(languages.keys()))
lang = languages[selected_lang]

# ---------- HEADER ----------
st.markdown(f"""
    <div style='
        text-align: center; 
        padding: 20px 0px; 
        background: linear-gradient(90deg, #4CAF50, #81C784);
        color: white; 
        font-size: 3rem; 
        font-weight: 700;
        font-family: "Roboto", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        border-radius: 10px;
        margin-bottom: 30px;
    '>
        {lang['title']}
    </div>
""", unsafe_allow_html=True)

# ---------- CHECK FOR DATA ----------
if "uploaded_df" not in st.session_state:
    st.warning(lang["warning"])
    st.stop()

df = st.session_state.uploaded_df.copy()

# ---------- CLEAN DUPLICATE COLUMNS ----------
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

df.columns = make_unique_columns(df.columns)

# ---------- DETECT COLUMN TYPES ----------
for col in df.columns:
    if df[col].dtype == object:
        try:
            df[col] = pd.to_datetime(df[col], errors='ignore')
        except:
            pass

date_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = [col for col in df.columns if df[col].dtype == 'object']

# ---------- FILTERS ----------
with st.sidebar:
    st.header(lang["filters"])

    if date_cols:
        date_col = st.selectbox("Select Date Column", date_cols)
        min_date, max_date = df[date_col].min(), df[date_col].max()
        date_range = st.date_input("Date Range", [min_date, max_date])
        if len(date_range) == 2:
            df = df[(df[date_col] >= pd.to_datetime(date_range[0])) & (df[date_col] <= pd.to_datetime(date_range[1]))]

    if cat_cols:
        category_col = st.selectbox("Category Column", cat_cols)
        selected_cats = st.multiselect("Select Categories", df[category_col].unique())
        if selected_cats:
            df = df[df[category_col].isin(selected_cats)]

    # Sorting feature
    sort_col = st.selectbox("Sort By", options=["None"] + df.columns.tolist())
    sort_order = st.radio("Order", ["Ascending", "Descending"])
    if sort_col != "None":
        df = df.sort_values(by=sort_col, ascending=True if sort_order=="Ascending" else False)

    # Reset filters button
    if st.button("🔄 Reset Filters"):
        st.session_state.pop("uploaded_df")
        st.success("✅ Filters cleared! Please re-upload your file.")
        st.stop()

# ---------- KPI METRICS ----------
st.markdown(f"### {lang['metrics']}")
if num_cols:
    cols = st.columns(min(4, len(num_cols)))
    for i, metric in enumerate(num_cols[:4]):
        with cols[i]:
            total = df[metric].sum()
            st.metric(label=metric, value=f"{total:,.0f}")
else:
    st.info("No numeric columns available for KPIs.")

# ---------- QUICK INSIGHTS ----------
insights_md = ""
if cat_cols:
    insights_md += f"*Top Category in {cat_cols[0]}:* {df[cat_cols[0]].value_counts().idxmax()}  \n"
if num_cols:
    insights_md += f"*Max Value in {num_cols[0]}:* {df[num_cols[0]].max():,.0f}  \n"
if date_cols:
    insights_md += f"*Date Range:* {df[date_cols[0]].min().date()} to {df[date_cols[0]].max().date()}"

st.markdown(f"""
    <h4>{lang['insights']}</h4>
    <p style="font-family: 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        {insights_md}
    </p>
""", unsafe_allow_html=True)

# ---------- VISUALIZATION SETTINGS ----------
st.sidebar.subheader("🎨 Visualization Settings")
viz_lib = st.sidebar.radio("Choose Visualization Library", ["Plotly", "Matplotlib", "Seaborn", "Altair"])
theme = st.sidebar.radio("Theme", ["Light", "Dark"])

# ---------- VISUALIZATION TABS ----------
tab_donut, tab_bar, tab_box, tab_hist, tab_corr, tab_scatter, tab_line, tab_anim, tab_map = st.tabs([
    "🍩 Donut Chart", "📊 Bar Chart", "📦 Box Plot",
    "📈 Histogram", "🔗 Correlation Heatmap", "⚪ Scatter Plot", 
    "📉 Line Chart", "🎥 Animated Plot", "🌍 Map Visualization"
])

# ---------- DONUT ----------
with tab_donut:
    if cat_cols and num_cols:
        if viz_lib == "Plotly":
            fig = px.pie(df, names=cat_cols[0], values=num_cols[0], hole=0.4, 
                         template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Altair":
            chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field=num_cols[0], type="quantitative"),
                color=alt.Color(field=cat_cols[0], type="nominal")
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Donut available only in Plotly / Altair.")
    else:
        st.info("Not enough data for donut chart.")

# ---------- BAR ----------
with tab_bar:
    if cat_cols and num_cols:
        if viz_lib == "Plotly":
            fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0], 
                         template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Matplotlib":
            fig, ax = plt.subplots()
            df.groupby(cat_cols[0])[num_cols[0]].mean().plot(kind="bar", ax=ax, 
                color="green" if theme=="Light" else "white")
            st.pyplot(fig)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.barplot(x=cat_cols[0], y=num_cols[0], data=df, ax=ax)
            st.pyplot(fig)
        elif viz_lib == "Altair":
            chart = alt.Chart(df).mark_bar().encode(x=cat_cols[0], y=num_cols[0], color=cat_cols[0])
            st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Not enough data for bar chart.")

# ---------- BOX PLOT ----------
with tab_box:
    if cat_cols and num_cols:
        if viz_lib == "Plotly":
            fig = px.box(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0],
                         template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.boxplot(x=cat_cols[0], y=num_cols[0], data=df, ax=ax)
            st.pyplot(fig)
        elif viz_lib == "Matplotlib":
            fig, ax = plt.subplots()
            df.boxplot(column=num_cols[0], by=cat_cols[0], ax=ax)
            st.pyplot(fig)
    else:
        st.info("Not enough data for boxplot.")

# ---------- HISTOGRAM ----------
with tab_hist:
    if num_cols:
        if viz_lib == "Plotly":
            fig = px.histogram(df, x=num_cols[0], nbins=20, 
                               template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.histplot(df[num_cols[0]], bins=20, kde=True, ax=ax)
            st.pyplot(fig)
        elif viz_lib == "Matplotlib":
            fig, ax = plt.subplots()
            ax.hist(df[num_cols[0]], bins=20, color="skyblue")
            st.pyplot(fig)
    else:
        st.info("No numeric columns for histogram.")

# ---------- CORRELATION ----------
with tab_corr:
    if num_cols:
        corr = df[num_cols].corr()
        if viz_lib == "Plotly":
            fig = px.imshow(corr, text_auto=True, template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.info("Correlation supported only in Plotly/Seaborn")
    else:
        st.info("Not enough numeric data for correlation heatmap.")

# ---------- SCATTER ----------
with tab_scatter:
    if len(num_cols) >= 2:
        if viz_lib == "Plotly":
            fig = px.scatter(df, x=num_cols[0], y=num_cols[1], color=cat_cols[0] if cat_cols else None,
                             template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.scatterplot(x=num_cols[0], y=num_cols[1], hue=cat_cols[0] if cat_cols else None, data=df, ax=ax)
            st.pyplot(fig)
        elif viz_lib == "Matplotlib":
            fig, ax = plt.subplots()
            ax.scatter(df[num_cols[0]], df[num_cols[1]], c="blue")
            st.pyplot(fig)
    else:
        st.info("Need at least 2 numeric columns for scatter plot.")

# ---------- LINE ----------
with tab_line:
    if date_cols and num_cols:
        if viz_lib == "Plotly":
            fig = px.line(df, x=date_cols[0], y=num_cols[0], color=cat_cols[0] if cat_cols else None,
                          template="plotly_dark" if theme=="Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif viz_lib == "Seaborn":
            fig, ax = plt.subplots()
            sns.lineplot(x=date_cols[0], y=num_cols[0], hue=cat_cols[0] if cat_cols else None, data=df, ax=ax)
            st.pyplot(fig)
        elif viz_lib == "Matplotlib":
            fig, ax = plt.subplots()
            ax.plot(df[date_cols[0]], df[num_cols[0]])
            st.pyplot(fig)
    else:
        st.info("Need date and numeric column for line chart.")

# ---------- ANIMATED ----------
with tab_anim:
    if date_cols and num_cols and cat_cols:
        fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0], animation_frame=date_cols[0], 
                     template="plotly_dark" if theme=="Dark" else "plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for animated plot.")

# ---------- MAP ----------
with tab_map:
    lat_cols = [c for c in df.columns if "lat" in c.lower()]
    lon_cols = [c for c in df.columns if "lon" in c.lower() or "lng" in c.lower()]
    if lat_cols and lon_cols:
        fig = px.scatter_mapbox(df, lat=lat_cols[0], lon=lon_cols[0], 
                                color=cat_cols[0] if cat_cols else None,
                                size=num_cols[0] if num_cols else None, mapbox_style="open-street-map",
                                template="plotly_dark" if theme=="Dark" else "plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No latitude/longitude columns found for map visualization.")
