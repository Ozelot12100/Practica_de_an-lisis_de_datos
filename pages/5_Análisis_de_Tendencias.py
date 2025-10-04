import streamlit as st
import plotly.express as px
import pandas as pd
from db_logic import ejecutar_consulta
import queries

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Tendencias", layout="wide")

# --- Título y Cabecera ---
st.title("📈 Análisis de Tendencias de Ventas")
st.markdown("Visualiza el rendimiento del negocio a lo largo del tiempo para identificar patrones y estacionalidad.")

# --- Cargar Datos para los Gráficos ---
df_ventas_mensuales = ejecutar_consulta(queries.ventas_mensuales)
df_ventas_categoria_mes = ejecutar_consulta(queries.ventas_categoria_por_mes)

# --- Gráfico 1: Tendencia de Ingresos Mensuales ---
st.header("Evolución de Ingresos Mensuales")

if not df_ventas_mensuales.empty:
    # Aseguramos que la columna de fecha esté en el formato correcto para ordenar
    df_ventas_mensuales['anio_mes'] = pd.to_datetime(df_ventas_mensuales['anio_mes']).dt.strftime('%Y-%m')
    df_ventas_mensuales = df_ventas_mensuales.sort_values('anio_mes')

    fig_ingresos = px.line(
        df_ventas_mensuales,
        x='anio_mes',
        y='ingresos_mensuales',
        title="Ingresos Totales Mes a Mes",
        markers=True,
        labels={"anio_mes": "Mes", "ingresos_mensuales": "Ingresos ($)"}
    )
    fig_ingresos.update_traces(line=dict(width=3))
    st.plotly_chart(fig_ingresos, use_container_width=True)
else:
    st.info("No hay suficientes datos de ventas para mostrar una tendencia mensual.")

st.markdown("---")

# --- Gráfico 2: Desglose de Ventas por Categoría a lo largo del Tiempo ---
st.header("Rendimiento de Categorías a lo largo del Tiempo")

if not df_ventas_categoria_mes.empty:
    # Aseguramos que la columna de fecha esté en el formato correcto
    df_ventas_categoria_mes['anio_mes'] = pd.to_datetime(df_ventas_categoria_mes['anio_mes']).dt.strftime('%Y-%m')
    df_ventas_categoria_mes = df_ventas_categoria_mes.sort_values('anio_mes')
    
    fig_categorias = px.bar(
        df_ventas_categoria_mes,
        x='anio_mes',
        y='cantidad_vendida',
        color='categoria',
        title="Unidades Vendidas por Categoría Mes a Mes",
        labels={"anio_mes": "Mes", "cantidad_vendida": "Unidades Vendidas", "categoria": "Categoría"}
    )
    st.plotly_chart(fig_categorias, use_container_width=True)
else:
    st.info("No hay suficientes datos de ventas por categoría para mostrar una tendencia.")