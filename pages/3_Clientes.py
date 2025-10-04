import streamlit as st
from db_logic import ejecutar_comando, ejecutar_consulta
import queries

# --- Configuración de la Página ---
st.set_page_config(page_title="Gestión de Clientes", layout="wide")

# --- Bloque de Notificaciones ---
if 'mensaje_toast' in st.session_state:
    st.toast(st.session_state.mensaje_toast['mensaje'], icon=st.session_state.mensaje_toast['icono'])
    del st.session_state.mensaje_toast

# --- Título y Cabecera ---
st.title("👥 Gestión de Clientes")
st.markdown("Añade, actualiza, consulta y borra los clientes de la base de datos.")

# --- LEER (Read) ---
st.header("Listado de Clientes")
df_clientes = ejecutar_consulta(queries.select_all_clientes)
st.dataframe(df_clientes, use_container_width=True, hide_index=True)

st.markdown("---")

# --- Interfaz de Creación y Actualización ---
col1, col2 = st.columns(2)

with col1:
    st.header("➕ Añadir Nuevo Cliente")
    with st.form("nuevo_cliente_form", clear_on_submit=True):
        nombre = st.text_input("Nombre Completo")
        ciudad = st.text_input("Ciudad")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
        
        if st.form_submit_button("Añadir Cliente"):
            if nombre and ciudad:
                valores = (nombre, ciudad, edad, sexo)
                if ejecutar_comando(queries.insert_cliente, valores):
                    st.session_state.mensaje_toast = {"mensaje": "¡Cliente añadido!", "icono": "✅"}
                    st.rerun()
            else:
                st.warning("Nombre y Ciudad son campos obligatorios.")

with col2:
    st.header("✏️ Modificar Cliente Existente")
    if not df_clientes.empty:
        cliente_a_modificar_id = st.selectbox(
            "Selecciona un cliente a modificar:",
            options=df_clientes['ID'],
            format_func=lambda x: f"ID:{x} - {df_clientes.loc[df_clientes['ID'] == x, 'nombre'].iloc[0]}"
        )
        cliente_actual = df_clientes.loc[df_clientes['ID'] == cliente_a_modificar_id].iloc[0]
        
        with st.form("modificar_cliente_form"):
            nombre_mod = st.text_input("Nombre Completo", value=cliente_actual['nombre'])
            ciudad_mod = st.text_input("Ciudad", value=cliente_actual['ciudad'])
            edad_mod = st.number_input("Edad", min_value=0, max_value=120, step=1, value=int(cliente_actual['edad']))
            
            # Para el selectbox, necesitamos encontrar el índice de la opción actual
            sexo_options = ["Masculino", "Femenino", "Otro"]
            try:
                sexo_index = sexo_options.index(cliente_actual['sexo'])
            except ValueError:
                sexo_index = 0
            
            sexo_mod = st.selectbox("Sexo", sexo_options, index=sexo_index)

            if st.form_submit_button("Actualizar Cliente"):
                valores = (nombre_mod, ciudad_mod, edad_mod, sexo_mod, int(cliente_a_modificar_id))
                if ejecutar_comando(queries.update_cliente, valores):
                    st.session_state.mensaje_toast = {"mensaje": "¡Cliente actualizado!", "icono": "✏️"}
                    st.rerun()
    else:
        st.info("No hay clientes para modificar.")

# --- BORRAR (Delete) ---
st.markdown("---")
st.header("❌ Borrar Cliente")
if not df_clientes.empty:
    cliente_a_borrar_id = st.selectbox(
        "Selecciona un cliente a borrar:",
        options=df_clientes['ID'],
        format_func=lambda x: f"ID:{x} - {df_clientes.loc[df_clientes['ID'] == x, 'nombre'].iloc[0]}",
        key="borrar_select"
    )
    if st.button("Borrar Cliente Seleccionado", type="primary"):
        if ejecutar_comando(queries.delete_cliente, (int(cliente_a_borrar_id),)):
            st.session_state.mensaje_toast = {"mensaje": "¡Cliente borrado!", "icono": "🗑️"}
            st.rerun()
else:
    st.info("No hay clientes para borrar.")