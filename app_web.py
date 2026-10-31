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
                        if registros[i][1] == doc_dep:
                            registros[i] = [nombre_dep, doc_dep, str(edad_dep), eps_dep, str(peso_dep), str(est_dep), f"{imc:.2f}", clasificacion_imc, grado_dep, contacto_dep, datetime.now().strftime("%Y-%m-%d")]
                            actualizado = True
                            break
                    if not actualizado:
                        registros.append([nombre_dep, doc_dep, str(edad_dep), eps_dep, str(peso_dep), str(est_dep), f"{imc:.2f}", clasificacion_imc, grado_dep, contacto_dep, datetime.now().strftime("%Y-%m-%d")])
                        
                    with open(ARCHIVO_DEPORTISTAS, mode="w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerows(registros)
                    st.success(f"¡Ficha de {nombre_dep} guardada con éxito! IMC Calculado: {imc:.2f} ({clasificacion_imc})")
                else:
                    st.warning("Por favor ingrese al menos el nombre y el documento.")

    with tab_cons_i:
        st.subheader("Historial y Consulta de Deportistas e IMC")
        if os.path.exists(ARCHIVO_DEPORTISTAS):
            with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                data = list(csv.reader(f))
                if len(data) > 1:
                    st.table(data)
                else:
                    st.info("No hay deportistas registrados.")
        else:
            st.info("Aún no hay registros en la base de datos.")

elif st.session_state.modulo_activo == "Control de Asistencia":
    mostrar_encabezado_institucional("Control de Asistencia")
    fecha_sesion = st.date_input("Seleccione Fecha de Entrenamiento", value=datetime.now())
    
    if os.path.exists(ARCHIVO_DEPORTISTAS):
        with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                nombres = [row[0] for row in reader[1:]]
                with st.form("form_asistencia_cal"):
                    st.subheader(f"Lista de Asistencia para el día: {fecha_sesion.strftime('%d/%m/%Y')}")
                    estados = {}
                    for nom in nombres:
                        estados[nom] = st.selectbox(f"Atleta: {nom}", ["Presente", "Ausente con Justificación", "Inasistencia Injustificada"], key=f"asist_{nom}")
                    submit_asist = st.form_submit_button("Guardar Asistencia de la Sesión")
                    
                    if submit_asist:
                        asistencias_previas = []
                        if os.path.exists(ARCHIVO_ASISTENCIAS):
                            with open(ARCHIVO_ASISTENCIAS, mode="r", encoding="utf-8") as fa:
                                asistencias_previas = list(csv.reader(fa))
                        
                        header_a = ["Fecha", "Nombre", "Estado"]
                        if not asistencias_previas:
                            asistencias_previas = [header_a]
                        
                        nuevas_asistencias = [row for row in asistencias_previas if not (row and row[0] == str(fecha_sesion))]
                        if len(nuevas_asistencias) == 0:
                            nuevas_asistencias = [header_a]
                            
                        for nom, est in estados.items():
                            nuevas_asistencias.append([str(fecha_sesion), nom, est])
                            
                        with open(ARCHIVO_ASISTENCIAS, mode="w", newline="", encoding="utf-8") as fa:
                            csv.writer(fa).writerows(nuevas_asistencias)
                        st.success("¡Asistencia registrada y actualizada correctamente sin duplicados!")
            else:
                st.info("No hay deportistas registrados para tomar asistencia.")
    else:
        st.info("Debe registrar deportistas primero en la ficha integral.")

elif st.session_state.modulo_activo == "Cargar Fichas, Exoneraciones y PDFs":
    mostrar_encabezado_institucional("Exoneraciones y PDFs")
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
    mostrar_encabezado_institucional("Panel Multimedia")
    opcion_multimedia = st.radio("Gestión de Multimedia:", ["Fotos del Club", "Vídeos de Técnica"], horizontal=True)
    st.markdown("---")
    
    if opcion_multimedia == "Fotos del Club":
        st.subheader("📤 Subir Nueva Foto")
        with st.form("form_subir_foto_multimedia"):
            foto_subida = st.file_uploader("Seleccione la imagen", type=["jpg", "jpeg", "png"])
            submit_foto = st.form_submit_button("Guardar Foto")
            if submit_foto:
                if foto_subida is not None:
                    ruta = FOTOS_CLUB_DIR / foto_subida.name
                    with open(ruta, "wb") as f:
                        f.write(foto_subida.getbuffer())
                    st.success(f"¡Foto '{foto_subida.name}' guardada con éxito!")
                    st.rerun()
                else:
                    st.warning("Seleccione una imagen primero.")
                
        st.markdown("---")
        st.subheader("🖼️ Galería de Fotografías")
        if os.path.exists(FOTOS_CLUB_DIR):
            lista_fotos = [f for f in os.listdir(FOTOS_CLUB_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if lista_fotos:
                for foto_item in lista_fotos:
                    col_f1, col_f2 = st.columns([3, 1])
                    with col_f1:
                        st.image(str(FOTOS_CLUB_DIR / foto_item), caption=foto_item, width=300)
                    with col_f2:
                        if st.button("🗑️ Eliminar Foto", key=f"del_foto_{foto_item}"):
                            st.session_state[f"confirm_del_foto_{foto_item}"] = True
                        
                        if st.session_state.get(f"confirm_del_foto_{foto_item}", False):
                            st.warning(f"¿Confirma eliminar '{foto_item}'?")
                            if st.button("Sí, eliminar definitivamente", key=f"yes_del_foto_{foto_item}"):
                                (FOTOS_CLUB_DIR / foto_item).unlink()
                                st.success("Foto eliminada correctamente.")
                                st.rerun()
                            if st.button("Cancelar", key=f"cancel_del_foto_{foto_item}"):
                                st.session_state[f"confirm_del_foto_{foto_item}"] = False
                                st.rerun()
                    st.markdown("---")
            else:
                st.info("No hay fotos guardadas aún.")
    else:
        st.subheader("📤 Subir Nuevo Vídeo")
        with st.form("form_subir_video_multimedia"):
            video_subido = st.file_uploader("Seleccione el archivo de vídeo", type=["mp4", "mov", "avi"])
            submit_video = st.form_submit_button("Guardar Vídeo")
            if submit_video:
                if video_subido is not None:
                    ruta_v = VIDEOS_DIR / video_subido.name
                    with open(ruta_v, "wb") as f:
                        f.write(video_subido.getbuffer())
                    st.success(f"¡Vídeo '{video_subido.name}' guardado con éxito!")
                    st.rerun()
                else:
                    st.warning("Seleccione un archivo de vídeo primero.")
                
        st.markdown("---")
        st.subheader("🎥 Videoteca Técnica y Reproducción")
        if os.path.exists(VIDEOS_DIR):
            lista_videos = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            if lista_videos:
                for vid_item in lista_videos:
                    st.write(f"🎬 **{vid_item}**")
                    
                    # Corrección robusta para asegurar renderizado visual del video en navegadores de escritorio
                    video_path = VIDEOS_DIR / vid_item
                    with open(video_path, "rb") as v_file:
                        video_bytes = v_file.read()
                    st.video(video_bytes, format="video/mp4")
                    
                    if st.button("🗑️ Eliminar Vídeo", key=f"del_vid_{vid_item}"):
                        st.session_state[f"confirm_del_vid_{vid_item}"] = True
                    
                    if st.session_state.get(f"confirm_del_vid_{vid_item}", False):
                        st.warning(f"¿Confirma eliminar el vídeo '{vid_item}'?")
                        if st.button("Sí, eliminar vídeo", key=f"yes_del_vid_{vid_item}"):
                            (VIDEOS_DIR / vid_item).unlink()
                            st.success("Vídeo eliminado correctamente.")
                            st.rerun()
                        if st.button("Cancelar", key=f"cancel_del_vid_{vid_item}"):
                            st.session_state[f"confirm_del_vid_{vid_item}"] = False
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("No hay vídeos guardados aún.")

elif st.session_state.modulo_activo == "Archivo de Eventos, Competencias y Ascensos":
    mostrar_encabezado_institucional("Archivo de Documentos")
    tab_doc_subir, tab_doc_ver = st.tabs(["Subir Documento / Archivo", "Consultar y Administrar Archivos"])
    
    with tab_doc_subir:
        with st.form("form_subir_archivo_general"):
            st.subheader("Subir Nuevo Documento al Archivo del Club")
            cat_sel = st.selectbox("Categoría", CATEGORIAS_DOCUMENTOS)
            nombre_doc = st.text_input("Nombre o Título del Documento")
            desc_doc = st.text_area("Descripción (Opcional)")
            fecha_doc = st.date_input("Fecha del Documento", value=datetime.now())
            
            archivo_subido = st.file_uploader(
                "Seleccione el archivo (PDF, Word, Excel, Imágenes u otros formatos)",
                type=["pdf", "docx", "doc", "xlsx", "xls", "csv", "jpg", "jpeg", "png", "txt"]
            )
            
            submit_archivo_gen = st.form_submit_button("Subir Archivo al Sistema")
            if submit_archivo_gen:
                if nombre_doc and archivo_subido is not None:
                    ext = archivo_subido.name.split('.')[-1]
                    nombre_archivo_seguro = f"{nombre_doc.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                    carpeta_destino = ARCHIVO_DOCUMENTOS_DIR / cat_sel
                    ruta_final = carpeta_destino / nombre_archivo_seguro
                    
                    with open(ruta_final, "wb") as f:
                        f.write(archivo_subido.getbuffer())
                        
                    meta_path = ARCHIVO_DOCUMENTOS_DIR / "metadatos_archivos.csv"
                    meta_exists = meta_path.exists()
                    with open(meta_path, mode="a", newline="", encoding="utf-8") as fm:
                        writer = csv.writer(fm)
                        if not meta_exists:
                            writer.writerow(["Categoria", "Nombre", "Descripcion", "Fecha", "NombreArchivo"])
                        writer.writerow([cat_sel, nombre_doc, desc_doc, str(fecha_doc), nombre_archivo_seguro])
                        
                    st.success(f"¡El documento '{nombre_doc}' se ha guardado exitosamente en la categoría '{cat_sel}'!")
                else:
                    st.warning("Por favor ingrese el nombre del documento y adjunte un archivo.")

    with tab_doc_ver:
        st.subheader("Consulta y Gestión por Categorías")
        cat_consulta = st.selectbox("Seleccione Categoría a Consultar", CATEGORIAS_DOCUMENTOS, key="sel_cat_consulta")
        carpeta_cat = ARCHIVO_DOCUMENTOS_DIR / cat_consulta
        
        if carpeta_cat.exists():
            archivos_en_cat = list(carpeta_cat.iterdir())
            if archivos_en_cat:
                for arch in archivos_en_cat:
                    if arch.is_file():
                        col_d1, col_d2, col_d3 = st.columns([2, 1, 1])
                        with col_d1:
                            st.write(f"📄 **{arch.name}**")
                        with col_d2:
                            with open(arch, "rb") as f_dl:
                                st.download_button(
                                    "⬇️ Descargar",
                                    data=f_dl,
                                    file_name=arch.name,
                                    key=f"dl_gen_{arch.name}"
                                )
                        with col_d3:
                            if st.button("🗑️ Eliminar", key=f"btn_del_arch_{arch.name}"):
                                st.session_state[f"confirm_del_arch_{arch.name}"] = True
                                
                            if st.session_state.get(f"confirm_del_arch_{arch.name}", False):
                                st.warning(f"¿Desea eliminar '{arch.name}'?")
                                if st.button("Sí, borrar", key=f"yes_del_arch_{arch.name}"):
                                    arch.unlink()
                                    st.success("Archivo eliminado.")
                                    st.rerun()
                                if st.button("Cancelar", key=f"cancel_del_arch_{arch.name}"):
                                    st.session_state[f"confirm_del_arch_{arch.name}"] = False
                                    st.rerun()
                st.markdown("---")
            else:
                st.info(f"No hay archivos almacenados en la categoría '{cat_consulta}'.")
        else:
            st.info("La carpeta de esta categoría no existe.")

elif st.session_state.modulo_activo == "Panel General del Entrenador (Solo Coach)":
    mostrar_encabezado_institucional("Panel del Entrenador")
    password_coach = st.text_input("Ingrese Contraseña de Autorización Coach", type="password")
    
    if password_coach == CONTRASENA_ENTRENADOR:
        st.success("✅ Acceso Autorizado al Panel de Control.")
        tab_dep_c, tab_reg_c, tab_del_c, tab_mac_c, tab_doc_c = st.tabs([
            "📋 Lista de Deportistas", 
            "➕ Registrar Deportista", 
            "🗑️ Eliminar Deportista", 
            "📊 Macroestructuras", 
            "📄 Documentos PDF"
        ])
        
        with tab_dep_c:
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                    data = list(csv.reader(f))
                    if len(data) > 1:
                        st.table(data)
                    else:
                        st.info("No hay deportistas registrados.")
            else:
                st.info("No hay registros en la base de datos.")

        with tab_reg_c:
            st.subheader("Registro Manual de Nuevo Deportista")
            with st.form("form_coach_reg_dep"):
                c1, c2 = st.columns(2)
                with c1:
                    nombres_reg = st.text_input("Nombres")
                    apellidos_reg = st.text_input("Apellidos")
                    doc_reg = st.text_input("Número de Documento")
                    fnac_reg = st.date_input("Fecha de Nacimiento", value=datetime(2010, 1, 1))
                    cat_reg = st.selectbox("Categoría", ["Infantil", "Cadetes", "Junior", "Sub-21", "Senior", "Master"])
                    genero_reg = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
                with c2:
                    tel_reg = st.text_input("Teléfono de Contacto")
                    acudiente_reg = st.text_input("Nombre del Acudiente")
                    tel_acu_reg = st.text_input("Teléfono del Acudiente")
                    fing_reg = st.date_input("Fecha de Ingreso al Club", value=datetime.now())
                    estado_reg = st.selectbox("Estado del Deportista", ["Activo", "Inactivo"])
                    eps_reg = st.text_input("EPS / Seguro Médico", value="EPS")
                
                submit_coach_dep = st.form_submit_button("Guardar Nuevo Deportista en el Sistema")
                if submit_coach_dep:
                    if nombres_reg and apellidos_reg and doc_reg:
                        edad_calc = datetime.now().year - fnac_reg.year - ((datetime.now().month, datetime.now().day) < (fnac_reg.month, fnac_reg.day))
                        nombre_completo = f"{nombres_reg} {apellidos_reg}"
                        
                        registros_dep = []
                        header_dep = ["Nombre", "Documento", "Edad", "EPS", "Peso", "Estatura", "IMC", "Clasificacion", "Grado", "Contacto", "Fecha"]
                        if os.path.exists(ARCHIVO_DEPORTISTAS):
                            with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as fd:
                                registros_dep = list(csv.reader(fd))
                        if not registros_dep:
                            registros_dep = [header_dep]
                            
                        duplicado = False
                        for r in registros_dep[1:]:
                            if len(r) > 1 and r[1] == doc_reg:
                                duplicado = True
                                break
                                
                        if duplicado:
                            st.error(f"⚠️ Ya existe un deportista registrado con el número de documento {doc_reg}.")
                        else:
                            nueva_fila = [nombre_completo, doc_reg, str(edad_calc), eps_reg, "60.0", "1.70", "20.76", "Normal", "Blanco (10° Kup)", tel_reg, str(fing_reg)]
                            registros_dep.append(nueva_fila)
                            with open(ARCHIVO_DEPORTISTAS, mode="w", newline="", encoding="utf-8") as fd:
                                writer = csv.writer(fd)
                                writer.writerows(registros_dep)
                            st.success(f"¡Deportista {nombre_completo} registrado con éxito! (Edad calculada: {edad_calc} años)")
                    else:
                        st.warning("Por favor complete los campos obligatorios: Nombres, Apellidos y Documento.")

        with tab_del_c:
            st.subheader("Eliminación Manual de Deportista")
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                    data_del = list(csv.reader(f))
                    if len(data_del) > 1:
                        filas_deps = data_del[1:]
                        opciones_dep = [f"{r[0]} (Doc: {r[1]})" for r in filas_deps if len(r) > 1]
                        atleta_seleccionado = st.selectbox("Seleccione el deportista a gestionar:", opciones_dep)
                        
                        if atleta_seleccionado:
                            doc_buscar = atleta_seleccionado.split("Doc: ")[1].replace(")", "").strip()
                            atleta_encontrado = None
                            for r in filas_deps:
                                if len(r) > 1 and r[1] == doc_buscar:
                                    atleta_encontrado = r
                                    break
                                    
                            if atleta_encontrado:
                                st.markdown(f"""
                                **Datos del deportista seleccionado:**
                                * **Nombre:** {atleta_encontrado[0]}
                                * **Documento:** {atleta_encontrado[1]}
                                * **Edad:** {atleta_encontrado[2]}
                                * **EPS:** {atleta_encontrado[3]}
                                * **Grado / Cinturón:** {atleta_encontrado[8] if len(atleta_encontrado)>8 else 'N/A'}
                                * **Contacto:** {atleta_encontrado[9] if len(atleta_encontrado)>9 else 'N/A'}
                                """)
                                
                                if st.button("❌ Eliminar este Deportista Permanentemente"):
                                    st.session_state[f"confirm_del_atleta_{doc_buscar}"] = True
                                    
                                if st.session_state.get(f"confirm_del_atleta_{doc_buscar}", False):
                                    st.warning(f"⚠️ ¿Está completamente seguro de eliminar a {atleta_encontrado[0]} del sistema?")
                                    if st.button("Sí, eliminar deportista", key=f"yes_del_atl_{doc_buscar}"):
                                        nuevos_deps = [data_del[0]] + [r for r in filas_deps if r[1] != doc_buscar]
                                        with open(ARCHIVO_DEPORTISTAS, mode="w", newline="", encoding="utf-8") as fw:
                                            csv.writer(fw).writerows(nuevos_deps)
                                        st.success(f"Deportista {atleta_encontrado[0]} eliminado correctamente.")
                                        st.rerun()
                                    if st.button("Cancelar", key=f"cancel_del_atl_{doc_buscar}"):
                                        st.session_state[f"confirm_del_atleta_{doc_buscar}"] = False
                                        st.rerun()
                    else:
                        st.info("No hay deportistas registrados para eliminar.")
            else:
                st.info("No hay base de datos de deportistas disponible.")
                        
        with tab_mac_c:
            st.subheader("Carga y Gestión de Macroestructuras de Entrenamiento")
            with st.form("form_subir_macro"):
                titulo_mac = st.text_input("Título de la Macroestructura (Ej: Macro Anual 2026)")
                archivo_mac = st.file_uploader("Subir Archivo (Excel o PDF)", type=["xlsx", "xls", "pdf", "csv"])
                submit_mac = st.form_submit_button("Subir Macroestructura")
                
                if submit_mac:
                    if titulo_mac and archivo_mac is not None:
                        ext = archivo_mac.name.split('.')[-1]
                        ruta_m = MACRO_DIR / f"{titulo_mac.replace(' ', '_').lower()}.{ext}"
                        with open(ruta_m, "wb") as fm:
                            fm.write(archivo_mac.getbuffer())
                        st.success(f"¡Macroestructura '{titulo_mac}' cargada con éxito!")
                    else:
                        st.warning("Ingrese un título y adjunte un archivo.")
                        
            st.markdown("---")
            st.subheader("Archivos Cargados y Descarga / Borrado")
            macros_disponibles = list(MACRO_DIR.glob("*.*"))
            if macros_disponibles:
                for mac_item in macros_disponibles:
                    cm1, cm2 = st.columns([3, 1])
                    with cm1:
                        st.write(f"📊 `{mac_item.name}`")
                    with cm2:
                        if st.button("🗑️ Borrar", key=f"del_mac_{mac_item.name}"):
                            mac_item.unlink()
                            st.success(f"Eliminado: {mac_item.name}")
                            st.rerun()
            else:
                st.info("No hay macroestructuras cargadas.")

        with tab_doc_c:
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

elif st.session_state.modulo_activo == "Pagos (Alerta)":
    mostrar_encabezado_institucional("Control de Pagos")
    dia_actual = datetime.now().day
    if dia_actual <= 5:
        st.warning(f"🚨 **¡AVISO INSTITUCIONAL DE MENSUALIDAD!** Nos encontramos en los primeros 5 días del mes (Día {dia_actual}). Por favor recuerde realizar el pago de su mensualidad a tiempo.")

    st.info(f"""
    📲 **MEDIOS DE PAGO OFICIALES DISPONIBLES:**
    * **Nequi:** `{NUMERO_PAGOS_DIGITALES}`
    * **Daviplata:** `{NUMERO_PAGOS_DIGITALES}`
    * **Llave / ID de Pago:** `{NUMERO_PAGOS_DIGITALES}`
    """)
    st.markdown("---")
    
    tab_p_ver, tab_p_reg, tab_p_rec = st.tabs(["📋 Consultar Pagos y Vencidos", "➕ Registrar Pago", "🧾 Generar Recibo Oficial"])
    
    with tab_p_ver:
        if os.path.exists(ARCHIVO_PAGOS):
            with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as f:
                reader_p = list(csv.reader(f))
                if len(reader_p) > 1:
                    for row in reader_p[1:]:
                        atleta = row[0]
                        estado = row[1]
                        fecha = row[2]
                        valor = row[3] if len(row) > 3 else "$60.000 COP"
                        if estado == "Pagado / Al Día":
                            st.success(f"✅ **{atleta}** — Estado: **Pagado** | Fecha: {fecha} | Valor: {valor}")
                        else:
                            st.error(f"🚨 **{atleta}** — Estado: **PENDIENTE / VENCIDO**")
                else:
                    st.info("No hay registros de pagos cargados.")
        else:
            st.info("Aún no hay historial de pagos.")

    with tab_p_reg:
        if os.path.exists(ARCHIVO_DEPORTISTAS):
            with open(ARCHIVO_DEPORTISTAS, mode="r", encoding="utf-8") as f:
                deps = [r[0] for r in list(csv.reader(f))[1:]]
                if deps:
                    with st.form("form_reg_pago"):
                        atleta_sel = st.selectbox("Seleccionar Deportista", deps)
                        estado_pago = st.selectbox("Estado", ["Pagado / Al Día", "Pendiente / Vencido"])
                        valor_pago = st.text_input("Valor Cancelado", value="$60.000 COP")
                        medio_pago = st.selectbox("Medio Utilizado", ["Nequi", "Daviplata", "Llave / Dale", "Efectivo", "Transferencia"])
                        fecha_pago = st.date_input("Fecha del Pago", value=datetime.now())
                        submit_p = st.form_submit_button("Guardar Estado de Pago")
                        
                        if submit_p:
                            pagos_data = []
                            if os.path.exists(ARCHIVO_PAGOS):
                                with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as fp:
                                    pagos_data = list(csv.reader(fp))
                            header_p = ["Deportista", "Estado", "Fecha", "Valor", "Medio"]
                            if not pagos_data:
                                pagos_data = [header_p]
                                
                            actualizado = False
                            for i in range(1, len(pagos_data)):
                                if pagos_data[i][0] == atleta_sel:
                                    pagos_data[i] = [atleta_sel, estado_pago, str(fecha_pago), valor_pago, medio_pago]
                                    actualizado = True
                                    break
                            if not actualizado:
                                pagos_data.append([atleta_sel, estado_pago, str(fecha_pago), valor_pago, medio_pago])
                                
                            with open(ARCHIVO_PAGOS, mode="w", newline="", encoding="utf-8") as fp:
                                csv.writer(fp).writerows(pagos_data)
                            st.success(f"¡Pago registrado correctamente para {atleta_sel}!")
                            st.rerun()
                else:
                    st.info("Debe registrar deportistas primero.")
        else:
            st.info("No hay deportistas en la base de datos.")

    with tab_p_rec:
        if os.path.exists(ARCHIVO_PAGOS):
            with open(ARCHIVO_PAGOS, mode="r", encoding="utf-8") as f:
                pagos_list = list(csv.reader(f))
                pagados = [r for r in pagos_list[1:] if len(r) > 1 and r[1] == "Pagado / Al Día"]
                if pagados:
                    nombres_pagados = [r[0] for r in pagados]
                    atleta_rec = st.selectbox("Seleccionar Atleta con Pago al Día:", nombres_pagados)
                    for r in pagados:
                        if r[0] == atleta_rec:
                            recibo_texto = (
                                "=====================================================\n"
                                "        CLUB JINSEI TAEKWONDO TENJO\n"
                                "     RECIBO OFICIAL DE PAGO DE MENSUALIDAD\n"
                                "=====================================================\n"
                                f"Deportista: {r[0]}\n"
                                f"Estado: {r[1]}\n"
                                f"Fecha de Pago: {r[2]}\n"
                                f"Valor: {r[3]}\n"
                                f"Medio Utilizado: {r[4]}\n"
                                "-----------------------------------------------------\n"
                                "Sede: Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque\n"
                                f"Teléfono de Pagos: {NUMERO_PAGOS_DIGITALES}\n"
                                "¡Gracias por su puntualidad y apoyo al club!\n"
                                "====================================================="
                            )
                            st.text_area("Comprobante Oficial Generado", recibo_texto, height=220)
                            st.download_button(
                                "⬇️ Descargar recibo",
                                data=recibo_texto,
                                file_name=f"recibo_{atleta_rec.replace(' ', '_')}.txt",
                                mime="text/plain",
                                key=f"descargar_recibo_{atleta_rec}"
                            )
                else:
                    st.info("No hay pagos al día para generar recibos.")
        else:
            st.info("Aún no hay registros de pagos.")

elif st.session_state.modulo_activo == "Agenda de Torneos y Eventos":
    mostrar_encabezado_institucional("Agenda de Torneos y Eventos")
    with st.form("form_agenda_ev"):
        nom_ev = st.text_input("Nombre del Torneo, Examen o Evento")
        fec_ev = st.date_input("Fecha del Evento")
        sub_ev = st.form_submit_button("Registrar en Agenda")
        if sub_ev:
            if nom_ev:
                with open(ARCHIVO_EVENTOS, mode="a", newline="", encoding="utf-8") as fe:
                    csv.writer(fe).writerows([[nom_ev, str(fec_ev)]])
                st.success("¡Evento agregado a la agenda!")
    if os.path.exists(ARCHIVO_EVENTOS):
        with open(ARCHIVO_EVENTOS, mode="r", encoding="utf-8") as fe:
            for r in csv.reader(fe):
                if r:
                    st.write(f"🏆 **{r[0]}** — Fecha: {r[1]}")