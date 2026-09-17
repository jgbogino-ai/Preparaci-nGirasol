import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURACION
# ==================================================

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?gid=884320541&single=true&output=csv"

st.set_page_config(
    page_title="extracción",
    page_icon="🏭",
    layout="wide"
)
import streamlit as st
import pandas as pd
import plotly.express as px



# ==================================================
# CARGA DE DATOS
# ==================================================

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL)

df = cargar_datos()

df.columns = df.columns.str.strip()

df["Marca temporal"] = pd.to_datetime(
    df["Marca temporal"],
    dayfirst=True,
    errors="coerce"
)

df = df.sort_values("Marca temporal")

ultimo = df.iloc[-1]

# ==================================================
# TÍTULO
# ==================================================

st.title("🌻 Dashboard Extracción de Girasol")

# ==================================================
# ESTADO PLANTA
# ==================================================

estado = str(ultimo["ESTADO DE PLANTA"])

if estado.upper() == "MARCHA":
    st.success(f"✅ Estado de Planta: {estado}")
else:
    st.error(f"⛔ Estado de Planta: {estado}")

# ==================================================
# KPIs
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Caudal Destilación",
        ultimo["CAUDAL DESTILACIÓN (lt/h)"]
    )

with col2:
    st.metric(
        "Densidad Destilación",
        ultimo["DENSIDAD DESTILACIÓN (kg/m3)"]
    )

with col3:
    st.metric(
        "Economizador",
        f"{ultimo['ECONOMIZADOR 60 TEMPERATURA (°C)']} °C"
    )

with col4:
    st.metric(
        "Operador",
        ultimo["Operador"]
    )

# ==================================================
# GRAFICO CAUDAL
# ==================================================

st.subheader("📈 Tendencia de Caudal")

fig = px.line(
    df,
    x="Marca temporal",
    y="CAUDAL DESTILACIÓN (lt/h)",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# GRAFICO DENSIDAD
# ==================================================

st.subheader("📈 Tendencia de Densidad")

fig = px.line(
    df,
    x="Marca temporal",
    y="DENSIDAD DESTILACIÓN (kg/m3)",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TEMPERATURAS
# ==================================================

columnas_temp = [
    c for c in df.columns
    if "TEMPERATURA" in c.upper()
]

if columnas_temp:

    st.subheader("🌡️ Temperaturas")

    fig = px.line(
        df,
        x="Marca temporal",
        y=columnas_temp
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# ULTIMOS 24 REGISTROS
# ==================================================

st.subheader("📋 Últimos 24 registros")

st.dataframe(
    df.tail(24),
    use_container_width=True,
    hide_index=True
)

# ==================================================
# ESTADÍSTICAS
# ==================================================

st.subheader("📊 Resumen")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Promedio Caudal",
        round(df["CAUDAL DESTILACIÓN (lt/h)"].mean(), 0)
    )

with c2:
    st.metric(
        "Máximo Caudal",
        round(df["CAUDAL DESTILACIÓN (lt/h)"].max(), 0)
    )

with c3:
    st.metric(
        "Promedio Densidad",
        round(df["DENSIDAD DESTILACIÓN (kg/m3)"].mean(), 1)
    )
