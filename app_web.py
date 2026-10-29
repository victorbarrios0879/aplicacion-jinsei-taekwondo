import streamlit as st
import os

# Configuración inicial de la página
st.set_page_config(page_title="Jinsei Taekwondo Tenjo", page_icon="🥋", layout="wide")

# Inicializar estados si no existen
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = "Invitado"
if "modulo_activo" not in st.session_state:
    st.session_state.modulo_activo = "Panel Principal"

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title(f"👤 {st.session_state.usuario_actual}")

# Logotipo o imagen si existe
IMG_LOGO = "assets/logo.png" if os.path.exists("assets/logo.png") else None
if IMG_LOGO:
    st.sidebar.image(IMG_LOGO, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Contacto / Pagos:**\n`3125046952`")
st.sidebar.markdown("---")

# Lista de módulos del sistema
modulos_lista = [
    "Panel Principal",
    "Ficha Integral del Deportista e IMC",
    "Control de Asistencia",
    "Panel General del Entrenador (Solo Coach)",
    "Galeria y Videos (Multimedia)",
    "Cargar Fichas, Exoneraciones y PDFs",
    "Agenda de Torneos y Eventos",
    "Pagos (Alerta)"
]

# Selector de navegación en la barra lateral
try:
    index_actual = modulos_lista.index(st.session_state.modulo_activo)
except ValueError:
    index_actual = 0

modulo_seleccionado = st.sidebar.selectbox("Seleccione un módulo:", modulos_lista, index=index_actual)
st.session_state.modulo_activo = modulo_seleccionado

st.sidebar.markdown("---")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.usuario_actual = "Invitado"
    st.session_state.modulo_activo = "Panel Principal"
    st.rerun()


# --- CUERPO PRINCIPAL DE LA APLICACIÓN ---

# 1. PANEL PRINCIPAL
if st.session_state.modulo_activo == "Panel Principal":
    st.title("🥋 Club Jinsei Taekwondo Tenjo")
    st.markdown("Bienvenido al sistema oficial de gestión deportiva, académica y administrativa.")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📁 Gestionar Exoneraciones y PDFs"):
            st.session_state.modulo_activo = "Cargar Fichas, Exoneraciones y PDFs"
            st.rerun()
    with col2:
        if st.button("🖼️ Ir a Multimedia y Videos"):
            st.session_state.modulo_activo = "Galeria y Videos (Multimedia)"
            st.rerun()
    with col3:
        if st.button("📅 Ver Agenda de Torneos"):
            st.session_state.modulo_activo = "Agenda de Torneos y Eventos"
            st.rerun()

# 2. FICHA INTEGRAL Y EXONERACIONES
elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
        
    st.header("Carta de Exoneración y Documentos PDF")
    
    EXONERACIONES_DIR = "documentos_exoneracion"
    os.makedirs(EXONERACIONES_DIR, exist_ok=True)

    tab_subir, tab_ver, tab_borrar = st.tabs(["Subir Documento", "Ver Documentos", "Eliminar Documento"])

    with tab_subir:
        st.markdown("### Subir Carta de Exoneración o Documento (PDF)")
        with st.form("form_exoneracion_pdf"):
            nombre_atleta_ex = st.text_input("Nombre Completo del Deportista")
            pdf_subido = st.file_uploader("Seleccione el archivo PDF", type=["pdf"])
            submit_pdf = st.form_submit_button("Subir Documento al Sistema")

            if submit_pdf:
                if nombre_atleta_ex and pdf_subido is not None:
                    ruta_guardado = os.path.join(EXONERACIONES_DIR, f"{nombre_atleta_ex}.pdf")
                    with open(ruta_guardado, "wb") as f:
                        f.write(pdf_subido.getbuffer())
                    st.success(f"¡Documento de {nombre_atleta_ex} guardado con éxito!")
                else:
                    st.error("Por favor complete el nombre y adjunte un archivo PDF.")

    with tab_ver:
        st.subheader("Documentos Registrados")
        if os.path.exists(EXONERACIONES_DIR):
            docs = [f for f in os.listdir(EXONERACIONES_DIR) if f.lower().endswith(".pdf")]
            if docs:
                for d in docs:
                    st.markdown(f"- 📄 {d}")
            else:
                st.info("No hay documentos guardados todavía.")
        else:
            st.info("La carpeta de documentos no existe.")

    with tab_borrar:
        st.subheader("Eliminar Documento del Sistema")
        if os.path.exists(EXONERACIONES_DIR):
            docs_disponibles = [f for f in os.listdir(EXONERACIONES_DIR) if f.lower().endswith(".pdf")]
            if docs_disponibles:
                doc_a_borrar = st.selectbox("Selecciona el documento PDF a eliminar:", docs_disponibles, key="sel_doc_usr_del")
                if st.button("❌ Eliminar Documento Seleccionado", key="btn_doc_usr_del"):
                    ruta_borrar = os.path.join(EXONERACIONES_DIR, doc_a_borrar)
                    if os.path.exists(ruta_borrar):
                        os.remove(ruta_borrar)
                        st.success(f"El documento '{doc_a_borrar}' ha sido eliminado.")
                        st.rerun()
            else:
                st.info("No hay documentos para eliminar.")
        else:
            st.info("La carpeta de documentos no existe.")

# 3. GALERÍA Y VIDEOS (MULTIMEDIA CON OPCIÓN DE ELIMINAR PARA EL COACH)
elif st.session_state.modulo_activo == "Galeria y Videos (Multimedia)":
    if st.button("⬅️ Volver al Panel Principal", key="btn_volver_multimedia"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
        
    st.header("🖼️ Galería y Videos - Jinsei Taekwondo Tenjo")
    st.markdown("Panel de administración multimedia para entrenamientos, katas y eventos oficiales.")
    
    FOTOS_DIR = "fotos_club"
    VIDEOS_DIR = "videos_club"
    os.makedirs(FOTOS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    
    tab_fotos, tab_videos = st.tabs(["📸 Gestión de Fotografías", "🎥 Gestión de Videos"])
    
    with tab_fotos:
        st.subheader("Administración de Fotos")
        sub_tab_f_subir, sub_tab_f_borrar = st.tabs(["Subir Foto", "Ver / Eliminar Fotos"])
        
        with sub_tab_f_subir:
            foto_subida = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"], key="subir_foto_clase")
            if foto_subida:
                ruta_foto = os.path.join(FOTOS_DIR, foto_subida.name)
                with open(ruta_foto, "wb") as f:
                    f.write(foto_subida.getbuffer())
                st.success(f"¡Foto '{foto_subida.name}' guardada correctamente!")
                st.image(foto_subida, caption="Vista previa", use_container_width=True)
        
        with sub_tab_f_borrar:
            fotos_disp = [f for f in os.listdir(FOTOS_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            if fotos_disp:
                foto_a_borrar = st.selectbox("Selecciona la foto a eliminar:", fotos_disp, key="sel_foto_del")
                if st.button("❌ Eliminar Foto Seleccionada", key="btn_foto_del"):
                    ruta_b_foto = os.path.join(FOTOS_DIR, foto_a_borrar)
                    if os.path.exists(ruta_b_foto):
                        os.remove(ruta_b_foto)
                        st.success(f"La foto '{foto_a_borrar}' ha sido eliminada con éxito.")
                        st.rerun()
            else:
                st.info("No hay fotos almacenadas en el sistema.")

    with tab_videos:
        st.subheader("Administración de Videos")
        sub_tab_v_subir, sub_tab_v_borrar = st.tabs(["Subir Video", "Ver / Eliminar Videos"])
        
        with sub_tab_v_subir:
            video_subido = st.file_uploader("Selecciona un video corto", type=["mp4", "mov"], key="subir_video_clase")
            if video_subido:
                ruta_video = os.path.join(VIDEOS_DIR, video_subido.name)
                with open(ruta_video, "wb") as f:
                    f.write(video_subido.getbuffer())
                st.success(f"¡Video '{video_subido.name}' guardado correctamente!")
                st.video(video_subido)
        
        with sub_tab_v_borrar:
            videos_disp = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith((".mp4", ".mov"))]
            if videos_disp:
                video_a_borrar = st.selectbox("Selecciona el video a eliminar:", videos_disp, key="sel_video_del")
                if st.button("❌ Eliminar Video Seleccionado", key="btn_video_del"):
                    ruta_b_video = os.path.join(VIDEOS_DIR, video_a_borrar)
                    if os.path.exists(ruta_b_video):
                        os.remove(ruta_b_video)
                        st.success(f"El video '{video_a_borrar}' ha sido eliminado con éxito.")
                        st.rerun()
            else:
                st.info("No hay videos almacenados en el sistema.")

# 4. AGENDA DE TORNEOS Y EVENTOS
elif st.session_state.modulo_activo == "Agenda de Torneos y Eventos":
    if st.button("⬅️ Volver al Panel Principal", key="btn_volver_agenda"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
        
    st.header("📅 Agenda de Torneos y Eventos Deportivos")
    st.markdown("Calendario oficial de competencias departamentales y festivales de taekwondo.")
    st.info("Próximamente: Registro de inscripciones y cronograma de pesaje para atletas de Jinsei Tenjo.")

# 5. PAGOS Y ALERTAS
elif st.session_state.modulo_activo == "Pagos (Alerta)":
    if st.button("⬅️ Volver al Panel Principal", key="btn_volver_pagos"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
        
    st.header("💳 Control de Pagos y Notificaciones")
    st.markdown(f"Canal digital autorizado de pagos del club vía Nequi / Daviplata: **3125046952**")

# OTROS MÓDULOS EN DESARROLLO
else:
    if st.button("⬅️ Volver al Panel Principal", key="btn_volver_generico"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.header(f"Módulo: {st.session_state.modulo_activo}")
    st.info("Esta sección se encuentra activa y configurándose para el club.")