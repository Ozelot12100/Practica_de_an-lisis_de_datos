import streamlit as st
from db_logic import ejecutar_comando, ejecutar_consulta

# --- Configuración de la Página ---
st.set_page_config(page_title="Catálogo de Productos", layout="wide")

# --- BLOQUE DE NOTIFICACIONES ---
# Este es el cambio clave. Revisa la memoria en cada recarga.
if 'mensaje_toast' in st.session_state:
    st.toast(st.session_state.mensaje_toast['mensaje'], icon=st.session_state.mensaje_toast['icono'])
    del st.session_state.mensaje_toast

# --- Título y Cabecera ---
st.title("📦 Gestión de Catálogo de Productos")
st.markdown("Crea, actualiza, lee y borra los productos de la base de datos.")

# --- LEER (Read) ---
st.header("Lista de Productos Actuales")
df_productos = ejecutar_consulta("SELECT * FROM Productos ORDER BY ID ASC")
st.dataframe(df_productos, use_container_width=True, hide_index=True)

st.markdown("---")

# --- Interfaz de Creación y Actualización ---
col1, col2 = st.columns(2)

with col1:
    st.header("➕ Añadir Nuevo Producto")
    with st.form("nuevo_producto_form", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre del Producto", placeholder="Ej: Monitor Curvo 4K")
        nueva_categoria = st.text_input("Categoría", placeholder="Ej: Monitores")
        nuevo_precio = st.number_input("Precio", min_value=0.01, format="%.2f")
        
        if st.form_submit_button("Añadir Producto"):
            if nuevo_nombre and nueva_categoria and nuevo_precio > 0:
                sql = "INSERT INTO Productos (nombre, categoria, precio) VALUES (%s, %s, %s)"
                if ejecutar_comando(sql, (nuevo_nombre, nueva_categoria, nuevo_precio)):
                    # Guardamos el mensaje y el icono en la memoria.
                    st.session_state.mensaje_toast = {
                        "mensaje": "¡Producto añadido con éxito!",
                        "icono": "✅"
                    }
                    st.rerun()
            else:
                st.warning("Todos los campos son obligatorios.")

with col2:
    st.header("✏️ Modificar Producto Existente")
    if not df_productos.empty:
        producto_a_modificar_id = st.selectbox(
            "Selecciona un producto a modificar:",
            options=df_productos['ID'],
            format_func=lambda x: f"ID:{x} - {df_productos.loc[df_productos['ID'] == x, 'nombre'].iloc[0]}"
        )
        producto_actual = df_productos.loc[df_productos['ID'] == producto_a_modificar_id].iloc[0]
        
        with st.form("modificar_producto_form"):
            nuevo_nombre_mod = st.text_input("Nuevo Nombre", value=producto_actual['nombre'])
            nueva_categoria_mod = st.text_input("Nueva Categoría", value=producto_actual['categoria'])
            nuevo_precio_mod = st.number_input("Nuevo Precio", value=float(producto_actual['precio']), format="%.2f")

            if st.form_submit_button("Actualizar Producto"):
                sql = "UPDATE Productos SET nombre=%s, categoria=%s, precio=%s WHERE ID=%s"
                valores = (nuevo_nombre_mod, nueva_categoria_mod, nuevo_precio_mod, int(producto_a_modificar_id))
                if ejecutar_comando(sql, valores):
                    st.session_state.mensaje_toast = {
                        "mensaje": f"¡Producto ID {producto_a_modificar_id} actualizado!",
                        "icono": "✏️"
                    }
                    st.rerun()
    else:
        st.info("No hay productos para modificar.")

# --- BORRAR (Delete) ---
st.markdown("---")
st.header("❌ Borrar Producto")
if not df_productos.empty:
    producto_a_borrar_id = st.selectbox(
        "Selecciona un producto a borrar:",
        options=df_productos['ID'],
        format_func=lambda x: f"ID:{x} - {df_productos.loc[df_productos['ID'] == x, 'nombre'].iloc[0]}",
        key="borrar_select"
    )
    if st.button("Borrar Producto Seleccionado", type="primary"):
        sql = "DELETE FROM Productos WHERE ID = %s"
        if ejecutar_comando(sql, (int(producto_a_borrar_id),)):
            st.session_state.mensaje_toast = {
                "mensaje": f"¡Producto ID {producto_a_borrar_id} borrado!",
                "icono": "🗑️"
            }
            st.rerun()
else:
    st.info("No hay productos para borrar.")