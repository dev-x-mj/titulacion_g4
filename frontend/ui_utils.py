import streamlit as st
import pandas as pd
import plotly.express as px

# Diccionario de códigos de estados para el mapa
state_code_map = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
}

# --- Tarjetas KPI  ---
def fancy_metric_card(label, value, help_text, icon="", color="#4CAF50"):
    st.markdown(f"""
    <div style="
        background: {color};
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        min-height: 120px;
    ">
        <h3 style="margin:0; font-size:18px;">{icon} {label}</h3>
        <h2 style="margin:5px 0; font-size: 28px;">{value}</h2>
        <small style="font-size: 14px;">{help_text}</small>
    </div>
    """, unsafe_allow_html=True)

# --- PESTAÑA 1 ---
def display_metrics(metrics, title="Evaluación de Precisión"):
    st.subheader(f"{title}")
    col1, col2 = st.columns(2)
    mape_value = metrics.get('mape', None)
    rmse_value = metrics.get('rmse', None)
    
    mape_display = f"{mape_value:.2f} %" if mape_value is not None else "N/A"
    rmse_display = f"$ {rmse_value:,.2f}" if rmse_value is not None else "N/A"
    
    col1.metric("Error Porcentual (MAPE)", mape_display, help="Mean Absolute Percentage Error.")
    col2.metric("Error Absoluto (RMSE)", rmse_display, help="Root Mean Squared Error.")

def display_forecast_chart_and_table(forecast_data):
    df_history = pd.DataFrame({
        'Date': pd.to_datetime(forecast_data['history']['index']),
        'Ventas Históricas': forecast_data['history']['data']
    })
    
    df_forecast = pd.DataFrame(forecast_data['forecast'])
    if df_forecast.empty:
        st.warning("No hay datos de pronóstico para mostrar.")
        return
        
    df_forecast['Date'] = pd.to_datetime(df_forecast['Date'])
    model_name = forecast_data['model_used']
    forecast_col_name = f"Pronóstico ({model_name})"
    
    df_forecast = df_forecast.rename(columns={'Sales Forecast': forecast_col_name})
    
    # Verificamos si la columna existe Y si tiene algún valor que no sea NaN o None
    has_bounds = 'Lower Bound' in df_forecast.columns and df_forecast['Lower Bound'].notna().any()

    df_history = df_history.set_index('Date')
    df_forecast = df_forecast.set_index('Date')
    
    # Preparar columnas para el GRÁFICO
    chart_cols = ['Ventas Históricas', forecast_col_name]
    if has_bounds:
        chart_cols.extend(['Lower Bound', 'Upper Bound'])
        
    combined_df = pd.concat([df_history, df_forecast[chart_cols[1:]]], axis=1)
    
    st.markdown("### Histórico vs. Pronóstico")
    st.line_chart(combined_df)
    
    st.markdown("### Tabla de Pronóstico Generado (Primeros 12 Períodos)")
    
    table_cols = [forecast_col_name]
    format_dict = {forecast_col_name: '${:,.2f}'}
    
    if has_bounds:
        table_cols.extend(['Lower Bound', 'Upper Bound'])
        format_dict['Lower Bound'] = '${:,.2f}'
        format_dict['Upper Bound'] = '${:,.2f}'
        
    table_df = df_forecast[table_cols].head(12)

    table_df.index = table_df.index.strftime('%Y-%m-%d')
    
    st.dataframe(table_df.style.format(format_dict, na_rep="-"), use_container_width=True)
    
