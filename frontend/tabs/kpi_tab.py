import streamlit as st
from api_client import fetch_global_kpis
from ui_utils import display_kpi_cards 

def render_kpi_tab():
    """
    Renderiza la pestaña de KPIs Globales.
    """
    st.title(" Visión General (KPIs)")
    st.markdown("Métricas clave de rendimiento (KPIs) a nivel de todo el dataset, sin filtros.")
    
    kpi_response = fetch_global_kpis()
    
    if kpi_response and kpi_response.get("status") == "success":
        
        display_kpi_cards(kpi_response['kpis'])
    else:
        st.warning("No se pudieron cargar los KPIs globales. Verifique que el API esté activo.")