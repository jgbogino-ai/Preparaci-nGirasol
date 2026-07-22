import streamlit as st
import pandas as pd

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?output=csv"

st.set_page_config(layout="wide")

st.title("Diagnóstico de Columnas")

df = pd.read_csv(URL)

st.subheader("Columnas detectadas")

for i, col in enumerate(df.columns):
    st.write(f"{i} - {col}")

st.subheader("Primer registro")

st.dataframe(df.head(1))
