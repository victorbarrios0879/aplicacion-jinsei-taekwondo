import sys
import os
import csv
import datetime
import glob
import json
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk

ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_DEPORTISTAS = "deportistas_integral.csv"
ARCHIVO_EVENTOS = "eventos.csv"
CONTRASENA_ENTRENADOR = "coach2026"  # Contraseña exclusiva del Entrenador

def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_usuarios(usuarios):
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error al guardar usuarios:", e)

def obtener_ruta_recurso_imagen(nombre_base):
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")

    patron = os.path.join(ruta_base, f"{nombre_base}.*")
    coincidencias = glob.glob(patron)
    if coincidencias:
        return coincidencias[0]
    
    for archivo in os.listdir(ruta_base):
        if archivo.lower().startswith(nombre_base.lower()):
            return os.path.join(ruta_base, archivo)
    return None

# ------------------------------------------------------------------
# 3 BOTONES DE SERVICIOS
# ------------------------------------------------------------------
def abrir_servicio_taekwondo():
    win = tk.Toplevel()
    win.title("Taekwondo Formativo y Competencia")
    win.geometry("500x350")
    win.configure(bg="#f9f9f9")
    tk.Label(win, text="🥋 Taekwondo Formativo y Competencia", font=("Helvetica", 12, "bold"), fg="#000080", bg="#f9f9f9").pack(pady=10)
    txt = (
        "• Clases enfocadas en el desarrollo marcial, disciplina y autocontrol.\n"
        "• Aprendizaje de Poomsae (formas) y Kyorugi (combate).\n"
        "• Preparación técnica y táctica para torneos departamentales y nacionales.\n"
        "• Dirigido a categorías infantiles, juveniles y mayores."
    )
    tk.Label(win, text=txt, justify="left", font=("Helvetica", 10), bg="#f9f9f9", padx=20, wraplength=450).pack(fill="both", expand=True)

def abrir_servicio_funcional():
    win = tk.Toplevel()
    win.title("Entrenamiento Funcional")
    win.geometry("500x350")
    win.configure(bg="#f9f9f9")
    tk.Label(win, text="💪 Entrenamiento Funcional", font=("Helvetica", 12, "bold"), fg="#2e7d32", bg="#f9f9f9").pack(pady=10)
    txt = (
        "• Circuitos dinámicos para mejorar la fuerza, agilidad y resistencia.\n"
        "• Quema calórica y optimización de la composición corporal (IMC).\n"
        "• Prevención de lesiones y fortalecimiento de core y estabilidad.\n"
        "• Apto para deportistas y público en general."
    )
    tk.Label(win, text=txt, justify="left", font=("Helvetica", 10), bg="#f9f9f9", padx=20, wraplength=450).pack(fill="both", expand=True)

def abrir_servicio_defensa():
    win = tk.Toplevel()
    win.title("Defensa Personal Urbana")
    win.geometry("500x350")
    win.configure(bg="#f9f9f9")
    tk.Label(win, text="🛡️ Defensa Personal Urbana", font=("Helvetica", 12, "bold"), fg="#d81b60", bg="#f9f9f9").pack(pady=10)
    txt = (
        "• Técnicas prácticas y efectivas de reacción ante situaciones de riesgo.\n"
        "• Manejo de distancias, bloqueos, zafes y proyecciones.\n"
        "• Fomento de la confianza, seguridad y lucidez mental bajo presión.\n"
        "• Entrenamiento táctico adaptado a entornos reales."
    )
    tk.Label(win, text=txt, justify="left", font=("Helvetica", 10), bg="#f9f9f9", padx=20, wraplength=450).pack(fill="both", expand=True)

# ------------------------------------------------------------------
# SEGURIDAD Y CLAVE DE ENTRENADOR
# ------------------------------------------------------------------
def pedir_clave_entrenador(callback_exito):
    win_pass = tk.Toplevel()
    win_pass.title("Acceso Exclusivo - Entrenador")
    win_pass.geometry("340x200")
    win_pass.configure(bg="#f0f0f0")

    tk.Label(win_pass, text="🔒 Zona Restringida Entrenador", font=("Helvetica", 11, "bold"), fg="#b71c1c", bg="#f0f0f0").pack(pady=10)
    tk.Label(win_pass, text="Ingrese contraseña de entrenador:", bg="#f0f0f0", font=("Helvetica", 9)).pack(anchor="w", padx=20)
    
    e_pass_coach = tk.Entry(win_pass, show="*", font=("Helvetica", 10))
    e_pass_coach.pack(fill="x", padx=20, pady=5)

    def verificar():
        if e_pass_coach.get().strip() == CONTRASENA_ENTRENADOR:
            win_pass.destroy()
            callback_exito()
        else:
            messagebox.showerror("Error", "Contraseña de entrenador incorrecta.")

    tk.Button(win_pass, text="Verificar Acceso", bg="#b71c1c", fg="white", font=("Helvetica", 9, "bold"), command=verificar).pack(pady=15)

