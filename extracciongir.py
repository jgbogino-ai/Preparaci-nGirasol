import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Extracción Girasol",
    page_icon="🌻",
    layout="wide"
)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?gid=884320541&single=true&output=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL)

df = cargar_datos()

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(r"\s+", " ", regex=True)

st.title("🌻 Dashboard Extracción Girasol")

st.success("Conexión exitosa")

st.subheader("Columnas detectadas")

st.write(df.columns.tolist())

st.subheader("Últimos registros")

st.dataframe(df.tail(10), use_container_width=True)
