import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime
import winsound
from PIL import Image, ImageTk

# Intentar importar el calendario gráfico interactivo
try:
    from tkcalendar import Calendar
    CALENDARIO_DISPONIBLE = True
except ImportError:
    CALENDARIO_DISPONIBLE = False

# Ruta exacta de la carpeta del proyecto
RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_DEPORTISTAS = os.path.join(RUTA_PROYECTO, "deportistas.txt")
ARCHIVO_USUARIOS = os.path.join(RUTA_PROYECTO, "usuarios.txt")
ARCHIVO_MACRO = os.path.join(RUTA_PROYECTO, "macroestructura.txt")
ARCHIVO_ASISTENCIAS = os.path.join(RUTA_PROYECTO, "asistencias.txt")
ARCHIVO_LOGROS = os.path.join(RUTA_PROYECTO, "logros.txt")
ARCHIVO_VIDEOS = os.path.join(RUTA_PROYECTO, "videos.txt")
ARCHIVO_PAGOS = os.path.join(RUTA_PROYECTO, "pagos.txt")
ARCHIVO_EXAMENES = os.path.join(RUTA_PROYECTO, "examenes.txt")
ARCHIVO_EVENTOS = os.path.join(RUTA_PROYECTO, "eventos_torneos.txt")

# Datos de Pago del Club
CUENTA_NEQUI = "312 504 6952"
CUENTA_DAVIPLATA = "312 504 6952"
LLAVE_CLUB = "312 504 6952"

# Variable global para rastrear usuario
USUARIO_ACTUAL = {"user": "invitado"}

# ---------------------------------------------------------
# FUNCIONES AUXILIARES PARA IMÁGENES
# ---------------------------------------------------------
def agregar_logo_a_ventana(parent, tamano=(60, 60)):
    try:
        for archivo in os.listdir(RUTA_PROYECTO):
            if archivo.lower().startswith("logo"):
                ruta_logo = os.path.join(RUTA_PROYECTO, archivo)
                img_pil = Image.open(ruta_logo).resize(tamano)
                logo_img = ImageTk.PhotoImage(img_pil)
                
                lbl_logo = tk.Label(parent, image=logo_img)
                lbl_logo.image = logo_img
                lbl_logo.pack(pady=2)
                return lbl_logo
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")
    return None

def agregar_foto_inferior_a_ventana(parent, tamano=(430, 140)):
    try:
        for archivo in os.listdir(RUTA_PROYECTO):
            if archivo.lower().startswith("foto"):
                ruta_foto = os.path.join(RUTA_PROYECTO, archivo)
                img_pil = Image.open(ruta_foto).resize(tamano)
                foto_img = ImageTk.PhotoImage(img_pil)
                
                lbl_foto = tk.Label(parent, image=foto_img)
                lbl_foto.image = foto_img
                lbl_foto.pack(side="bottom", pady=5)
                return lbl_foto
    except Exception as e:
        print(f"No se pudo cargar la foto inferior: {e}")
    return None

# ---------------------------------------------------------
# CÁLCULOS Y ARCHIVOS
# ---------------------------------------------------------
def calcular_imc(peso, talla):
    try:
        peso = float(peso)
        talla = float(talla)
        if talla <= 0:
            return 0.0, "Talla inválida"
        imc = peso / (talla ** 2)
        if imc < 18.5:
            estado = "Bajo peso"
        elif 18.5 <= imc < 24.9:
            estado = "Peso normal"
        elif 25.0 <= imc < 29.9:
            estado = "Sobrepeso"
        else:
            estado = "Obesidad"
        return round(imc, 2), estado
    except ValueError:
        return 0.0, "Datos no válidos"

def guardar_expediente(doc, nombre, grado, peso, talla, imc, estado_imc, cat, ficha, exon, img_pdf, foto_perfil):
    registro = f"{doc}|{nombre}|{grado}|{peso}kg|{talla}m|IMC:{imc}({estado_imc})|Cat:{cat}|Ficha:{ficha}|Exon:{exon}|ImgPdf:{img_pdf}|Foto:{foto_perfil}\n"
    with open(ARCHIVO_DEPORTISTAS, "a", encoding="utf-8") as f:
        f.write(registro)

def obtener_lista_deportistas():
    deportistas = []
    if os.path.exists(ARCHIVO_DEPORTISTAS):
        with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split("|")
                if len(datos) >= 2:
                    deportistas.append((datos[0], datos[1], datos[-1] if "Foto:" in datos[-1] else "foto.png"))
    return deportistas

# ---------------------------------------------------------
# VERIFICACIÓN DE PERMISO DE ENTRENADOR
# ---------------------------------------------------------
def verificar_clave_entrenador():
    ventana_verif = tk.Toplevel()
    ventana_verif.title("🔐 Autorización de Entrenador")
    ventana_verif.geometry("340x200")
    ventana_verif.config(padx=15, pady=10)
    
    tk.Label(ventana_verif, text="🛡️ Permiso del Entrenador Requerido", font=("Arial", 10, "bold"), fg="red").pack(pady=5)
    tk.Label(ventana_verif, text="Ingrese contraseña de Entrenador/Admin:").pack(pady=2)

    ent_clave_admin = tk.Entry(ventana_verif, show="*", width=25)
    ent_clave_admin.pack(pady=5)

    resultado = {"autorizado": False}

    def confirmar():
        clave = ent_clave_admin.get().strip()
        autenticado = False
        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split("|")
                    if len(datos) >= 2 and datos[1] == clave:
                        autenticado = True
                        break

        if autenticado:
            resultado["autorizado"] = True
            ventana_verif.destroy()
        else:
            messagebox.showerror("Acceso Denegado", "Contraseña de Entrenador incorrecta.")

    tk.Button(ventana_verif, text="Autorizar Operación", bg="red", fg="white", font=("Arial", 9, "bold"), command=confirmar).pack(pady=10)
    ventana_verif.wait_window()
    return resultado["autorizado"]

# ---------------------------------------------------------
# MÓDULOS DE GESTIÓN (PAGOS, TORNEOS, EXCEL, ETC.)
# ---------------------------------------------------------
def abrir_calendario_torneos():
    ventana_torneos = tk.Toplevel()
    ventana_torneos.title("📅 Torneos y Eventos Institucionales")
    ventana_torneos.geometry("580x680")
    ventana_torneos.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_torneos, tamano=(45, 45))
    tk.Label(ventana_torneos, text="🏆 AGENDA DE TORNEOS Y EVENTOS", font=("Arial", 11, "bold"), fg="#00695C").pack(pady=2)

    frame_form = tk.LabelFrame(ventana_torneos, text=" Registrar Nuevo Evento / Torneo ", padx=10, pady=5)
    frame_form.pack(fill="x", pady=3)

    tk.Label(frame_form, text="Nombre del Evento:").grid(row=0, column=0, sticky="w", pady=2)
    ent_nom_evento = tk.Entry(frame_form, width=28)
    ent_nom_evento.insert(0, "Copa Departamental Cundinamarca")
    ent_nom_evento.grid(row=0, column=1, pady=2)

    tk.Label(frame_form, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=2)
    ent_fec_evento = tk.Entry(frame_form, width=28)
    ent_fec_evento.insert(0, datetime.now().strftime("%Y-%m-%d"))
    ent_fec_evento.grid(row=1, column=1, pady=2)

    tk.Label(frame_form, text="Tipo de Evento:").grid(row=2, column=0, sticky="w", pady=2)
    combo_tipo_ev = ttk.Combobox(frame_form, values=["Torneo / Competencia", "Examen de Cinturón (Kup)", "Seminario Técnico", "Campamento de Entrenamiento"], state="readonly", width=25)
    combo_tipo_ev.current(0)
    combo_tipo_ev.grid(row=2, column=1, pady=2)

    def guardar_evento():
        nom = ent_nom_evento.get().strip()
        fec = ent_fec_evento.get().strip()
        tipo = combo_tipo_ev.get()

        if not nom or not fec:
            messagebox.showerror("Error", "Complete el nombre y la fecha.")
            return

        registro = f"Fecha:{fec} | Tipo:{tipo} | Evento:{nom}\n"
        with open(ARCHIVO_EVENTOS, "a", encoding="utf-8") as f:
            f.write(registro)

        messagebox.showinfo("Éxito", f"¡Evento '{nom}' agendado correctamente!")
        cargar_historial_eventos()

    tk.Button(frame_form, text="📅 Registrar Evento en la Agenda", bg="#00695C", fg="white", font=("Arial", 9, "bold"), command=guardar_evento).grid(row=3, column=0, columnspan=2, pady=6)

    tk.Label(ventana_torneos, text="Próximos Torneos y Eventos del Club:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_eventos = tk.Text(ventana_torneos, width=68, height=8, font=("Consolas", 8))
    txt_eventos.pack(pady=2)

    def cargar_historial_eventos():
        txt_eventos.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_EVENTOS):
            with open(ARCHIVO_EVENTOS, "r", encoding="utf-8") as f:
                txt_eventos.insert(tk.END, f.read())

    cargar_historial_eventos()
    agregar_foto_inferior_a_ventana(ventana_torneos, tamano=(430, 130))