# PESTAÑA 2 
def display_kpi_cards(kpis):
    """
    Renderiza solo las tarjetas de KPIs para la Visión General.
    """
    st.subheader("Indicadores Clave de Rendimiento (Global)")
    
    # Fila 1
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    cards_row1 = [
        (row1_col1, "Total de Ventas", f"${kpis['total_sales']:,.0f}", "Total de Ventas del dataset.", "", "#1E88E5"),
        (row1_col2, "Ganancia Total", f"${kpis['total_profit']:,.0f}", "Ganancia Total del dataset.", " ", "#434047"),
        (row1_col3, "Tasa de Ganancia (%)", f"{kpis['profit_ratio']:.2%}", "Tasa de Ganancia (%) del dataset.", "", "#FDD835")
    ]
    for col, label, value, help_text, icon, color in cards_row1:
        with col:
            fancy_metric_card(label, value, help_text, icon, color)

    # Fila 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    cards_row2 = [
        (row2_col1, "Órdenes Totales", f"{kpis['total_orders']:,}", "Órdenes Totales del dataset.", "", "#1E88E5"),
        (row2_col2, "Ticket Promedio", f"${kpis['avg_ticket']:,.2f}", "Ticket Promedio del dataset.", "", "#434047"),
        (row2_col3, "Descuento Promedio", f"{kpis['avg_discount']:.2%}", "Descuento Promedio del dataset.", "", "#FB8C00")
    ]
    for col, label, value, help_text, icon, color in cards_row2:
        with col:
            fancy_metric_card(label, value, help_text, icon, color)
            
    # Fila 3
    row3_col1, row3_col2 = st.columns(2)
    cards_row3 = [
        (row3_col1, "Tiempo Prom. de Envio", f"{kpis['avg_shipping_time']:.1f} Días", "", "#8E24AA"),
        (row3_col2, "Región con más ventas", kpis['top_region'], "", "#D81B60")
    ]
    for col, label, value, icon, color in cards_row3:
        with col:
            fancy_metric_card(label, value, f"{label} del dataset.", icon, color)

