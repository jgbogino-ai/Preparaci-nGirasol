import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURACION
# ==================================================

URL = https://docs.google.com/spreadsheets/d/e/2PACX-1vQAJcBxFTNaLQ6cpo7rMLhYSbqpGks79AztDgPULIobXyB1gHMyZI7TOVJg2zm62PJq7CQlN7pMie2N/pub?output=csv

st.set_page_config(
    page_title="extracción",
    page_icon="🏭",
    layout="wide"
)
