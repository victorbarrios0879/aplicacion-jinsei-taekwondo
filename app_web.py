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

def navegar_a(modulo):
    """Mantiene sincronizados el módulo activo y el selector lateral sin duplicar widgets."""
    st.session_state.modulo_activo = modulo
    st.session_state.menu_lateral_principal = modulo


def sincronizar_menu_lateral():
    st.session_state.modulo_activo = st.session_state.menu_lateral_principal

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

# ESTILOS INSTITUCIONALES Y FONDO CON FOTO DE DEPORTISTAS (foto.JPG)
def localizar_fotografia_fondo():
    candidatos = [
        BASE_DIR / "foto.JPG",
        ASSETS_DIR / "foto.JPG",
        BASE_DIR / "foto.jpg",
        ASSETS_DIR / "foto.jpg",
    ]
    for candidato in candidatos:
        if candidato.is_file():
            return candidato

    for carpeta in (BASE_DIR, ASSETS_DIR):
        if carpeta.is_dir():
            for archivo in carpeta.iterdir():
                if archivo.is_file() and archivo.name.lower() == "foto.jpg":
                    return archivo
    return None


def aplicar_estilos_institucionales():
    foto_bg_path = localizar_fotografia_fondo()
    imagen_css = ""
    if foto_bg_path:
        with open(foto_bg_path, "rb") as archivo:
            encoded_bg = base64.b64encode(archivo.read()).decode("ascii")
        mime = "image/png" if foto_bg_path.suffix.lower() == ".png" else "image/jpeg"
        imagen_css = f'url("data:{mime};base64,{encoded_bg}")'
    else:
        st.warning(
            "No se encontró foto.JPG. Coloca el archivo en la misma carpeta "
            "que app_web.py para utilizarlo como fondo."
        )

    css = f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.58), rgba(255, 255, 255, 0.58)),
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
    .card-title-custom {{ font-size: 18px; font-weight: bold; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
    .card-desc-custom {{ font-size: 13px; opacity: 0.95; font-weight: normal; }}
    .badge-icon {{ padding: 4px 10px; border-radius: 20px; font-size: 12px; background: #1E3A8A; color: white; margin-right: 6px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

aplicar_estilos_institucionales()

# ----------------- AUTENTICACIÓN Y LOGIN -----------------
if not st.session_state.autenticado:
    _, col_principal, _ = st.columns([0.5, 3, 0.5])

    with col_principal:
        logo_file = ASSETS_DIR / "logo.png"
        if not logo_file.exists():
            logo_file = BASE_DIR / "logo.png"

        # Logo institucional a la izquierda y nombre del club alineado a su derecha.
        col_logo, col_titulo = st.columns([0.8, 3.2], vertical_alignment="center")
        with col_logo:
            if logo_file.exists():
                st.image(str(logo_file), width=105)
            else:
                st.warning("No se encontró logo.png en la carpeta raíz ni en assets.")
        with col_titulo:
            st.markdown(
                "<div style='display:flex;align-items:center;min-height:105px;'>"
                "<h2 style='color:#1E3A8A;margin:0;line-height:1.2;'>"
                "JINSEI Club de Taekwondo Tenjo</h2></div>",
                unsafe_allow_html=True
            )
            
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

# ----------------- PANEL PRIVADO Y NAVEGACIÓN -----------------
st.sidebar.title(f"👤 {st.session_state.get('usuario_actual', 'Coach')}")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.modulo_activo = "Panel Principal"
    st.rerun()

st.sidebar.info("Jinsei Taekwondo — Tenjo")
logo_lateral = ASSETS_DIR / "logo.png"
if not logo_lateral.exists():
    logo_lateral = BASE_DIR / "logo.png"
if logo_lateral.exists():
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

if st.session_state.get("menu_lateral_principal") not in modulos_lista:
    st.session_state.menu_lateral_principal = st.session_state.modulo_activo
else:
    st.session_state.menu_lateral_principal = st.session_state.modulo_activo

st.sidebar.selectbox(
    "Seleccione un módulo:",
    modulos_lista,
    key="menu_lateral_principal",
    on_change=sincronizar_menu_lateral
)

if st.session_state.modulo_activo != "Panel Principal":
    st.button(
        "⬅️ Regresar al menú principal",
        key="btn_regresar_menu_principal",
        use_container_width=True,
        on_click=navegar_a,
        args=("Panel Principal",)
    )
    st.markdown("---")

# ----------------- MÓDULOS DE TRABAJO -----------------

if st.session_state.modulo_activo == "Panel Principal":
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
            if st.button("📁 Abrir Ficha e IMC", use_container_width=True, key="btn_m1"):
                navegar_a("Ficha Integral del Deportista e IMC")
                st.rerun()

            st.markdown('''
                <div class="card-servicio bg-rojo">
                    <div class="card-title-custom"><span class="badge-icon">03</span> Galería y Videos (Multimedia)</div>
                    <div class="card-desc-custom">Fotografías, eventos institucionales y videoteca técnica del club.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📸 Abrir Multimedia", use_container_width=True, key="btn_m3"):
                navegar_a("Galería y Videos (Multimedia)")
                st.rerun()

            st.markdown('''
                <div class="card-servicio bg-verde">
                    <div class="card-title-custom"><span class="badge-icon">05</span> Control de Asistencia</div>
                    <div class="card-desc-custom">Calendario interactivo de asistencia diaria por sesión.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📊 Abrir Asistencia", use_container_width=True, key="btn_m5"):
                navegar_a("Control de Asistencia")
                st.rerun()

        with c_mod2:
            st.markdown('''
                <div class="card-servicio bg-verde">
                    <div class="card-title-custom"><span class="badge-icon">02</span> Panel del Entrenador</div>
                    <div class="card-desc-custom">Gestión completa de atletas, macroestructuras y documentos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("🥋 Abrir Panel Coach", use_container_width=True, key="btn_m2"):
                navegar_a("Panel General del Entrenador (Solo Coach)")
                st.rerun()

            st.markdown('''
                <div class="card-servicio bg-amarillo">
                    <div class="card-title-custom"><span class="badge-icon">04</span> Exoneraciones y PDFs</div>
                    <div class="card-desc-custom">Gestión y borrado de cartas de deslinde de responsabilidad legal.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("📄 Abrir Exoneraciones", use_container_width=True, key="btn_m6"):
                navegar_a("Cargar Fichas, Exoneraciones y PDFs")
                st.rerun()

            st.markdown('''
                <div class="card-servicio bg-azul">
                    <div class="card-title-custom"><span class="badge-icon">06</span> Control de Pagos</div>
                    <div class="card-desc-custom">Estado de mensualidades, recibos oficiales y alertas de pagos.</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("💰 Abrir Pagos", use_container_width=True, key="btn_m8"):
                navegar_a("Pagos (Alerta)")
                st.rerun()

elif st.session_state.modulo_activo == "Ficha Integral del Deportista e IMC":
    st.header("📋 Ficha Integral del Deportista y Cálculo de IMC")
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
    st.header("📊 Control de Asistencia mediante Calendario")
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
                        
                        # Filtrar duplicados para la misma fecha y deportista
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
        st.subheader("🖼️ Galería de Fotografías")
        if os.path.exists(FOTOS_CLUB_DIR):
            lista_fotos = [f for f in os.listdir(FOTOS_CLUB_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if lista_fotos:
                for foto_item in lista_fotos:
                    st.image(str(FOTOS_CLUB_DIR / foto_item), caption=foto_item, width=300)
                
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
        st.subheader("🎥 Videoteca Técnica y Reproducción")
        if os.path.exists(VIDEOS_DIR):
            lista_videos = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            if lista_videos:
                for vid_item in lista_videos:
                    st.write(f"🎬 **{vid_item}**")
                    st.video(str(VIDEOS_DIR / vid_item))
                
                video_a_borrar = st.selectbox("Seleccione vídeo a eliminar:", lista_videos, key="sel_v_borrar")
                if st.button("❌ Eliminar Vídeo Seleccionado", key="btn_del_v_dir"):
                    os.remove(VIDEOS_DIR / video_a_borrar)
                    st.success(f"El vídeo '{video_a_borrar}' ha sido eliminado.")
                    st.rerun()
            else:
                st.info("No hay vídeos guardados aún.")

elif st.session_state.modulo_activo == "Panel General del Entrenador (Solo Coach)":
    st.header("⚙️ Panel General del Entrenador (Exclusivo Coach)")
    password_coach = st.text_input("Ingrese Contraseña de Autorización Coach", type="password")
    
    if password_coach == CONTRASENA_ENTRENADOR:
        st.success("✅ Acceso Autorizado al Panel de Control.")
        tab_dep_c, tab_mac_c, tab_doc_c = st.tabs(["📋 Lista y Borrado de Deportistas", "📊 Macroestructuras", "📄 Documentos PDF"])
        
        with tab_dep_c:
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
    st.header("💰 Control de Pagos y Recaudos del Club")
    
    # Sistema automático de alarma para los primeros 5 días del mes
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
                            recibo_texto = f"""
=====================================================
        CLUB JINSEI TAEKWONDO TENJO
     RECIBO OFICIAL DE PAGO DE MENSUALIDAD
=====================================================
Deportista: {r[0]}
Estado: {r[1]}
Fecha de Pago: {r[2]}
Valor: {r[3]}
Medio Utilizado: {r[4]}
-----------------------------------------------------
Sede: Tenjo, Cundinamarca — Vereda Chincé, Sector Zoque
Teléfono de Pagos: {NUMERO_PAGOS_DIGITALES}
¡Gracias por su puntualidad y apoyo al club!
=====================================================
                            """
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
    st.header("📅 Agenda de Torneos y Eventos")
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