def exportar_reportes_excel():
    if not verificar_clave_entrenador():
        return

    archivo_destino = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV (Excel)", "*.csv"), ("Todos los archivos", "*.*")], title="Guardar Reporte General")
    if archivo_destino:
        try:
            with open(archivo_destino, "w", encoding="utf-8-sig") as f_out:
                f_out.write("=== REPORTE GENERAL CLUB JINSEI TAEKWONDO TENJO ===\n\n")
                
                f_out.write("--- DEPORTISTAS REGISTRADOS ---\n")
                if os.path.exists(ARCHIVO_DEPORTISTAS):
                    with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                        f_out.write(f.read())
                
                f_out.write("\n--- HISTORIAL DE ASISTENCIAS ---\n")
                if os.path.exists(ARCHIVO_ASISTENCIAS):
                    with open(ARCHIVO_ASISTENCIAS, "r", encoding="utf-8") as f:
                        f_out.write(f.read())

                f_out.write("\n--- HISTORIAL DE PAGOS ---\n")
                if os.path.exists(ARCHIVO_PAGOS):
                    with open(ARCHIVO_PAGOS, "r", encoding="utf-8") as f:
                        f_out.write(f.read())

            messagebox.showinfo("Exportación Exitosa", f"¡Reporte exportado correctamente a:\n{archivo_destino}\nPuedes abrirlo directamente con Excel!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}")

def abrir_modulo_pagos():
    ventana_pagos = tk.Toplevel()
    ventana_pagos.title("💳 Pagos Nequi / Daviplata / Llave y Recibos")
    ventana_pagos.geometry("620x720")
    ventana_pagos.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_pagos, tamano=(45, 45))
    tk.Label(ventana_pagos, text="📲 RECAUDO Y MEDIOS DE PAGO - JINSEI TAEKWONDO", font=("Arial", 11, "bold"), fg="#1D6F42").pack(pady=2)

    frame_info_cuentas = tk.LabelFrame(ventana_pagos, text=" Cuentas y Llave Oficial del Club ", padx=10, pady=5, font=("Arial", 9, "bold"))
    frame_info_cuentas.pack(fill="x", pady=3)

    info_txt = (
        f"• NEQUI: {CUENTA_NEQUI}  (Titular: Jinsei Taekwondo)\n"
        f"• DAVIPLATA: {CUENTA_DAVIPLATA}  (Titular: Jinsei Taekwondo)\n"
        f"• LLAVE BRE-B / PAGO MÓVIL: {LLAVE_CLUB}"
    )
    tk.Label(frame_info_cuentas, text=info_txt, font=("Arial", 9, "bold"), fg="#004D40", justify="left").pack(anchor="w")

    frame_reg_pago = tk.LabelFrame(ventana_pagos, text=" Registrar Pago / Mensualidad ", padx=10, pady=5)
    frame_reg_pago.pack(fill="x", pady=3)

    tk.Label(frame_reg_pago, text="Deportista:").grid(row=0, column=0, sticky="w", pady=2)
    combo_deps_pago = ttk.Combobox(frame_reg_pago, state="readonly", width=25)
    combo_deps_pago.grid(row=0, column=1, pady=2)
    deps_lista = obtener_lista_deportistas()
    combo_deps_pago["values"] = [f"{d[1]} ({d[0]})" for d in deps_lista]
    if combo_deps_pago["values"]:
        combo_deps_pago.current(0)

    tk.Label(frame_reg_pago, text="Medio de Pago:").grid(row=1, column=0, sticky="w", pady=2)
    combo_medio = ttk.Combobox(frame_reg_pago, values=["Llave (Pago Móvil)", "Nequi", "Daviplata", "Efectivo / Transferencia"], state="readonly", width=25)
    combo_medio.current(0)
    combo_medio.grid(row=1, column=1, pady=2)

    tk.Label(frame_reg_pago, text="Valor Pagado ($):").grid(row=2, column=0, sticky="w", pady=2)
    ent_monto = tk.Entry(frame_reg_pago, width=28)
    ent_monto.insert(0, "80000")
    ent_monto.grid(row=2, column=1, pady=2)

    tk.Label(frame_reg_pago, text="N° Comprobante / Ref:").grid(row=3, column=0, sticky="w", pady=2)
    ent_ref = tk.Entry(frame_reg_pago, width=28)
    ent_ref.insert(0, "REF-123456")
    ent_ref.grid(row=3, column=1, pady=2)

    def guardar_recibo_pago():
        dep = combo_deps_pago.get()
        medio = combo_medio.get()
        monto = ent_monto.get().strip()
        ref = ent_ref.get().strip()
        fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not monto or not ref:
            messagebox.showerror("Error", "Ingrese el monto y la referencia del comprobante.")
            return

        registro = f"Fecha:{fecha_pago} | {dep} | Medio:{medio} | Monto:${monto} | Ref:{ref}\n"
        with open(ARCHIVO_PAGOS, "a", encoding="utf-8") as f:
            f.write(registro)

        recibo_texto = f"=== RECIBO DIGITAL DE CAJA ===\nJinsei Taekwondo Tenjo\nFecha: {fecha_pago}\nDeportista: {dep}\nMedio: {medio}\nMonto: ${monto}\nRef/Aprobación: {ref}\n¡PAGO RECIBIDO A CONFORMIDAD!"
        messagebox.showinfo("🧾 Recibo Digital Generado", recibo_texto)
        cargar_historial_pagos()

    tk.Button(frame_reg_pago, text="🧾 Registrar Pago y Emitir Recibo", bg="#1D6F42", fg="white", font=("Arial", 9, "bold"), command=guardar_recibo_pago).grid(row=4, column=0, columnspan=2, pady=6)

    tk.Label(ventana_pagos, text="Historial de Transacciones Registradas:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_pagos = tk.Text(ventana_pagos, width=72, height=6, font=("Consolas", 8))
    txt_pagos.pack(pady=2)

    def cargar_historial_pagos():
        txt_pagos.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_PAGOS):
            with open(ARCHIVO_PAGOS, "r", encoding="utf-8") as f:
                txt_pagos.insert(tk.END, f.read())

    cargar_historial_pagos()
    agregar_foto_inferior_a_ventana(ventana_pagos, tamano=(430, 130))

