import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURACION
# ==================================================

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSPwdonlIsyjr7cLcQm0tdn-D5Q5hi2345xHQA1bQACv9D8qPABYMtHijFjxPgEoejnE8SWRjsKovpd/pub?output=csv"

st.set_page_config(
    page_title="Pelleteado",
    page_icon="🏭",
    layout="wide"
)

# ==================================================
# DATOS
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
# ULTIMA CARGA
# ==================================================

fecha_ultima = ultimo["Marca temporal"]
operador_ultimo = ultimo["Operador"]
supervisor_ultimo = ultimo["Supervisor"]

ahora = pd.Timestamp.now() - pd.Timedelta(hours=3)

horas_sin_carga = (
    ahora - fecha_ultima
).total_seconds() / 3600

st.title("🏭 Dashboard Pelleteado")

if horas_sin_carga > 2:

    st.error(
        f"""
🚨 ALERTA DE CARGA

Operador: {operador_ultimo}

Supervisor: {supervisor_ultimo}

Última carga:
{fecha_ultima.strftime('%d/%m/%Y %H:%M')}

Han transcurrido
{horas_sin_carga:.1f} horas sin registros.
"""
    )

else:

    st.success(
        f"""
✅ Última carga registrada

Operador: {operador_ultimo}

Supervisor: {supervisor_ultimo}

Fecha:
{fecha_ultima.strftime('%d/%m/%Y %H:%M')}
"""
    )

# ==================================================
# FUNCIONES SEMAFOROS
# ==================================================

def sem_amperaje(v):

    if v < 140:
        return ("🔴 ROJO", "red")

    elif v <= 145:
        return ("🟡 AMARILLO", "orange")

    else:
        return ("🟢 VERDE", "green")


def sem_temperatura(v):

    if v > 35:
        return ("🔴 ROJO", "red")

    elif v >= 25:
        return ("🟡 AMARILLO", "orange")

    else:
        return ("🟢 VERDE", "green")


def sem_humedad(v):

    if v < 10:
        return ("🔴 ROJO", "red")

    elif v < 11:
        return ("🟡 AMARILLO", "orange")

    elif v <= 12.5:
        return ("🟢 VERDE", "green")

    elif v <= 13:
        return ("🟡 AMARILLO", "orange")

    else:
        return ("🔴 ROJO", "red")


# ==================================================
# TARJETA
# ==================================================

def tarjeta(titulo, valor, estado, color):

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            color:white;
            padding:12px;
            border-radius:12px;
            text-align:center;
            margin:5px;
        ">
            <h3>{titulo}</h3>
            <h2>{valor}</h2>
            <h3>{estado}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# VARIABLES
# ==================================================

amp1 = pd.to_numeric(
    ultimo["Amperaje de pelleteadora 1"],
    errors="coerce"
)

amp2 = pd.to_numeric(
    ultimo["Amperarje pelleteadora 2"],
    errors="coerce"
)

amp3 = pd.to_numeric(
    ultimo["Amperaje pelleteadora 3"],
    errors="coerce"
)

temp1 = pd.to_numeric(
    ultimo["Temperatura de material de salida enfriador de pellet 1 (°C)"],
    errors="coerce"
)

temp2 = pd.to_numeric(
    ultimo["Temperatura de material de salida enfriador de pellet 2 (°C)"],
    errors="coerce"
)

temp3 = pd.to_numeric(
    ultimo["Temperatura de material de salida enfriador de pellet 3 (°C)"],
    errors="coerce"
)

humedad = pd.to_numeric(
    ultimo["Humedad de pellet de girasol (correo laboratorio)"],
    errors="coerce"
)

# ==================================================
# KPI
# ==================================================

st.header("📊 Indicadores")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Humedad Pellet %",
    round(humedad,2)
)

c2.metric(
    "Destino",
    str(ultimo["Destino de pellet de girasol"])
)

c3.metric(
    "Silo Destino",
    str(ultimo["Número de silo destino"])
)

# ==================================================
# PELLETEADORAS
# ==================================================

st.header("⚙️ Pelleteadoras")

a,b,c = st.columns(3)

estado,color = sem_amperaje(amp1)
with a:
    tarjeta(
        "PELLETEADORA 1",
        f"{amp1:.0f} A",
        estado,
        color
    )

estado,color = sem_amperaje(amp2)
with b:
    tarjeta(
        "PELLETEADORA 2",
        f"{amp2:.0f} A",
        estado,
        color
    )

estado,color = sem_amperaje(amp3)
with c:
    tarjeta(
        "PELLETEADORA 3",
        f"{amp3:.0f} A",
        estado,
        color
    )

# ==================================================
# ENFRIADORES
# ==================================================

st.header("❄️ Enfriadores")

d,e,f = st.columns(3)

estado,color = sem_temperatura(temp1)
with d:
    tarjeta(
        "ENFRIADOR 1",
        f"{temp1:.1f} °C",
        estado,
        color
    )

estado,color = sem_temperatura(temp2)
with e:
    tarjeta(
        "ENFRIADOR 2",
        f"{temp2:.1f} °C",
        estado,
        color
    )

estado,color = sem_temperatura(temp3)
with f:
    tarjeta(
        "ENFRIADOR 3",
        f"{temp3:.1f} °C",
        estado,
        color
    )

# ==================================================
# HUMEDAD
# ==================================================

st.header("💧 Humedad Pellet")

estado,color = sem_humedad(humedad)

tarjeta(
    "HUMEDAD",
    f"{humedad:.2f} %",
    estado,
    color
)

# ==================================================
# ULTIMAS 15 CARGAS
# ==================================================

st.subheader("📋 Últimas 15 cargas")

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
    registros["Marca temporal"]
    .dt.strftime("%d/%m/%Y %H:%M")
)

st.table(registros)

# ==================================================
# TORTA OPERADORES
# ==================================================

st.header("👷 Participación por Operador")

df_operadores = df[
    df["Marca temporal"] >= pd.Timestamp("2026-07-01")
]

df_operadores = (
    df_operadores.groupby("Operador")
    .size()
    .reset_index(name="Registros")
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
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)
