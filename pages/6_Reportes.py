# pages/6_Reportes.py

import streamlit as st
from db_logic import ejecutar_consulta
import queries
import report_generator

# --- Configuración de la Página ---
st.set_page_config(page_title="Centro de Reportes", layout="wide")
st.title("📄 Centro de Descarga de Reportes")
st.markdown("Selecciona y descarga los informes que necesites en el formato que desees.")

# --- Función Reutilizable para Crear Secciones ---
# --- CAMBIO CLAVE: Se elimina el decorador @st.cache_data de esta función ---
def crear_seccion_reporte(titulo, descripcion, df_datos, nombre_archivo_base):
    """
    Dibuja una sección completa de reporte con vista previa y botones de descarga.
    Esta función se dedica solo a la INTERFAZ, por lo que no debe estar en caché.
    """
    st.header(titulo)
    st.write(descripcion)
    
    if df_datos.empty:
        st.info("No hay datos disponibles para generar este reporte.")
        return

    st.dataframe(df_datos.head())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
           f"📥 Descargar como CSV", data=report_generator.convertir_df_a_csv(df_datos),
           file_name=f'{nombre_archivo_base}.csv', mime='text/csv', key=f'csv_{nombre_archivo_base}'
        )
    with col2:
        st.download_button(
           f"📊 Descargar como Excel", data=report_generator.convertir_df_a_excel(df_datos),
           file_name=f'{nombre_archivo_base}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key=f'xlsx_{nombre_archivo_base}'
        )
    with col3:
        st.download_button(
           f"📋 Descargar como PDF", data=report_generator.convertir_df_a_pdf(df_datos, titulo),
           file_name=f'{nombre_archivo_base}.pdf', mime='application/pdf', key=f'pdf_{nombre_archivo_base}'
        )

# --- Carga de Todos los Datos para los Reportes ---
# La eficiencia se mantiene porque la función ejecutar_consulta SÍ está en caché en db_logic.py
df_ventas = ejecutar_consulta(queries.select_all_ventas)
df_resumen_categoria = ejecutar_consulta(queries.resumen_ventas_por_categoria)
df_clientes = ejecutar_consulta(queries.select_all_clientes)
df_clientes_vip = ejecutar_consulta(queries.reporte_clientes_vip)
df_productos_estancados = ejecutar_consulta(queries.reporte_productos_estancados)

# --- Construcción de la Página ---
# Ahora llamamos a la función sin caché, que dibujará los botones correctamente en cada ejecución.

crear_seccion_reporte(
    titulo="Reporte de Clientes VIP",
    descripcion="Top 10 clientes ordenados por el monto total de sus compras.",
    df_datos=df_clientes_vip,
    nombre_archivo_base="reporte_clientes_vip"
)
st.markdown("---")

crear_seccion_reporte(
    titulo="Reporte de Productos Estancados",
    descripcion="Lista de productos sin ventas en los últimos 6 meses.",
    df_datos=df_productos_estancados,
    nombre_archivo_base="reporte_productos_estancados"
)
st.markdown("---")

crear_seccion_reporte(
    titulo="Historial de Ventas Detallado",
    descripcion="Contiene el detalle de cada transacción.",
    df_datos=df_ventas,
    nombre_archivo_base="historial_ventas"
)
st.markdown("---")

crear_seccion_reporte(
    titulo="Resumen de Ventas por Categoría",
    descripcion="Agrupa las ventas totales por categoría de producto.",
    df_datos=df_resumen_categoria,
    nombre_archivo_base="resumen_ventas_categoria"
)
st.markdown("---")

crear_seccion_reporte(
    titulo="Lista de Clientes",
    descripcion="Contiene la información de todos los clientes registrados.",
    df_datos=df_clientes,
    nombre_archivo_base="lista_clientes"
)