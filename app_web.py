import streamlit as st
import os
import csv
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image

# Inicializar variables de estado al iniciar la app
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "modulo_activo" not in st.session_state:
    st.session_state.modulo_activo = "Panel Principal"

# Configuración de la página web
st.set_page_config(
    page_title="Jinsei Taekwondo Tenjo - Panel Principal",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Archivos de persistencia local
ARCHIVO_DEPORTISTAS = "deportistas_integral.csv"
ARCHIVO_EVENTOS = "eventos.csv"
ARCHIVO_USUARIOS = "usuarios_sistema.csv"
ARCHIVO_ASISTENCIAS = "asistencias.csv"
ARCHIVO_MACRO = "macroestructura_sesiones.csv"
ARCHIVO_PAGOS = "pagos_deportistas.csv"
ARCHIVO_VIDEOS_CSV = "videos_registro.csv"
ARCHIVO_FOTOS_CSV = "fotos_registro.csv"
CONTRASENA_ENTRENADOR = "coach2026"
TELEFONO_CLUB = "+57 312 504 6952" 
NUMERO_PAGOS_DIGITALES = "3125046952"  # Nequi, Daviplata, Llave

# Directorio raíz y carpetas locales
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

# Carga de imágenes con PIL y rutas
def cargar_imagen_autodetectada(nombre_clave):
    carpetas_a_buscar = [ASSETS_DIR, BASE_DIR]
    for carpeta in carpetas_a_buscar:
        if carpeta.exists():
            for archivo in os.listdir(carpeta):
                if nombre_clave.lower() in archivo.lower() and archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    try:
                        return Image.open(carpeta / archivo), carpeta / archivo
                    except Exception:
                        pass
    return None, None
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
import os
import base64

# Cargar imagen de fondo de forma segura desde assets
foto_bg_path = "assets/foto.JPG"  # O el archivo que tengas en assets
if os.path.exists(foto_bg_path):
    with open(foto_bg_path, "rb") as img_file:
        FOTO_BG_BASE64 = base64.b64encode(img_file.read()).decode()
else:
    FOTO_BG_BASE64 = ""
# ----------------- CSS: FONDO PROTAGÓNICO Y ENCABEZADO -----------------
css_background = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.78), rgba(255, 255, 255, 0.78)), url("data:image/jpeg;base64,{FOTO_BG_BASE64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .header-branding {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }}
    .header-logo {{
        width: 80px;
        height: 80px;
        object-fit: contain;
        border-radius: 50%;
    }}
    .header-text {{
        display: flex;
        flex-direction: column;
    }}
    .main-title-inline {{ 
        font-size: 28px; 
        color: #1E3A8A; 
        font-weight: 800; 
        margin: 0;
        text-transform: uppercase;
        line-height: 1.1;
    }}
    .sub-title-inline {{ 
        font-size: 14px; 
        color: #334155; 
        margin: 3px 0 0 0;
        font-weight: 700;
    }}
    .location-text {{
        font-size: 12px;
        color: #059669;
        font-weight: 700;
        margin-top: 2px;
    }}
    .contact-text {{
        font-size: 12px;
        color: #1E3A8A;
        font-weight: 700;
        margin-top: 2px;
    }}
    
    div.stButton > button {{
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 6px 12px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.12) !important;
    }}
    
    .card-servicio {{
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }}
    .bg-azul {{ background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }}
    .bg-verde {{ background: linear-gradient(135deg, #15803D 0%, #22C55E 100%); }}
    .bg-rojo {{ background: linear-gradient(135deg, #B91C1C 0%, #EF4444 100%); }}
    .bg-amarillo {{ background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%); color: #1E293B; }}
    
    .card-title-custom {{ font-size: 18px; font-weight: bold; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .card-desc-custom {{ font-size: 13px; opacity: 0.95; font-weight: normal; }}

    .badge-icon {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        background: #1E3A8A;
        color: white;
        margin-right: 6px;
    }}

    .exoneracion-box {{ 
        background-color: #FFFFFF; 
        border: 2px solid #3B82F6; 
        padding: 22px; 
        border-radius: 12px; 
        color: #1E293B; 
        font-size: 14px; 
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    .recibo-card {{
        background: #FFFFFF;
        border: 2px dashed #1E3A8A;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        color: #1E293B;
    }}
    </style>
"""
st.markdown(css_background, unsafe_allow_html=True)

# ----------------- FUNCIONES DE USUARIOS Y RECUPERACIÓN -----------------
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

# Cargar logo de forma segura en base64 para el login/encabezado
logo_path = "assets/logo.JPG.jpeg"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as logo_file:
        LOGO_BASE64 = base64.b64encode(logo_file.read()).decode()
else:
    LOGO_BASE64 = ""
if not st.session_state.autenticado:
    col_acc1, col_acc2, col_acc3 = st.columns([1, 2, 1])
    
    with col_acc2:
        html_header_login = f"""
            <div class="header-branding" style="justify-content: center; margin-top: 25px;">
                <img src="data:image/jpeg;base64,{LOGO_BASE64}" class="header-logo">
                <div class="header-text">
                    <h1 class="main-title-inline">JINSEI TAEKWONDO TENJO</h1>
                    <p class="sub-title-inline">Portal Web de Gestión Deportiva e Integración</p>
                    <p class="location-text">📍 Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque</p>
                    <p class="contact-text">📞 Contacto / WhatsApp: {TELEFONO_CLUB}</p>
                </div>
            </div>
        """
        st.markdown(html_header_login, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse", "❓ Recuperar Credenciales"])
        
        with tab1:
            with st.form("form_login"):
                st.subheader("Ingrese a su cuenta")
                usuario_ingreso = st.text_input("Usuario o Correo")
                password_ingreso = st.text_input("Contraseña", type="password")
                submit_ingreso = st.form_submit_button("Entrar al Sistema")
                
                if submit_ingreso:
                    if verificar_usuario(usuario_ingreso, password_ingreso):
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = usuario_ingreso
                        st.success("¡Acceso concedido!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")
                        
        with tab2:
            with st.form("form_registro"):
                st.subheader("Crear nueva cuenta")
                nuevo_user = st.text_input("Elija un Nombre de Usuario")
                nuevo_email = st.text_input("Correo Electrónico")
                nuevo_pass = st.text_input("Contraseña", type="password")
                submit_registro = st.form_submit_button("Crear Cuenta")
                
                if submit_registro:
                    if nuevo_user and nuevo_pass and nuevo_email:
                        exito, mensaje = registrar_nuevo_usuario(nuevo_user, nuevo_pass, nuevo_email)
                        if exito:
                            st.success(mensaje + " Ahora vaya a la pestaña 'Iniciar Sesión'.")
                        else:
                            st.error(mensaje)
                    else:
                        st.warning("Por favor complete todos los campos.")

        with tab3:
            with st.form("form_recuperar"):
                st.subheader("Recuperar Usuario o Contraseña")
                st.write("Ingrese el correo electrónico registrado con el que creó su cuenta:")
                email_recuperar = st.text_input("Correo Electrónico Registrado")
                submit_recuperar = st.form_submit_button("Enviar Credenciales al Correo")
                
                if submit_recuperar:
                    if email_recuperar:
                        encontrado, user_rec, pass_rec = recuperar_credenciales(email_recuperar)
                        if encontrado:
                            st.success(f"📧 Se ha enviado un mensaje a {email_recuperar} con sus datos de acceso.")
                            st.info(f"**Usuario:** {user_rec} | **Contraseña:** {pass_rec}")
                        else:
                            st.error("No se encontró ninguna cuenta asociada a este correo electrónico.")
                    else:
                        st.warning("Por favor ingrese su correo electrónico.")
    
    st.stop()

# ----------------- APLICACIÓN PRINCIPAL -----------------
st.sidebar.title(f"👤 {st.session_state.usuario_actual}")
# Definir IMG_LOGO por seguridad si no existe
# Cargar el logo oficial directamente desde la carpeta assets en la barra lateral
st.sidebar.image("logo.png", use_container_width=True)
# Botón rápido de contacto en la barra lateral
st.sidebar.markdown(f"📱 **Contacto / Pagos:**\n`{NUMERO_PAGOS_DIGITALES}`")
st.sidebar.markdown("---")

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

modulo_seleccionado = st.sidebar.selectbox("Seleccione un módulo:", modulos_lista, index=index_actual, key="menu_lateral_principal")
st.session_state.modulo_activo = modulo_seleccionado

# --- CUERPO PRINCIPAL ---
if st.session_state.modulo_activo == "Panel Principal":
    st.title("🥋 Club Jinsei Taekwondo Tenjo")
    st.markdown("Sistema oficial de gestión deportiva, académica y administrativa.")

elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    st.header("Carta de Exoneración y Documentos PDF")
    st.header("📄 Carta de Exoneración y Documentos PDF")
    
    tab_subir, tab_ver, tab_borrar = st.tabs(["Subir Documento", "Ver Documentos", "🗑️ Eliminar Documento"])
    
    with tab_subir:
        st.markdown("""
        <div class="exoneracion-box">
            <b>CLUB JINSEI TAEKWONDO TENJO</b><br>
            <b>ACUERDO DE EXONERACIÓN DE RESPONSABILIDAD Y ASUNCIÓN DE RIESGOS</b><br>
            <i>Sede: Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque</i><br><br>
            Por medio del presente documento, el deportista o su acudiente legal declaran que entienden y aceptan la práctica deportiva.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
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
        else:
            st.info("La carpeta de documentos no existe o está vacía.")

    with tab_borrar:
        st.subheader("🗑️ Eliminar Documento (Usuario)")
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
            st.info("La carpeta de documentos no existe o está vacía.")
    "Generar Carnet Digital (Con Foto y Logo)",
    "Agenda de Torneos y Eventos (Cargar/Manual)",
    "Pagos (Alerta)"

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.modulo_activo = "Panel Principal"
    st.rerun()

# --- BOTÓN / FLECHA UNIVERSAL DE REGRESO ---
if st.session_state.modulo_activo != "Panel Principal":
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.modulo_activo = "Panel Principal"
        st.rerun()
    st.markdown("---")

# --- MÓDULO: PANEL PRINCIPAL ---
if st.session_state.modulo_activo == "Panel Principal":
    html_header_main = f"""
        <div class="header-branding">
            <img src="data:image/jpeg;base64,{LOGO_BASE64}" class="header-logo">
            <div class="header-text">
                <h1 class="main-title-inline">¡JINSEI TAEKWONDO!</h1>
                <p class="sub-title-inline">Panel de Gestión Integral y Entrenador — Tenjo</p>
                <p class="location-text">📍 Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque</p>
                <p class="contact-text">📞 Contacto / WhatsApp: {TELEFONO_CLUB}</p>
            </div>
        </div>
    """
    st.markdown(html_header_main, unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🎯 Servicios Principales del Club")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    with col_s1:
        if st.button("🥋 S1: Taekwondo", use_container_width=True):
            st.session_state.ver_s1 = not st.session_state.get("ver_s1", False)
        if st.session_state.get("ver_s1", False):
            st.info("Formación Marcial: Técnica Kyorugi (combate), Poomsae (formas), acondicionamiento físico marcial y disciplina Kup/Dan.")
            
    with col_s2:
        if st.button("🏃 S2: Funcional", use_container_width=True):
            st.session_state.ver_s2 = not st.session_state.get("ver_s2", False)
        if st.session_state.get("ver_s2", False):
            st.success("Entrenamiento Funcional: Potencia, resistencia cardiovascular, flexibilidad metabólica y movilidad atlética.")

    with col_s3:
        if st.button("🛡️ S3: Defensa", use_container_width=True):
            st.session_state.ver_s3 = not st.session_state.get("ver_s3", False)
        if st.session_state.get("ver_s3", False):
            st.warning("Defensa Personal (Hosinsul): Agarres, zafes, desarmes y manejo de situaciones de riesgo real.")

    with col_s4:
        if st.button("💰 Pagos (Alerta)", use_container_width=True):
            st.session_state.modulo_activo = "Pagos (Alerta)"
            st.rerun()

    st.markdown("---")
st.subheader("⚡ Acceso Rápido a Módulos de Trabajo")

c_mod1, c_mod2 = st.columns(2)

with c_mod1:
    st.markdown("""
        <div class="card-servicio bg-azul">
            <div class="card-title-custom"><span class="badge-icon">01</span> Ficha Integral e IMC</div>
            <div class="card-desc-custom">Registro completo de datos de deportistas, EPS y cálculo nutricional IMC.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📁 Abrir Ficha e IMC", use_container_width=True, key="btn_m1"):
        st.session_state.modulo_activo = "Ficha Integral del Deportista e IMC"
        st.rerun()

    st.markdown("""
        <div class="card-servicio bg-rojo">
            <div class="card-title-custom"><span class="badge-icon">03</span> Galería y Videos (Multimedia)</div>
            <div class="card-desc-custom">Carga de podios, medallas, fotografías y videoteca técnica del club.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📸 Abrir Multimedia", use_container_width=True, key="btn_m3"):
        st.session_state.modulo_activo = "Galeria y Videos (Multimedia)"
        st.rerun()

    st.markdown("""
        <div class="card-servicio bg-verde">
            <div class="card-title-custom"><span class="badge-icon">05</span> Control de Asistencia</div>
            <div class="card-desc-custom">Registro de asistencia diaria por sesión y consulta de historial.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Abrir Asistencia", use_container_width=True, key="btn_m5"):
        st.session_state.modulo_activo = "Control de Asistencia"
        st.rerun()

    st.markdown("""
        <div class="card-servicio bg-amarillo">
            <div class="card-title-custom"><span class="badge-icon">07</span> Agenda de Torneos y Eventos</div>
            <div class="card-desc-custom">Calendario interactivo de exámenes y campeonatos.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🏆 Abrir Agenda", use_container_width=True, key="btn_m7"):
        st.session_state.modulo_activo = "Agenda de Torneos y Eventos"
        st.rerun()

with c_mod2:
    st.markdown("""
        <div class="card-servicio bg-verde">
            <div class="card-title-custom"><span class="badge-icon">02</span> Panel General del Entrenador</div>
            <div class="card-desc-custom">Centro administrativo: gestión de deportistas, macroestructura y documentos.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🥋 Abrir Panel Coach", use_container_width=True, key="btn_m2"):
        st.session_state.modulo_activo = "Panel General del Entrenador (Solo Coach)"
        st.rerun()

    st.markdown("""
        <div class="card-servicio bg-amarillo">
            <div class="card-title-custom"><span class="badge-icon">04</span> Generar Carnet Digital</div>
            <div class="card-desc-custom">Generación inmediata del carnet oficial con foto e insignia.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🏅 Abrir Carnet", use_container_width=True, key="btn_m4"):
        st.session_state.modulo_activo = "Generar Carnet Digital (Con Foto y Logo)"
        st.rerun()

    st.markdown("""
        <div class="card-servicio bg-azul">
            <div class="card-title-custom"><span class="badge-icon">06</span> Exoneraciones y PDFs</div>
            <div class="card-desc-custom">Firma digital y subida de cartas de deslinde de responsabilidad legal.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📄 Abrir Exoneraciones", use_container_width=True, key="btn_m6"):
        st.session_state.modulo_activo = "Cargar Fichas, Exoneraciones y PDFs"
        st.rerun()
    ed = row[2] if len(row) > 2 else "N/A"
    ep = row[3] if len(row) > 3 else "N/A"
    peso = float(row[4]) if len(row) > 4 else 60.0
    estatura = float(row[5]) if len(row) > 5 else 1.70
    grd = row[6] if len(row) > 6 else "N/A"
    tel = row[7] if len(row) > 7 else "N/A"
                            
imc = peso / (estatura ** 2)
st.info(f"**Documento:** {doc} | **Edad:** {ed} años | **EPS:** {ep} | **Contacto:** {tel}")
st.write(f"**Grado Actual:** {grd}")
if imc < 18.5:
    st.warning("Clasificación IMC: Bajo peso")
elif 18.5 <= imc < 25:
    st.success("Clasificación IMC: Peso normal (Saludable)")
elif 25 <= imc < 30:
    st.warning("Clasificación IMC: Sobrepeso")
else:
    st.error("Clasificación IMC: Obesidad")
st.write("Registre la asistencia diaria de los alumnos a las clases de Taekwondo y Funcional.")
fecha_asistencia = st.date_input("Fecha de la sesión", value=datetime.now())
if os.path.exists(ARCHIVO_DEPORTISTAS):
        with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
if len(reader) > 1:
                nombres = [row[0] for row in reader[1:]]
                with st.form("form_asistencia"):
                    st.subheader(f"Lista de Asistencia - {fecha_asistencia.strftime('%d/%m/%Y')}")
                    asistencias_marcadas = {}
                    for nombre in nombres:
                        asistencias_marcadas[nombre] = st.checkbox(f"Presente: {nombre}", value=True)
                    guardar_asistencia = st.form_submit_button("Guardar Asistencia del Día")
                    if guardar_asistencia:
                        file_exists = os.path.exists(ARCHIVO_ASISTENCIAS)
                        with open(ARCHIVO_ASISTENCIAS, mode="a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            if not file_exists:
                                writer.writerow(["Fecha", "Nombre", "Estado"])
                            for nombre, estado in asistencias_marcadas.items():
                                writer.writerow([str(fecha_asistencia), nombre, "Presente" if estado else "Ausente"])
 if len(reader) > 1:
            nombres = [row[0] for row in reader[1:]]
            with st.form("form_asistencia"):
                st.subheader(f"Lista de Asistencia - {fecha_asistencia.strftime('%d/%m/%Y')}")
                asistencias_marcadas = {}
                for nombre in nombres:
                    asistencias_marcadas[nombre] = st.checkbox(f"Presente: {nombre}", value=True)
                guardar_asistencia = st.form_submit_button("Guardar Asistencia del Día")

            if guardar_asistencia:
                file_exists = os.path.exists(ARCHIVO_ASISTENCIAS)
                with open(ARCHIVO_ASISTENCIAS, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Fecha", "Nombre", "Estado"])
                    for nombre, estado in asistencias_marcadas.items():
                        writer.writerow([str(fecha_asistencia), nombre, "Presente" if estado else "Ausente"])
                st.success("¡Asistencia registrada correctamente!")
        else:
            st.info("No hay deportistas registrados para tomar asistencia.")
    with open(ARCHIVO_ASISTENCIAS, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if len(reader) > 1:
        with open(ARCHIVO_ASISTENCIAS, "rb") as file_asist_csv:
            st.download_button(
                label=" Descargar Historial de Asistencias (Excel/CSV)",
                data=file_asist_csv,
                file_name="asistencias_jinsei.csv",
                mime="text/csv",
            )
        st.markdown("---")
        st.table(reader[1:])
    else:
        st.info("No hay historial guardado aún.")

# --- MÓDULO UNIFICADO PROTEGIDO: PANEL GENERAL DEL ENTRENADOR ---
elif st.session_state.modulo_activo == "Panel General del Entrenador (Solo Coach)":
    st.header("⚙️ Panel General del Entrenador (Exclusivo Coach)")
    st.write("Área administrativa protegida para la gestión completa del dojang, deportistas, planificaciones y documentos.")
    
    password_coach_ingresada = st.text_input("Ingrese la Contraseña del Entrenador para acceder", type="password")
    
    if password_coach_ingresada == CONTRASENA_ENTRENADOR:
        st.success("✅ Acceso autorizado al Panel del Entrenador.")
        st.markdown("---")
        
        tab_adm_deportistas, tab_adm_macro, tab_adm_docs = st.tabs([
            "📋 Gestión de Deportistas", 
            "📊 Macroestructura y Sesiones (con Excel)", 
            "📄 Exoneraciones (PDFs)"
        ])
        
        with tab_adm_deportistas:
            st.subheader("Administración de Atletas")
            sub_tab_list, sub_tab_add, sub_tab_del = st.tabs(["Base de Datos", "Agregar Atleta", "Eliminar Atleta"])
            
            with sub_tab_list:
                if os.path.exists(ARCHIVO_DEPORTISTAS):
                    with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                        reader_dep = list(csv.reader(f))
                        if len(reader_dep) > 1:
                            st.table(reader_dep)
                        else:
                            st.info("No hay deportistas en la base de datos.")
                else:
                    st.info("Archivo de deportistas no encontrado.")
                    
            with sub_tab_add:
                with st.form("form_add_coach_unificado"):
                    n_nom = st.text_input("Nombre Completo")
                    n_doc = st.text_input("Documento")
                    n_eda = st.number_input("Edad", min_value=3, max_value=99, value=12)
                    n_eps = st.text_input("EPS")
                    n_pes = st.number_input("Peso (kg)", min_value=10.0, max_value=200.0, value=50.0)
                    n_est = st.number_input("Estatura (m)", min_value=0.5, max_value=2.5, value=1.50)
                    n_gra = st.selectbox("Grado", ["Blanco (10° Kup)", "Amarillo (8° Kup)", "Verde (6° Kup)", "Azul (4° Kup)", "Rojo (2° Kup)", "Negro (1° Dan)"])
                    n_tel = st.text_input("Contacto")
                    if st.form_submit_button("Guardar en Base de Datos"):
                        if n_nom:
                            file_exists = os.path.exists(ARCHIVO_DEPORTISTAS)
                            with open(ARCHIVO_DEPORTISTAS, mode="a", newline="", encoding="utf-8") as f:
                                writer = csv.writer(f)
                                if not file_exists:
                                    writer.writerow(["Nombre", "Documento", "Edad", "EPS", "Peso", "Estatura", "Grado", "Contacto"])
                                writer.writerow([n_nom, n_doc, n_eda, n_eps, n_pes, n_est, n_gra, n_tel])
                            st.success(f"¡Deportista {n_nom} agregado exitosamente!")
                            st.rerun()
                        else:
                            st.warning("Ingrese al menos el nombre.")
                            
            with sub_tab_del:
                if os.path.exists(ARCHIVO_DEPORTISTAS):
                    with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                        reader_del = list(csv.reader(f))
                        if len(reader_del) > 1:
                            nombres_del = [row[0] for row in reader_del[1:]]
                            a_eliminar = st.selectbox("Seleccione el deportista a eliminar:", nombres_del)
                            if st.button("❌ Eliminar Permanentemente"):
                                nuevos_registros = [reader_del[0]] + [row for row in reader_del[1:] if row[0] != a_eliminar]
                                with open(ARCHIVO_DEPORTISTAS, mode="w", newline="", encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerows(nuevos_registros)
                                st.success(f"¡El deportista {a_eliminar} ha sido eliminado!")
                                st.rerun()
                        else:
                            st.info("No hay deportistas para eliminar.")
                            
        with tab_adm_macro:
            st.subheader("Planificación Anual y Carga de Archivos Excel")
            sub_macro_reg, sub_macro_subir_excel, sub_macro_ver = st.tabs(["Registrar Manual", "📤 Subir Excel / Archivo", "📋 Ver Planificación"])
            
            with sub_macro_reg:
                with st.form("form_macro_unificado"):
                    ciclo = st.selectbox("Tipo de Planificación", ["Mesociclo de Fuerza", "Mesociclo de Resistencia", "Microciclo Técnico Poomsae", "Microciclo Kyorugi (Combate)", "Evaluación / Examen de Grado"])
                    fecha_sesion = st.date_input("Fecha de Aplicación", value=datetime.now())
                    objetivo = st.text_area("Objetivo Técnico / Físico de la Sesión")
                    detalles = st.text_area("Desarrollo de la Sesión (Calentamiento, Fase Central, Vuelta a la calma)")
                    
                    if st.form_submit_button("Guardar Planificación Manual"):
                        if objetivo and detalles:
                            file_exists = os.path.exists(ARCHIVO_MACRO)
                            with open(ARCHIVO_MACRO, mode="a", newline="", encoding="utf-8") as f:
                                writer = csv.writer(f)
                                if not file_exists:
                                    writer.writerow(["Tipo", "Fecha", "Objetivo", "Detalles"])
                                writer.writerow([ciclo, str(fecha_sesion), objetivo, detalles])
                            st.success("¡Planificación guardada con éxito!")
                        else:
                            st.warning("Por favor complete los campos obligatorios.")
                            
            with sub_macro_subir_excel:
                with st.form("form_subir_macro_excel"):
                    st.subheader("Subir Planificación en Excel")
                    titulo_excel = st.text_input("Título del Ciclo o Macroestructura (Ej: Macro Anual 2026)")
                    archivo_excel = st.file_uploader("Seleccione archivo de Excel (.xlsx, .xls) o CSV", type=["xlsx", "xls", "csv"])
                    submit_excel = st.form_submit_button("Subir Archivo de Planificación")
                    
                    if submit_excel:
                        if titulo_excel and archivo_excel is not None:
                            nombre_limpio_exc = titulo_excel.replace(" ", "_").lower()
                            ext_exc = archivo_excel.name.split('.')[-1]
                            nombre_archivo_exc_final = f"{nombre_limpio_exc}.{ext_exc}"
                            ruta_exc_destino = MACRO_DIR / nombre_archivo_exc_final
                            with open(ruta_exc_destino, "wb") as f:
                                f.write(archivo_excel.getbuffer())
                            st.success(f"¡Archivo '{archivo_excel.name}' subido y guardado exitosamente!")
                        else:
                            st.warning("Por favor ingrese un título y adjunte un archivo válido.")
                            
            with sub_macro_ver:
                st.subheader("Planificaciones Manuales Registradas")
                if os.path.exists(ARCHIVO_MACRO):
                    with open(ARCHIVO_MACRO, mode="r", encoding="utf-8") as f:
                        reader_m = list(csv.reader(f))
                        if len(reader_m) > 1:
                            st.table(reader_m)
                        else:
                            st.info("No hay planificaciones manuales registradas todavía.")
                else:
                    st.info("Aún no se han creado registros manuales.")
                    
                st.markdown("---")
                st.subheader("Archivos de Excel / CSV Subidos")
                archivos_excel_list = list(MACRO_DIR.glob("*.*"))
                if archivos_excel_list:
                    for arch_ex in archivos_excel_list:
                        col_ex1, col_ex2 = st.columns([3, 1])
                        with col_ex1:
                            st.write(f"📊 `{arch_ex.name}`")
                        with col_ex2:
                            with open(arch_ex, "rb") as f_ex:
                                st.download_button(
                                    label="⬇️ Descargar",
                                    data=f_ex,
                                    file_name=arch_ex.name,
                                    mime="application/octet-stream",
                                    key=f"dl_ex_{arch_ex.name}"
                                )
                else:
                    st.info("No hay archivos de Excel cargados en el sistema.")
                    
        with tab_adm_docs:
            st.subheader("Documentos y Cartas de Exoneración Firmadas")
            archivos_pdf = list(EXONERACIONES_DIR.glob("*.pdf"))
            if archivos_pdf:
                st.write(f"Se encontraron **{len(archivos_pdf)}** documentos firmados en el sistema:")
                for archivo in archivos_pdf:
                    col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
                    with col_p1:
                        st.write(f"📄 `{archivo.name}`")
                    with col_p2:
                        with open(archivo, "rb") as f:
                            st.download_button(
                                label="⬇️ Descargar",
                                data=f,
                                file_name=archivo.name,
                                mime="application/pdf",
                                key=f"dl_panel_{archivo.name}"
                            )
                    with col_p3:
                        if st.button("🗑️ Borrar", key=f"del_pdf_{archivo.name}"):
                            try:
                                archivo.unlink()
                                st.success(f"¡{archivo.name} eliminado!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
            else:
                st.info("No hay documentos PDF cargados todavía.")
                
    elif password_coach_ingresada != "":
        st.error("⚠️ Contraseña incorrecta. Acceso denegado al panel de administración.")

# --- MÓDULO UNIFICADO MULTIMEDIA: FOTOGRAFÍAS Y VIDEOS ---
elif st.session_state.modulo_activo == "Galería y Videos (Multimedia)":
    st.header("📸 Galería y Videoteca del Club Jinsei Taekwondo")
    
    # Menú simple en radio para alternar entre gestionar fotos o videos
    opcion_multimedia = st.radio("Seleccione qué desea gestionar:", ["Gestión de Fotos", "Gestión de Vídeos"], horizontal=True)
    st.markdown("---")
    
    if opcion_multimedia == "Gestión de Fotos":
        st.subheader("📤 Subir Nueva Foto")
        foto_subida = st.file_uploader("Seleccione la imagen", type=["jpg", "jpeg", "png"], key="subir_foto_dir")
        if st.button("Guardar Foto", key="btn_save_f_dir"):
            if foto_subida is not None:
                ruta = os.path.join(FOTOS_DIR, foto_subida.name)
                with open(ruta, "wb") as f:
                    f.write(foto_subida.getbuffer())
                st.success(f"¡Foto '{foto_subida.name}' guardada con éxito!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🖼️ Fotos Actuales y Opción de Borrado")
        if os.path.exists(FOTOS_DIR):
            lista_fotos = [f for f in os.listdir(FOTOS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if lista_fotos:
                foto_a_borrar = st.selectbox("Seleccione la foto que desea eliminar:", lista_fotos, key="sel_f_borrar")
                if st.button("❌ Eliminar Foto Seleccionada", key="btn_del_f_dir"):
                    os.remove(os.path.join(FOTOS_DIR, foto_a_borrar))
                    st.success(f"La foto '{foto_a_borrar}' ha sido eliminada.")
                    st.rerun()
            else:
                st.info("No hay fotos guardadas en el sistema.")
        else:
            st.info("La carpeta de fotos no existe.")
            
    else:
        st.subheader("📤 Subir Nuevo Vídeo")
        video_subido = st.file_uploader("Seleccione el archivo de vídeo", type=["mp4", "mov", "avi"], key="subir_video_dir")
        if st.button("Guardar Vídeo", key="btn_save_v_dir"):
            if video_subido is not None:
                ruta_v = os.path.join(VIDEOS_DIR, video_subido.name)
                with open(ruta_v, "wb") as f:
                    f.write(video_subido.getbuffer())
                st.success(f"¡Vídeo '{video_subido.name}' guardado con éxito!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🎥 Vídeos Actuales y Opción de Borrado")
        if os.path.exists(VIDEOS_DIR):
            lista_videos = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            if lista_videos:
                video_a_borrar = st.selectbox("Seleccione el vídeo que desea eliminar:", lista_videos, key="sel_v_borrar")
                if st.button("❌ Eliminar Vídeo Seleccionado", key="btn_del_v_dir"):
                    os.remove(os.path.join(VIDEOS_DIR, video_a_borrar))
                    st.success(f"El vídeo '{video_a_borrar}' ha sido eliminado.")
                    st.rerun()
            else:
                st.info("No hay vídeos guardados en el sistema.")
        else:
            st.info("La carpeta de vídeos no existe.")

elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    st.header("📄 Carta de Exoneración y Documentos PDF")
    
    tab_subir, tab_ver, tab_borrar = st.tabs(["Subir Documento", "Ver Documentos", "🗑️ Eliminar Documento"])
    
    with tab_subir:
        st.markdown("""
        <div class="exoneracion-box">
            <b>CLUB JINSEI TAEKWONDO TENJO</b><br>
            <b>ACUERDO DE EXONERACIÓN DE RESPONSABILIDAD Y ASUNCIÓN DE RIESGOS</b><br>
            <i>Sede: Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque</i><br><br>
            Por medio del presente documento, el deportista o su acudiente legal declaran que entienden y aceptan la práctica deportiva.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
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
        else:
            st.info("La carpeta de documentos no existe o está vacía.")

    with tab_borrar:
        st.subheader("🗑️ Eliminar Documento")
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
            st.info("La carpeta de documentos no existe o está vacía.")

elif st.session_state.modulo_activo == "Generar Carnet Digital (Con Foto y Logo)":
    st.header("📇 Generador de Carnet Digital Oficial")
    if os.path.exists(ARCHIVO_DEPORTISTAS):
        with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                nombres = [row[0] for row in reader[1:]]
                seleccionado = st.selectbox("Seleccionar Atleta:", nombres)
                col_c1, col_c2 = st.columns([1, 1])
                with col_c1:
                    for row in reader[1:]:
                        if row[0] == seleccionado:
                            doc = row[1] if len(row) > 1 else "N/A"
                            ed = row[2] if len(row) > 2 else "N/A"
                            grd = row[6] if len(row) > 6 else "N/A"
                            st.markdown(f"""
                            <div style="border: 4px solid #1E3A8A; padding: 20px; border-radius: 15px; background: white; text-align: center; color: black; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                                <h2 style="color: #1E3A8A; margin:0; font-size: 22px;">CLUB JINSEI TAEKWONDO</h2>
                                <p style="font-size:11px; color:gray; margin-bottom:2px;">TENJO — CUNDINAMARCA | CARNET 2026</p>
                                <p style="font-size:10px; color:#059669; font-weight:bold;">Vereda Chincé, Sector Zoque</p>
                                <p style="font-size:10px; color:#1E3A8A; font-weight:bold;">Tel: {TELEFONO_CLUB}</p>
                                <hr>
                                <h3 style="margin: 10px 0; color:#0F172A;">{row[0]}</h3>
                                <p><b>Documento:</b> {doc}</p>
                                <p><b>Grado:</b> {grd}</p>
                                <p><b>Edad:</b> {ed} años</p>
                                <div style="background-color: #16A34A; color: white; padding: 6px; border-radius: 5px; margin-top: 15px; font-weight: bold;">ESTADO: ACTIVO</div>
                            </div>
                            """, unsafe_allow_html=True)
                with col_c2:
                    st.subheader("Fotografía del Deportista")
                    if IMG_FOTO:
                        st.image(IMG_FOTO, caption=f"Foto Oficial: {seleccionado}", width=220)
                    else:
                        st.info("Para asignar la foto oficial del atleta, coloque un archivo nombrado 'foto.JPG' en la carpeta assets.")
            else:
                st.info("Debe registrar deportistas primero.")
    else:
        st.info("No hay base de datos activa.")

elif st.session_state.modulo_activo == "Agenda de Torneos y Eventos (Cargar/Manual)":
    st.header("📅 Agenda de Torneos, Exámenes y Eventos")
    with st.form("form_evento"):
        nuevo_evento = st.text_input("Nombre del Torneo o Examen")
        fecha_evento = st.date_input("Fecha programada")
        submit_evento = st.form_submit_button("Registrar en Agenda")
        if submit_evento:
            if nuevo_evento:
                with open(ARCHIVO_EVENTOS, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([nuevo_evento, str(fecha_evento), datetime.now().strftime("%Y-%m-%d")])
                st.success("¡Evento agregado con éxito!")
    if os.path.exists(ARCHIVO_EVENTOS):
        st.subheader("Eventos Programados:")
        with open(ARCHIVO_EVENTOS, mode="r", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row:
                    st.write(f"• **{row[0]}** — Fecha: {row[1]}")

# --- MÓDULO: PAGOS Y MÉTODOS DIGITALES CON RECIBO ---
elif st.session_state.modulo_activo == "Pagos (Alerta)":
    st.header("💰 Control de Pagos, Métodos Digitales y Recibos")
    
    # Caja informativa de medios de pago
    st.info(f"""
    📲 **MÉTODOS DE PAGO DIGITAL DISPONIBLES:**
    * **Nequi:** `{NUMERO_PAGOS_DIGITALES}`
    * **Daviplata:** `{NUMERO_PAGOS_DIGITALES}`
    * **Dale / Llave:** `{NUMERO_PAGOS_DIGITALES}`
    
    *Una vez realizado el pago, informe al Entrenador o registre la transacción para generar su recibo oficial.*
    """)
    st.markdown("---")
    
    tab_pago_ver, tab_pago_reg, tab_pago_recibo = st.tabs([
        "📋 Estado de Pagos Actuales", 
        "➕ Registrar Pago / Mensualidad", 
        "🧾 Generar Recibo de Pago"
    ])
    
    with tab_pago_ver:
        if os.path.exists(ARCHIVO_PAGOS):
            with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                if len(reader) > 1:
                    st.write("### Listado de Control Financiero:")
                    for row in reader[1:]:
                        atleta_p = row[0]
                        estado_p = row[1]
                        fecha_p = row[2]
                        monto_p = row[3] if len(row) > 3 else "60.000 COP"
                        metodo_p = row[4] if len(row) > 4 else "Nequi / Daviplata"
                        
                        if estado_p == "Al Día":
                            st.success(f"✅ **{atleta_p}** — Estado: **Al Día** | Último pago: {fecha_p} | Valor: {monto_p} ({metodo_p})")
                        else:
                            st.error(f"🚨 **{atleta_p}** — Alerta: **Pago Pendiente / Atrasado** | Ref: {fecha_p}")
                else:
                    st.info("No hay registros de pagos cargados.")
        else:
            st.info("Aún no hay registros de pagos guardados. Utilice la pestaña de registro para agregar estados.")
            
    with tab_pago_reg:
        if st.session_state.usuario_actual == "admin" or st.session_state.usuario_actual == "coach":
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                    reader_dep = list(csv.reader(f))
                    if len(reader_dep) > 1:
                        nombres_deps = [row[0] for row in reader_dep[1:]]
                        with st.form("form_estado_pago"):
                            atleta_elegido = st.selectbox("Seleccione Deportista", nombres_deps)
                            estado_seleccionado = st.selectbox("Estado de Mensualidad", ["Al Día", "Pendiente / Vencido"])
                            monto_ingresado = st.text_input("Valor Pagado (Ej: $60.000 COP)", value="$60.000 COP")
                            metodo_ingresado = st.selectbox("Medio de Pago", ["Nequi", "Daviplata", "Llave / Dale", "Efectivo", "Transferencia Bancaria"])
                            fecha_pago_reg = st.date_input("Fecha del Pago", value=datetime.now())
                            submit_pago = st.form_submit_button("Guardar Estado de Pago y Habilitar Recibo")
                            
                            if submit_pago:
                                registros_pagos = []
                                if os.path.exists(ARCHIVO_PAGOS):
                                    with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as fp:
                                        registros_pagos = list(csv.reader(fp))
                                
                                header_p = ["Deportista", "Estado", "Fecha", "Monto", "Metodo"]
                                if not registros_pagos:
                                    registros_pagos = [header_p]
                                
                                actualizado = False
                                for i in range(1, len(registros_pagos)):
                                    if registros_pagos[i][0] == atleta_elegido:
                                        registros_pagos[i][1] = estado_seleccionado
                                        registros_pagos[i][2] = str(fecha_pago_reg)
                                        if len(registros_pagos[i]) > 3:
                                            registros_pagos[i][3] = monto_ingresado
                                            registros_pagos[i][4] = metodo_ingresado
                                        else:
                                            registros_pagos[i].extend([monto_ingresado, metodo_ingresado])
                                        actualizado = True
                                        break
                                if not actualizado:
                                    registros_pagos.append([atleta_elegido, estado_seleccionado, str(fecha_pago_reg), monto_ingresado, metodo_ingresado])
                                    
                                with open(ARCHIVO_PAGOS, mode="w", newline="", encoding="utf-8") as fp:
                                    writer_p = csv.writer(fp)
                                    writer_p.writerows(registros_pagos)
                                st.success(f"¡Estado de pago y comprobante registrados para {atleta_elegido}!")
                                st.rerun()
                    else:
                        st.info("No hay deportistas registrados en la base de datos.")
            else:
                st.info("Debe registrar deportistas primero.")
        else:
            st.error("⚠️ Acceso restringido. La modificación de estados de pago es exclusiva para el Entrenador (Coach).")

    with tab_pago_recibo:
        st.subheader("📄 Generación de Recibo Digital Oficial")
        if os.path.exists(ARCHIVO_PAGOS):
            with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as f:
                reader_r = list(csv.reader(f))
                if len(reader_r) > 1:
                    al_dia_list = [row for row in reader_r[1:] if row[1] == "Al Día"]
                    if al_dia_list:
                        nombres_recibo = [row[0] for row in al_dia_list]
                        atleta_recibo_sel = st.selectbox("Seleccionar Deportista con Pago al Día:", nombres_recibo)
                        
                        for r_row in al_dia_list:
                            if r_row[0] == atleta_recibo_sel:
                                f_pago = r_row[2]
                                val_pago = r_row[3] if len(r_row) > 3 else "$60.000 COP"
                                met_pago = r_row[4] if len(r_row) > 4 else "Nequi / Daviplata"
                                num_recibo = f"JINSEI-{datetime.now().strftime('%Y%m%d')}-{r_row[0][:3].upper()}"
                                
                                texto_recibo = f"""
=====================================================
          CLUB JINSEI TAEKWONDO TENJO
      RECIBO OFICIAL DE PAGO Y MENSUALIDAD
=====================================================
Nº Comprobante: {num_recibo}
Fecha de Emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}
-----------------------------------------------------
Deportista / Alumno: {r_row[0]}
Concepto: Mensualidad de Entrenamiento
Monto Recibido: {val_pago}
Medio de Pago: {met_pago}
Fecha de Transacción: {f_pago}
Estado: PAGO CONFIRMADO / AL DÍA
-----------------------------------------------------
Sede: Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque
Tel / WhatsApp Pagos: {NUMERO_PAGOS_DIGITALES}
¡Gracias por ser parte de la familia Jinsei Taekwondo!
=====================================================
                                """
                                st.markdown(f"""
                                <div class="recibo-card">
                                    <h3 style="color:#1E3A8A; margin-top:0;">🧾 RECIBO DE PAGO COMPROBADO</h3>
                                    <p><b>Comprobante N°:</b> <code>{num_recibo}</code></p>
                                    <p><b>Recibimos de:</b> {r_row[0]}</p>
                                    <p><b>Valor:</b> {val_pago} | <b>Medio:</b> {met_pago}</p>
                                    <p><b>Fecha de Pago:</b> {f_pago}</p>
                                    <p style="color:#15803D; font-weight:bold;">ESTADO: CONFIRMADO Y AL DÍA ✅</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.download_button(
                                    label="📥 Descargar Recibo Oficial (.TXT)",
                                    data=texto_recibo,
                                    file_name=f"recibo_pago_{r_row[0].replace(' ', '_').lower()}.txt",
                                    mime="text/plain"
                                )
                    else:
                        st.info("No hay deportistas con pagos confirmados 'Al Día' para generar recibo.")
                else:
                    st.info("No hay historial de pagos registrado.")
        else:
            st.info("No existe la base de datos de pagos todavía.")