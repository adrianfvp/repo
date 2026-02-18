import streamlit as st
import time

# Configuración de página con estilo moderno
st.set_page_config(
    page_title="LA GRULLA | Producción",
    page_icon="🏗️",
    layout="centered"
)

# Estilo CSS personalizado para un look minimalista
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        border-radius: 20px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .task-card {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 10px solid;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.markdown("<h1 style='text-align: center; color: #1e1e1e;'>🏗️ LA GRULLA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Control de Tiempos y Producción</p>", unsafe_allow_html=True)

# Inicializar estados
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed' not in st.session_state:
    st.session_state.completed = []

# --- ÁREA DE CREACIÓN ---
with st.expander("➕ Crear Nueva Tarea de Producción", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("¿En qué vas a trabajar?", placeholder="Ej: Edición de audio - Episodio 1")
    with col2:
        mins = st.number_input("Minutos", min_value=1, value=25)
    
    notes = st.text_area("Notas / Checklist interno", placeholder="Escribe aquí los pasos (ej: Limpiar ruido, ecualizar...)")
    color = st.color_picker("Color de identificación", "#3498db")
    
    if st.button("Agregar a la línea de tiempo", use_container_width=True):
        if name:
            st.session_state.tasks.append({
                "name": name, 
                "time": mins * 60, 
                "color": color, 
                "notes": notes
            })
            st.rerun()

# --- PANEL DE TRABAJO ---
if st.session_state.tasks:
    st.markdown("### ⏳ Tareas Pendientes")
    for idx, task in enumerate(st.session_state.tasks):
        # Tarjeta visual
        st.markdown(f"""
            <div class="task-card" style="border-left-color: {task['color']};">
                <h4 style="margin:0;">{task['name']}</h4>
                <p style="color: #888; font-size: 0.9em;">Duración: {task['time']//60} min</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detalle de la tarea y controles
        with st.container():
            col_notes, col_action = st.columns([3, 1])
            with col_notes:
                st.info(f"📋 **Notas:**\n{task['notes'] if task['notes'] else 'Sin notas adicionales.'}")
            
            with col_action:
                if st.button("Iniciar ▶️", key=f"start_{idx}", use_container_width=True):
                    placeholder = st.empty()
                    progress_bar = st.progress(0)
                    
                    for s in range(task['time'], -1, -1):
                        m, sc = divmod(s, 60)
                        placeholder.metric("Tiempo Restante", f"{m:02d}:{sc:02d}")
                        progress_bar.progress(1.0 - (s / task['time']))
                        time.sleep(1)
                    
                    # Finalización
                    st.balloons()
                    st.session_state.completed.append(task['name'])
                    st.session_state.tasks.pop(idx)
                    
                    # Sonido forzado con Script
                    st.components.v1.html("""
                        <audio id="beep" autoplay>
                            <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
                        </audio>
                        <script>document.getElementById('beep').play();</script>
                    """, height=0)
                    
                    st.success("¡Tarea Completada!")
                    time.sleep(2)
                    st.rerun()

# --- CHECKLIST DE COMPLETADAS ---
if st.session_state.completed:
    st.write("---")
    st.markdown("### ✅ Logros del Día")
    for done in st.session_state.completed:
        st.checkbox(done, value=True, disabled=True)
    
    if st.button("Limpiar historial"):
        st.session_state.completed = []
        st.rerun()
