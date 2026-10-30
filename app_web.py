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

# Archivos de persistencia local
ARCHIVO_DEPORTISTAS = "deportistas_integral.csv"
ARCHIVO_EVENTOS = "eventos.csv"
ARCHIVO_USUARIOS = "usuarios_sistema.csv"
ARCHIVO_ASISTENCIAS = "asistencias.csv"
ARCHIVO_MACRO = "macroestructura_sesiones.csv"
ARCHIVO_PAGOS = "pagos_deportistas.csv"
CONTRASENA_ENTRENADOR = "coach2026"
TELEFONO_CLUB = "+57 312 504 6952" 
NUMERO_PAGOS_DIGITALES = "3125046952"

# Directorios del sistema
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

# ----------------- FUNCIONES DE USUARIOS -----------------
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
# ESTILOS E IMAGEN DE FONDO
def aplicar_estilos_fondo():
    foto_bg_path = ASSETS_DIR / "foto.JPG"
    encoded = ""
    if os.path.exists(foto_bg_path):
        with open(foto_bg_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            
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

aplicar_estilos_fondo()