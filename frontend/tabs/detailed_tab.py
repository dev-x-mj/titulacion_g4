# Contenido para: frontend/tabs/detailed_tab.py

import streamlit as st
from api_client import fetch_global_kpis
from ui_utils import display_detailed_charts # <-- ¡Cambiado!

def render_detailed_tab():
    """
    Renderiza la pestaña de Análisis Detallado.
    """
    st.title("📈 Análisis Detallado (Mapas y Tablas)")
    st.markdown("Análisis profundo de geografía, productos y categorías.")
    
    kpi_response = fetch_global_kpis()
    
    if kpi_response and kpi_response.get("status") == "success":
        # ¡Cambiado! Solo pasamos los KPIs a la función de gráficos
        display_detailed_charts(kpi_response['kpis'])
    else:
        st.warning("No se pudieron cargar los datos detallados. Verifique que el API esté activo.")