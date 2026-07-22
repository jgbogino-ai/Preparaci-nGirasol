import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?output=csv"

st.set_page_config(
    page_title="Preparación Girasol",
    page_icon="🌻",
    layout="wide"
)

st.title("🌻 Dashboard Preparación de Girasol")

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL)

df = cargar_datos()

st.success("Datos actualizados automáticamente desde Google Sheets")

st.subheader("Últimos registros")
st.dataframe(df.tail(10))

# Operadores

if "Operador" in df.columns:

    operadores = (
        df.groupby("Operador")
        .size()
        .reset_index(name="Registros")
        .sort_values("Registros", ascending=False)
    )

    st.subheader("Participación por operador")

    fig = px.pie(
        operadores,
        values="Registros",
        names="Operador",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Registros por operador")

    fig2 = px.bar(
        operadores,
        x="Operador",
        y="Registros",
        color="Registros"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(operadores)

st.info("Versión inicial del Dashboard")