# --- PESTAÑA 3 
def display_detailed_charts(kpis):
    """
    Renderiza todos los mapas y GRÁFICOS para el Análisis Detallado.
    """
    
    # --- Sección 1: Análisis Geográfico (¿Dónde?) ---
    st.subheader("Análisis Geográfico")
    
    # 1. Mapa de rentabilidad 
    profit_state_df = pd.DataFrame(list(kpis['profit_by_state'].items()), columns=['State', 'Profit'])
    profit_state_df['code'] = profit_state_df['State'].map(state_code_map)
    
    fig_map = px.choropleth(
        profit_state_df,
        locations='code',
        locationmode="USA-states",
        color='Profit',
        scope="usa",
        color_continuous_scale=px.colors.diverging.RdYlGn,
        custom_data=['State'] 
    )
    
    fig_map.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>Ganancia: $%{z:,.2f}<extra></extra>")
    fig_map.update_layout(
        title_text="Rentabilidad por Estado",
        title_x=0.35,
        geo=dict(lakecolor='rgb(255,255,255)'),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    st.plotly_chart(fig_map, use_container_width=True)
        
    # 2. Gráfico de Anillo: Participación por Región 
    df_region = pd.DataFrame(list(kpis['sales_by_region'].items()), columns=['Región', 'Ventas'])
    
    fig_region_donut = px.pie(
        df_region, 
        names='Región', 
        values='Ventas', 
        title='Participación por Región', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_region_donut.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Ventas: $%{value:,.2f}<br>%{percent} del total<extra></extra>"
    )
    st.plotly_chart(fig_region_donut, use_container_width=True)

    # Gráficos de Barras para Estados
    col1, col2 = st.columns(2)
    top_state_df = pd.DataFrame(
        sorted(kpis['profit_by_state'].items(), key=lambda x: x[1], reverse=True)[:5],
        columns=['Estado', 'Ganancia']
    )
    bottom_state_df = pd.DataFrame(
        sorted(kpis['profit_by_state'].items(), key=lambda x: x[1])[:5],
        columns=['Estado', 'Ganancia']
    )
    with col1:
        fig_top_states = px.bar(
            top_state_df.sort_values('Ganancia', ascending=True), 
            x='Ganancia', 
            y='Estado', 
            orientation='h', 
            title='Top 5 Estados Más Rentables',
            color='Ganancia', 
            color_continuous_scale='Greens'
        )
        fig_top_states.update_traces(hovertemplate="<b>%{y}</b><br>Ganancia: $%{x:,.2f}<extra></extra>")
        fig_top_states.update_layout(yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
        st.plotly_chart(fig_top_states, use_container_width=True)
        
    with col2:
        fig_bottom_states = px.bar(
            bottom_state_df.sort_values('Ganancia', ascending=False), 
            x='Ganancia', 
            y='Estado', 
            orientation='h', 
            title='Top 5 Estados Menos Rentables',
            color='Ganancia', 
            color_continuous_scale='Reds_r'
        )
        fig_bottom_states.update_traces(hovertemplate="<b>%{y}</b><br>Ganancia: $%{x:,.2f}<extra></extra>")
        fig_bottom_states.update_layout(yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
        st.plotly_chart(fig_bottom_states, use_container_width=True)

    st.divider()

    # --- Sección 2: Análisis de Producto ---
    st.subheader("Rentabilidad por Producto")
    
    # Gráficos de Barras para Productos
    df_top_prod = pd.DataFrame(list(kpis['top_10_products_profit'].items()), columns=['Producto', 'Ganancia'])
    fig_top_prod = px.bar(
        df_top_prod.sort_values('Ganancia', ascending=True), 
        x='Ganancia', 
        y='Producto', 
        orientation='h', 
        title='Top 10 Productos Más Rentables',
        color='Ganancia', 
        color_continuous_scale='Greens',
        height=400
    )
    fig_top_prod.update_traces(hovertemplate="<b>%{y}</b><br>Ganancia: $%{x:,.2f}<extra></extra>")
    fig_top_prod.update_layout(yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
    st.plotly_chart(fig_top_prod, use_container_width=True)

    df_bottom_prod = pd.DataFrame(list(kpis['bottom_10_products_profit'].items()), columns=['Producto', 'Ganancia'])
    fig_bottom_prod = px.bar(
        df_bottom_prod.sort_values('Ganancia', ascending=False), 
        x='Ganancia', 
        y='Producto', 
        orientation='h', 
        title='Top 10 Productos Menos Rentables',
        color='Ganancia', 
        color_continuous_scale='Reds_r',
        height=400
    )
    fig_bottom_prod.update_traces(hovertemplate="<b>%{y}</b><br>Ganancia: $%{x:,.2f}<extra></extra>")
    fig_bottom_prod.update_layout(yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
    st.plotly_chart(fig_bottom_prod, use_container_width=True)

    st.divider()

    # --- Sección 3: Análisis de Categoría ---
    st.subheader("Análisis de Categoría")
    
    # Gráfico de Anillo para Ventas por Categoría
    df_cat = pd.DataFrame(list(kpis['sales_by_category'].items()), columns=['Categoría', 'Ventas'])
    fig_cat_donut = px.pie(
        df_cat, 
        names='Categoría', 
        values='Ventas', 
        title='Ventas por Categoría', 
        hole=0.4
    )
    fig_cat_donut.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Ventas: $%{value:,.2f}<br>%{percent} del total<extra></extra>"
    )
    st.plotly_chart(fig_cat_donut, use_container_width=True)
    
    # Gráfico de Barras para Ganancia por Subcategoría
    df_sub = pd.DataFrame(list(kpis['profit_by_subcategory'].items()), columns=['Subcategoría', 'Ganancia'])
    df_sub_sorted = df_sub.sort_values('Ganancia', ascending=True)
    fig_sub_bar = px.bar(
        df_sub_sorted, 
        x='Ganancia', 
        y='Subcategoría', 
        orientation='h', 
        title='Ganancia por Subcategoría',
        color='Ganancia',
        color_continuous_scale='RdYlGn',
        height=600
    )
    fig_sub_bar.update_traces(hovertemplate="<b>%{y}</b><br>Ganancia: $%{x:,.2f}<extra></extra>")
    fig_sub_bar.update_layout(yaxis_title=None, xaxis_title=None)
    st.plotly_chart(fig_sub_bar, use_container_width=True)