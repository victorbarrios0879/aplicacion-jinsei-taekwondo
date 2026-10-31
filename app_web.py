import streamlit as st
import os
import csv
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image

# ----------------- CONFIGURACIÓN Y ESTADO DE SESIÓN -----------------
st.set_page_config(
    page_title="Jinsei Taekwondo Tenjo - Panel Principal",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

modulos_lista = [
    "Panel Principal",
    "Ficha Integral del Deportista e IMC",
    "Control de Asistencia",
    "Panel General del Entrenador (Solo Coach)",
    "Galería y Videos (Multimedia)",
    "Cargar Fichas, Exoneraciones y PDFs",
    "Archivo de Eventos, Competencias y Ascensos",
    "Agenda de Torneos y Eventos",
    "Pagos (Alerta)"
]

# MAPEO DE NOMBRES DE MÓDULOS A CLAVES SIMPLES PARA LA URL
MODULO_A_SLUG = {
    "Panel Principal": "inicio",
    "Ficha Integral del Deportista e IMC": "imc",
    "Control de Asistencia": "asistencia",
    "Panel General del Entrenador (Solo Coach)": "coach",
    "Galería y Videos (Multimedia)": "multimedia",
    "Cargar Fichas, Exoneraciones y PDFs": "exoneraciones",
    "Archivo de Eventos, Competencias y Ascensos": "archivo",
    "Agenda de Torneos y Eventos": "agenda",
    "Pagos (Alerta)": "pagos"
}
SLUG_A_MODULO = {v: k for k, v in MODULO_A_SLUG.items()}

# SINCRONIZACIÓN DE LA NAVEGACIÓN CON LA URL (Para botón Atrás en celulares)
query_params = st.query_params
slug_actual = query_params.get("modulo", "inicio")
modulo_desde_url = SLUG_A_MODULO.get(slug_actual, "Panel Principal")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "modulo_activo" not in st.session_state or st.session_state.modulo_activo != modulo_desde_url:
    st.session_state.modulo_activo = modulo_desde_url

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

def cambiar_modulo(nuevo_modulo):
    """Cambia el módulo activo, actualiza la URL para soportar 'Atrás' en móviles y recarga."""
    st.session_state.modulo_activo = nuevo_modulo
    st.query_params["modulo"] = MODULO_A_SLUG.get(nuevo_modulo, "inicio")
    st.rerun()

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

ARCHIVO_DOCUMENTOS_DIR = BASE_DIR / "archivo_documentos_club"
ARCHIVO_DOCUMENTOS_DIR.mkdir(exist_ok=True)
CATEGORIAS_DOCUMENTOS = ["Eventos", "Competencias", "Exámenes de ascenso", "Otros documentos del club"]
for cat in CATEGORIAS_DOCUMENTOS:
    (ARCHIVO_DOCUMENTOS_DIR / cat).mkdir(exist_ok=True)

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

# ----------------- DIAGNÓSTICO Y LOCALIZACIÓN DE FONDO (jinsei.JPG) -----------------
def localizar_fotografia_fondo():
    ruta_principal = BASE_DIR / "assets" / "jinsei.JPG"
    if ruta_principal.exists():
        return ruta_principal
        
    respaldos = [
        BASE_DIR / "assets" / "jinsei.jpg",
        BASE_DIR / "jinsei.JPG",
        BASE_DIR / "jinsei.jpg"
    ]
    for r in respaldos:
        if r.exists():
            return r
            
    return None

def aplicar_estilos_institucionales():
    foto_bg_path = localizar_fotografia_fondo()
    imagen_css = ""
    
    if foto_bg_path and foto_bg_path.exists():
        with open(foto_bg_path, "rb") as archivo:
            encoded_bg = base64.b64encode(archivo.read()).decode("ascii")
        mime = "image/png" if foto_bg_path.suffix.lower() == ".png" else "image/jpeg"
        imagen_css = f'url("data:{mime};base64,{encoded_bg}")'
    else:
        archivos_en_assets = []
        if ASSETS_DIR.exists():
            archivos_en_assets = [f.name for f in ASSETS_DIR.iterdir()]
        else:
            archivos_en_assets = ["La carpeta 'assets' no existe en el servidor."]
            
        st.error(
            f"⚠️ **DIAGNÓSTICO DE ERROR DE FONDO:**\n\n"
            f"- **Ubicación de app_web.py:** `{BASE_DIR}`\n"
            f"- **Ruta principal verificada:** `{BASE_DIR / 'assets' / 'jinsei.JPG'}` (No encontrada)\n"
            f"- **Archivos reales encontrados en la carpeta 'assets':** `{archivos_en_assets}`"
        )

    css = f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.72)),
            {imagen_css if imagen_css else "none"};
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(255,255,255,0.15);
    }}
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {{
        background-color: transparent;
    }}
    .login-container {{
        background: rgba(255, 255, 255, 0.90);
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        max-width: 450px;
        margin: 0 auto;
    }}
    .card-servicio {{
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }}
    .bg-azul {{ background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); }}
    .bg-verde {{ background: linear-gradient(135deg, #15803D 0%, #22C55E 100%); }}
    .bg-rojo {{ background: linear-gradient(135deg, #B91C1C 0%, #EF4444 100%); }}
    .bg-amarillo {{ background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%); color: #1E293B; }}
    .bg-morado {{ background: linear-gradient(135deg, #581C87 0%, #9333EA 100%); }}
    .card-title-custom {{ font-size: 18px; font-weight: bold; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
    .card-desc-custom {{ font-size: 13px; opacity: 0.95; font-weight: normal; }}
    .badge-icon {{ padding: 4px 10px; border-radius: 20px; font-size: 12px; background: #1E3A8A; color: white; margin-right: 6px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

aplicar_estilos_institucionales()

def localizar_logo():
    candidatos = [
        ASSETS_DIR / "logo.png",
        ASSETS_DIR / "LOGO.png",
        BASE_DIR / "logo.png",
        BASE_DIR / "LOGO.png"
    ]
    for c in candidatos:
        if c.is_file():
            return c
    return None

def obtener_logo_base64():
    logo_path = localizar_logo()
    if logo_path and logo_path.exists():
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        mime = "image/png" if logo_path.suffix.lower() == ".png" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"
    return ""

def mostrar_encabezado_institucional(titulo_modulo=""):
    """Función global reutilizable con logo institucional fijo a 260px de altura real."""
    logo_base64 = obtener_logo_base64()
    
    img_html = f'<img src="{logo_base64}" style="height: 260px; width: auto; max-width: 100%; display: block;" />' if logo_base64 else '🥋'
    
    titulo_texto = f"JINSEI Club de Taekwondo Tenjo — <span style='font-size: 22px; color: #334155;'>{titulo_modulo}</span>" if titulo_modulo else "JINSEI Club de Taekwondo Tenjo"
    
    header_html = f"""
    <div style="display: flex; align-items: center; gap: 25px; margin-bottom: 20px; flex-wrap: wrap;">
        <div>{img_html}</div>
        <div>
            <h1 style="color: #1E3A8A; margin: 0; font-size: 32px; line-height: 1.2;">{titulo_texto}</h1>
        </div>
    </div>
    <hr style="margin-top: 5px; margin-bottom: 25px;">
    """
    st.markdown(header_html, unsafe_allow_html=True)

# ----------------- AUTENTICACIÓN Y LOGIN -----------------
if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.4, 1])

    with col_centro:
        logo_base64 = obtener_logo_base64()
        img_login_html = f'<img src="{logo_base64}" style="height: 220px; width: auto; max-width: 100%; display: block;" />' if logo_base64 else '🥋'

        login_header_html = f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 10px;">
            <div>{img_login_html}</div>
            <div>
                <h2 style="color: #1E3A8A; margin: 0; line-height: 1.1; font-size: 28px;">JINSEI</h2>
                <p style="color: #475569; margin: 0; font-size: 15px;">Taekwondo Tenjo</p>
            </div>
        </div>
        <hr style="margin: 15px 0;">
        """
        st.markdown(login_header_html, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🔑 Ingresar", "📝 Registrarse", "❓ Recuperar"])

        with tab1:
            with st.form("form_login"):
                st.markdown("#### Iniciar Sesión")
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
            with st.form("form_registro"):
                st.markdown("#### Nuevo Usuario")
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
            with st.form("form_recuperar"):
                st.markdown("#### Recuperar Cuenta")
                correo_recuperar = st.text_input("Correo registrado")
                submit_recuperar = st.form_submit_button("Buscar", use_container_width=True)
                
            if submit_recuperar:
                encontrado, u, p = recuperar_credenciales(correo_recuperar)
                if encontrado:
                    st.info(f"🔑 Usuario: **{u}** | Clave: **{p}**")
                else:
                    st.error("No se encontró cuenta asociada.")

    st.stop()

# ----------------- PANEL PRIVADO Y NAVEGACIÓN -----------------
st.sidebar.title(f"👤 {st.session_state.get('usuario_actual', 'Coach')}")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.modulo_activo = "Panel Principal"
    st.query_params.clear()
    st.rerun()

st.sidebar.info("Jinsei Taekwondo — Tenjo")
logo_lateral = localizar_logo()
if logo_lateral and logo_lateral.exists():
    st.sidebar.image(str(logo_lateral), use_container_width=True)

st.sidebar.markdown(f"📱 **Contacto / Pagos:**\n`{NUMERO_PAGOS_DIGITALES}`")
st.sidebar.markdown("---")

try:
    index_actual = modulos_lista.index(st.session_state.modulo_activo)
except ValueError:
    index_actual = 0

def actualizar_desde_sidebar():
    nuevo_sel = st.session_state.menu_lateral_select
    st.session_state.modulo_activo = nuevo_sel
    st.query_params["modulo"] = MODULO_A_SLUG.get(nuevo_sel, "inicio")

st.sidebar.selectbox(
    "Seleccione un módulo:",
    modulos_lista,
    index=index_actual,
    key="menu_lateral_select",
    on_change=actualizar_desde_sidebar
)

if st.session_state.modulo_activo != "Panel Principal":
    if st.button("⬅️ Regresar al menú principal", use_container_width=True):
        cambiar_modulo("Panel Principal")
    st.markdown("---")

# ----------------- MÓDULOS DE TRABAJO -----------------

if st.session_state.modulo_activo == "Panel Principal":
    mostrar_encabezado_institucional("Panel Principal")
    col_izq, col_der = st.columns([1.2, 2.8])
    
    with col_izq:
        st.subheader("🏛️ Servicios del Club")
        with st.expander("🥋 1. TAEKWONDO"):
            st.write("Formación deportiva y marcial para niños, jóvenes y adultos, enfocada en disciplina, respeto, técnica, autocontrol y desarrollo integral.")
        with st.expander("🏃 2. ENTRENAMIENTO FUNCIONAL"):
            st.write("Acondicionamiento físico, desarrollo de fuerza, resistencia, coordinación, flexibilidad y capacidades físicas.")
        with st.expander("🛡️ 3. DEFENSA PERSONAL"):
            st.write("Formación en técnicas de prevención, seguridad personal, reacción y defensa ante situaciones de riesgo.")
        
        st.markdown("---")
        st.info("📍 **Sede:** Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque\n📞 **WhatsApp:** " + TELEFONO_CLUB)

    with col_der:
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
            if st.button("📁 Abrir Ficha e IMC", use_container_width=True, key="btn_card_imc"):
                cambiar_modulo("Ficha Integral del Deportista e IMC")

            st.markdown('''
                <div class="card-servicio bg-rojo">
                    <div class="card-title-custom"><span class="badge-icon">03</span> Galería y Videos (Multimedia)</div>
                    <div class="card-desc-custom">Fotografías, eventos institucionales y videoteca técnica del club.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📸 Abrir Multimedia", use_container_width=True, key="btn_card_multimedia"):
                cambiar_modulo("Galería y Videos (Multimedia)")

            st.markdown('''
                <div class="card-servicio bg-verde">
                    <div class="card-title-custom"><span class="badge-icon">05</span> Control de Asistencia</div>
                    <div class="card-desc-custom">Calendario interactivo de asistencia diaria por sesión.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📊 Abrir Asistencia", use_container_width=True, key="btn_card_asistencia"):
                cambiar_modulo("Control de Asistencia")

            st.markdown('''
                <div class="card-servicio bg-morado">
                    <div class="card-title-custom"><span class="badge-icon">07</span> Archivo de Documentos</div>
                    <div class="card-desc-custom">Eventos, competencias, exámenes de ascenso y otros archivos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📂 Abrir Archivo de Documentos", use_container_width=True, key="btn_card_documentos"):
                cambiar_modulo("Archivo de Eventos, Competencias y Ascensos")

        with c_mod2:
            st.markdown('''
                <div class="card-servicio bg-verde">
                    <div class="card-title-custom"><span class="badge-icon">02</span> Panel del Entrenador</div>
                    <div class="card-desc-custom">Gestión completa de atletas, macroestructuras y documentos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("🥋 Abrir Panel Coach", use_container_width=True, key="btn_card_coach"):
                cambiar_modulo("Panel General del Entrenador (Solo Coach)")

            st.markdown('''
                <div class="card-servicio bg-amarillo">
                    <div class="card-title-custom"><span class="badge-icon">04</span> Exoneraciones y PDFs</div>
                    <div class="card-desc-custom">Gestión y borrado de cartas de deslinde de responsabilidad legal.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📄 Abrir Exoneraciones", use_container_width=True, key="btn_card_exoneraciones"):
                cambiar_modulo("Cargar Fichas, Exoneraciones y PDFs")

            st.markdown('''
                <div class="card-servicio bg-azul">
                    <div class="card-title-custom"><span class="badge-icon">06</span> Control de Pagos</div>
                    <div class="card-desc-custom">Estado de mensualidades, recibos oficiales y alertas de pagos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("💰 Abrir Pagos", use_container_width=True, key="btn_card_pagos"):
                cambiar_modulo("Pagos (Alerta)")

            st.markdown('''
                <div class="card-servicio bg-amarillo">
                    <div class="card-title-custom"><span class="badge-icon">08</span> Agenda de Torneos</div>
                    <div class="card-desc-custom">Calendario y registro de torneos y eventos próximos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📅 Abrir Agenda", use_container_width=True, key="btn_card_agenda"):
                cambiar_modulo("Agenda de Torneos y Eventos")

elif st.session_state.modulo_activo == "Ficha Integral del Deportista e IMC":
    mostrar_encabezado_institucional("Ficha Integral e IMC")
    tab_reg_i, tab_cons_i = st.tabs(["Registrar / Actualizar Deportista", "Consultar Historial e IMC"])
    
    with tab_reg_i:
        with st.form("form_ficha_integral"):
            nombre_dep = st.text_input("Nombre Completo del Deportista")
            doc_dep = st.text_input("Documento de Identidad")
            edad_dep = st.number_input("Edad", min_value=3, max_value=99, value=15)
            eps_dep = st.text_input("EPS / Seguro Médico")
            peso_dep = st.number_input("Peso Actual (kg)", min_value=10.0, max_value=200.0, value=60.0)
            est_dep = st.number_input("Estatura Actual (m)", min_value=0.5, max_value=2.5, value=1.70)
            grado_dep = st.selectbox("Grado / Cinturón", ["Blanco (10° Kup)", "Amarillo (8° Kup)", "Verde (6° Kup)", "Azul (4° Kup)", "Rojo (2° Kup)", "Negro (1° Dan)"])
            contacto_dep = st.text_input("Teléfono de Contacto / Acudiente")
            
            submit_ficha = st.form_submit_button("Guardar o Actualizar Ficha e IMC")
            if submit_ficha:
                if nombre_dep and doc_dep:
                    imc = peso_dep / (est_dep ** 2)
                    clasificacion_imc = "Bajo peso" if imc < 18.5 else ("Normal" if imc < 25 else ("Sobrepeso" if imc < 30 else "Obesidad"))
                    
                    registros = []
                    if os.path.exists(ARCHIVO_DEPORTISTAS):
                        with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                            registros = list(csv.reader(f))
                    
                    header = ["Nombre", "Documento", "Edad", "EPS", "Peso", "Estatura", "IMC", "Clasificacion", "Grado", "Contacto", "Fecha"]
                    if not registros:
                        registros = [header]
                    
                    actualizado = False
                    for i in range(1, len(registros)):