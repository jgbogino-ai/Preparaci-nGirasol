import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURACION
# ==================================================

st.set_page_config(
    page_title="Dashboard Extracción Girasol",
    page_icon="🌻",
    layout="wide"
)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?gid=884320541&single=true&output=csv"

# ==================================================
# CARGA DATOS
# ==================================================

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL)

df = cargar_datos()

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(r"\s+", " ", regex=True)

df["Marca temporal"] = pd.to_datetime(
    df["Marca temporal"],
    dayfirst=True,
    errors="coerce"
)

df = df.sort_values("Marca temporal")

ultimo = df.iloc[-1]

# ==================================================
# TITULO
# ==================================================

st.title("🌻 Dashboard Extracción Girasol")

# ==================================================
# ESTADO PLANTA
# ==================================================

estado = str(ultimo["ESTADO DE PLANTA"])

if estado.upper() == "MARCHA":
    st.success(f"✅ Estado de Planta: {estado}")
else:
    st.error(f"⛔ Estado de Planta: {estado}")

# ==================================================
# KPI PRINCIPALES
# ==================================================

st.subheader("📊 Indicadores Principales")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Caudal Destilación",
        round(float(ultimo["CAUDAL DESTILACIÓN (lt/h)"]), 0)
    )

with c2:
    st.metric(
        "Caudal Extractor",
        round(float(ultimo["CAUDAL A EXTRACTOR (lt/h)"]), 0)
    )

with c3:
    st.metric(
        "Temp. Extractor",
        round(float(ultimo["EXTRACTOR TEMPERATURA (°C)"]), 1)
    )

with c4:
    st.metric(
        "Densidad",
        round(float(ultimo["DENSIDAD DESTILACIÓN (kg/m3)"]), 1)
    )

# ==================================================
# KPI SECUNDARIOS
# ==================================================

st.subheader("⚙️ Vacíos y Solvente")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Vacío Extractor",
        round(float(ultimo["EXTRACTOR VACÍO (mmca)"]), 0)
    )

with c2:
    st.metric(
        "Vacío Toaster",
        round(float(ultimo["TOSTER VACÍO (mmHg)"]), 0)
    )

with c3:
    st.metric(
        "Stock TKA",
        round(float(ultimo["TKA SOLVENTE STOCK (lt)"]), 0)
    )

with c4:
    st.metric(
        "Stock TKB",
        round(float(ultimo["TKB SOLVENTE STOCK (lt)"]), 0)
    )

# ==================================================
# NIVELES
# ==================================================

st.subheader("🛢️ Niveles")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Nivel TK34",
        f"{round(float(ultimo['NIVEL TK34 (%)']),1)} %"
    )

with c2:
    st.metric(
        "Nivel TK17",
        f"{round(float(ultimo['NIVEL TK17 (%)']),1)} %"
    )

# ==================================================
# TEMPERATURAS
# ==================================================

st.subheader("🌡️ Temperaturas")

fig = px.line(
    df,
    x="Marca temporal",
    y=[
        "EXTRACTOR TEMPERATURA (°C)",
        "TOSTER TEMPERATURA PISO (°C)",
        "TOSTER TEMPERATURA GASES (°C)",
        "ECONOMIZADOR 60 TEMPERATURA (°C)"
    ],
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ====
