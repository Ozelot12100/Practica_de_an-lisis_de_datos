import streamlit as st
from db_logic import ejecutar_comando, ejecutar_consulta
import queries
import pandas as pd # Necesitamos pandas para manejar las fechas

# --- Configuración de la Página ---
st.set_page_config(page_title="Registro de Ventas", layout="wide")

# --- Bloque de Notificaciones ---
if 'mensaje_toast' in st.session_state:
    st.toast(st.session_state.mensaje_toast['mensaje'], icon=st.session_state.mensaje_toast['icono'])
    del st.session_state.mensaje_toast

# --- Título y Cabecera ---
st.title("💸 Registro de Ventas")
st.markdown("Registra nuevas ventas y consulta el historial de transacciones.")

# --- Cargar Datos Necesarios para los Formularios ---
# Obtenemos los clientes y productos para usarlos en los selectbox
df_clientes = ejecutar_consulta(queries.select_all_clientes)
df_productos = ejecutar_consulta("SELECT * FROM Productos ORDER BY nombre ASC")


# --- Interfaz de Registro de Venta ---
st.header("➕ Registrar Nueva Venta")

with st.form("nueva_venta_form", clear_on_submit=True):
    # Creamos listas desplegables (selectbox) con los clientes y productos existentes
    cliente_seleccionado_id = st.selectbox(
        "Selecciona un Cliente:",
        options=df_clientes['ID'],
        format_func=lambda x: f"ID:{x} - {df_clientes.loc[df_clientes['ID'] == x, 'nombre'].iloc[0]}"
    )
    
    producto_seleccionado_id = st.selectbox(
        "Selecciona un Producto:",
        options=df_productos['ID'],
        format_func=lambda x: f"ID:{x} - {df_productos.loc[df_productos['ID'] == x, 'nombre'].iloc[0]}"
    )

    cantidad = st.number_input("Cantidad Vendida", min_value=1, step=1)
    fecha_venta = st.date_input("Fecha de la Venta")
    
    if st.form_submit_button("Registrar Venta"):
        if cliente_seleccionado_id and producto_seleccionado_id and cantidad > 0:
            valores = (int(cliente_seleccionado_id), int(producto_seleccionado_id), cantidad, fecha_venta)
            if ejecutar_comando(queries.insert_venta, valores):
                st.session_state.mensaje_toast = {"mensaje": "¡Venta registrada con éxito!", "icono": "🎉"}
                st.rerun()
        else:
            st.warning("Todos los campos son obligatorios.")

st.markdown("---")

# --- LEER (Read): Historial de Ventas ---
st.header("📖 Historial de Transacciones")
df_ventas = ejecutar_consulta(queries.select_all_ventas)

# Formateamos las columnas para mejor visualización
df_ventas_display = df_ventas.copy()
df_ventas_display['total_venta'] = df_ventas_display['total_venta'].apply(lambda x: f"${x:,.2f}")
df_ventas_display['precio'] = df_ventas_display['precio'].apply(lambda x: f"${x:,.2f}")

st.dataframe(df_ventas_display, use_container_width=True, hide_index=True)

# --- BORRAR (Delete) ---
st.markdown("---")
st.header("❌ Cancelar una Venta")
if not df_ventas.empty:
    venta_a_borrar_id = st.selectbox(
        "Selecciona una venta para cancelar (por su ID de transacción):",
        options=df_ventas['ID']
    )
    
    if st.button("Cancelar Venta Seleccionada", type="primary"):
        if ejecutar_comando(queries.delete_venta, (int(venta_a_borrar_id),)):
            st.session_state.mensaje_toast = {"mensaje": f"¡Venta ID {venta_a_borrar_id} cancelada!", "icono": "🗑️"}
            st.rerun()
else:
    st.info("No hay ventas registradas para cancelar.")