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

c1, c2, c3, c4, c5, c6 = st.columns(6)

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

with c5:
    st.metric(
        "TK Destino",
        str(ultimo["# TK DESTINO CRUDO"])
    )

with c6:

    espacio = pd.to_numeric(
        ultimo["cm ESPACIO DESTINO CRUDO"],
        errors="coerce"
    )

    if pd.isna(espacio):
        st.metric("Espacio Libre TK", "Sin dato")

    elif espacio < 50:
        st.error(f"🔴 {espacio:.0f} cm")

    elif espacio < 100:
        st.warning(f"🟡 {espacio:.0f} cm")

    else:
        st.success(f"🟢 {espacio:.0f} cm")
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

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)


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
# ACEITE MINERAL ENTRADA ABSORBEDORA

aceite_abs = valor_seguro(
    "Temperatura de aceite mineral entrada a absorbedora (°C)"
)

with c5:

    st.markdown("### Aceite Abs.")

    if aceite_abs is None:
        st.warning("Sin dato")

    elif aceite_abs < 25:
        st.error(f"🔴 {aceite_abs:.1f} °C")

    elif aceite_abs <= 31:
        st.success(f"🟢 {aceite_abs:.1f} °C")

    elif aceite_abs <= 35:
        st.warning(f"🟡 {aceite_abs:.1f} °C")

    else:
        st.error(f"🔴 {aceite_abs:.1f} °C")


# INGRESO EXPELLER

temp_expeller = valor_seguro(
    "Temperatura de ingreso de expeller (°C)"
)

with c6:

    st.markdown("### Expeller")

    if temp_expeller is None:
        st.warning("Sin dato")

    elif temp_expeller < 50:
        st.error(f"🔴 {temp_expeller:.1f} °C")

    elif temp_expeller < 55:
        st.warning(f"🟡 {temp_expeller:.1f} °C")

    elif temp_expeller <= 60:
        st.success(f"🟢 {temp_expeller:.1f} °C")

    else:
        st.error(f"🔴 {temp_expeller:.1f} °C")


# SALIDA TORRE

temp_torre = valor_seguro(
    "Temperatura agua salida de torre (°C)"
)

with c7:

    st.markdown("### Salida Torre")

    if temp_torre is None:
        st.warning("Sin dato")

    elif temp_torre <= 26:
        st.success(f"🟢 {temp_torre:.1f} °C")

    elif temp_torre <= 30:
        st.warning(f"🟡 {temp_torre:.1f} °C")

    else:
        st.error(f"🔴 {temp_torre:.1f} °C")

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
