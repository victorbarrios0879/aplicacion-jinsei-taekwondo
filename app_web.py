import streamlit as st
import os
import csv
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image

# ----------------- CONFIGURACIÓN Y ESTADO DE SESIÓN -----------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "modulo_activo" not in st.session_state:
    st.session_state.modulo_activo = "Panel Principal"

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

st.set_page_config(
    page_title="Jinsei Taekwondo Tenjo - Panel Principal",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

ARCHIVO_DEPORTISTAS = "deportistas_integral.csv"
ARCHIVO_EVENTOS = "eventos.csv"
ARCHIVO_USUARIOS = "usuarios_sistema.csv"
ARCHIVO_ASISTENCIAS = "asistencias.csv"
ARCHIVO_MACRO = "macroestructura_sesiones.csv"
ARCHIVO_PAGOS = "pagos_deportistas.csv"
CONTRASENA_ENTRENADOR = "coach2026"
TELEFONO_CLUB = "+57 312 504 6952" 
NUMERO_PAGOS_DIGITALES = "3125046952"

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
EXONERACIONES_DIR = BASE_DIR / "documentos_exoneracion"
EXONERACIONES_DIR.mkdir(exist_ok=True)
VIDEOS_DIR = BASE_DIR / "videos_club"
VIDEOS_DIR.mkdir(exist_ok=True)
FOTOS_CLUB_DIR = BASE_DIR / "fotos_club"
FOTOS_CLUB_DIR.mkdir(exist_ok=True)
MACRO_DIR = BASE_DIR / "macroestructura_archivos"
MACRO_DIR.mkdir(exist_ok=True)

def verificar_usuario(user, pwd):
    if user == "admin" and pwd == CONTRASENA_ENTRENADOR:
        return True
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2 and row[0] == user and row[1] == pwd:
                    return True
    return False

def registrar_nuevo_usuario(user, pwd, email):
    if user == "admin":
        return False, "El usuario admin está reservado."
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == user:
                    return False, "El nombre de usuario ya existe."
    
    file_exists = os.path.exists(ARCHIVO_USUARIOS)
    with open(ARCHIVO_USUARIOS, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Usuario", "Contraseña", "Correo"])
        writer.writerow([user, pwd, email])
    return True, "¡Usuario registrado con éxito!"

def recuperar_credenciales(email_consulta):
    if email_consulta.strip().lower() == "admin@jinsei.com":
        return True, "admin", CONTRASENA_ENTRENADOR
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2].strip().lower() == email_consulta.strip().lower():
                    return True, row[0], row[1]
    return False, None, None

# Estilos limpios sin comillas conflictivas
css = """
<style>
.stApp {
    background-color: #f5f5f5;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.card-servicio {
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
    color: white;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
.bg-azul { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }
.bg-verde { background: linear-gradient(135deg, #15803D 0%, #22C55E 100%); }
.bg-rojo { background: linear-gradient(135deg, #B91C1C 0%, #EF4444 100%); }
.bg-amarillo { background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%); color: #1E293B; }
.card-title-custom { font-size: 18px; font-weight: bold; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.card-desc-custom { font-size: 13px; opacity: 0.95; font-weight: normal; }
.badge-icon { padding: 4px 10px; border-radius: 20px; font-size: 12px; background: #1E3A8A; color: white; margin-right: 6px; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

if not st.session_state.autenticado:
    _, col_principal, _ = st.columns([1, 2.5, 1])

    with col_principal:
        logo_file = ASSETS_DIR / "logo.png"
        if os.path.exists(logo_file):
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                st.image(str(logo_file), width=120)

        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Club Jinsei Taekwondo Tenjo</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569;'>Sistema oficial de gestión deportiva y administrativa</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse", "❓ Recuperar Credenciales"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("form_login"):
                st.subheader("Ingrese a su cuenta")
                usuario_ingreso = st.text_input("Usuario o Correo")
                password_ingreso = st.text_input("Contraseña", type="password")
                submit_ingreso = st.form_submit_button("Entrar al Sistema", use_container_width=True)

            if submit_ingreso:
                if verificar_usuario(usuario_ingreso, password_ingreso):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario_ingreso
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("form_registro"):
                st.subheader("📝 Registro de Nuevo Usuario")
                nuevo_user = st.text_input("Nombre de Usuario")
                nuevo_email = st.text_input("Correo Electrónico")
                nuevo_pass = st.text_input("Contraseña", type="password")
                submit_registro = st.form_submit_button("Registrarse", use_container_width=True)
                
            if submit_registro:
                if nuevo_user and nuevo_pass and nuevo_email:
                    exito, msg = registrar_nuevo_usuario(nuevo_user, nuevo_pass, nuevo_email)
                    if exito:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Por favor complete todos los campos.")

        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("form_recuperar"):
                st.subheader("❓ Recuperar Credenciales")
                correo_recuperar = st.text_input("Ingrese su correo registrado")
                submit_recuperar = st.form_submit_button("Buscar Credenciales", use_container_width=True)
                
            if submit_recuperar:
                encontrado, u, p = recuperar_credenciales(correo_recuperar)
                if encontrado:
                    st.info(f"🔑 Sus credenciales son -> Usuario: **{u}** | Contraseña: **{p}**")
                else:
                    st.error("No se encontró ninguna cuenta asociada a este correo.")

    st.stop()

# VISTA PRIVADA
st.sidebar.title(f"👤 {st.session_state.get('usuario_actual', 'Coach')}")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.modulo_activo = "Panel Principal"
    st.rerun()

st.sidebar.info("Jinsei Taekwondo — Tenjo")
logo_lateral = ASSETS_DIR / "logo.png"
if os.path.exists(logo_lateral):
    st.sidebar.image(str(logo_lateral), use_container_width=True)

st.sidebar.markdown(f"📱 **Contacto / Pagos:**\n`{NUMERO_PAGOS_DIGITALES}`")
st.sidebar.markdown("---")

modulos_lista = [
    "Panel Principal",
    "Ficha Integral del Deportista e IMC",
    "Control de Asistencia",
    "Panel General del Entrenador (Solo Coach)",
    "Galería y Videos (Multimedia)",
    "Cargar Fichas, Exoneraciones y PDFs",
    "Agenda de Torneos y Eventos",
    "Pagos (Alerta)"
]

try:
    index_actual = modulos_lista.index(st.session_state.modulo_activo)
except ValueError:
    index_actual = 0

modulo_seleccionado = st.sidebar.selectbox("Seleccione un módulo:", modulos_lista, index=index_actual, key="menu_lateral_principal")
st.session_state.modulo_activo = modulo_seleccionado

if st.session_state.modulo_activo != "Panel Principal":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.markdown("---")

if st.session_state.modulo_activo == "Panel Principal":
    st.title("🥋 Club Jinsei Taekwondo Tenjo")
    st.markdown("Sistema oficial de gestión deportiva, académica y administrativa.")
    st.markdown("---")
    
    st.subheader("⚡ Acceso Rápido a Módulos de Trabajo")
    c_mod1, c_mod2 = st.columns(2)

    with c_mod1:
        st.markdown('''
            <div class="card-servicio bg-azul">
                <div class="card-title-custom"><span class="badge-icon">01</span> Ficha Integral e IMC</div>
                <div class="card-desc-custom">Registro completo de datos de deportistas, EPS y cálculo nutricional.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("📁 Abrir Ficha e IMC", use_container_width=True, key="btn_m1"):
            st.session_state.modulo_activo = "Ficha Integral del Deportista e IMC"
            st.rerun()

        st.markdown('''
            <div class="card-servicio bg-rojo">
                <div class="card-title-custom"><span class="badge-icon">03</span> Galería y Videos (Multimedia)</div>
                <div class="card-desc-custom">Fotografías, eventos institucionales y videoteca técnica del club.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("📸 Abrir Multimedia", use_container_width=True, key="btn_m3"):
            st.session_state.modulo_activo = "Galería y Videos (Multimedia)"
            st.rerun()

        st.markdown('''
            <div class="card-servicio bg-verde">
                <div class="card-title-custom"><span class="badge-icon">05</span> Control de Asistencia</div>
                <div class="card-desc-custom">Registro diario por sesión y consulta de historial de deportistas.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("📊 Abrir Asistencia", use_container_width=True, key="btn_m5"):
            st.session_state.modulo_activo = "Control de Asistencia"
            st.rerun()

    with c_mod2:
        st.markdown('''
            <div class="card-servicio bg-verde">
                <div class="card-title-custom"><span class="badge-icon">02</span> Panel General del Entrenador</div>
                <div class="card-desc-custom">Centro administrativo: gestión de deportistas, macroestructura y borrado.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("🥋 Abrir Panel Coach", use_container_width=True, key="btn_m2"):
            st.session_state.modulo_activo = "Panel General del Entrenador (Solo Coach)"
            st.rerun()

        st.markdown('''
            <div class="card-servicio bg-amarillo">
                <div class="card-title-custom"><span class="badge-icon">04</span> Exoneraciones y PDFs</div>
                <div class="card-desc-custom">Gestión y borrado de cartas de deslinde de responsabilidad legal.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("📄 Abrir Exoneraciones", use_container_width=True, key="btn_m6"):
            st.session_state.modulo_activo = "Cargar Fichas, Exoneraciones y PDFs"
            st.rerun()

        st.markdown('''
            <div class="card-servicio bg-azul">
                <div class="card-title-custom"><span class="badge-icon">06</span> Control de Pagos</div>
                <div class="card-desc-custom">Estado de mensualidades, recibos oficiales y alertas de pagos.</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("💰 Abrir Pagos", use_container_width=True, key="btn_m8"):
            st.session_state.modulo_activo = "Pagos (Alerta)"
            st.rerun()

elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    st.header("📄 Carta de Exoneración y Documentos PDF")
    tab_subir, tab_ver, tab_borrar = st.tabs(["Subir Documento", "Ver Documentos", "🗑️ Eliminar Documento"])
    
    with tab_subir:
        with st.form("form_exoneracion_pdf"):
            st.subheader("Subir Carta de Exoneración o Documento (PDF)")
            nombre_atleta_ex = st.text_input("Nombre Completo del Deportista")
            pdf_subido = st.file_uploader("Seleccione el archivo PDF", type=["pdf"])
            submit_pdf = st.form_submit_button("Subir Documento al Sistema")
            if submit_pdf:
                if nombre_atleta_ex and pdf_subido is not None:
                    nombre_limpio = nombre_atleta_ex.replace(" ", "_").lower()
                    ruta_destino = EXONERACIONES_DIR / f"exoneracion_{nombre_limpio}.pdf"
                    with open(ruta_destino, "wb") as f:
                        f.write(pdf_subido.getbuffer())
                    st.success(f"¡Documento de {nombre_atleta_ex} cargado con éxito!")
                else:
                    st.warning("Por favor ingrese el nombre y adjunte el archivo PDF.")

    with tab_ver:
        st.subheader("Documentos Cargados en el Sistema")
        if os.path.exists(EXONERACIONES_DIR):
            archivos_pdf = list(EXONERACIONES_DIR.glob("*.pdf"))
            if archivos_pdf:
                for archivo in archivos_pdf:
                    col_v1, col_v2 = st.columns([3, 1])
                    with col_v1:
                        st.write(f"📄 `{archivo.name}`")
                    with col_v2:
                        with open(archivo, "rb") as f_dl:
                            st.download_button("⬇️ Descargar", data=f_dl, file_name=archivo.name, mime="application/pdf", key=f"dl_usr_{archivo.name}")
            else:
                st.info("No hay documentos de exoneración cargados todavía.")

    with tab_borrar:
        st.subheader("🗑️ Eliminar Documento PDF")
        if os.path.exists(EXONERACIONES_DIR):
            docs_disponibles = [f for f in os.listdir(EXONERACIONES_DIR) if f.lower().endswith(".pdf")]
            if docs_disponibles:
                doc_a_borrar = st.selectbox("Selecciona el documento PDF a eliminar:", docs_disponibles, key="sel_doc_usr_del")
                if st.button("❌ Eliminar Documento Seleccionado", key="btn_doc_usr_del"):
                    ruta_borrar = EXONERACIONES_DIR / doc_a_borrar
                    if os.path.exists(ruta_borrar):
                        os.remove(ruta_borrar)
                        st.success(f"El documento '{doc_a_borrar}' ha sido eliminado.")
                        st.rerun()
            else:
                st.info("No hay documentos para eliminar.")

elif st.session_state.modulo_activo == "Galería y Videos (Multimedia)":
    st.header("📸 Galería y Videoteca del Club Jinsei Taekwondo")
    opcion_multimedia = st.radio("Gestión de Multimedia:", ["Fotos del Club", "Vídeos de Técnica"], horizontal=True)
    st.markdown("---")
    
    if opcion_multimedia == "Fotos del Club":
        st.subheader("📤 Subir Nueva Foto")
        foto_subida = st.file_uploader("Seleccione la imagen", type=["jpg", "jpeg", "png"], key="subir_foto_dir")
        if st.button("Guardar Foto", key="btn_save_f_dir"):
            if foto_subida is not None:
                ruta = FOTOS_CLUB_DIR / foto_subida.name
                with open(ruta, "wb") as f:
                    f.write(foto_subida.getbuffer())
                st.success(f"¡Foto '{foto_subida.name}' guardada con éxito!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🖼️ Fotos Registradas y Eliminar")
        if os.path.exists(FOTOS_CLUB_DIR):
            lista_fotos = [f for f in os.listdir(FOTOS_CLUB_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if lista_fotos:
                foto_a_borrar = st.selectbox("Seleccione foto a eliminar:", lista_fotos, key="sel_f_borrar")
                if st.button("❌ Eliminar Foto Seleccionada", key="btn_del_f_dir"):
                    os.remove(FOTOS_CLUB_DIR / foto_a_borrar)
                    st.success(f"La foto '{foto_a_borrar}' ha sido eliminada.")
                    st.rerun()
            else:
                st.info("No hay fotos guardadas aún.")
    else:
        st.subheader("📤 Subir Nuevo Vídeo")
        video_subido = st.file_uploader("Seleccione el archivo de vídeo", type=["mp4", "mov", "avi"], key="subir_video_dir")
        if st.button("Guardar Vídeo", key="btn_save_v_dir"):
            if video_subido is not None:
                ruta_v = VIDEOS_DIR / video_subido.name
                with open(ruta_v, "wb") as f:
                    f.write(video_subido.getbuffer())
                st.success(f"¡Vídeo '{video_subido.name}' guardado con éxito!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🎥 Vídeos Registrados y Eliminar")
        if os.path.exists(VIDEOS_DIR):
            lista_videos = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            if lista_videos:
                video_a_borrar = st.selectbox("Seleccione vídeo a eliminar:", lista_videos, key="sel_v_borrar")
                if st.button("❌ Eliminar Vídeo Seleccionado", key="btn_del_v_dir"):
                    os.remove(VIDEOS_DIR / video_a_borrar)
                    st.success(f"El vídeo '{video_a_borrar}' ha sido eliminada.")
                    st.rerun()
            else:
                st.info("No hay vídeos guardados aún.")

elif st.session_state.modulo_activo == "Panel General del Entrenador (Solo Coach)":
    st.header("⚙️ Panel General del Entrenador (Exclusivo Coach)")
    password_coach = st.text_input("Ingrese Contraseña de Autorización Coach", type="password")
    
    if password_coach == CONTRASENA_ENTRENADOR:
        st.success("✅ Acceso Autorizado al Panel de Control.")
        tab_dep, tab_doc_coach = st.tabs(["📋 Lista y Borrado de Deportistas", "📄 Documentos PDF"])
        
        with tab_dep:
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                    data = list(csv.reader(f))
                    if len(data) > 1:
                        st.table(data)
                        nombres_del = [row[0] for row in data[1:]]
                        dep_del = st.selectbox("Deportista a eliminar:", nombres_del)
                        if st.button("❌ Eliminar Atleta Seleccionado"):
                            nuevos = [data[0]] + [r for r in data[1:] if r[0] != dep_del]
                            with open(ARCHIVO_DEPORTISTAS, mode="w", newline="", encoding="utf-8") as fw:
                                csv.writer(fw).writerows(nuevos)
                            st.success(f"Atleta {dep_del} eliminado correctamente.")
                            st.rerun()
                    else:
                        st.info("No hay deportistas registrados.")
        with tab_doc_coach:
            st.subheader("Administración de Archivos Exoneración")
            archivos_pdf = list(EXONERACIONES_DIR.glob("*.pdf"))
            if archivos_pdf:
                for pdf_item in archivos_pdf:
                    c_n, c_b = st.columns([3, 1])
                    with c_n:
                        st.write(f"📄 `{pdf_item.name}`")
                    with c_b:
                        if st.button(f"🗑️ Eliminar", key=f"del_pdf_c_{pdf_item.name}"):
                            pdf_item.unlink()
                            st.success(f"Eliminado: {pdf_item.name}")
                            st.rerun()
    elif password_coach != "":
        st.error("⚠️ Contraseña incorrecta.")