def abrir_carnet_y_examenes():
    ventana_carnet = tk.Toplevel()
    ventana_carnet.title("🥋 Carnet Digital y Exámenes de Ascenso")
    ventana_carnet.geometry("580x700")
    ventana_carnet.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_carnet, tamano=(45, 45))
    tk.Label(ventana_carnet, text="CARNET Y EXÁMENES DE ASCENSO (KUP/DAN)", font=("Arial", 11, "bold"), fg="#3F51B5").pack(pady=2)

    frame_carnet = tk.LabelFrame(ventana_carnet, text=" 🪪 Carnet Digital del Deportista ", padx=10, pady=5, bg="#E8EAF6")
    frame_carnet.pack(fill="x", pady=3)

    combo_deps_carnet = ttk.Combobox(frame_carnet, state="readonly", width=28)
    combo_deps_carnet.pack(pady=2)
    deps_lista = obtener_lista_deportistas()
    combo_deps_carnet["values"] = [f"{d[1]} ({d[0]})" for d in deps_lista]

    lbl_info_carnet = tk.Label(frame_carnet, text="Seleccione un deportista para generar su carnet digital.", font=("Arial", 9), bg="#E8EAF6")
    lbl_info_carnet.pack(pady=4)

    def ver_carnet_digital():
        idx = combo_deps_carnet.current()
        if idx >= 0:
            dep_info = deps_lista[idx]
            texto_c = f"🥋 CLUB JINSEI TAEKWONDO TENJO 🥋\nDOCUMENTO: {dep_info[0]}\nDEPORTISTA: {dep_info[1]}\nESTADO: ACTIVO / AFILIADO\n[ CÓDIGO QR OFICIAL VERIFICADO ]"
            lbl_info_carnet.config(text=texto_c, fg="navy", font=("Arial", 9, "bold"))

    combo_deps_carnet.bind("<<ComboboxSelected>>", lambda e: ver_carnet_digital())
    if deps_lista:
        combo_deps_carnet.current(0)
        ver_carnet_digital()

    frame_exam = tk.LabelFrame(ventana_carnet, text=" Evaluación y Requisitos de Ascenso ", padx=10, pady=5)
    frame_exam.pack(fill="x", pady=3)

    tk.Label(frame_exam, text="Poomsae / Formas:").grid(row=0, column=0, sticky="w", pady=2)
    combo_poomsae = ttk.Combobox(frame_exam, values=["Aprobado (Excelente)", "Aprobado (Aceptable)", "Pendiente"], state="readonly", width=22)
    combo_poomsae.current(0)
    combo_poomsae.grid(row=0, column=1, pady=2)

    tk.Label(frame_exam, text="Combate / Kyorugi:").grid(row=1, column=0, sticky="w", pady=2)
    combo_combate = ttk.Combobox(frame_exam, values=["Aprobado (Excelente)", "Aprobado (Aceptable)", "Pendiente"], state="readonly", width=22)
    combo_combate.current(0)
    combo_combate.grid(row=1, column=1, pady=2)

    def registrar_examen():
        dep = combo_deps_carnet.get()
        p = combo_poomsae.get()
        c = combo_combate.get()

        if not dep:
            messagebox.showerror("Error", "Seleccione un deportista.")
            return

        registro = f"Fecha:{datetime.now().strftime('%Y-%m-%d')} | {dep} | Poomsae:{p} | Combate:{c} | RESULTADO: APTO PARA ASCENSO\n"
        with open(ARCHIVO_EXAMENES, "a", encoding="utf-8") as f:
            f.write(registro)

        messagebox.showinfo("Éxito", f"¡Evaluación de ascenso registrada para {dep}!")
        cargar_historial_examenes()

    tk.Button(frame_exam, text="🎓 Registrar Resultado de Examen", bg="#3F51B5", fg="white", font=("Arial", 9, "bold"), command=registrar_examen).grid(row=2, column=0, columnspan=2, pady=6)

    tk.Label(ventana_carnet, text="Historial de Exámenes de Ascenso:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_exam = tk.Text(ventana_carnet, width=68, height=5, font=("Consolas", 8))
    txt_exam.pack(pady=2)

    def cargar_historial_examenes():
        txt_exam.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_EXAMENES):
            with open(ARCHIVO_EXAMENES, "r", encoding="utf-8") as f:
                txt_exam.insert(tk.END, f.read())

    cargar_historial_examenes()
    agregar_foto_inferior_a_ventana(ventana_carnet, tamano=(430, 130))

def abrir_metricas_rendimiento():
    ventana_met = tk.Toplevel()
    ventana_met.title("📊 Métricas de Rendimiento Físico e IMC")
    ventana_met.geometry("560x640")
    ventana_met.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_met, tamano=(45, 45))
    tk.Label(ventana_met, text="📊 EVOLUCIÓN Y MÉTRICAS ANTROPOMÉTRICAS", font=("Arial", 11, "bold"), fg="#E65100").pack(pady=2)

    frame_sel = tk.Frame(ventana_met)
    frame_sel.pack(fill="x", pady=3)

    tk.Label(frame_sel, text="Seleccionar Deportista:").pack(side="left", padx=5)
    combo_deps_met = ttk.Combobox(frame_sel, state="readonly", width=28)
    combo_deps_met.pack(side="left", padx=5)

    deps_lista = obtener_lista_deportistas()
    combo_deps_met["values"] = [f"{d[1]} ({d[0]})" for d in deps_lista]

    txt_met = tk.Text(ventana_met, width=65, height=12, font=("Consolas", 8))
    txt_met.pack(pady=5)

    def mostrar_metricas_deportista(event=None):
        idx = combo_deps_met.current()
        txt_met.delete("1.0", tk.END)
        if idx >= 0:
            doc_target = deps_lista[idx][0]
            nom_target = deps_lista[idx][1]
            txt_met.insert(tk.END, f"=== HISTORIAL FÍSICO DE {nom_target} ({doc_target}) ===\n\n")

            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                    for linea in f:
                        if linea.startswith(doc_target):
                            datos = linea.strip().split("|")
                            txt_met.insert(tk.END, f"• Grado: {datos[2]}\n• Peso/Talla: {datos[3]} / {datos[4]}\n• {datos[5]}\n• Categoría: {datos[6]}\n-----------------------------------------\n")

    combo_deps_met.bind("<<ComboboxSelected>>", mostrar_metricas_deportista)
    if deps_lista:
        combo_deps_met.current(0)
        mostrar_metricas_deportista()

    agregar_foto_inferior_a_ventana(ventana_met, tamano=(430, 140))

def verificar_alertas_pagos():
    dia_actual = datetime.now().day
    if dia_actual <= 5:
        try:
            for _ in range(3):
                winsound.Beep(1200, 300)
        except Exception:
            pass
        messagebox.showwarning("⚠️ ALERTA DE PAGOS DE MENSUALIDAD", 
                              f"¡Atención Entrenador / Administrador!\n\n"
                              f"Hoy estamos a día {dia_actual} del mes.\n"
                              f"Recuerde realizar el recaudo vía LLAVE ({LLAVE_CLUB}), NEQUI ({CUENTA_NEQUI}) o DAVIPLATA ({CUENTA_DAVIPLATA}).\n"
                              "Por favor verifique los comprobantes de los deportistas.")

