import streamlit as st
from api_client import fetch_global_kpis
from ui_utils import display_detailed_charts 
def render_detailed_tab():
    """
    Renderiza la pestaña de Análisis Detallado.
    """
    st.title("Análisis Detallado del Negocio")
    st.markdown("Visión profunda de rentabilidad por geografía, productos y segmentos.")
    
    kpi_response = fetch_global_kpis()
    
    if kpi_response and kpi_response.get("status") == "success":
       
        display_detailed_charts(kpi_response['kpis'])
    else:
        st.warning("No se pudieron cargar los datos detallados. Verifique que el API esté activo.")