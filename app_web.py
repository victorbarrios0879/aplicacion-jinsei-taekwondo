import streamlit as st
import os
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Club Jinsei Taekwondo Tenjo",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DETECTAR FOTO DE FONDO Y LOGOTIPO DESDE LA CARPETA ASSETS ---
os.makedirs("assets", exist_ok=True)

# Buscar logo en assets
logo_path = None
for f in os.listdir("assets"):
    if f.lower().startswith("logo") and f.lower().endswith((".png", ".jpg", ".jpeg")):
        logo_path = os.path.join("assets", f)
        break

# Buscar fondo de deportistas en assets
fondo_path = None
for f in os.listdir("assets"):
    if any(k in f.lower() for k in ["fondo", "deportist", "taekwondo", "entren"]) and f.lower().endswith((".jpg", ".png", ".jpeg")):
        fondo_path = os.path.join("assets", f)
        break

# Si no hay fondo específico, usamos una ruta genérica o un color sólido elegante
css_fondo = f"""
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                          url("{fondo_path.replace(os.sep, '/')}" if fondo_path else "https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
"""

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown(f"""
    <style>
    {css_fondo}
    .card-box {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #ff4b4b;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ARCHIVOS Y CARPETAS DE DATOS ---
EXONERACIONES_DIR = "documentos_exoneracion"
FOTOS_DIR = "fotos_club"
VIDEOS_DIR = "videos_club"
MACRO_DIR = "macroestructura_archivos"
CSV_DEPORTISTAS = "archivo_deportistas.csv"

for d in [EXONERACIONES_DIR, FOTOS_DIR, VIDEOS_DIR, MACRO_DIR]:
    os.makedirs(d, exist_ok=True)

if not os.path.exists(CSV_DEPORTISTAS):
    df_init = pd.DataFrame(columns=["Documento", "Nombre Completo", "Categoría", "Edad", "Telefono"])
    df_init.to_csv(CSV_DEPORTISTAS, index=False)

# Inicializar estados
if "autenticado_coach" not in st.session_state:
    st.session_state.autenticado_coach = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = "Invitado"
if "modulo_activo" not in st.session_state:
    st.session_state.modulo_activo = "Panel Principal"

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title(f"👤 {st.session_state.usuario_actual}")

if logo_path and os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Contacto / Pagos:**\n`3125046952`")
st.sidebar.markdown("---")

modulos_lista = [
    "Panel Principal",
    "Panel General del Entrenador (Solo Coach)",
    "Ficha Integral del Deportista e IMC",
    "Control de Asistencia",
    "Galeria y Videos (Multimedia)",
    "Cargar Fichas, Exoneraciones y PDFs",
    "Macroestructura de Entrenamiento",
    "Agenda de Torneos y Eventos",
    "Pagos (Alerta)"
]

try:
    index_actual = modulos_lista.index(st.session_state.modulo_activo)
except ValueError:
    index_actual = 0

modulo_seleccionado = st.sidebar.selectbox("Seleccione un módulo:", modulos_lista, index=index_actual)
st.session_state.modulo_activo = modulo_seleccionado

st.sidebar.markdown("---")
if st.session_state.autenticado_coach:
    if st.sidebar.button("Cerrar Sesión de Coach"):
        st.session_state.autenticado_coach = False
        st.session_state.usuario_actual = "Invitado"
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()


# --- CUERPO PRINCIPAL DE LA APLICACIÓN ---

# 1. PANEL PRINCIPAL (BOTONES DISTRIBUIDOS)
if st.session_state.modulo_activo == "Panel Principal":
    st.title("🥋 Club Jinsei Taekwondo Tenjo")
    st.markdown("Sistema oficial de gestión deportiva, académica y administrativa.")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔐 Panel del Entrenador (Coach)", use_container_width=True):
            st.session_state.modulo_activo = "Panel General del Entrenador (Solo Coach)"
            st.rerun()
    with col2:
        if st.button("📁 Exoneraciones y PDFs", use_container_width=True):
            st.session_state.modulo_activo = "Cargar Fichas, Exoneraciones y PDFs"
            st.rerun()
    with col3:
        if st.button("🖼️ Galería y Multimedia", use_container_width=True):
            st.session_state.modulo_activo = "Galeria y Videos (Multimedia)"
            st.rerun()

    st.markdown("---")
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("📈 Macroestructura", use_container_width=True):
            st.session_state.modulo_activo = "Macroestructura de Entrenamiento"
            st.rerun()
    with col5:
        if st.button("📊 Ficha Integral y IMC", use_container_width=True):
            st.session_state.modulo_activo = "Ficha Integral del Deportista e IMC"
            st.rerun()
    with col6:
        if st.button("📅 Agenda de Torneos", use_container_width=True):
            st.session_state.modulo_activo = "Agenda de Torneos y Eventos"
            st.rerun()

# 2. PANEL GENERAL DEL ENTRENADOR (ACCESO CON CONTRASEÑA Y GESTIÓN TOTAL)
elif st.session_state.modulo_activo == "Panel General del Entrenador (Solo Coach)":
    st.header("🔐 Panel Administrativo del Entrenador")
    
    if not st.session_state.autenticado_coach:
        st.markdown("Por favor ingrese la contraseña de acceso exclusivo para el entrenador:")
        pass_ingresada = st.text_input("Contraseña de Acceso", type="password")
        if st.button("Ingresar como Entrenador"):
            if pass_ingresada == "jinsei2026" or pass_ingresada == "coach123":
                st.session_state.autenticado_coach = True
                st.session_state.usuario_actual = "Entrenador Victor"
                st.success("¡Acceso concedido con éxito!")
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Intente nuevamente.")
    else:
        st.success("✨ Sesión de Entrenador Activa")
        
        tab_inscripcion, tab_archivos, tab_multimedia, tab_macro = st.tabs([
            "👥 Gestión de Deportistas", 
            "📁 Archivos y Exoneraciones", 
            "🖼️ Multimedia (Fotos/Videos)", 
            "📈 Macroestructura"
        ])
        
        with tab_inscripcion:
            st.subheader("Inscripción y Control Manual de Deportistas")
            df_deps = pd.read_csv(CSV_DEPORTISTAS)
            
            with st.form("form_nuevo_deportista"):
                st.markdown("### Registrar Nuevo Deportista")
                c1, c2 = st.columns(2)
                with c1:
                    doc_dep = st.text_input("Número de Documento / ID")
                    nombre_dep = st.text_input("Nombre Completo")
                    edad_dep = st.number_input("Edad", min_value=3, max_value=90, value=15)
                with c2:
                    cat_dep = st.selectbox("Categoría", ["Infantil", "Cadete", "Junior", "Sub-21", "Senior", "Máster"])
                    tel_dep = st.text_input("Teléfono de Contacto")
                
                if st.form_submit_button("Registrar Deportista en el Sistema"):
                    if doc_dep and nombre_dep:
                        if str(doc_dep) in df_deps["Documento"].astype(str).values:
                            st.warning("Ya existe un deportista registrado con ese documento.")
                        else:
                            nuevo_reg = pd.DataFrame([[doc_dep, nombre_dep, cat_dep, edad_dep, tel_dep]], 
                                                     columns=["Documento", "Nombre Completo", "Categoría", "Edad", "Telefono"])
                            df_deps = pd.concat([df_deps, nuevo_reg], ignore_index=True)
                            df_deps.to_csv(CSV_DEPORTISTAS, index=False)
                            st.success(f"¡Deportista {nombre_dep} inscrito correctamente!")
                            st.rerun()
                    else:
                        st.error("Complete documento y nombre.")
            
            st.markdown("---")
            st.subheader("Listado y Eliminación Manual de Deportistas")
            if not df_deps.empty:
                st.dataframe(df_deps, use_container_width=True)
                dep_a_borrar = st.selectbox("Seleccione deportista a eliminar:", df_deps["Nombre Completo"].tolist(), key="sel_dep_borrar")
                if st.button("❌ Eliminar Deportista Seleccionado"):
                    df_deps = df_deps[df_deps["Nombre Completo"] != dep_a_borrar]
                    df_deps.to_csv(CSV_DEPORTISTAS, index=False)
                    st.success(f"Deportista {dep_a_borrar} eliminado.")
                    st.rerun()
            else:
                st.info("No hay deportistas inscritos.")

        with tab_archivos:
            st.subheader("Gestión de Exoneraciones y Documentos PDF")
            sub_t1, sub_t2 = st.tabs(["Subir Documento PDF", "Eliminar Documento PDF"])
            with sub_t1:
                with st.form("form_coach_pdf"):
                    nom_atleta = st.text_input("Nombre del Deportista / Archivo")
                    pdf_file = st.file_uploader("Seleccionar PDF", type=["pdf"])
                    if st.form_submit_button("Guardar PDF"):
                        if nom_atleta and pdf_file:
                            path_pdf = os.path.join(EXONERACIONES_DIR, f"{nom_atleta}.pdf")
                            with open(path_pdf, "wb") as f:
                                f.write(pdf_file.getbuffer())
                            st.success(f"Documento de {nom_atleta} subido con éxito.")
            with sub_t2:
                pdfs_disp = [f for f in os.listdir(EXONERACIONES_DIR) if f.lower().endswith(".pdf")]
                if pdfs_disp:
                    pdf_del = st.selectbox("Seleccione PDF a eliminar:", pdfs_disp)
                    if st.button("❌ Borrar PDF Seleccionado"):
                        os.remove(os.path.join(EXONERACIONES_DIR, pdf_del))
                        st.success("Documento eliminado.")
                        st.rerun()

        with tab_multimedia:
            st.subheader("Administración de Galería (Fotos y Videos)")
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.markdown("### 📸 Fotografías")
                foto_sub = st.file_uploader("Subir Foto", type=["jpg", "png", "jpeg"], key="coach_foto")
                if foto_sub:
                    with open(os.path.join(FOTOS_DIR, foto_sub.name), "wb") as f:
                        f.write(foto_sub.getbuffer())
                    st.success("¡Foto guardada!")
                fotos_lst = [f for f in os.listdir(FOTOS_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
                if fotos_lst:
                    f_del = st.selectbox("Eliminar foto:", fotos_lst, key="del_f_coach")
                    if st.button("❌ Borrar Foto"):
                        os.remove(os.path.join(FOTOS_DIR, f_del))
                        st.success("Foto eliminada.")
                        st.rerun()
            with m_col2:
                st.markdown("### 🎥 Videos")
                vid_sub = st.file_uploader("Subir Video", type=["mp4", "mov"], key="coach_vid")
                if vid_sub:
                    with open(os.path.join(VIDEOS_DIR, vid_sub.name), "wb") as f:
                        f.write(vid_sub.getbuffer())
                    st.success("¡Video guardado!")
                vids_lst = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith((".mp4", ".mov"))]
                if vids_lst:
                    v_del = st.selectbox("Eliminar video:", vids_lst, key="del_v_coach")
                    if st.button("❌ Borrar Video"):
                        os.remove(os.path.join(VIDEOS_DIR, v_del))
                        st.success("Video eliminado.")
                        st.rerun()

        with tab_macro:
            st.subheader("📈 Planificación y Macroestructura Deportiva")
            macro_sub = st.file_uploader("Subir Archivo de Macroestructura", type=["pdf", "xlsx", "xls", "docx", "csv"])
            if macro_sub:
                path_macro = os.path.join(MACRO_DIR, macro_sub.name)
                with open(path_macro, "wb") as f:
                    f.write(macro_sub.getbuffer())
                st.success("Archivo de macroestructura guardado.")
            archivos_macro = os.listdir(MACRO_DIR)
            if archivos_macro:
                macro_del = st.selectbox("Seleccione archivo a eliminar:", archivos_macro)
                if st.button("❌ Eliminar Archivo de Macroestructura"):
                    os.remove(os.path.join(MACRO_DIR, macro_del))
                    st.success("Archivo eliminado.")
                    st.rerun()

# 3. MÓDULOS DE CONSULTA Y PÚBLICOS
elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.header("Carta de Exoneración y Documentos PDF")
    if os.path.exists(EXONERACIONES_DIR):
        for d in [f for f in os.listdir(EXONERACIONES_DIR) if f.lower().endswith(".pdf")]:
            st.markdown(f"- 📄 {d}")

elif st.session_state.modulo_activo == "Galeria y Videos (Multimedia)":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.header("🖼️ Galería y Videos - Jinsei Taekwondo Tenjo")
    tab_f, tab_v = st.tabs(["Fotografías", "Videos"])
    with tab_f:
        if os.path.exists(FOTOS_DIR):
            for foto in [f for f in os.listdir(FOTOS_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]:
                st.image(os.path.join(FOTOS_DIR, foto), caption=foto, use_container_width=True)
    with tab_v:
        if os.path.exists(VIDEOS_DIR):
            for vid in [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith((".mp4", ".mov"))]:
                st.video(os.path.join(VIDEOS_DIR, vid))

elif st.session_state.modulo_activo == "Macroestructura de Entrenamiento":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.header("📈 Macroestructura del Club")
    if os.path.exists(MACRO_DIR):
        for mf in os.listdir(MACRO_DIR):
            st.markdown(f"- 📋 {mf}")

else:
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.header(f"Módulo: {st.session_state.modulo_activo}")
    st.info("Sección activa.")