def abrir_recuperacion():
    ventana_rec = tk.Toplevel()
    ventana_rec.title("Recuperar Contraseña")
    ventana_rec.geometry("420x420")
    ventana_rec.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_rec, tamano=(45, 45))
    tk.Label(ventana_rec, text="🔐 Recuperación de Datos", font=("Arial", 11, "bold"), fg="navy").pack(pady=2)

    tk.Label(ventana_rec, text="Usuario:").pack(anchor="w")
    ent_user_rec = tk.Entry(ventana_rec, width=28)
    ent_user_rec.pack(pady=2)

    tk.Label(ventana_rec, text="Correo de Recuperación:").pack(anchor="w")
    ent_mail_rec = tk.Entry(ventana_rec, width=28)
    ent_mail_rec.pack(pady=2)

    def buscar_credenciales():
        user = ent_user_rec.get().strip()
        correo = ent_mail_rec.get().strip()
        if not user or not correo:
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        encontrado = False
        clave_encontrada = ""
        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split("|")
                    if len(datos) >= 3 and datos[0] == user and datos[2] == correo:
                        encontrado = True
                        clave_encontrada = datos[1]
                        break

        if encontrado:
            messagebox.showinfo("¡Datos Encontrados!", f"Tu contraseña es: {clave_encontrada}")
            ventana_rec.destroy()
        else:
            messagebox.showerror("Error", "Los datos no coinciden con ningún registro.")

    tk.Button(ventana_rec, text="Recuperar Contraseña", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), command=buscar_credenciales).pack(pady=8)
    agregar_foto_inferior_a_ventana(ventana_rec, tamano=(360, 130))

# ---------------------------------------------------------
# VENTANA 1: LOGIN Y REGISTRO
# ---------------------------------------------------------
def abrir_login():
    ventana_auth = tk.Tk()
    ventana_auth.title("Jinsei Taekwondo - Acceso al Sistema")
    ventana_auth.geometry("480x760")
    ventana_auth.config(padx=20, pady=5)

    agregar_logo_a_ventana(ventana_auth, tamano=(65, 65))
    tk.Label(ventana_auth, text="🥋 Jinsei Taekwondo Tenjo", font=("Arial", 12, "bold"), fg="navy").pack(pady=2)

    frame_login = tk.LabelFrame(ventana_auth, text=" Iniciar Sesión ", padx=10, pady=5, font=("Arial", 9, "bold"))
    frame_login.pack(fill="x", pady=4)

    tk.Label(frame_login, text="Usuario:").grid(row=0, column=0, sticky="w", pady=2)
    ent_user_log = tk.Entry(frame_login, width=25)
    ent_user_log.grid(row=0, column=1, pady=2)

    tk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=2)
    ent_pass_log = tk.Entry(frame_login, width=25, show="*")
    ent_pass_log.grid(row=1, column=1, pady=2)

    def verificar_login():
        user = ent_user_log.get().strip()
        clave = ent_pass_log.get().strip()
        
        if not os.path.exists(ARCHIVO_USUARIOS):
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        autenticado = False
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split("|")
                if len(datos) >= 2 and datos[0] == user and datos[1] == clave:
                    autenticado = True
                    USUARIO_ACTUAL["user"] = user
                    break

        if autenticado:
            messagebox.showinfo("¡Bienvenido!", f"Acceso correcto. Bienvenido {user}.")
            ventana_auth.destroy()
            verificar_alertas_pagos()
            abrir_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    tk.Button(frame_login, text="🔑 Ingresar", bg="#1D6F42", fg="white", font=("Arial", 9, "bold"), width=18, command=verificar_login).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(frame_login, text="¿Olvidaste tu contraseña?", fg="blue", relief="flat", font=("Arial", 8), command=abrir_recuperacion).grid(row=3, column=0, columnspan=2)

    frame_reg = tk.LabelFrame(ventana_auth, text=" Registrar Nuevo Usuario ", padx=10, pady=5, font=("Arial", 9, "bold"))
    frame_reg.pack(fill="x", pady=4)

    tk.Label(frame_reg, text="Nuevo Usuario:").grid(row=0, column=0, sticky="w", pady=2)
    ent_user_reg = tk.Entry(frame_reg, width=25)
    ent_user_reg.grid(row=0, column=1, pady=2)

    tk.Label(frame_reg, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=2)
    ent_pass_reg = tk.Entry(frame_reg, width=25, show="*")
    ent_pass_reg.grid(row=1, column=1, pady=2)

    tk.Label(frame_reg, text="Correo (Recup.):").grid(row=2, column=0, sticky="w", pady=2)
    ent_mail_reg = tk.Entry(frame_reg, width=25)
    ent_mail_reg.grid(row=2, column=1, pady=2)

    def registrar_usuario():
        user = ent_user_reg.get().strip()
        clave = ent_pass_reg.get().strip()
        correo = ent_mail_reg.get().strip()

        if not user or not clave or not correo:
            messagebox.showerror("Error", "Por favor completa todos los campos de registro.")
            return

        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip().split("|")[0] == user:
                        messagebox.showwarning("Atención", "El usuario ya está registrado.")
                        return

        with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
            f.write(f"{user}|{clave}|{correo}\n")

        messagebox.showinfo("Éxito", "¡Cuenta registrada exitosamente!")
        ent_user_reg.delete(0, tk.END)
        ent_pass_reg.delete(0, tk.END)
        ent_mail_reg.delete(0, tk.END)

    tk.Button(frame_reg, text="📝 Crear Cuenta", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), width=18, command=registrar_usuario).grid(row=3, column=0, columnspan=2, pady=5)

    agregar_foto_inferior_a_ventana(ventana_auth, tamano=(430, 150))
    ventana_auth.mainloop()