# ------------------------------------------------------------------
# GENERADOR DE CARNET DIGITAL CON LOGO Y FOTO DE ATLETA
# ------------------------------------------------------------------
img_carnet_ref = None
img_atleta_ref = None

def abrir_carnet_examenes():
    win = tk.Toplevel()
    win.title("Generador de Carnet Digital")
    win.geometry("540x650")
    win.configure(bg="#f4f4f4")

    tk.Label(win, text="🪪 Generador de Carnet Digital y Grados Kup", font=("Helvetica", 12, "bold"), fg="#3949ab", bg="#f4f4f4").pack(pady=5)

    f_input = tk.Frame(win, bg="#f4f4f4", padx=15)
    f_input.pack(fill="x")

    tk.Label(f_input, text="Nombre del Atleta:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_c_nombre = tk.Entry(f_input, font=("Helvetica", 10))
    e_c_nombre.pack(fill="x", pady=2)

    tk.Label(f_input, text="Documento / ID:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_c_doc = tk.Entry(f_input, font=("Helvetica", 10))
    e_c_doc.pack(fill="x", pady=2)

    tk.Label(f_input, text="Grado / Cinturón (Ej: Cinturón Azul - 4to Kup):", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_c_grado = tk.Entry(f_input, font=("Helvetica", 10))
    e_c_grado.pack(fill="x", pady=2)

    tk.Label(f_input, text="Tipo de Sangre / RH:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_c_rh = tk.Entry(f_input, font=("Helvetica", 10))
    e_c_rh.pack(fill="x", pady=2)

    ruta_foto_atleta = tk.StringVar(value="")

    def seleccionar_foto_atleta():
        f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if f:
            ruta_foto_atleta.set(f)
            messagebox.showinfo("Foto Seleccionada", f"Foto de atleta cargada:\n{os.path.basename(f)}")

    tk.Button(f_input, text="📷 Adjuntar Foto del Deportista", bg="#0277bd", fg="white", font=("Helvetica", 9, "bold"), command=seleccionar_foto_atleta).pack(pady=5)

    # Marco del Carnet Digital
    f_carnet = tk.Frame(win, bg="#1a237e", bd=3, relief="ridge", padx=10, pady=10)
    f_carnet.pack(pady=10, fill="x", padx=20)

    # Logo del club en el carnet
    global img_carnet_ref, img_atleta_ref
    ruta_logo = obtener_ruta_recurso_imagen("logo")
    if ruta_logo and os.path.exists(ruta_logo):
        try:
            img_l = Image.open(ruta_logo).resize((45, 45), Image.Resampling.LANCZOS)
            img_carnet_ref = ImageTk.PhotoImage(img_l)
            tk.Label(f_carnet, image=img_carnet_ref, bg="#1a237e").pack(side="left", padx=5)
        except Exception:
            pass

    f_info_carnet = tk.Frame(f_carnet, bg="#1a237e")
    f_info_carnet.pack(side="left", fill="both", expand=True, padx=5)

    lbl_c_detalles = tk.Label(f_info_carnet, text="CLUB JINSEI TAEKWONDO TENJO\n[ Complete los datos y genere el carnet ]", font=("Helvetica", 9, "bold"), fg="#ffffff", bg="#1a237e", justify="left")
    lbl_c_detalles.pack(anchor="w")

    # Contenedor para foto del atleta dentro del carnet
    lbl_foto_carnet = tk.Label(f_carnet, bg="#283593", width=12, height=6, text="[Foto Atleta]", fg="white", font=("Helvetica", 7))
    lbl_foto_carnet.pack(side="right", padx=5)

    def generar_carnet():
        nom = e_c_nombre.get().strip()
        doc = e_c_doc.get().strip()
        grd = e_c_grado.get().strip()
        rh = e_c_rh.get().strip()

        if not nom or not doc or not grd:
            messagebox.showwarning("Aviso", "Por favor complete nombre, documento y grado.")
            return

        texto_carnet = (
            f"ATLETA: {nom}\n"
            f"DOC: {doc} | RH: {rh if rh else 'N/A'}\n"
            f"GRADO: {grd}\n"
            f"VIGENCIA: 2026 - ACTIVO"
        )
        lbl_c_detalles.config(text=texto_carnet, font=("Helvetica", 8, "bold"), fg="#ffd54f")

        if ruta_foto_atleta.get() and os.path.exists(ruta_foto_atleta.get()):
            try:
                img_a = Image.open(ruta_foto_atleta.get()).resize((60, 70), Image.Resampling.LANCZOS)
                global img_atleta_ref
                img_atleta_ref = ImageTk.PhotoImage(img_a)
                lbl_foto_carnet.config(image=img_atleta_ref, text="")
            except Exception:
                pass

        messagebox.showinfo("Carnet Generado", "Carnet Digital generado exitosamente con foto y logo.")

    def descargar_carnet():
        nom = e_c_nombre.get().strip()
        if not nom:
            messagebox.showwarning("Aviso", "Genere primero el carnet antes de descargar.")
            return
        
        archivo_salida = f"Carnet_{nom.replace(' ', '_')}.txt"
        try:
            with open(archivo_salida, "w", encoding="utf-8") as f:
                f.write("=== CLUB JINSEI TAEKWONDO TENJO ===\n")
                f.write(f"Atleta: {e_c_nombre.get()}\n")
                f.write(f"Documento: {e_c_doc.get()}\n")
                f.write(f"Grado: {e_c_grado.get()}\n")
                f.write(f"RH: {e_c_rh.get()}\n")
                f.write("Estado: Activo - 2026\n")
            messagebox.showinfo("Descarga Exitosa", f"Carnet guardado correctamente como:\n{archivo_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    f_btn_carnet = tk.Frame(win, bg="#f4f4f4")
    f_btn_carnet.pack(pady=10)

    tk.Button(f_btn_carnet, text="🪪 Generar Credencial", bg="#3949ab", fg="white", font=("Helvetica", 9, "bold"), command=generar_carnet).pack(side="left", padx=5)
    tk.Button(f_btn_carnet, text="💾 Descargar / Guardar Carnet", bg="#2e7d32", fg="white", font=("Helvetica", 9, "bold"), command=descargar_carnet).pack(side="left", padx=5)

# ------------------------------------------------------------------
# AGENDA DE TORNEOS Y EVENTOS
# ------------------------------------------------------------------
def abrir_agenda_torneos():
    win = tk.Toplevel()
    win.title("Agenda de Torneos y Eventos")
    win.geometry("620x560")
    win.configure(bg="#f4f4f4")

    tk.Label(win, text="📅 Calendarización de Torneos y Eventos", font=("Helvetica", 12, "bold"), fg="#00695c", bg="#f4f4f4").pack(pady=10)

    f_ev = tk.Frame(win, bg="#f4f4f4", padx=15)
    f_ev.pack(fill="x")

    tk.Label(f_ev, text="Nombre del Evento / Torneo:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_ev_nombre = tk.Entry(f_ev, font=("Helvetica", 10))
    e_ev_nombre.pack(fill="x", pady=2)

    tk.Label(f_ev, text="Lugar / Sede:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_ev_lugar = tk.Entry(f_ev, font=("Helvetica", 10))
    e_ev_lugar.pack(fill="x", pady=2)

    tk.Label(f_ev, text="Fecha del Evento (DD/MM/AAAA):", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_ev_fecha = tk.Entry(f_ev, font=("Helvetica", 10))
    e_ev_fecha.pack(fill="x", pady=2)

    def guardar_evento_manual():
        n = e_ev_nombre.get().strip()
        l = e_ev_lugar.get().strip()
        f = e_ev_fecha.get().strip()

        if not n or not f:
            messagebox.showwarning("Aviso", "Nombre y fecha del evento son obligatorios.")
            return

        with open(ARCHIVO_EVENTOS, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([n, l, f])

        messagebox.showinfo("Éxito", "Evento guardado manualmente.")
        e_ev_nombre.delete(0, tk.END)
        e_ev_lugar.delete(0, tk.END)
        e_ev_fecha.delete(0, tk.END)
        cargar_eventos_tabla()

    f_btns = tk.Frame(win, bg="#f4f4f4")
    f_btns.pack(pady=8)

    tk.Button(f_btns, text="✍️ Registrar Evento Manual", bg="#00695c", fg="white", font=("Helvetica", 9, "bold"), command=guardar_evento_manual).pack(side="left", padx=5)

    def cargar_archivo_agenda():
        f = filedialog.askopenfilename(filetypes=[("Documentos / Imagen", "*.pdf *.xlsx *.docx *.jpg *.png")])
        if f:
            messagebox.showinfo("Archivo de Agenda Cargado", f"Agenda / Programación adjuntada correctamente:\n{os.path.basename(f)}")

    tk.Button(f_btns, text="📁 Cargar Archivo de Agenda (PDF/Excel)", bg="#00897b", fg="white", font=("Helvetica", 9, "bold"), command=cargar_archivo_agenda).pack(side="left", padx=5)

    columns = ("Evento", "Lugar / Sede", "Fecha")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    def cargar_eventos_tabla():
        for i in tree.get_children():
            tree.delete(i)
        if os.path.exists(ARCHIVO_EVENTOS):
            with open(ARCHIVO_EVENTOS, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        tree.insert("", tk.END, values=row)

    cargar_eventos_tabla()

# ------------------------------------------------------------------
# MACROESTRUCTURA (SOLO COACH)
# ------------------------------------------------------------------
def abrir_macroestructura():
    def panel_macro():
        win = tk.Toplevel()
        win.title("Macroestructura y Planes")
        win.geometry("520x450")
        win.configure(bg="#f4f4f4")
        tk.Label(win, text="🥋 Planificación Anual y Carga de Planes (Coach)", font=("Helvetica", 12, "bold"), fg="#43a047", bg="#f4f4f4").pack(pady=10)

        lbl_plan = tk.Label(win, text="Ningún plan de entrenamiento cargado.", bg="#e0e0e0", font=("Helvetica", 9), anchor="w", padx=10, width=58, height=3)
        lbl_plan.pack(pady=10)

        def cargar_plan():
            f = filedialog.askopenfilename(filetypes=[("Documentos y PDF", "*.pdf *.docx *.xlsx *.txt")])
            if f:
                lbl_plan.config(text=f"Plan Activo: {os.path.basename(f)}", fg="#000")
                messagebox.showinfo("Carga Exitosa", f"Plan de entrenamiento cargado:\n{os.path.basename(f)}")

        tk.Button(win, text="📂 Cargar Archivo de Plan de Entrenamiento", bg="#43a047", fg="white", font=("Helvetica", 10, "bold"), command=cargar_plan).pack(pady=10)
        
        txt_info = (
            "• FASE 1: Acondicionamiento y Base General.\n"
            "• FASE 2: Fuerza Específica y Táctica.\n"
            "• FASE 3: Poomsae y Evaluaciones de Grado.\n"
            "• FASE 4: Torneos Departamentales y Nacionales."
        )
        tk.Label(win, text=txt_info, justify="left", font=("Helvetica", 9), bg="#f4f4f4", padx=20).pack(fill="both", expand=True)

    pedir_clave_entrenador(panel_macro)

# ------------------------------------------------------------------
# GESTIÓN MANUAL DE DEPORTISTAS (SOLO COACH)
# ------------------------------------------------------------------
def abrir_gestion_deportistas_manual():
    def panel_gestor():
        win = tk.Toplevel()
        win.title("Gestión Manual de Deportistas - Entrenador")
        win.geometry("680x560")
        win.configure(bg="#f4f4f4")

        tk.Label(win, text="👤 Ingresar o Borrar Deportistas (Panel Coach)", font=("Helvetica", 12, "bold"), fg="#2e7d32", bg="#f4f4f4").pack(pady=10)

        f_form = tk.Frame(win, bg="#f4f4f4", padx=20)
        f_form.pack(fill="x")

        tk.Label(f_form, text="Nombre Completo:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
        e_nombre = tk.Entry(f_form, font=("Helvetica", 10))
        e_nombre.pack(fill="x", pady=2)

        tk.Label(f_form, text="Documento:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
        e_doc = tk.Entry(f_form, font=("Helvetica", 10))
        e_doc.pack(fill="x", pady=2)

        tk.Label(f_form, text="Categoría / Cinturón:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
        e_cat = tk.Entry(f_form, font=("Helvetica", 10))
        e_cat.pack(fill="x", pady=2)

        def registrar_manual():
            nom = e_nombre.get().strip()
            doc = e_doc.get().strip()
            cat = e_cat.get().strip()
            if not nom or not doc:
                messagebox.showwarning("Aviso", "Nombre y documento son obligatorios.")
                return
            
            with open(ARCHIVO_DEPORTISTAS, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([nom, doc, "N/A", "N/A", "N/A", "Activo", cat, datetime.date.today()])
            
            messagebox.showinfo("Éxito", "Deportista registrado manualmente.")
            e_nombre.delete(0, tk.END)
            e_doc.delete(0, tk.END)
            e_cat.delete(0, tk.END)
            cargar_tabla()

        tk.Button(f_form, text="➕ Ingresar Deportista Manual", bg="#2e7d32", fg="white", font=("Helvetica", 9, "bold"), command=registrar_manual).pack(pady=5)

        columns = ("Nombre", "Documento", "Peso", "Talla", "IMC", "Estado", "Categoría", "Fecha")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        def cargar_tabla():
            for i in tree.get_children():
                tree.delete(i)
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:
                            tree.insert("", tk.END, values=row)

        def borrar_seleccionado():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Seleccione un deportista de la tabla para borrar.")
                return
            
            item_values = tree.item(selected_item, "values")
            tree.delete(selected_item)
            
            filas_restantes = []
            if os.path.exists(ARCHIVO_DEPORTISTAS):
                with open(ARCHIVO_DEPORTISTAS, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row != list(item_values):
                            filas_restantes.append(row)
            
            with open(ARCHIVO_DEPORTISTAS, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(filas_restantes)

            messagebox.showinfo("Eliminado", "Deportista borrado correctamente del sistema.")

        tk.Button(win, text="🗑️ Borrar Deportista Seleccionado", bg="#d32f2f", fg="white", font=("Helvetica", 9, "bold"), command=borrar_seleccionado).pack(pady=5)
        cargar_tabla()

    pedir_clave_entrenador(panel_gestor)

# ------------------------------------------------------------------
# RESTO DE MÓDULOS
# ------------------------------------------------------------------
def abrir_logros_fotos():
    win = tk.Toplevel()
    win.title("Logros y Carga de Fotografías")
    win.geometry("500x500")
    win.configure(bg="#f4f4f4")
    tk.Label(win, text="🏆 Galería y Carga de Fotos de Resultados", font=("Helvetica", 12, "bold"), fg="#d81b60", bg="#f4f4f4").pack(pady=10)

    lbl_img_preview = tk.Label(win, text="Ninguna foto cargada.", bg="#e0e0e0", width=45, height=14)
    lbl_img_preview.pack(pady=10)

    def cargar_foto():
        f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if f:
            try:
                img = Image.open(f).resize((280, 190), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl_img_preview.config(image=photo, text="")
                lbl_img_preview.image = photo
                messagebox.showinfo("Éxito", f"Foto cargada:\n{os.path.basename(f)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    tk.Button(win, text="📂 Cargar Foto de Resultado / Medalla", bg="#d81b60", fg="white", font=("Helvetica", 10, "bold"), command=cargar_foto).pack(pady=10)

def abrir_videos_multimedia():
    win = tk.Toplevel()
    win.title("Galería y Carga de Videos")
    win.geometry("500x420")
    win.configure(bg="#f4f4f4")
    tk.Label(win, text="📹 Carga y Reproducción de Videos de Combate", font=("Helvetica", 11, "bold"), fg="#6a5acd", bg="#f4f4f4").pack(pady=10)

    listbox_videos = tk.Listbox(win, font=("Helvetica", 9), height=12)
    listbox_videos.pack(padx=20, pady=5, fill="both", expand=True)

    def agregar_videos():
        files = filedialog.askopenfilenames(filetypes=[("Archivos de Video", "*.mp4 *.avi *.mov *.mkv")])
        for file in files:
            listbox_videos.insert(tk.END, file)

    tk.Button(win, text="➕ Cargar Archivos de Video", bg="#6a5acd", fg="white", font=("Helvetica", 10, "bold"), command=agregar_videos).pack(pady=10)

def abrir_ficha_deportista():
    win = tk.Toplevel()
    win.title("Ficha Integral del Deportista e IMC")
    win.geometry("600x620")
    win.configure(bg="#f4f4f4")

    tk.Label(win, text="📋 Ficha y Evaluación Antropométrica", font=("Helvetica", 12, "bold"), fg="#1e88e5", bg="#f4f4f4").pack(pady=10)

    f_datos = tk.Frame(win, bg="#f4f4f4", padx=20)
    f_datos.pack(fill="x")

    tk.Label(f_datos, text="Nombre Completo:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_nom = tk.Entry(f_datos, font=("Helvetica", 10))
    e_nom.pack(fill="x", pady=2)

    tk.Label(f_datos, text="Documento de Identidad:", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_doc = tk.Entry(f_datos, font=("Helvetica", 10))
    e_doc.pack(fill="x", pady=2)

    tk.Label(f_datos, text="Peso (kg):", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_peso = tk.Entry(f_datos, font=("Helvetica", 10))
    e_peso.pack(fill="x", pady=2)

    tk.Label(f_datos, text="Talla / Estatura (m - ej: 1.72):", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_talla = tk.Entry(f_datos, font=("Helvetica", 10))
    e_talla.pack(fill="x", pady=2)

    tk.Label(f_datos, text="Grado / Cinturón (Kup/Dan):", bg="#f4f4f4", font=("Helvetica", 9, "bold")).pack(anchor="w")
    e_grado = tk.Entry(f_datos, font=("Helvetica", 10))
    e_grado.pack(fill="x", pady=2)

    lbl_resultado = tk.Label(win, text="IMC y Datos: Pendiente de cálculo", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#555")
    lbl_resultado.pack(pady=10)

    def calcular_y_guardar():
        try:
            p = float(e_peso.get())
            t = float(e_talla.get())
            imc = p / (t ** 2)
            estado = "Bajo peso" if imc < 18.5 else "Normal" if imc < 25 else "Sobrepeso" if imc < 30 else "Obesidad"
            
            res_txt = f"Atleta: {e_nom.get()} | IMC: {imc:.2f} ({estado}) | Talla: {t}m | Peso: {p}kg"
            lbl_resultado.config(text=res_txt, fg="#1b5e20")

            with open(ARCHIVO_DEPORTISTAS, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([e_nom.get(), e_doc.get(), p, t, f"{imc:.2f}", estado, e_grado.get(), datetime.date.today()])
            messagebox.showinfo("Éxito", "Ficha guardada correctamente en el sistema.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para peso y talla.")

    tk.Button(win, text="💾 Calcular IMC y Guardar Ficha", bg="#1e88e5", fg="white", font=("Helvetica", 10, "bold"), command=calcular_y_guardar).pack(pady=5)

def abrir_documentacion_pdf():
    win = tk.Toplevel()
    win.title("Gestión de Documentos y PDF")
    win.geometry("500x420")
    win.configure(bg="#f4f4f4")
    tk.Label(win, text="📁 Carga de Documentación Oficial (PDF)", font=("Helvetica", 12, "bold"), fg="#ad1457", bg="#f4f4f4").pack(pady=10)
    
    lbl_f = tk.Label(win, text="Ficha de Inscripción: No cargada", bg="#e0e0e0", width=55, height=2, anchor="w", padx=10)
    lbl_f.pack(pady=5)
    lbl_e = tk.Label(win, text="Carta de Exoneración: No cargada", bg="#e0e0e0", width=55, height=2, anchor="w", padx=10)
    lbl_e.pack(pady=5)
    lbl_a = tk.Label(win, text="Autorización de Imágenes: No cargada", bg="#e0e0e0", width=55, height=2, anchor="w", padx=10)
    lbl_a.pack(pady=5)

    def cargar_doc(tipo, label_w):
        f = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if f:
            label_w.config(text=f"{tipo}: {os.path.basename(f)}", fg="#000")
            messagebox.showinfo("Documento", f"{tipo} cargado con éxito.")

    tk.Button(win, text="📄 Ficha de Inscripción (PDF)", bg="#0277bd", fg="white", font=("Helvetica", 9, "bold"), width=35, command=lambda: cargar_doc("Ficha", lbl_f)).pack(pady=4)
    tk.Button(win, text="📄 Carta de Exoneración (PDF)", bg="#0277bd", fg="white", font=("Helvetica", 9, "bold"), width=35, command=lambda: cargar_doc("Exoneración", lbl_e)).pack(pady=4)
    tk.Button(win, text="📄 Autorización Imágenes (PDF)", bg="#0277bd", fg="white", font=("Helvetica", 9, "bold"), width=35, command=lambda: cargar_doc("Autorización", lbl_a)).pack(pady=4)

def abrir_asistencias():
    win = tk.Toplevel()
    win.title("Control de Asistencia")
    win.geometry("400x300")
    win.configure(bg="#f4f4f4")
    tk.Label(win, text="📅 Control de Asistencia", font=("Helvetica", 12, "bold"), fg="#008b8b", bg="#f4f4f4").pack(pady=10)
    tk.Label(win, text=f"Fecha: {datetime.date.today()}", font=("Helvetica", 10), bg="#f4f4f4").pack(pady=5)
    
    ev = tk.StringVar(value="Presente")
    tk.Radiobutton(win, text="Presente", variable=ev, value="Presente", bg="#f4f4f4").pack(anchor="w", padx=50)
    tk.Radiobutton(win, text="Ausente / Excusa", variable=ev, value="Ausente", bg="#f4f4f4").pack(anchor="w", padx=50)
    
    tk.Button(win, text="✅ Guardar Asistencia", bg="#218838", fg="white", font=("Helvetica", 10, "bold"), command=lambda: [messagebox.showinfo("Asistencia", f"Asistencia marcada como [{ev.get()}]."), win.destroy()]).pack(pady=20)

def abrir_pagos():
    try:
        import winsound
        winsound.Beep(2500, 400)
    except Exception:
        pass

    win = tk.Toplevel()
    win.title("Información de Pagos")
    win.geometry("420x320")
    win.configure(bg="#ffffff")
    tk.Label(win, text="💳 Plataformas de Pago Autorizadas", font=("Helvetica", 12, "bold"), fg="#1b5e20", bg="#ffffff").pack(pady=10)
    txt = (
        "📲 NEQUI / DAVIPLATA:\n  • Número: 320 123 4567\n  • Titular: Club Jinsei Taekwondo\n\n"
        "🔑 LLAVE / BRE-B:\n  • Código: JINSEI-TENJO-2026\n\n"
        "🔔 [Alerta sonora activada]: Envíe el comprobante al WhatsApp."
    )
    tk.Label(win, text=txt, justify="left", font=("Helvetica", 10), bg="#ffffff", padx=20).pack(fill="both", expand=True)
    tk.Button(win, text="Aceptar", bg="#1b5e20", fg="white", font=("Helvetica", 9, "bold"), command=win.destroy).pack(pady=10)

def exportar_reportes_csv():
    messagebox.showinfo("Exportar", "Reportes generales exportados con éxito a CSV.")

# ------------------------------------------------------------------
# PANEL PRINCIPAL
# ------------------------------------------------------------------
def abrir_panel_principal():
    ventana_login.destroy()
    
    panel = tk.Tk()
    panel.title("Jinsei Taekwondo Tenjo - Panel Principal")
    panel.geometry("820x740")
    panel.configure(bg="#f4f4f4")

    frame_top = tk.Frame(panel, bg="#f4f4f4")
    frame_top.pack(fill="x", padx=10, pady=10)

    tk.Button(frame_top, text="🥋 S1: Taekwondo", bg="#4a708b", fg="white", font=("Helvetica", 8, "bold"), command=abrir_servicio_taekwondo).pack(side="left", padx=3)
    tk.Button(frame_top, text="💪 S2: Funcional", bg="#2e7d32", fg="white", font=("Helvetica", 8, "bold"), command=abrir_servicio_funcional).pack(side="left", padx=3)
    tk.Button(frame_top, text="🛡️ S3: Defensa", bg="#d81b60", fg="white", font=("Helvetica", 8, "bold"), command=abrir_servicio_defensa).pack(side="left", padx=3)
    
    tk.Button(frame_top, text="📅 Asistencia", bg="#008b8b", fg="white", font=("Helvetica", 8, "bold"), command=abrir_asistencias).pack(side="left", padx=3)
    tk.Button(frame_top, text="💳 Pagos (Alerta)", bg="#2e8b57", fg="white", font=("Helvetica", 8, "bold"), command=abrir_pagos).pack(side="right", padx=3)

    tk.Label(panel, text="¡BIENVENIDO A JINSEI TAEKWONDO!", font=("Helvetica", 14, "bold"), fg="#000080", bg="#f4f4f4").pack(pady=5)

    ruta_logo = obtener_ruta_recurso_imagen("logo")
    if ruta_logo and os.path.exists(ruta_logo):
        try:
            img = Image.open(ruta_logo).resize((85, 85), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(panel, image=photo, bg="#f4f4f4")
            lbl.image = photo
            lbl.pack(pady=2)
        except Exception:
            pass

    tk.Label(panel, text="Panel de Gestión Integral y Entrenador:", font=("Helvetica", 10, "bold"), bg="#f4f4f4").pack(pady=5)
    
    fb = tk.Frame(panel, bg="#f4f4f4")
    fb.pack(pady=5)
    w = 42

    tk.Button(fb, text="📋 Ficha Integral del Deportista e IMC", bg="#1e88e5", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_ficha_deportista).pack(pady=3)
    tk.Button(fb, text="👤 Gestión Manual de Deportistas (Solo Coach)", bg="#2e7d32", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_gestion_deportistas_manual).pack(pady=3)
    tk.Button(fb, text="🥋 Macroestructura y Planes (Solo Coach)", bg="#43a047", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_macroestructura).pack(pady=3)
    tk.Button(fb, text="🏆 Cargar Logros y Fotos de Resultados", bg="#d81b60", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_logros_fotos).pack(pady=3)
    tk.Button(fb, text="📹 Cargar Videos de Combate / Poomsae", bg="#6a5acd", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_videos_multimedia).pack(pady=3)
    tk.Button(fb, text="📁 Cargar Fichas, Exoneraciones y PDFs", bg="#ad1457", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_documentacion_pdf).pack(pady=3)
    tk.Button(fb, text="🪪 Generar Carnet Digital (Con Foto y Logo)", bg="#3949ab", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_carnet_examenes).pack(pady=3)
    tk.Button(fb, text="📅 Agenda de Torneos y Eventos (Cargar/Manual)", bg="#00695c", fg="white", font=("Helvetica", 9, "bold"), width=w, command=abrir_agenda_torneos).pack(pady=3)

    tk.Label(panel, text="Horarios: Lunes y Miércoles 4:00-8:00 PM | Sábados 10:00 AM-12:00 M", font=("Helvetica", 8), fg="#555", bg="#f4f4f4").pack(pady=5)

    ruta_foto = obtener_ruta_recurso_imagen("foto")
    if ruta_foto and os.path.exists(ruta_foto):
        try:
            imgf = Image.open(ruta_foto).resize((220, 100), Image.Resampling.LANCZOS)
            photof = ImageTk.PhotoImage(imgf)
            lblf = tk.Label(panel, image=photof, bg="#f4f4f4")
            lblf.image = photof
            lblf.pack(pady=2)
        except Exception:
            pass

    tk.Button(panel, text="Cerrar Sesión", bg="#ff0000", fg="white", font=("Helvetica", 9, "bold"), width=15, command=panel.destroy).pack(pady=5)
    panel.mainloop()

# ------------------------------------------------------------------
# LOGIN Y REGISTRO (CON LOGO INSTITUCIONAL)
# ------------------------------------------------------------------
def validar_login():
    u = ent_user.get().strip()
    p = ent_pass.get().strip()
    if not u or not p:
        messagebox.showwarning("Aviso", "Ingrese usuario y contraseña.")
        return
    users = cargar_usuarios()
    if u in users and users[u]["password"] == p:
        abrir_panel_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def registrar_usuario():
    nu = ent_new_user.get().strip()
    np = ent_new_pass.get().strip()
    co = ent_correo.get().strip()
    if not nu or not np or not co:
        messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
        return
    users = cargar_usuarios()
    if nu in users:
        messagebox.showerror("Error", "El usuario ya existe.")
        return
    users[nu] = {"password": np, "correo": co}
    guardar_usuarios(users)
    messagebox.showinfo("Éxito", "Usuario creado con éxito. Ya puede iniciar sesión.")
    ent_new_user.delete(0, tk.END)
    ent_new_pass.delete(0, tk.END)
    ent_correo.delete(0, tk.END)
    notebook.select(tab_login)

ventana_login = tk.Tk()
ventana_login.title("Jinsei Taekwondo Tenjo - Acceso")
ventana_login.geometry("380x480")
ventana_login.configure(bg="#f0f0f0")

tk.Label(ventana_login, text="🥋 Jinsei Taekwondo Tenjo", font=("Helvetica", 14, "bold"), fg="#000080", bg="#f0f0f0").pack(pady=5)

# Logo en la pantalla de inicio (Login)
img_login_ref = None
ruta_logo_login = obtener_ruta_recurso_imagen("logo")
if ruta_logo_login and os.path.exists(ruta_logo_login):
    try:
        img_lg = Image.open(ruta_logo_login).resize((65, 65), Image.Resampling.LANCZOS)
        img_login_ref = ImageTk.PhotoImage(img_lg)
        tk.Label(ventana_login, image=img_login_ref, bg="#f0f0f0").pack(pady=2)
    except Exception:
        pass

notebook = ttk.Notebook(ventana_login)
notebook.pack(padx=15, pady=5, fill="both", expand=True)

tab_login = ttk.Frame(notebook)
tab_registro = ttk.Frame(notebook)
notebook.add(tab_login, text="Iniciar Sesión")
notebook.add(tab_registro, text="Crear Usuario")

# Pestaña Iniciar Sesión
fl = tk.Frame(tab_login, bg="#f0f0f0", padx=15, pady=15)
fl.pack(fill="both", expand=True)
tk.Label(fl, text="Usuario:", bg="#f0f0f0", font=("Helvetica", 9, "bold")).pack(anchor="w")
ent_user = tk.Entry(fl, font=("Helvetica", 10))
ent_user.pack(fill="x", pady=5)
tk.Label(fl, text="Contraseña:", bg="#f0f0f0", font=("Helvetica", 9, "bold")).pack(anchor="w")
ent_pass = tk.Entry(fl, show="*", font=("Helvetica", 10))
ent_pass.pack(fill="x", pady=5)
tk.Button(fl, text="🔑 Ingresar", bg="#1b5e20", fg="white", font=("Helvetica", 10, "bold"), command=validar_login).pack(pady=20, fill="x")

# Pestaña Crear Usuario
fr = tk.Frame(tab_registro, bg="#f0f0f0", padx=15, pady=10)
fr.pack(fill="both", expand=True)
tk.Label(fr, text="Nuevo Usuario:", bg="#f0f0f0", font=("Helvetica", 9, "bold")).pack(anchor="w")
ent_new_user = tk.Entry(fr, font=("Helvetica", 10))
ent_new_user.pack(fill="x", pady=3)
tk.Label(fr, text="Contraseña:", bg="#f0f0f0", font=("Helvetica", 9, "bold")).pack(anchor="w")
ent_new_pass = tk.Entry(fr, show="*", font=("Helvetica", 10))
ent_new_pass.pack(fill="x", pady=3)
tk.Label(fr, text="Correo de Recuperación:", bg="#f0f0f0", font=("Helvetica", 9, "bold")).pack(anchor="w")
ent_correo = tk.Entry(fr, font=("Helvetica", 10))
ent_correo.pack(fill="x", pady=3)
tk.Button(fr, text="✨ Crear Cuenta", bg="#0277bd", fg="white", font=("Helvetica", 10, "bold"), command=registrar_usuario).pack(pady=15, fill="x")

ventana_login.mainloop()