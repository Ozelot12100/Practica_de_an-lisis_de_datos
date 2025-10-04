import streamlit as st
import plotly.express as px
import queries
from db_logic import ejecutar_consulta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

# --- Título del Dashboard ---
st.title("📊 Dashboard de Marketing y Ventas")

# --- Carga de Datos ---
@st.cache_data
def cargar_datos_dashboard():
    """Ejecuta todas las consultas del dashboard y las devuelve en un diccionario."""
    datos = {
        "ingresos": ejecutar_consulta(queries.ingresos_anuales),
        "ciudad": ejecutar_consulta(queries.clientes_por_ciudad),
        "sexo": ejecutar_consulta(queries.clientes_por_sexo),
        "top_productos": ejecutar_consulta(queries.top_productos_vendidos),
        "categoria": ejecutar_consulta(queries.ingresos_por_categoria)
    }
    return datos

# Cargamos los datos
datos_dashboard = cargar_datos_dashboard()
df_ingresos = datos_dashboard["ingresos"]
df_ciudad = datos_dashboard["ciudad"]
df_sexo = datos_dashboard["sexo"]
df_top_productos = datos_dashboard["top_productos"]
df_categoria = datos_dashboard["categoria"]

# --- Preparar los KPIs ---
ingresos_totales = df_ingresos['ingresos_totales'].iloc[0] if not df_ingresos.empty else 0
producto_estrella_nombre = df_top_productos['nombre'].iloc[0] if not df_top_productos.empty else "N/A"
producto_estrella_cantidad = df_top_productos['total_unidades_vendidas'].iloc[0] if not df_top_productos.empty else 0
ciudad_principal_nombre = df_ciudad['ciudad'].iloc[0] if not df_ciudad.empty else "N/A"
ciudad_principal_clientes = df_ciudad['numero_de_clientes'].iloc[0] if not df_ciudad.empty else 0

# --- Visualización del Dashboard ---
st.header("Resumen General ✨")

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales (2025)", f"${ingresos_totales:,.2f}")
col2.metric("Producto Estrella", producto_estrella_nombre, f"{int(producto_estrella_cantidad)} unidades")
col3.metric("Ciudad Principal", ciudad_principal_nombre, f"{ciudad_principal_clientes} clientes")

st.markdown("---")

# --- Análisis Gráfico ---
st.header("Análisis Gráfico para Marketing 📈")

# Top productos
st.subheader("🏆 Top 5 Productos más Vendidos")
fig_productos = px.bar(
    df_top_productos, x='total_unidades_vendidas', y='nombre', orientation='h',
    title='Unidades Vendidas por Producto',
    labels={'total_unidades_vendidas': 'Total Unidades', 'nombre': 'Producto'},
    color='nombre'
)
st.plotly_chart(fig_productos, use_container_width=True)

# Distribución por sexo
st.subheader("👥 Distribución de Clientes por Sexo")
fig_sexo = px.pie(
    df_sexo, names='sexo', values='total', title='Porcentaje de Clientes por Sexo',
    color='sexo', color_discrete_map={'Masculino': '#1f77b4', 'Femenino': '#ff7f0e'}
)
st.plotly_chart(fig_sexo, use_container_width=True)

# Clientes por ciudad
st.subheader("🗺️ Clientes por Ciudad")
fig_ciudad = px.bar(
    df_ciudad, x='ciudad', y='numero_de_clientes', title='Número de Clientes por Ciudad',
    labels={'numero_de_clientes': 'Número de Clientes', 'ciudad': 'Ciudad'},
    color='ciudad'
)
st.plotly_chart(fig_ciudad, use_container_width=True)

st.markdown("---")

# --- Análisis Adicional ---
st.header("Análisis Adicional 🔎")
st.subheader("💰 Ingresos por Categoría de Producto")
fig_categoria = px.bar(
    df_categoria, x='total_ventas', y='categoria', orientation='h',
    title='Ingresos Generados por Categoría',
    labels={'total_ventas': 'Ingresos ($)', 'categoria': 'Categoría'},
    color='categoria'
)
st.plotly_chart(fig_categoria, use_container_width=True)
