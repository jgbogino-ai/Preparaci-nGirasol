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
df.columns = df.columns.str.strip()

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

st.markdown("# Estado Planta: 🟢 NORMAL")

# ======================================
# KPI
# ======================================
# Advertencia Humedad de Salida

if hum_salida < 6 or hum_salida > 8:
    st.error(
        f"⚠ Humedad Salida Secadora fuera de rango: {hum_salida:.1f}%"
    )
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



# ======================================
# OPERADORES
# ======================================

st.subheader("👷 Participación por operador (desde 01/07/2026)")



# Filtrar operadores desde 01/07/2026

df["Marca temporal"] = pd.to_datetime(
    df["Marca temporal"],
    dayfirst=True,
    errors="coerce"
)

df_operadores = df[
    df["Marca temporal"] >= pd.Timestamp("2026-07-01")
]

operadores = (
    df_operadores.groupby("Operador")
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
# SEMÁFOROS COMPLETOS DEL PROCESO
# ======================================

st.subheader("🟢🟡🔴 Estado del Proceso")

def mostrar_estado(nombre, valor, estado, color):
    st.markdown(
        f"""
        <div style="
        padding:10px;
        border-radius:10px;
        margin:5px;
        background-color:{color};
        color:white;
        font-weight:bold;">
        {nombre}: {valor} → {estado}
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# FUNCIONES DE SEMÁFORO
# -------------------------------

def sem_lamina(v):
    return ("🟢 VERDE","green") if v <= 0.9 else ("🔴 ROJO","red")

def sem_prensa12(v):
    if v < 140:
        return ("🔴 ROJO","red")
    elif v <= 150:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🟢 VERDE","green")

def sem_prensa3(v):
    if v < 60:
        return ("🔴 ROJO","red")
    elif v <= 70:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🟢 VERDE","green")

def sem_cocina1(v):
    return ("🟢 VERDE","green") if 111 <= v <= 114 else ("🔴 ROJO","red")

def sem_cocina2(v):
    return ("🟢 VERDE","green") if 104 <= v <= 110 else ("🔴 ROJO","red")

def sem_hum_entrada(v):
    if v < 9:
        return ("🟢 VERDE","green")
    elif v <= 10:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🔴 ROJO","red")

def sem_hum_salida(v):
    return ("🟢 VERDE","green") if 6 <= v <= 8 else ("🔴 ROJO","red")

def sem_pesaje(v):
    if v < 15:
        return ("🔴 ROJO","red")
    elif v <= 16:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🟢 VERDE","green")

def sem_expeller(v):
    if v < 12:
        return ("🔴 ROJO","red")
    elif v < 14:
        return ("🟡 AMARILLO","orange")
    elif v <= 16:
        return ("🟢 VERDE","green")
    else:
        return ("🔴 ROJO","red")

def sem_gases(v):
    if v > 80:
        return ("🔴 ROJO","red")
    elif v >= 70:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🟢 VERDE","green")

# -------------------------------
# LECTURA DE VARIABLES
# -------------------------------

lam_der_prensas = float(ultimo["Espesor lámina derecha (0,xx) MOLINO LADO PRENSAS"])
# lam_der_prensas = float(
#     ultimo["Espesor lámina derecha (0,xx) MOLINO LADO PRENSAS"]
# )
lam_izq_prensas = float(ultimo["Espesor lámina izquierda (0,xx) MOLINO LADO PRENSAS"])
# lam_izq_prensas = float(
#     ultimo["Espesor lámina izquierda (0,xx) MOLINO LADO PRENSAS"]
# )

corr1 = float(ultimo["Corriente (AMP) PRENSA 1"])
corr2 = float(ultimo["Corriente (AMP) PRENSA 2"])
corr3 = float(ultimo["Corriente (AMP) PRENSA 3"])

coc1 = float(ultimo["Temperatura (°C) COCINA 1"])
coc2 = float(ultimo["Temperatura (°C) COCINA 2"])

hum_ent = float(ultimo["Humedad de entrada secadora (%)"])
hum_sal = float(ultimo["Humedad salida secadora (%)"])

pesaje = float(ultimo["Pesaje de balanza (tn/h)"])

exp1 = float(ultimo["Espesor expeller (mm) PRENSA 1"])
exp2 = float(ultimo["Espesor expeller (mm) PRENSA 2"])
exp3 = float(ultimo["Espesor expeller (mm) PRENSA 3"])

gases = float(ultimo["TEMPERATURA DE GASES DE ENFRIADOR"])

# -------------------------------
# FILA 1
# -------------------------------

c1,c2,c3 = st.columns(3)

with c1:
    est,col = sem_lamina(lam_der_prensas)
    mostrar_estado("Lámina Der.", round(lam_der_prensas,2), est, col)

with c2:
    est,col = sem_lamina(lam_izq_prensas)
    mostrar_estado("Lámina Izq.", round(lam_izq_prensas,2), est, col)

with c3:
    est,col = sem_cocina1(coc1)
    mostrar_estado("Cocina 1", round(coc1,1), est, col)

# -------------------------------
# FILA 2
# -------------------------------

c4,c5,c6 = st.columns(3)

with c4:
    est,col = sem_cocina2(coc2)
    mostrar_estado("Cocina 2", round(coc2,1), est, col)

with c5:
    est,col = sem_hum_entrada(hum_ent)
    mostrar_estado("Humedad Entrada", round(hum_ent,1), est, col)

with c6:
    est,col = sem_hum_salida(hum_sal)
    mostrar_estado("Humedad Salida", round(hum_sal,1), est, col)

# -------------------------------
# FILA 3
# -------------------------------

c7,c8,c9 = st.columns(3)

with c7:
    est,col = sem_prensa12(corr1)
    mostrar_estado("Prensa 1", round(corr1,0), est, col)

with c8:
    est,col = sem_prensa12(corr2)
    mostrar_estado("Prensa 2", round(corr2,0), est, col)

with c9:
    est,col = sem_prensa3(corr3)
    mostrar_estado("Prensa 3", round(corr3,0), est, col)

# -------------------------------
# FILA 4
# -------------------------------

c10,c11,c12 = st.columns(3)

with c10:
    est,col = sem_expeller(exp1)
    mostrar_estado("Expeller P1", round(exp1,1), est, col)

with c11:
    est,col = sem_expeller(exp2)
    mostrar_estado("Expeller P2", round(exp2,1), est, col)

with c12:
    est,col = sem_expeller(exp3)
    mostrar_estado("Expeller P3", round(exp3,1), est, col)

# -------------------------------
# FILA 5
# -------------------------------

c13,c14 = st.columns(2)

with c13:
    est,col = sem_pesaje(pesaje)
    mostrar_estado("Pesaje tn/h", round(pesaje,1), est, col)

with c14:
    est,col = sem_gases(gases)
    mostrar_estado("Temp. Gases", round(gases,1), est, col)

# ALERTA ESPECIAL GASES

if gases > 80:
    st.error(
        "⚠ TEMPERATURA DE GASES DE ENFRIADOR MAYOR A 80°C - REVISAR ENFRIADOR"
    )
# ======================================
# ÚLTIMOS REGISTROS
# ======================================

st.subheader("📋 Últimos Registros")

st.dataframe(
    df.tail(20),
    use_container_width=True
)
