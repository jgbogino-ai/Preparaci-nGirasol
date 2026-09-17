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
# ULTIMO REGISTRO
# ==================================================

ahora = pd.Timestamp.now()

ultima_carga = df["Marca temporal"].max()

horas = (ahora - ultima_carga).total_seconds() / 3600

st.subheader("📡 Estado de Carga")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Último Registro",
        ultima_carga.strftime("%d/%m/%Y %H:%M")
    )

with c2:

    if horas <= 2:
        st.success(f"✅ Hace {horas:.1f} horas")
    else:
        st.error(f"🚨 Hace {horas:.1f} horas")

# ==================================================
# ESTADO PLANTA
# ==================================================

estado = str(ultimo["ESTADO DE PLANTA"])

if estado.upper() == "MARCHA":
    st.success(f"✅ Estado de Planta: {estado}")
else:
    st.error(f"⛔ Estado de Planta: {estado}")

# ==================================================
# FUNCION NUMERICA SEGURA
# ==================================================

def valor_seguro(columna):
    valor = pd.to_numeric(ultimo[columna], errors="coerce")

    if pd.isna(valor):
        return None

    return float(valor)
# ==================================================
# ULTIMO REGISTRO
# ==================================================

ahora = pd.Timestamp.now()

ultima_carga 
# ==================================================
# KPI PRINCIPALES
# ==================================================

st.subheader("📊 Indicadores Principales")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Caudal Destilación",
    valor_seguro("CAUDAL DESTILACIÓN (lt/h)")
)

c2.metric(
    "Caudal Extractor",
    valor_seguro("CAUDAL A EXTRACTOR (lt/h)")
)

temp_ext = valor_seguro("EXTRACTOR TEMPERATURA (°C)")

c3.metric(
    "Temp. Extractor",
    temp_ext
)

c4.metric(
    "Densidad",
    valor_seguro("DENSIDAD DESTILACIÓN (kg/m3)")
)

# ==================================================
# VACIOS Y SOLVENTE
# ==================================================

st.subheader("⚙️ Vacíos y Solvente")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Vacío Extractor",
    valor_seguro("EXTRACTOR VACÍO (mmca)")
)

c2.metric(
    "Vacío Toaster",
    valor_seguro("TOSTER VACÍO (mmHg)")
)

c3.metric(
    "Stock TKA",
    valor_seguro("TKA SOLVENTE STOCK (lt)")
)

c4.metric(
    "Stock TKB",
    valor_seguro("TKB SOLVENTE STOCK (lt)")
)

# ==================================================
# NIVELES
# ==================================================

st.subheader("🛢️ Niveles")

c1, c2 = st.columns(2)

tk34 = valor_seguro("NIVEL TK34 (%)")
tk17 = valor_seguro("NIVEL TK17 (%)")

c1.metric(
    "Nivel TK34",
    "Sin dato" if tk34 is None else f"{tk34:.1f}%"
)

c2.metric(
    "Nivel TK17",
    "Sin dato" if tk17 is None else f"{tk17:.1f}%"
)

# ==================================================
# SEMAFOROS OPERATIVOS
# ==================================================

st.subheader("🚦 Estado Operativo")

c1, c2, c3, c4 = st.columns(4)

# ==========================================
# EXTRACTOR
# ==========================================

temp_ext = valor_seguro("EXTRACTOR TEMPERATURA (°C)")

with c1:

    st.markdown("### Extractor")

    if temp_ext is None:
        st.warning("Sin dato")

    elif temp_ext < 50:
        st.error(f"🔴 {temp_ext:.1f} °C")

    elif temp_ext < 55:
        st.warning(f"🟡 {temp_ext:.1f} °C")

    elif temp_ext <= 62:
        st.success(f"🟢 {temp_ext:.1f} °C")

    else:
        st.error(f"🔴 {temp_ext:.1f} °C")


# ==========================================
# SALIDA TOSTER
# ==========================================

temp_piso = valor_seguro("TOSTER TEMPERATURA PISO (°C)")

with c2:

    st.markdown("### Salida Toaster")

    if temp_piso is None:
        st.warning("Sin dato")

    elif temp_piso < 100:
        st.error(f"🔴 {temp_piso:.1f} °C")

    elif temp_piso <= 120:
        st.success(f"🟢 {temp_piso:.1f} °C")

    else:
        st.error(f"🔴 {temp_piso:.1f} °C")


# ==========================================
# GASES TOSTER
# ==========================================

temp_gases = valor_seguro("TOSTER TEMPERATURA GASES (°C)")

with c3:

    st.markdown("### Gases Toaster")

    if temp_gases is None:
        st.warning("Sin dato")

    elif temp_gases < 70:
        st.error(f"🔴 {temp_gases:.1f} °C")

    elif temp_gases < 75:
        st.warning(f"🟡 {temp_gases:.1f} °C")

    elif temp_gases <= 85:
        st.success(f"🟢 {temp_gases:.1f} °C")

    else:
        st.error(f"🔴 {temp_gases:.1f} °C")


# ==========================================
# ACEITE MINERAL CALENTADOR 121
# ==========================================

aceite = valor_seguro(
    "ACEITE MINERAL CALENTADOR 121 TEMPERATURA (°C)"
)

with c4:

    st.markdown("### Aceite Mineral")

    if aceite is None:
        st.warning("Sin dato")

    elif aceite < 105:
        st.error(f"🔴 {aceite:.1f} °C")

    elif aceite <= 112:
        st.success(f"🟢 {aceite:.1f} °C")

    elif aceite <= 115:
        st.warning(f"🟡 {aceite:.1f} °C")

    else:
        st.error(f"🔴 {aceite:.1f} °C")
# ==================================================
# ULTIMOS 24 REGISTROS
# ==================================================

st.subheader("📋 Últimos 24 Registros")

st.dataframe(
    df.tail(24),
    use_container_width=True,
    hide_index=True
)

# ==================================================
# COMENTARIOS
# ==================================================

st.subheader("📝 Últimos Comentarios")

if "COMENTARIOS:" in df.columns:

    comentarios = df[
        [
            "Marca temporal",
            "Operador",
            "COMENTARIOS:"
        ]
    ].tail(10)

    st.dataframe(
        comentarios,
        use_container_width=True,
        hide_index=True
    )