# ---------------------------------------------------------
# ASISTENCIAS, LOGROS Y VIDEOS
# ---------------------------------------------------------
def abrir_control_asistencias():
    ventana_asis = tk.Toplevel()
    ventana_asis.title("📅 Control de Asistencias Interactivo")
    ventana_asis.geometry("660x730")
    ventana_asis.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_asis, tamano=(45, 45))
    tk.Label(ventana_asis, text="CONTROL Y CALENDARIO DE ASISTENCIAS", font=("Arial", 11, "bold"), fg="#1D6F42").pack(pady=2)

    frame_top = tk.Frame(ventana_asis)
    frame_top.pack(fill="x", pady=3)

    if CALENDARIO_DISPONIBLE:
        cal = Calendar(frame_top, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(side="left", padx=5)
    else:
        cal = None
        tk.Label(frame_top, text="[ Instale pip install tkcalendar ]", fg="red").pack(side="left")

    frame_foto_dep = tk.LabelFrame(frame_top, text=" Deportista Seleccionado ", padx=10, pady=5)
    frame_foto_dep.pack(side="right", fill="both", expand=True, padx=5)

    lbl_foto_perfil = tk.Label(frame_foto_dep, text="[ Foto ]", bg="#D3D3D3", width=14, height=6)
    lbl_foto_perfil.pack(pady=2)

    combo_deportistas = ttk.Combobox(frame_foto_dep, state="readonly", width=22)
    combo_deportistas.pack(pady=2)

    deportistas_lista = obtener_lista_deportistas()
    nombres_deps = [f"{d[1]} ({d[0]})" for d in deportistas_lista]
    combo_deportistas["values"] = nombres_deps

    def actualizar_foto_deportista(event=None):
        idx = combo_deportistas.current()
        if idx >= 0:
            info_dep = deportistas_lista[idx]
            nombre_foto = info_dep[2].replace("Foto:", "").strip()
            
            ruta_foto = os.path.join(RUTA_PROYECTO, nombre_foto)
            if not os.path.exists(ruta_foto):
                ruta_foto = os.path.join(RUTA_PROYECTO, "foto.png")

            try:
                if os.path.exists(ruta_foto):
                    img_pil = Image.open(ruta_foto).resize((85, 95))
                    foto_tk = ImageTk.PhotoImage(img_pil)
                    lbl_foto_perfil.config(image=foto_tk, text="")
                    lbl_foto_perfil.image = foto_tk
                else:
                    lbl_foto_perfil.config(image="", text="[ Sin Foto ]")
            except Exception:
                lbl_foto_perfil.config(image="", text="[ Error Foto ]")

    combo_deportistas.bind("<<ComboboxSelected>>", actualizar_foto_deportista)

    if nombres_deps:
        combo_deportistas.current(0)
        actualizar_foto_deportista()

    def marcar_asistencia_calendario():
        if not combo_deportistas.get():
            messagebox.showerror("Error", "Seleccione un deportista de la lista.")
            return

        fecha_sel = cal.get_date() if CALENDARIO_DISPONIBLE else datetime.now().strftime("%Y-%m-%d")
        dep_nom = combo_deportistas.get()

        registro = f"Fecha: {fecha_sel} | {dep_nom}\n"
        with open(ARCHIVO_ASISTENCIAS, "a", encoding="utf-8") as f:
            f.write(registro)

        if CALENDARIO_DISPONIBLE:
            try:
                date_obj = cal.selection_get()
                cal.calevent_create(date_obj, 'Asistencia Marcada', 'asistencia_marcada')
                cal.tag_config('asistencia_marcada', background='green', foreground='white')
            except Exception as e:
                print(f"Error pintando verde en el calendario: {e}")

        messagebox.showinfo("¡Asistencia Registrada!", f"🟢 Fecha pintada en verde: {fecha_sel}\nDeportista: {dep_nom}")
        cargar_historial_asistencias()

    tk.Button(ventana_asis, text="🟢 Marcar Asistencia en Verde", bg="#1D6F42", fg="white", font=("Arial", 9, "bold"), command=marcar_asistencia_calendario).pack(pady=4)

    tk.Label(ventana_asis, text="Historial de Asistencias:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_historial = tk.Text(ventana_asis, width=72, height=6, font=("Consolas", 8))
    txt_historial.pack(pady=2)

    def cargar_historial_asistencias():
        txt_historial.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_ASISTENCIAS):
            with open(ARCHIVO_ASISTENCIAS, "r", encoding="utf-8") as f:
                txt_historial.insert(tk.END, f.read())

    cargar_historial_asistencias()
    agregar_foto_inferior_a_ventana(ventana_asis, tamano=(430, 140))

def abrir_logros_y_competencias():
    ventana_logros = tk.Toplevel()
    ventana_logros.title("🏆 Logros, Competencias y Registro Fotográfico")
    ventana_logros.geometry("580x700")
    ventana_logros.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_logros, tamano=(45, 45))
    tk.Label(ventana_logros, text="🏆 RECONOCIMIENTOS Y REGISTRO FOTOGRÁFICO", font=("Arial", 11, "bold"), fg="#D81B60").pack(pady=2)

    frame_form = tk.LabelFrame(ventana_logros, text=" Registrar Logro / Medalla / Competencia ", padx=10, pady=5)
    frame_form.pack(fill="x", pady=3)

    tk.Label(frame_form, text="Deportista:").grid(row=0, column=0, sticky="w", pady=2)
    combo_deps_logro = ttk.Combobox(frame_form, state="readonly", width=25)
    combo_deps_logro.grid(row=0, column=1, pady=2)
    deportistas_lista = obtener_lista_deportistas()
    combo_deps_logro["values"] = [f"{d[1]} ({d[0]})" for d in deportistas_lista]
    if combo_deps_logro["values"]:
        combo_deps_logro.current(0)

    tk.Label(frame_form, text="Competencia / Evento:").grid(row=1, column=0, sticky="w", pady=2)
    ent_evento = tk.Entry(frame_form, width=28)
    ent_evento.insert(0, "Torneo Departamental / Copa Tenjo")
    ent_evento.grid(row=1, column=1, pady=2)

    tk.Label(frame_form, text="Logro / Medalla:").grid(row=2, column=0, sticky="w", pady=2)
    combo_medalla = ttk.Combobox(frame_form, values=["🥇 Medalla de Oro", "🥈 Medalla de Plata", "🥉 Medalla de Bronce", "📜 Participación / Mención"], state="readonly", width=25)
    combo_medalla.current(0)
    combo_medalla.grid(row=2, column=1, pady=2)

    ruta_foto_logro = {"path": "Sin Foto"}
    def seleccionar_foto_competencia():
        arch = filedialog.askopenfilename(title="Seleccionar Foto de Competencia/Logro", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg"), ("Todos", "*.*")])
        if arch:
            ruta_foto_logro["path"] = os.path.basename(arch)
            lbl_foto_log_status.config(text=f"✓ {os.path.basename(arch)[:15]}...", fg="green")

    tk.Button(frame_form, text="📷 Foto de Competencia", command=seleccionar_foto_competencia).grid(row=3, column=0, pady=2, sticky="w")
    lbl_foto_log_status = tk.Label(frame_form, text="Sin Foto", fg="gray")
    lbl_foto_log_status.grid(row=3, column=1, sticky="w")

    def guardar_logro():
        dep = combo_deps_logro.get()
        ev = ent_evento.get().strip()
        med = combo_medalla.get()
        ft = ruta_foto_logro["path"]

        if not dep or not ev:
            messagebox.showerror("Error", "Ingrese el evento y deportista.")
            return

        registro = f"Deportista:{dep} | Evento:{ev} | Logro:{med} | Foto:{ft}\n"
        with open(ARCHIVO_LOGROS, "a", encoding="utf-8") as f:
            f.write(registro)

        messagebox.showinfo("Éxito", f"¡Logro registrado para {dep}!")
        cargar_historial_logros()

    tk.Button(frame_form, text="🏆 Guardar Logro Destacado", bg="#D81B60", fg="white", font=("Arial", 9, "bold"), command=guardar_logro).grid(row=4, column=0, columnspan=2, pady=6)

    tk.Label(ventana_logros, text="Historial de Logros del Club:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_logros = tk.Text(ventana_logros, width=68, height=6, font=("Consolas", 8))
    txt_logros.pack(pady=2)

    def cargar_historial_logros():
        txt_logros.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_LOGROS):
            with open(ARCHIVO_LOGROS, "r", encoding="utf-8") as f:
                txt_logros.insert(tk.END, f.read())

    cargar_historial_logros()
    agregar_foto_inferior_a_ventana(ventana_logros, tamano=(430, 140))

def abrir_modulo_videos():
    ventana_vid = tk.Toplevel()
    ventana_vid.title("🎥 Videos de Entrenamientos y Competencias")
    ventana_vid.geometry("580x680")
    ventana_vid.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_vid, tamano=(45, 45))
    tk.Label(ventana_vid, text="🎬 REGISTRO Y BIBLIOTECA DE VIDEOS", font=("Arial", 11, "bold"), fg="#673AB7").pack(pady=2)

    frame_form = tk.LabelFrame(ventana_vid, text=" Cargar / Enlazar Video ", padx=10, pady=5)
    frame_form.pack(fill="x", pady=3)

    tk.Label(frame_form, text="Título / Tema del Video:").grid(row=0, column=0, sticky="w", pady=2)
    ent_titulo_vid = tk.Entry(frame_form, width=28)
    ent_titulo_vid.insert(0, "Poomsae Taegeuk / Combate Final")
    ent_titulo_vid.grid(row=0, column=1, pady=2)

    tk.Label(frame_form, text="Categoría del Video:").grid(row=1, column=0, sticky="w", pady=2)
    combo_cat_vid = ttk.Combobox(frame_form, values=["Entrenamiento Técnico", "Entrenamiento Funcional", "Competencia / Combate", "Defensa Personal"], state="readonly", width=25)
    combo_cat_vid.current(0)
    combo_cat_vid.grid(row=1, column=1, pady=2)

    ruta_video_sel = {"path": "Sin Archivo"}
    def seleccionar_archivo_video():
        arch = filedialog.askopenfilename(title="Seleccionar Archivo de Video Corto", filetypes=[("Archivos de Video", "*.mp4;*.avi;*.mov;*.mkv"), ("Todos", "*.*")])
        if arch:
            ruta_video_sel["path"] = os.path.basename(arch)
            lbl_vid_status.config(text=f"✓ {os.path.basename(arch)[:18]}...", fg="green")

    tk.Button(frame_form, text="📁 Cargar Archivo Video (.MP4)", command=seleccionar_archivo_video).grid(row=2, column=0, pady=2, sticky="w")
    lbl_vid_status = tk.Label(frame_form, text="Sin Archivo", fg="gray")
    lbl_vid_status.grid(row=2, column=1, sticky="w")

    def guardar_registro_video():
        tit = ent_titulo_vid.get().strip()
        cat = combo_cat_vid.get()
        vid = ruta_video_sel["path"]

        if not tit:
            messagebox.showerror("Error", "Ingrese un título para el video.")
            return

        registro = f"Fecha:{datetime.now().strftime('%Y-%m-%d')} | Título:{tit} | Cat:{cat} | Archivo:{vid}\n"
        with open(ARCHIVO_VIDEOS, "a", encoding="utf-8") as f:
            f.write(registro)

        messagebox.showinfo("Éxito", "¡Video registrado en la biblioteca del club!")
        cargar_historial_videos()

    tk.Button(frame_form, text="💾 Registrar Video", bg="#673AB7", fg="white", font=("Arial", 9, "bold"), command=guardar_registro_video).grid(row=3, column=0, columnspan=2, pady=6)

    tk.Label(ventana_vid, text="Biblioteca de Videos Registrados:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(3, 2))
    txt_vids = tk.Text(ventana_vid, width=68, height=6, font=("Consolas", 8))
    txt_vids.pack(pady=2)

    def cargar_historial_videos():
        txt_vids.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_VIDEOS):
            with open(ARCHIVO_VIDEOS, "r", encoding="utf-8") as f:
                txt_vids.insert(tk.END, f.read())

    cargar_historial_videos()
    agregar_foto_inferior_a_ventana(ventana_vid, tamano=(430, 140))

