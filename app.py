import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?output=csv"

st.set_page_config(
    page_title="Preparación de Girasol",
    page_icon="🌻",
    layout="wide"
)

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL)

df = cargar_datos()

st.title("🌻 Dashboard Preparación de Girasol")

# ======================================
# Último registro
# ======================================

ultimo = df.iloc[-1]

hum_entrada = float(ultimo["Humedad de entrada secadora (%)"])
hum_salida = float(ultimo["Humedad salida secadora (%)"])
pesaje = float(ultimo["Pesaje de balanza (tn/h)"])
temp_gases = float(ultimo["TEMPERATURA DE GASES DE ENFRIADOR"])

# ======================================
# ALERTAS
# ======================================

alertas = []

if hum_salida < 6 or hum_salida > 8:
    alertas.append("🔴 Humedad salida fuera de rango")

if hum_entrada > 10:
    alertas.append("🔴 Humedad entrada alta")

if temp_gases > 80:
    alertas.append("🔴 Temperatura de gases > 80°C")

# ======================================
# ESTADO GENERAL
# ======================================

if len(alertas) > 0:
    estado = "🔴 ALERTA"
else:
    estado = "🟢 NORMAL"

st.markdown(f"# Estado Planta: {estado}")

# ======================================
# KPI
# ======================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Producción tn/h",
    round(pesaje, 2)
)

c2.metric(
    "Humedad Entrada %",
    round(hum_entrada, 2)
)

c3.metric(
    "Humedad Salida %",
    round(hum_salida, 2)
)

c4.metric(
    "Temp. Gases °C",
    round(temp_gases, 2)
)

# ======================================
# ALERTAS ACTIVAS
# ======================================

st.subheader("⚠ Alertas activas")

if len(alertas) == 0:
    st.success("Sin alertas activas")
else:
    for alerta in alertas:
        st.error(alerta)

# ======================================
# OPERADORES
# ======================================

st.subheader("👷 Participación por operador")

operadores = (
    df.groupby("Operador")
    .size()
    .reset_index(name="Registros")
    .sort_values("Registros", ascending=False)
)

fig = px.pie(
    operadores,
    values="Registros",
    names="Operador",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================
# BARRAS OPERADORES
# ======================================

fig2 = px.bar(
    operadores,
    x="Operador",
    y="Registros",
    color="Registros",
    text="Registros"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================================
# CORRIENTES
# ======================================

st.subheader("⚡ Corrientes de Prensas")

corrientes = pd.DataFrame({
    "Prensa":[
        "Prensa 1",
        "Prensa 2",
        "Prensa 3"
    ],
    "AMP":[
        float(ultimo["Corriente (AMP) PRENSA 1"]),
        float(ultimo["Corriente (AMP) PRENSA 2"]),
        float(ultimo["Corriente (AMP) PRENSA 3"])
    ]
})

fig3 = px.bar(
    corrientes,
    x="Prensa",
    y="AMP",
    color="AMP",
    text="AMP"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================================
# ÚLTIMOS REGISTROS
# ======================================

st.subheader("📋 Últimos Registros")

st.dataframe(
    df.tail(20),
    use_container_width=True
)
