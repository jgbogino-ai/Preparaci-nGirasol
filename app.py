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
df["Marca temporal"] = pd.to_datetime(
    df["Marca temporal"],
    dayfirst=True,
    errors="coerce"
)

df = df.sort_values("Marca temporal")

ultima_carga = df.iloc[-1]

fecha_ultima = ultima_carga["Marca temporal"]

operador_ultimo = ultima_carga["Operador"]

supervisor_ultimo = ultima_carga["Supervisor"]

horas_sin_carga = (
    pd.Timestamp.now() - fecha_ultima
).total_seconds() / 3600

if horas_sin_carga > 2:

    st.markdown(
        f"""
        <div style="
            background:#b71c1c;
            color:white;
            padding:15px;
            border-radius:12px;
            text-align:center;
            margin-bottom:20px;
        ">
            <h2>🚨 ALERTA DE CARGA</h2>

            <h3>Operador: {operador_ultimo}</h3>

            <h3>Supervisor: {supervisor_ultimo}</h3>

            <h3>
            Última carga:
            {fecha_ultima.strftime('%d/%m/%Y %H:%M')}
            </h3>

            <h2>
            {horas_sin_carga:.1f} horas sin registros
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div style="
            background:#1b5e20;
            color:white;
            padding:15px;
            border-radius:12px;
            text-align:center;
            margin-bottom:20px;
        ">
            <h2>✅ ÚLTIMA CARGA REGISTRADA</h2>

            <h3>Operador: {operador_ultimo}</h3>

            <h3>Supervisor: {supervisor_ultimo}</h3>

            <h3>
            {fecha_ultima.strftime('%d/%m/%Y %H:%M')}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )


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
# FUNCIONES SEMAFOROS
# ======================================

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

def sem_gases(v):
    if v > 80:
        return ("🔴 ROJO","red")
    elif v >= 70:
        return ("🟡 AMARILLO","orange")
    else:
        return ("🟢 VERDE","green")

# ======================================
# VARIABLES
# ======================================

corr1 = float(ultimo["Corriente (AMP) PRENSA 1"])
corr2 = float(ultimo["Corriente (AMP) PRENSA 2"])
corr3 = float(ultimo["Corriente (AMP) PRENSA 3"])

coc1 = float(ultimo["Temperatura (°C) COCINA 1"])
coc2 = float(ultimo["Temperatura (°C) COCINA 2"])

lam_der = float(
    ultimo["Espesor lámina derecha (0,xx) MOLINO LADO PRENSAS"]
)

lam_izq = float(
    ultimo["Espesor lámina izquierda (0,xx) MOLINO LADO PRENSAS"]
)

hum_ent = float(
    ultimo["Humedad de entrada secadora (%)"]
)

hum_sal = float(
    ultimo["Humedad salida secadora (%)"]
)

gases = float(
    ultimo["TEMPERATURA DE GASES DE ENFRIADOR"]
)

# ======================================
# FUNCION TARJETA
# ======================================

def tarjeta(titulo, valor, estado, color):

    st.markdown(
        f"""
        <div style="
        background-color:{color};
        border-radius:15px;
        padding:6px;
        margin:5px;
        text-align:center;
        color:white;">
        <h3>{titulo}</h3>
        <h2>{valor}</h2>
        <h4>{titulo}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
# ======================================
# PRENSAS
# ======================================

st.header("🔧 Prensas")

c1,c2,c3 = st.columns(3)

estado,color = sem_prensa12(corr1)
with c1:
    tarjeta("PRENSA 1", f"{corr1:.0f} A", estado, color)

estado,color = sem_prensa12(corr2)
with c2:
    tarjeta("PRENSA 2", f"{corr2:.0f} A", estado, color)

estado,color = sem_prensa3(corr3)
with c3:
    tarjeta("PRENSA 3", f"{corr3:.0f} A", estado, color)

# ======================================
# COCINAS
# ======================================

st.header("🍳 Cocinas")

c4,c5 = st.columns(2)

estado,color = sem_cocina1(coc1)
with c4:
    tarjeta("COCINA 1", f"{coc1:.1f} °C", estado, color)

estado,color = sem_cocina2(coc2)
with c5:
    tarjeta("COCINA 2", f"{coc2:.1f} °C", estado, color)

# ======================================
# LAMINADORES
# ======================================

st.header("📏 Laminadores")

c6,c7 = st.columns(2)

estado,color = sem_lamina(lam_der)
with c6:
    tarjeta("LAMINA DERECHA", f"{lam_der:.2f} mm", estado, color)

estado,color = sem_lamina(lam_izq)
with c7:
    tarjeta("LAMINA IZQUIERDA", f"{lam_izq:.2f} mm", estado, color)

# ======================================
# HUMEDADES
# ======================================

st.header("💧 Humedades")

c8,c9 = st.columns(2)

estado,color = sem_hum_entrada(hum_ent)
with c8:
    tarjeta("ENTRADA SECADORA", f"{hum_ent:.1f} %", estado, color)

estado,color = sem_hum_salida(hum_sal)
with c9:
    tarjeta("SALIDA SECADORA", f"{hum_sal:.1f} %", estado, color)

# ======================================
# PRODUCCION
# ======================================

st.header("📦 Producción")

estado,color = sem_pesaje(pesaje)

tarjeta(
    "PESAJE",
    f"{pesaje:.1f} tn/h",
    estado,
    color
)

# ======================================
# ENFRIADOR
# ======================================

st.header("♨️ Enfriador")

estado,color = sem_gases(gases)

tarjeta(
    "TEMP. GASES",
    f"{gases:.1f} °C",
    estado,
    color
)

if gases > 80:
    st.error(
        "⚠ TEMPERATURA DE GASES MAYOR A 80°C - REVISAR ENFRIADOR"
    )

# ======================================
# ULTIMOS REGISTROS
# ======================================

#st.subheader("📋 Últimos Registros")

#df_mostrar = df.copy()


#st.dataframe(
#    df.tail(20).astype(str),
#   use_container_width=True
#)
# ======================================
# ULTIMOS REGISTROS
# ======================================

# ======================================
# ULTIMAS 5 CARGAS
# ======================================

st.subheader("📋 Últimas 15 cargas realizadas")

try:

    registros = df[
        [
            "Marca temporal",
            "Operador",
            "Supervisor"
        ]
    ].tail(15)

    registros = registros.sort_values(
        by="Marca temporal",
        ascending=False
    )

    registros["Marca temporal"] = (
        pd.to_datetime(
            registros["Marca temporal"]
        ).dt.strftime("%d/%m/%Y %H:%M")
    )

    st.table(registros)

except Exception as e:

    st.error(f"Error al mostrar registros: {e}")

# ======================================
# PARTICIPACION POR OPERADOR
# ======================================

st.header("👷 Participación por Operador")

df_operadores = df[
    df["Marca temporal"] >= pd.Timestamp("2026-07-01")
]

df_operadores = (
    df_operadores.groupby("Operador")
    .size()
    .reset_index(name="Registros")
    .sort_values("Registros", ascending=False)
)

fig = px.pie(
    df_operadores,
    values="Registros",
    names="Operador",
    hole=0.55
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    height=650
)

st.plotly_chart(
    fig,
    use_container_width=True
)