def abrir_resena_services():
    ventana_serv = tk.Toplevel()
    ventana_serv.title("Reseña Detallada de Servicios")
    ventana_serv.geometry("520x600")
    ventana_serv.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_serv, tamano=(45, 45))
    tk.Label(ventana_serv, text="📖 RESEÑA DE NUESTROS PROGRAMAS", font=("Arial", 11, "bold"), fg="navy").pack(pady=2)

    txt_resena = tk.Text(ventana_serv, width=58, height=15, font=("Arial", 9), wrap="word")
    txt_resena.pack(pady=3)

    contenido = (
        "1. CLASES DE TAEKWONDO:\n"
        "   - Enfoque: Arte marcial olímpico y tradicional. Formación en patadas, formas (Poomsae), combate (Kyorugi) y disciplina marcial.\n"
        "   - Beneficios: Desarrollo de coordinación, respeto, autoestima y alto rendimiento deportivo.\n\n"
        "2. ENTRENAMIENTO FUNCIONAL:\n"
        "   - Enfoque: Acondicionamiento físico integral mediante ejercicios de fuerza, resistencia, agilidad e hipertrofia enfocada.\n"
        "   - Beneficios: Quema de grasa, aumento de tono muscular y optimización motriz general.\n\n"
        "3. DEFENSA PERSONAL:\n"
        "   - Enfoque: Técnicas tácticas y prácticas de autoprotección, liberaciones y reacción rápida ante situaciones de agresión.\n"
        "   - Beneficios: Autoconfianza, reacción bajo presión y seguridad en el entorno cotidiano."
    )
    txt_resena.insert(tk.END, contenido)
    txt_resena.config(state="disabled")
    
    agregar_foto_inferior_a_ventana(ventana_serv, tamano=(400, 140))

