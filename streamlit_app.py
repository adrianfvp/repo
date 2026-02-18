import streamlit as st
import time

# Configuración de marca para LA GRULLA
st.set_page_config(page_title="LA GRULLA - Pomodoro", page_icon="🏗️", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🏗️ LA GRULLA: Productividad</h1>", unsafe_allow_html=True)
st.write("---")

# Base de datos temporal para las tareas
if 'lista_trabajos' not in st.session_state:
    st.session_state.lista_trabajos = []

# Formulario de entrada
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        nombre = st.text_input("Nombre del Proyecto/Tarea", placeholder="Ej: Grabación Podcast")
    with col2:
        tiempo = st.number_input("Minutos", min_value=1, value=25)
    with col3:
        color = st.color_picker("Color de etiqueta", "#e67e22")

    if st.button("➕ Añadir al Planificador", use_container_width=True):
        if nombre:
            st.session_state.lista_trabajos.append({"nombre": nombre, "segundos": tiempo * 60, "color": color})
            st.rerun()

# Visualización de la lista y ejecución
if st.session_state.lista_trabajos:
    st.subheader("Plan de Trabajo Actual")
    
    for i, tarea in enumerate(st.session_state.lista_trabajos):
        with st.expander(f"📌 {tarea['nombre']} ({tarea['segundos']//60} min)", expanded=True):
            col_info, col_btn = st.columns([3, 1])
            
            col_info.markdown(f"<div style='border-left: 5px solid {tarea['color']}; padding-left: 10px;'>Prioridad: {tarea['nombre']}</div>", unsafe_allow_html=True)
            
            if col_btn.button(f"Iniciar ▶️", key=f"run_{i}"):
                placeholder = st.empty()
                progreso = st.progress(0)
                segundos_totales = tarea['segundos']
                
                for s in range(segundos_totales, -1, -1):
                    m, sec = divmod(s, 60)
                    placeholder.metric("Tiempo Restante", f"{m:02d}:{sec:02d}")
                    progreso.progress(1.0 - (s / segundos_totales))
                    time.sleep(1)
                
                # EFECTO DE COMPLETADO
                st.balloons()
                st.success(f"✅ ¡{tarea['nombre']} terminado!")
                # Sonido de campana
                st.components.v1.html("""
                    <audio autoplay>
                        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                    </audio>
                """, height=0)

if st.button("Vaciar Lista"):
    st.session_state.lista_trabajos = []
    st.rerun()
