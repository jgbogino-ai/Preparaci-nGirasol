import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURACION
# ==================================================

st.set_page_config(
    page_title="Dashboard Extracción Girasol",
    page_icon="💨",
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

st.title("💨 Dashboard Extracción Girasol")

# ==================================================
# HORA ACTUAL
# ==================================================

from datetime import datetime
from zoneinfo import ZoneInfo

ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))

st.info(
    f"🕒 Hora actual: {ahora.strftime('%d/%m/%Y %H:%M')}"
)

# ==================================================
# ULTIMO REGISTRO
# ==================================================

ultima_carga = df["Marca temporal"].max()

# usar la misma hora argentina que se muestra arriba
ahora_local = ahora.replace(tzinfo=None)

horas = (ahora_local - ultima_carga).total_seconds() / 3600

operador_ultimo = str(ultimo["Operador"])

st.subheader("📡 Estado de Carga")

if horas <= 2:

    st.success(
        f"""
✅ REGISTRO AL DÍA

👤 Operador: {operador_ultimo}

🕒 Último registro: {ultima_carga.strftime('%d/%m/%Y %H:%M')}

⏱ Hace {horas:.1f} hs
"""
    )

else:

    st.error(
        f"""
🚨 SIN REGISTROS RECIENTES

👤 Operador: {operador_ultimo}

🕒 Último registro: {ultima_carga.strftime('%d/%m/%Y %H:%M')}

⏱ Hace {horas:.1f} hs
"""
    )

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
# KPI PRINCIPALES
# ==================================================

st.subheader("📊 Indicadores Principales")

# -------------------------
# FILA 1
# -------------------------

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Caudal Dest.",
        round(float(ultimo["CAUDAL DESTILACIÓN (lt/h)"]), 0)
    )

with c2:
    st.metric(
        "Tipo Aceite",
        str(ultimo["Tipo de aceite"])
    )

with c3:
    st.metric(
        "Extractor",
        round(float(ultimo["EXTRACTOR TEMPERATURA (°C)"]), 1)
    )

with c4:
    st.metric(
        "Densidad",
        round(float(ultimo["DENSIDAD DESTILACIÓN (kg/m3)"]), 1)
    )

with c5:

    tk_destino = str(ultimo["# TK DESTINO CRUDO"])

    espacio = pd.to_numeric(
        ultimo["cm ESPACIO DESTINO CRUDO"],
        errors="coerce"
    )

    st.metric(
        "TK Destino",
        tk_destino
    )

    if pd.isna(espacio):

        st.info("Espacio libre: Sin dato")

    elif espacio < 100:

        st.error(
            f"🚨 Espacio libre: {espacio:.0f} cm"
        )

    else:

        st.success(
            f"✅ Espacio libre: {espacio:.0f} cm"
        )
# -------------------------
# FILA 2
# -------------------------

c7, c8, c9 = st.columns(3)

with c7:
    st.metric(
        "Vacío Extr.",
        valor_seguro("EXTRACTOR VACÍO (mmca)")
    )

with c8:
    st.metric(
        "TKA",
        valor_seguro("TKA SOLVENTE STOCK (lt)")
    )

with c9:
    st.metric(
        "TKB",
        valor_seguro("TKB SOLVENTE STOCK (lt)")
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

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Extractor</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    55 - 62 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Salida Toaster</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    100 - 120 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Gases Toaster</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    75 - 85 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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
# ACEITE MINERAL
# ==========================================

aceite = valor_seguro(
    "ACEITE MINERAL CALENTADOR 121 TEMPERATURA (°C)"
)

with c4:

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Aceite Mineral</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    105 - 112 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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

# ==========================================
# ACEITE ABSORBEDORA
# ==========================================

aceite_abs = valor_seguro(
    "Temperatura de aceite mineral entrada a absorbedora (°C)"
)

with c5:

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Aceite Abs.</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    25 - 31 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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

# ==========================================
# EXPELLER
# ==========================================

temp_expeller = valor_seguro(
    "Temperatura de ingreso de expeller (°C)"
)

with c6:

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Expeller</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    55 - 60 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

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

# ==========================================
# SALIDA TORRE
# ==========================================

temp_torre = valor_seguro(
    "Temperatura agua salida de torre (°C)"
)

with c7:

    st.markdown("""
    <div style="height:75px">
    <b style="font-size:18px">Salida Torre</b><br>
    <span style="color:#7FFF7F;font-size:14px">
    ≤ 26 °C
    </span>
    </div>
    """, unsafe_allow_html=True)

    if temp_torre is None:
        st.warning("Sin dato")
    elif temp_torre <= 26:
        st.success(f"🟢 {temp_torre:.1f} °C")
    elif temp_torre <= 30:
        st.warning(f"🟡 {temp_torre:.1f} °C")
    else:
        st.error(f"🔴 {temp_torre:.1f} °C")
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