def abrir_ficha_tecnica():
    ventana_ficha = tk.Toplevel()
    ventana_ficha.title("🥋 Ficha Técnica del Deportista")
    ventana_ficha.geometry("560x860")
    ventana_ficha.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_ficha, tamano=(45, 45))
    tk.Label(ventana_ficha, text="EXPEDIENTE Y FICHA TÉCNICA", font=("Arial", 11, "bold")).pack(pady=2)

    frame_datos = tk.LabelFrame(ventana_ficha, text=" Datos Personales y Grado ", padx=10, pady=5)
    frame_datos.pack(fill="x", pady=3)

    tk.Label(frame_datos, text="Nombre Completo:").grid(row=0, column=0, sticky="w")
    ent_nombre = tk.Entry(frame_datos, width=28)
    ent_nombre.grid(row=0, column=1, pady=2)

    tk.Label(frame_datos, text="Cédula / Documento:").grid(row=1, column=0, sticky="w")
    ent_doc = tk.Entry(frame_datos, width=28)
    ent_doc.grid(row=1, column=1, pady=2)

    tk.Label(frame_datos, text="Grado / Cinturón:").grid(row=2, column=0, sticky="w")
    combo_grado = ttk.Combobox(frame_datos, values=[
        "Blanco (10° Kup)", "Amarillo (8° Kup)", "Verde (6° Kup)", 
        "Azul (4° Kup)", "Rojo (2° Kup)", "Negro (1° Dan)"
    ], state="readonly", width=25)
    combo_grado.current(0)
    combo_grado.grid(row=2, column=1, pady=2)

    tk.Label(frame_datos, text="Categoría:").grid(row=3, column=0, sticky="w")
    ent_cat = tk.Entry(frame_datos, width=28)
    ent_cat.insert(0, "Infantil / Cadete / Mayores")
    ent_cat.grid(row=3, column=1, pady=2)

    frame_fisico = tk.LabelFrame(ventana_ficha, text=" Antropometría (IMC) ", padx=10, pady=5)
    frame_fisico.pack(fill="x", pady=3)

    tk.Label(frame_fisico, text="Peso (kg):").grid(row=0, column=0, sticky="w")
    ent_peso = tk.Entry(frame_fisico, width=12)
    ent_peso.insert(0, "50.0")
    ent_peso.grid(row=0, column=1, pady=2, sticky="w")

    tk.Label(frame_fisico, text="Talla (m):").grid(row=1, column=0, sticky="w")
    ent_talla = tk.Entry(frame_fisico, width=12)
    ent_talla.insert(0, "1.60")
    ent_talla.grid(row=1, column=1, pady=2, sticky="w")

    lbl_resultado_imc = tk.Label(frame_fisico, text="IMC: --", font=("Arial", 10, "bold"), fg="blue")
    lbl_resultado_imc.grid(row=2, column=0, columnspan=2, pady=3)

    def calcular_y_mostrar_imc():
        imc, estado = calcular_imc(ent_peso.get(), ent_talla.get())
        lbl_resultado_imc.config(text=f"IMC: {imc} ({estado})")

    tk.Button(frame_fisico, text="Calcular IMC", command=calcular_y_mostrar_imc, bg="#2196F3", fg="white").grid(row=1, column=2, padx=10)

    frame_docs = tk.LabelFrame(ventana_ficha, text=" Archivos y Fotografía del Deportista ", padx=10, pady=5)
    frame_docs.pack(fill="x", pady=3)

    rutas = {"ficha": "Pendiente", "exon": "Pendiente", "img_pdf": "Pendiente", "foto": "foto.png"}

    lbl_preview_foto = tk.Label(frame_docs, text="[ Vista Previa ]", bg="#E0E0E0", width=14, height=6)
    lbl_preview_foto.grid(row=0, column=2, rowspan=4, padx=10, pady=2)

    def seleccionar_foto():
        archivo = filedialog.askopenfilename(title="Seleccionar Foto Deportista", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg"), ("Todos", "*.*")])
        if archivo:
            rutas["foto"] = os.path.basename(archivo)
            lbl_ft.config(text=f"✓ {os.path.basename(archivo)[:14]}...", fg="green")
            try:
                img_pil = Image.open(archivo).resize((90, 100))
                foto_tk = ImageTk.PhotoImage(img_pil)
                lbl_preview_foto.config(image=foto_tk, text="")
                lbl_preview_foto.image = foto_tk
            except Exception as e:
                print(f"Error cargando foto: {e}")

    def seleccionar_pdf(tipo, lbl_destino, titulo):
        archivo = filedialog.askopenfilename(title=f"Seleccionar {titulo}", filetypes=[("Archivos PDF", "*.pdf"), ("Todos", "*.*")])
        if archivo:
            nombre = os.path.basename(archivo)
            rutas[tipo] = nombre
            lbl_destino.config(text=f"✓ {nombre[:14]}...", fg="green")

    tk.Button(frame_docs, text="📷 Foto Deportista", command=seleccionar_foto).grid(row=0, column=0, pady=2, sticky="w")
    lbl_ft = tk.Label(frame_docs, text="foto.png", fg="gray")
    lbl_ft.grid(row=0, column=1, padx=5, sticky="w")

    tk.Button(frame_docs, text="📄 Ficha Inscripción", command=lambda: seleccionar_pdf("ficha", lbl_f, "Ficha")).grid(row=1, column=0, pady=2, sticky="w")
    lbl_f = tk.Label(frame_docs, text="No seleccionado", fg="gray")
    lbl_f.grid(row=1, column=1, padx=5, sticky="w")

    tk.Button(frame_docs, text="📄 Exoneración PDF", command=lambda: seleccionar_pdf("exon", lbl_e, "Exoneración")).grid(row=2, column=0, pady=2, sticky="w")
    lbl_e = tk.Label(frame_docs, text="No seleccionado", fg="gray")
    lbl_e.grid(row=2, column=1, padx=5, sticky="w")

    tk.Button(frame_docs, text="📄 Aut. Imágenes", command=lambda: seleccionar_pdf("img_pdf", lbl_i, "Imágenes")).grid(row=3, column=0, pady=2, sticky="w")
    lbl_i = tk.Label(frame_docs, text="No seleccionado", fg="gray")
    lbl_i.grid(row=3, column=1, padx=5, sticky="w")

    def procesar_guardado():
        doc = ent_doc.get().strip()
        nom = ent_nombre.get().strip()
        if not doc or not nom:
            messagebox.showerror("Error", "El nombre y el documento son obligatorios.")
            return

        imc, estado = calcular_imc(ent_peso.get(), ent_talla.get())
        guardar_expediente(doc, nom, combo_grado.get(), ent_peso.get(), ent_talla.get(), imc, estado, ent_cat.get(),
                          rutas["ficha"], rutas["exon"], rutas["img_pdf"], rutas["foto"])

        messagebox.showinfo("Éxito", f"¡Expediente de {nom} guardado correctamente!")
        ventana_ficha.destroy()

    tk.Button(ventana_ficha, text="💾 GUARDAR FICHA TÉCNICA", bg="#1D6F42", fg="white", font=("Arial", 10, "bold"), command=procesar_guardado).pack(pady=6)
    agregar_foto_inferior_a_ventana(ventana_ficha, tamano=(430, 140))

def abrir_listado():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Gestión y Registro Manual de Deportistas")
    ventana_lista.geometry("740x680")
    ventana_lista.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_lista, tamano=(45, 45))
    tk.Label(ventana_lista, text="📋 GESTIÓN Y LISTADO MANUAL DE DEPORTISTAS", font=("Arial", 11, "bold")).pack(pady=3)

    frame_manual = tk.LabelFrame(ventana_lista, text=" ➕ Ingreso Manual de Nuevo Deportista ", padx=10, pady=5, font=("Arial", 9, "bold"))
    frame_manual.pack(fill="x", pady=3)

    tk.Label(frame_manual, text="Cédula/Doc:").grid(row=0, column=0, sticky="w", pady=2)
    ent_man_doc = tk.Entry(frame_manual, width=15)
    ent_man_doc.grid(row=0, column=1, pady=2, padx=2)

    tk.Label(frame_manual, text="Nombre:").grid(row=0, column=2, sticky="w", pady=2)
    ent_man_nom = tk.Entry(frame_manual, width=22)
    ent_man_nom.grid(row=0, column=3, pady=2, padx=2)

    tk.Label(frame_manual, text="Cinturón:").grid(row=1, column=0, sticky="w", pady=2)
    combo_man_grado = ttk.Combobox(frame_manual, values=["Blanco (10° Kup)", "Amarillo (8° Kup)", "Verde (6° Kup)", "Azul (4° Kup)", "Rojo (2° Kup)", "Negro (1° Dan)"], state="readonly", width=14)
    combo_man_grado.current(0)
    combo_man_grado.grid(row=1, column=1, pady=2, padx=2)

    def agregar_deportista_manual():
        doc = ent_man_doc.get().strip()
        nom = ent_man_nom.get().strip()
        grado = combo_man_grado.get()

        if not doc or not nom:
            messagebox.showerror("Error", "Documento y Nombre son obligatorios.")
            return

        guardar_expediente(doc, nom, grado, "50.0", "1.60", "19.5", "Normal", "General", "Pendiente", "Pendiente", "Pendiente", "foto.png")
        messagebox.showinfo("Éxito", f"¡Deportista {nom} registrado manualmente!")
        ent_man_doc.delete(0, tk.END)
        ent_man_nom.delete(0, tk.END)
        cargar_datos_listbox()

    tk.Button(frame_manual, text="➕ Agregar Manualmente", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), command=agregar_deportista_manual).grid(row=1, column=2, columnspan=2, padx=5, pady=2)

    frame_list = tk.Frame(ventana_lista)
    frame_list.pack(fill="both", expand=True, padx=10, pady=3)

    scrollbar = tk.Scrollbar(frame_list, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    listbox_deportistas = tk.Listbox(frame_list, width=95, height=10, yscrollcommand=scrollbar.set, font=("Consolas", 9))
    listbox_deportistas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox_deportistas.yview)

    def cargar_datos_listbox():
        listbox_deportistas.delete(0, tk.END)
        if os.path.exists(ARCHIVO_DEPORTISTAS):
            with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                for linea in f:
                    listbox_deportistas.insert(tk.END, linea.strip())

    cargar_datos_listbox()

    def borrar_deportista_seleccionado():
        seleccion = listbox_deportistas.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un deportista de la lista para borrar.")
            return

        item_texto = listbox_deportistas.get(seleccion[0])
        
        if not verificar_clave_entrenador():
            return

        if messagebox.askyesno("Confirmar Retiro/Eliminación", f"¿Confirmar retiro del deportista del sistema?\n\n{item_texto}"):
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                
                with open(ARCHIVO_DEPORTISTAS, "w", encoding="utf-8") as f:
                    for linea in lineas:
                        if linea.strip() != item_texto:
                            f.write(linea)

                messagebox.showinfo("Éxito", "Deportista retirado y borrado correctamente.")
                cargar_datos_listbox()

    tk.Button(ventana_lista, text="🗑️ Borrar / Retirar Deportista (Solo Entrenador)", bg="red", fg="white", font=("Arial", 10, "bold"), command=borrar_deportista_seleccionado).pack(pady=4)
    agregar_foto_inferior_a_ventana(ventana_lista, tamano=(430, 130))

