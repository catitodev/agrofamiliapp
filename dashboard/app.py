# Dashboard Streamlit para gestores públicos

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_BASE = "http://backend:8000"

st.set_page_config(
    page_title="AgroFamíliApp - Painel Gestor",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AgroFamíliApp - Painel de Gestão")

st.sidebar.header("Filtros")
date_range = st.sidebar.date_input("Período", [])

try:
    stats = requests.get(f"{API_BASE}/stats", timeout=5).json()
except:
    stats = {"total_interactions": 0, "avg_rating": 0, "agents": {}}

col1, col2, col3 = st.columns(3)
col1.metric("Total de Interações", stats.get("total_interactions", 0))
col2.metric("Avaliação Média", f"{stats.get('avg_rating', 0):.1f}/5")
col3.metric("Agentes Ativos", len(stats.get("agents", {})))

st.subheader("Distribuição por Agente")
if stats.get("agents"):
    df = pd.DataFrame([
        {"Agente": k, "Interações": v}
        for k, v in stats["agents"].items()
    ])
    fig = px.bar(df, x="Agente", y="Interações", color="Agente")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível ainda.")

st.subheader("Interações Recentes")
st.write("O painel mostra dados agregados e anonizados das interações dos agricultores com o sistema.")