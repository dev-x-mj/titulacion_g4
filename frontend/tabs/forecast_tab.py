import streamlit as st
# Importamos desde los otros archivos del frontend 
from api_client import fetch_forecast
from ui_utils import display_metrics, display_forecast_chart_and_table

def render_forecast_tab(config):
    """
    Renderiza la pestaña de Pronóstico de Ventas.
    """
    st.title(" Demand Planning: Dashboard de Pronóstico de Ventas")

    # --- Sidebar de Filtros ---
    st.sidebar.header("Configuración del Pronóstico")
    
    model_options = ["SARIMA", "XGBoost"]
    selected_model = st.sidebar.selectbox("Modelo de Pronóstico:", model_options)
    
    # Lógica de Frecuencias
    all_freqs = config.get("frequencies", {"Mensual (ME)": "ME"})
    forecast_freqs = {key: val for key, val in all_freqs.items() if val != "AE"} # Excluir Anual
    freq_names = list(forecast_freqs.keys())
    freq_codes = forecast_freqs
    selected_freq_name = st.sidebar.selectbox("Frecuencia de Análisis:", freq_names)
    selected_freq_code = freq_codes[selected_freq_name]
    
    # Filtros de Categoría y Región
    category_options = config.get("categories", [])
    selected_category = st.sidebar.selectbox("Categoría:", category_options, index=0)
    
    region_options = config.get("regions", [])
    selected_region = st.sidebar.selectbox("Región:", region_options, index=0)
    
    # Slider de Horizonte (dinámico)
    if selected_freq_name == "Mensual (ME)":
        min_val, max_val, def_val = 1, 36, 12
    elif selected_freq_name == "Trimestral (QE)":
        min_val, max_val, def_val = 1, 8, 4
    else: # Por si acaso
        min_val, max_val, def_val = 1, 3, 2
        
    forecast_steps = st.sidebar.slider(
        'Horizonte de Pronóstico (Períodos):',
        min_value=min_val,
        max_value=max_val,
        value=def_val,
        step=1
    )
    
    # Botón para ejecutar
    if st.sidebar.button("Generar Pronóstico y Evaluación", type="primary"):
        with st.spinner(f"Calculando pronóstico ({selected_freq_name}) con {selected_model}..."):
            forecast_result = fetch_forecast(
                selected_category,
                selected_region,
                selected_model,
                forecast_steps,
                selected_freq_code
            )
        
        if forecast_result:
            st.session_state['forecast_data'] = forecast_result
            st.success("Pronóstico generado y validado con éxito.")
        else:
            st.session_state['forecast_data'] = None # Limpiar en caso de error
            
    # --- Área de Resultados ---
    if st.session_state.get('forecast_data') and st.session_state['forecast_data']['status'] == "success":
        data = st.session_state['forecast_data']
        st.divider()
        display_metrics(data['metrics'], f"Evaluación de Precisión ({selected_model})")
        display_forecast_chart_and_table(data)
        
        if selected_model == "XGBoost":
            st.info("💡 **Nota:** XGBoost no calcula intervalos de confianza por defecto.")
            
    elif st.session_state.get('forecast_data') is None:
        st.info("Seleccione los filtros y haga clic en 'Generar Pronóstico' para comenzar el análisis.")