def abrir_macroestructura():
    ventana_macro = tk.Toplevel()
    ventana_macro.title("🏋️ Macroestructura de Entrenamiento")
    ventana_macro.geometry("540x680")
    ventana_macro.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_macro, tamano=(45, 45))
    tk.Label(ventana_macro, text="PLANIFICACIÓN DE ENTRENAMIENTO", font=("Arial", 12, "bold"), fg="darkred").pack(pady=2)

    frame_form = tk.LabelFrame(ventana_macro, text=" Datos del Plan ", padx=10, pady=5)
    frame_form.pack(fill="x", pady=3)

    tk.Label(frame_form, text="Fase / Mesociclo:").grid(row=0, column=0, sticky="w", pady=2)
    combo_fase = ttk.Combobox(frame_form, values=["Preparatoria General", "Preparatoria Especial", "Competitiva", "Transición"], state="readonly", width=25)
    combo_fase.current(0)
    combo_fase.grid(row=0, column=1, pady=2)

    tk.Label(frame_form, text="Microciclo (Semana):").grid(row=1, column=0, sticky="w", pady=2)
    ent_micro = tk.Entry(frame_form, width=28)
    ent_micro.insert(0, "Semana 1 (Desarrollo)")
    ent_micro.grid(row=1, column=1, pady=2)

    tk.Label(frame_form, text="Objetivo Técnico/Físico:").grid(row=2, column=0, sticky="w", pady=2)
    ent_obj = tk.Entry(frame_form, width=28)
    ent_obj.grid(row=2, column=1, pady=2)

    tk.Label(frame_form, text="Carga / Intensidad:").grid(row=3, column=0, sticky="w", pady=2)
    combo_carga = ttk.Combobox(frame_form, values=["Alta (80%-90%)", "Media (60%-70%)", "Baja (Recuperación)"], state="readonly", width=25)
    combo_carga.current(0)
    combo_carga.grid(row=3, column=1, pady=2)

    tk.Label(ventana_macro, text="Planes Guardados:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(3, 2))
    text_planes = tk.Text(ventana_macro, width=62, height=6, font=("Consolas", 8))
    text_planes.pack(pady=2)

    def cargar_planes():
        text_planes.delete("1.0", tk.END)
        if os.path.exists(ARCHIVO_MACRO):
            with open(ARCHIVO_MACRO, "r", encoding="utf-8") as f:
                text_planes.insert(tk.END, f.read())

    cargar_planes()

    def guardar_plan():
        fase = combo_fase.get()
        micro = ent_micro.get().strip()
        obj = ent_obj.get().strip()
        carga = combo_carga.get()

        if not obj:
            messagebox.showerror("Error", "El objetivo del entrenamiento es obligatorio.")
            return

        registro = f"Fase:{fase} | {micro} | Obj:{obj} | Carga:{carga}\n"
        
        with open(ARCHIVO_MACRO, "a", encoding="utf-8") as f:
            f.write(registro)

        messagebox.showinfo("Éxito", "¡Plan de entrenamiento guardado con éxito!")
        cargar_planes()

    tk.Button(ventana_macro, text="💾 Guardar Plan de Entrenamiento", bg="#1D6F42", fg="white", font=("Arial", 10, "bold"), command=guardar_plan).pack(pady=6)
    agregar_foto_inferior_a_ventana(ventana_macro, tamano=(430, 140))

# ---------------------------------------------------------
# MENÚ PRINCIPAL COMPLETO Y ACTUALIZADO
# ---------------------------------------------------------
def abrir_menu_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Jinsei Taekwondo Tenjo - Panel Principal")
    ventana_principal.geometry("500x880")
    ventana_principal.config(padx=15, pady=5)

    agregar_logo_a_ventana(ventana_principal, tamano=(55, 55))
    tk.Label(ventana_principal, text="¡BIENVENIDO A JINSEI TAEKWONDO!", font=("Arial", 11, "bold"), fg="navy").pack(pady=2)

    frame_serv_asis = tk.Frame(ventana_principal)
    frame_serv_asis.pack(fill="x", pady=2)

    tk.Button(frame_serv_asis, text="📖 Servicios", bg="#607D8B", fg="white", font=("Arial", 8, "bold"), width=12, command=abrir_resena_services).pack(side="left", padx=2)
    tk.Button(frame_serv_asis, text="📅 Asistencias", bg="#009688", fg="white", font=("Arial", 8, "bold"), width=12, command=abrir_control_asistencias).pack(side="left", padx=2)
    tk.Button(frame_serv_asis, text="🎥 Videos", bg="#673AB7", fg="white", font=("Arial", 8, "bold"), width=12, command=abrir_modulo_videos).pack(side="left", padx=2)
    tk.Button(frame_serv_asis, text="💳 Llave/Pagos", bg="#1D6F42", fg="white", font=("Arial", 8, "bold"), width=15, command=abrir_modulo_pagos).pack(side="right", padx=2)

    frame_servicios = tk.LabelFrame(ventana_principal, text=" 🥋 Programas y Disciplinas ", padx=10, pady=4, font=("Arial", 9, "bold"))
    frame_servicios.pack(fill="x", pady=3)

    info_servicios = (
        "• Clases de Taekwondo: Formación marcial, formas y combate.\n"
        "• Entrenamiento Funcional: Fuerza, resistencia y tono muscular.\n"
        "• Defensa Personal: Técnicas prácticas de autoprotección urbana."
    )
    tk.Label(frame_servicios, text=info_servicios, justify="left", font=("Arial", 8), fg="#333333").pack(anchor="w")

    tk.Label(ventana_principal, text="Opciones de Gestión Deportiva:").pack(pady=2)

    tk.Button(ventana_principal, text="📝 Ficha Técnica, Fotos e IMC", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=38, command=abrir_ficha_tecnica).pack(pady=3)
    tk.Button(ventana_principal, text="📋 Ver, Borrar e Ingresar Deportistas", font=("Arial", 10, "bold"), bg="#1D6F42", fg="white", width=38, command=abrir_listado).pack(pady=3)
    tk.Button(ventana_principal, text="🏋️ Macroestructura (Entrenador)", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=38, command=abrir_macroestructura).pack(pady=3)
    tk.Button(ventana_principal, text="🏆 Logros y Registro Fotográfico", font=("Arial", 10, "bold"), bg="#D81B60", fg="white", width=38, command=abrir_logros_y_competencias).pack(pady=3)
    tk.Button(ventana_principal, text="🪪 Carnet Digital y Exámenes (Kup)", font=("Arial", 10, "bold"), bg="#3F51B5", fg="white", width=38, command=abrir_carnet_y_examenes).pack(pady=3)
    tk.Button(ventana_principal, text="📊 Métricas de Rendimiento e IMC", font=("Arial", 10, "bold"), bg="#E65100", fg="white", width=38, command=abrir_metricas_rendimiento).pack(pady=3)
    tk.Button(ventana_principal, text="📅 Agenda de Torneos y Eventos", font=("Arial", 10, "bold"), bg="#00695C", fg="white", width=38, command=abrir_calendario_torneos).pack(pady=3)
    tk.Button(ventana_principal, text="📊 Exportar Reportes a Excel (CSV)", font=("Arial", 10, "bold"), bg="#C2185B", fg="white", width=38, command=exportar_reportes_excel).pack(pady=3)

    tk.Label(ventana_principal, text="Horarios:\nLunes y Miércoles: 4:00 PM - 8:00 PM | Sábados: 10:00 AM - 12:00 M", justify="center", fg="gray", font=("Arial", 8)).pack(pady=2)

    tk.Button(ventana_principal, text="Cerrar Sesión", font=("Arial", 9), bg="red", fg="white", width=18, command=ventana_principal.destroy).pack(pady=2)

    agregar_foto_inferior_a_ventana(ventana_principal, tamano=(430, 120))
    ventana_principal.mainloop()

# ---------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------
if __name__ == "__main__":
    abrir_login()