import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_elements import elements, dashboard, html, mui

st.set_page_config(page_title="Dashboard Builder", layout="wide", page_icon="📊")

if "tiles" not in st.session_state:
    st.session_state["tiles"] = []

if "data" not in st.session_state:
    st.session_state["data"] = None

st.sidebar.subheader("➕ Add Tile")
chart_type = st.sidebar.selectbox("Chart Type", ["Scatter", "Bar", "Line", "Histogram", "Pie"])
x_axis = st.sidebar.selectbox("X-axis", st.session_state["data"].columns if st.session_state["data"] is not None else [])
y_axis = st.sidebar.selectbox("Y-axis", st.session_state["data"].columns if st.session_state["data"] is not None else [])

if st.sidebar.button("Add Chart"):
    tile_id = f"tile_{len(st.session_state['tiles'])+1}"
    st.session_state["tiles"].append({
        "id": tile_id,
        "type": chart_type,
        "x": x_axis,
        "y": y_axis,
        "x_pos": 0,
        "y_pos": len(st.session_state["tiles"]) * 5,
        "w": 6,
        "h": 8,
    })

st.markdown("### 📊 Dashboard")

if st.session_state["tiles"] and st.session_state["data"] is not None:

    layout = [
        dashboard.Item(tile["id"], tile["x_pos"], tile["y_pos"], tile["w"], tile["h"])
        for tile in st.session_state["tiles"]
    ]

    with elements("dashboard"):
        with dashboard.Grid(layout, draggableHandle=".draggable"):

            for tile in st.session_state["tiles"]:
                df = st.session_state["data"]

                # Build chart
                if tile["type"] == "Scatter":
                    fig = px.scatter(df, x=tile["x"], y=tile["y"])
                elif tile["type"] == "Bar":
                    fig = px.bar(df, x=tile["x"], y=tile["y"])
                elif tile["type"] == "Line":
                    fig = px.line(df, x=tile["x"], y=tile["y"])
                elif tile["type"] == "Histogram":
                    fig = px.histogram(df, x=tile["x"])
                elif tile["type"] == "Pie":
                    fig = px.pie(df, names=tile["x"], values=tile["y"])

                with mui.Paper(key=tile["id"], elevation=3, sx={"p":2, "borderRadius":2}):
                    mui.Typography(tile["id"], variant="h6", className="draggable")

                    html.Iframe(
                        srcDoc=fig.to_html(include_plotlyjs="cdn"),
                        style={"width": "100%", "height": "100%", "border": "none"},
                    )
