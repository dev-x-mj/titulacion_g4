# Contenido para: backend/services/kpi_service.py

import pandas as pd

def calculate_global_kpis(df):
    """
    Calcula KPIs clave de rendimiento a nivel global y detallado.
    """
    if df is None or df.empty:
        return {}

    # --- KPIs financieros ---
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df.shape[0]
    avg_discount = df['Discount'].mean()
    profit_ratio = total_profit / total_sales if total_sales != 0 else 0
    avg_ticket = total_sales / max(1, total_orders)

    # --- KPIs logísticos ---
    df['Shipping_Time'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    avg_shipping_time = df['Shipping_Time'].mean()
    pct_late_shipments = (df['Shipping_Time'] > 7).mean() * 100

    # --- KPIs geográficos ---
    profit_by_state = df.groupby('State')['Profit'].sum().to_dict()
    sales_by_region = df.groupby('Region')['Sales'].sum().to_dict()
    top_region = max(sales_by_region, key=sales_by_region.get) if sales_by_region else "N/A"
    bottom_region = min(sales_by_region, key=sales_by_region.get) if sales_by_region else "N/A"

    # --- KPIs de producto ---
    product_profit = df.groupby('Product_Name')['Profit'].sum().sort_values(ascending=False)
    top_10_products_profit = product_profit.head(10).to_dict()
    bottom_10_products_profit = product_profit.tail(10).sort_values(ascending=True).to_dict()

    # --- KPIs por categoría/segmento/subcategoría ---
    sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False).to_dict()
    sales_by_segment = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False).to_dict()
    profit_by_subcategory = df.groupby('Sub_Category')['Profit'].sum().sort_values(ascending=False).to_dict()

    return {
        # Financieros
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "avg_discount": avg_discount,
        "profit_ratio": profit_ratio,
        "avg_ticket": avg_ticket,
        # Logistica
        "avg_shipping_time": avg_shipping_time,
        "pct_late_shipments": pct_late_shipments,
        # Geografía
        "profit_by_state": profit_by_state,
        "sales_by_region": sales_by_region,
        "top_region": top_region,
        "bottom_region": bottom_region,
        # Producto
        "top_10_products_profit": top_10_products_profit,
        "bottom_10_products_profit": bottom_10_products_profit,
        # Categoría/Segmento/Subcategoría
        "sales_by_category": sales_by_category,
        "sales_by_segment": sales_by_segment,
        "profit_by_subcategory": profit_by_subcategory
    }

def get_regional_analysis(df):
    """
    Calcula las ventas por región y devuelve la mejor región.
    """
    if df is None or df.empty:
        return {"top_region": "N/A", "top_sales": 0, "sales_by_region": {}}
    
    regional_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    
    if regional_sales.empty:
        return {"top_region": "N/A", "top_sales": 0, "sales_by_region": {}}

    top_region = regional_sales.idxmax()
    top_sales = regional_sales.max()
    sales_by_region_dict = regional_sales.to_dict()
    
    return {
        "top_region": top_region,
        "top_sales": top_sales,
        "sales_by_region": sales_by_region_dict
    }