import customtkinter as ctk
import os, sys, json, subprocess
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ExodusMain(ctk.CTk):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

class ExodusMain(ctk.CTk):
    def __init__(self, rol="Operario"):
        super().__init__()
    
        self.title("Exodus Contable ver. 1.0")
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                self.tema_actual = config.get("tema", "claro").lower()
        except (FileNotFoundError, json.JSONDecodeError):
            self.tema_actual = "claro"

        if self.tema_actual == "oscuro":
            ctk.set_appearance_mode("dark")
        elif self.tema_actual == "sistema":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode("light")

        ctk.set_default_color_theme("blue")

        self.colores = {
            "claro": {
                "topbar": "#1E88E5",
                "sidebar": "#1565C0",
                "content": "#E3F2FD",
                "texto_titulo": "#0D47A1",
                "boton": "#1976D2",
                "hover": "#0D47A1"
            },
            "oscuro": {
                "topbar": "#0D47A1",
                "sidebar": "#1E1E1E",
                "content": "#121212",
                "texto_titulo": "#BBDEFB",
                "boton": "#1565C0",
                "hover": "#0D47A1"
            }
        }

        self.tema_actual = self.tema_actual if self.tema_actual in ["claro", "oscuro"] else "claro"

        self.geometry("1200x850")
        try:
            self.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        self.after(100, lambda: self.wm_state("zoomed"))

        self.rol = rol

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        try:
            if self.tema_actual == "oscuro":
                self.iconbitmap("iconexodark.ico")
            else:
                self.iconbitmap("iconexolight.ico")
        except Exception as e:
            print(f"Error cargando ícono: {e}")

        self.topbar = ctk.CTkFrame(self, fg_color=self.colores[self.tema_actual]["topbar"], height=50, corner_radius=0)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.title_label = ctk.CTkLabel(
            self.topbar,
            text="Exodus Contable",
            font=("Helvetica", 18, "bold"),
            text_color="white" if self.tema_actual == "claro" else "#BBDEFB"
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        self.sidebar = ctk.CTkFrame(self, fg_color=self.colores[self.tema_actual]["sidebar"], width=220, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        self.content = ctk.CTkFrame(self, fg_color=self.colores[self.tema_actual]["content"])
        self.content.grid(row=1, column=1, sticky="nsew")

        self._setup_sidebar()
        self.welcomescreen()
        self.state("zoomed")

    def _setup_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Menú", text_color="white",
                     font=("Helvetica", 16, "bold")).pack(pady=15)

        buttons = [
            ("Inventarios", self.openbills),
            ("Contabilidad", self.accountingstats),
            ("Recurso Humano", self.workers),
            ("Configuración", self.configtools),
            ("Cerrar sesión", self.logout),
            ("Salir", self.exit),
        ]

        for text, cmd in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                fg_color=self.colores[self.tema_actual]["boton"],
                hover_color=self.colores[self.tema_actual]["hover"],
                font=("Helvetica", 13, "bold")
            ).pack(fill="x", padx=15, pady=5)

    def clearcontent(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def welcomescreen(self):
        self.clearcontent()
        ctk.CTkLabel(self.content, text="Bienvenido a Exodus Contable",
                     font=("Helvetica", 24, "bold"), text_color="#0D47A1").pack(pady=60)
        ctk.CTkLabel(self.content, text="Explora las nuevas funciones del sistema.",
                     font=("Helvetica", 14)).pack()
        
## MÓDULOS (igual que antes pero en CTk)

    def openbills(self):
        self.clearcontent()
        ctk.CTkLabel(self.content, text="Inventarios", font=("Helvetica", 18, "bold")).pack(pady=40)

    def accountingstats(self):
        self.clearcontent()
        ctk.CTkLabel(self.content, text="Contabilidad", font=("Helvetica", 18, "bold")).pack(pady=40)

    def workers(self):
        self.clearcontent()
        ctk.CTkLabel(self.content, text="Nómina", font=("Helvetica", 18, "bold")).pack(pady=40)

    def configtools(self):
        self.clearcontent()
        ctk.CTkLabel(self.content, text="Configuración",
                     font=("Helvetica", 22, "bold"), text_color="#0D47A1").pack(pady=20)

        options_frame = ctk.CTkFrame(self.content, fg_color=self.colores[self.tema_actual]["content"])
        options_frame.pack(pady=10)

        ctk.CTkButton(options_frame, text="Administrar Usuarios",
                      command=self.adminusuarios, font=("Helvetica", 15, "bold"),
                      fg_color=self.colores[self.tema_actual]["boton"], hover_color=self.colores[self.tema_actual]["hover"], width=320, height=45).pack(pady=10)

        ctk.CTkButton(options_frame, text="Administrar Etiquetas Contables",
                      command=self.adminetiquetas, font=("Helvetica", 15, "bold"),
                      fg_color=self.colores[self.tema_actual]["boton"], hover_color=self.colores[self.tema_actual]["hover"], width=320, height=45).pack(pady=10)

        ctk.CTkButton(options_frame, text="Monitorear Usuarios",
                      command=self.seeloginsusers, font=("Helvetica", 15, "bold"),
                      fg_color=self.colores[self.tema_actual]["boton"], hover_color=self.colores[self.tema_actual]["hover"], width=320, height=45).pack(pady=10)
        
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                tema_actual = config.get("tema", "claro").capitalize()
        except (FileNotFoundError, json.JSONDecodeError):
            tema_actual = "Claro"

        ctk.CTkLabel(options_frame, text="Tema del sistema:",
                 font=("Helvetica", 15, "bold"),
                 text_color="#0D47A1").pack(pady=(20, 5))
        
        tema_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["Claro", "Oscuro", "Sistema"],
            command=self.cambiar_tema
        )
        tema_menu.pack(pady=5)

        if tema_actual in ["Claro", "Oscuro", "Sistema"]:
            tema_menu.set(tema_actual)
        else:
            tema_menu.set("Claro")

    def backbutt(self, parent_frame, command=None):
        if command is None:
            command = self.configtools

        back_button = ctk.CTkButton(
            parent_frame,
            text="← Volver",
            font=("Helvetica", 13, "bold"),
            width=90,
            height=30,
            corner_radius=8,
            fg_color="#90CAF9",
            hover_color="#64B5F6",
            text_color="#0D47A1",
            command=command
        )
        back_button.pack(anchor="w", padx=15, pady=10)

    def cambiar_tema(self, modo):
        modo = modo.lower()
        if modo == "oscuro":
            ctk.set_appearance_mode("dark")
        elif modo == "sistema":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode("light")
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}

        config["tema"] = modo

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        self.tema_actual = modo if modo in ["claro", "oscuro"] else "claro"
        self.actualizar_colores()
        try:
            if self.tema_actual == "oscuro":
                self.iconbitmap("iconexodark.ico")
            else:
                self.iconbitmap("iconexolight.ico")
        except Exception as e:
            print(f"Error cambiando ícono: {e}")
        
    def actualizar_colores(self):
        colores = self.colores[self.tema_actual]

        # Contenedores principales
        self.topbar.configure(fg_color=colores["topbar"])
        self.sidebar.configure(fg_color=colores["sidebar"])
        self.content.configure(fg_color=colores["content"])
        self.title_label.configure(
            text_color="white" if self.tema_actual == "claro" else "#BBDEFB"
        )

        # Botones de la barra lateral
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=colores["boton"],
                    hover_color=colores["hover"]
                )

        # Contenido dinámico (Configuración, Usuarios, etc.)
        for widget in self.content.winfo_children():
            self._aplicar_colores_a_widget(widget, colores)

    def _aplicar_colores_a_widget(self, widget, colores):
        if isinstance(widget, ctk.CTkFrame) or isinstance(widget, ctk.CTkScrollableFrame):
            widget.configure(fg_color=colores["content"])

        elif isinstance(widget, ctk.CTkButton):
            widget.configure(fg_color=colores["boton"], hover_color=colores["hover"])

        elif isinstance(widget, ctk.CTkLabel):
            widget.configure(text_color=colores["texto_titulo"])

        elif isinstance(widget, ctk.CTkEntry):
            widget.configure(
                fg_color="#1E1E1E" if self.tema_actual == "oscuro" else "white",
                text_color="#E3E3E3" if self.tema_actual == "oscuro" else "black"
            )
        for child in widget.winfo_children():
            self._aplicar_colores_a_widget(child, colores)


## Funciones del administrador de usuarios del modulo de configuración

    def adminusuarios(self):
        self.clearcontent()
        self.backbutt(self.content)
        ctk.CTkLabel(self.content, text="Administrar Usuarios",
                 font=("Helvetica", 22, "bold"), text_color="#0D47A1").pack(pady=10)
        ctk.CTkLabel(self.content, text="Gestiona los usuarios del sistema",
                    font=("Helvetica", 13), text_color="gray30").pack(pady=(0, 10))

        try:
            with open("DBusuarios.json", "r", encoding="utf-8") as f:
                usuarios = json.load(f)
            print("Usuarios cargados:", usuarios)
        except FileNotFoundError:
            usuarios = []

        if not usuarios:
            ctk.CTkLabel(self.content, text="No hay usuarios registrados.",
                        font=("Helvetica", 14), text_color="gray50").pack(pady=20)
            return

        table = ctk.CTkScrollableFrame(self.content, width=720, height=400, fg_color=self.colores[self.tema_actual]["content"])
        table.pack(pady=10)

        header = ctk.CTkFrame(table, fg_color=self.colores[self.tema_actual]["sidebar"])
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Usuario", text_color="white",
                    font=("Helvetica", 13, "bold"), width=20, anchor="w").pack(side="left", padx=40, pady=5)
        ctk.CTkLabel(header, text="Rol", text_color="white",
                    font=("Helvetica", 13, "bold"), width=15, anchor="w").pack(side="left", padx=40, pady=5)

        for u in usuarios:
            fila = ctk.CTkFrame(table, fg_color=self.colores[self.tema_actual]["content"])
            fila.pack(fill="x", pady=1)
            ctk.CTkLabel(fila, text=u.get("usuario", ""), width=20,
                        font=("Helvetica", 12), anchor="w", text_color=self.colores[self.tema_actual]["texto_titulo"]).pack(side="left", padx=40, pady=3)
            ctk.CTkLabel(fila, text=u.get("rol", ""), width=15,
                        font=("Helvetica", 12), anchor="w", text_color=self.colores[self.tema_actual]["texto_titulo"]).pack(side="left", padx=40, pady=3)
        
        buttons_frame = ctk.CTkFrame(
            self.content,
            fg_color=self.colores[self.tema_actual]["content"]
        )
        buttons_frame.pack(pady=20)

        btn_agregar = ctk.CTkButton(
            buttons_frame,
            text="Agregar Usuario",
            fg_color="#2E7D32", hover_color="#1B5E20",
            command=self.opadduser, width=180
        )
        btn_agregar.pack(side="left", padx=10)

        btn_editar = ctk.CTkButton(
            buttons_frame,
            text="Editar Usuario",
            fg_color="#0277BD", hover_color="#01579B",
            command=self.opedituser, width=180
        )
        btn_editar.pack(side="left", padx=10)

        btn_eliminar = ctk.CTkButton(
            buttons_frame,
            text="X Eliminar Usuario",
            fg_color="#C62828", hover_color="#B71C1C",
            command=self.opdeleteuser, width=180
        )
        btn_eliminar.pack(side="left", padx=10)

    def opadduser(self):
        win = ctk.CTkToplevel(self)
        win.title("Agregar Nuevo Usuario")
        win.geometry("360x380")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass
        
        win.transient(self)
        win.grab_set()
        win.focus_force()

        win.update_idletasks()
        width = 360
        height = 380
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(win, text="Nuevo Usuario", font=("Helvetica", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(win, text="Usuario:").pack()
        user_entry = ctk.CTkEntry(win, width=260)
        user_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Contraseña:").pack()
        pass_entry = ctk.CTkEntry(win, show="*", width=260)
        pass_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Rol:").pack(pady=(8, 0))
        roles = ["Administrador", "Contador", "RRHH", "Operario"]
        rol_menu = ctk.CTkOptionMenu(win, values=roles)
        rol_menu.pack(pady=5)

        def guardar():
            nuevo_user = user_entry.get().strip()
            nueva_pass = pass_entry.get().strip()
            # rol_menu.get() devuelve una cadena; si está vacía, usamos Operario
            nuevo_rol = rol_menu.get() if rol_menu.get() else "Operario"

            if not nuevo_user or not nueva_pass:
                CTkMessagebox(title="Campos Vacíos",
                            message="Debes llenar todos los campos antes de continuar.",
                            icon="warning")
                return

            if "." not in nuevo_user:
                CTkMessagebox(title="Formato Inválido",
                            message="El formato de usuario debe ser Nombre.Apellido\nEjemplo: Juan.Perez",
                            icon="warning")
                return

            partes = nuevo_user.split(".")
            if len(partes) != 2 or not all(p.isalpha() for p in partes):
                CTkMessagebox(title="Formato Inválido",
                            message="El formato de usuario debe ser Nombre.Apellido\nEjemplo: Juan.Perez",
                            icon="warning")
                return

            nombre = partes[0].capitalize()
            apellido = partes[1].capitalize()
            nuevo_user = f"{nombre}.{apellido}"

            try:
                with open("DBusuarios.json", "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                usuarios = []

            for u in usuarios:
                if u.get("usuario") == nuevo_user:
                    messagebox.showerror("Error", "El usuario ya existe.")
                    return

            usuarios.append({
                "usuario": nuevo_user,
                "contraseña": nueva_pass,
                "rol": nuevo_rol
            })

            with open("DBusuarios.json", "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Éxito", f"Usuario '{nuevo_user}' agregado correctamente.")
            win.destroy()
            self.adminusuarios()  # refresca la lista

        ctk.CTkButton(win, text="Guardar", command=guardar, width=160).pack(pady=18)

    def opedituser(self):
        try:
            with open("DBusuarios.json", "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except FileNotFoundError:
            usuarios = []

        if not usuarios:
            messagebox.showinfo("Info", "No hay usuarios para editar.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Editar Usuario")
        win.geometry("420x420")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        win.transient(self)
        win.grab_set()
        win.focus_force()
        
        win.update_idletasks()
        width = 420
        height = 420
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        win.update_idletasks()
        width = 420
        height = 420
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(win, text="Selecciona un usuario para editar", font=("Helvetica", 14, "bold")).pack(pady=10)

        usuarios_nombres = [u.get("usuario", "") for u in usuarios]
        user_menu = ctk.CTkOptionMenu(win, values=usuarios_nombres)
        user_menu.pack(pady=10)

        ctk.CTkLabel(win, text="Nueva contraseña:").pack(pady=(10, 0))
        new_pass = ctk.CTkEntry(win, show="*", width=260)
        new_pass.pack(pady=5)

        ctk.CTkLabel(win, text="Nuevo rol:").pack(pady=(10, 0))
        roles = ["Administrador", "Contador", "RRHH", "Operario"]
        new_rol = ctk.CTkOptionMenu(win, values=roles)
        new_rol.pack(pady=5)

        def guardar_cambio():
            sel_user = user_menu.get()
            cambio_pass = new_pass.get().strip()
            cambio_rol = new_rol.get() if new_rol.get() else "Operario"

            if not sel_user:
                messagebox.showwarning("Atención", "Selecciona un usuario.")
                return

            for u in usuarios:
                if u.get("usuario") == sel_user:
                    if cambio_pass:
                        u["contraseña"] = cambio_pass
                    u["rol"] = cambio_rol
                    break

            with open("DBusuarios.json", "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Éxito", f"Usuario '{sel_user}' actualizado correctamente.")
            win.destroy()
            self.adminusuarios()

        ctk.CTkButton(win, text="Guardar Cambios", command=guardar_cambio, width=180).pack(pady=18)

    def opdeleteuser(self):
        try:
            with open("DBusuarios.json", "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except FileNotFoundError:
            usuarios = []

        if not usuarios:
            messagebox.showinfo("Info", "No hay usuarios para eliminar.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Eliminar Usuario")
        win.geometry("360x300")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        win.transient(self)
        win.grab_set()
        win.focus_force()

        ctk.CTkLabel(win, text="Selecciona un usuario para eliminar", font=("Helvetica", 14, "bold")).pack(pady=10)

        usuarios_nombres = [u.get("usuario", "") for u in usuarios]
        user_menu = ctk.CTkOptionMenu(win, values=usuarios_nombres)
        user_menu.pack(pady=10)

        def eliminar():
            sel_user = user_menu.get()
            if not sel_user:
                messagebox.showwarning("Atención", "Selecciona un usuario.")
                return

            if sel_user.lower() == "adminis":
                messagebox.showwarning("Atención", "No se puede eliminar al administrador principal.")
                return

            confirm = messagebox.askyesno("Confirmar", f"Eliminar usuario '{sel_user}'?")
            if not confirm:
                return

            usuarios_filtrados = [u for u in usuarios if u.get("usuario") != sel_user]
            with open("DBusuarios.json", "w", encoding="utf-8") as f:
                json.dump(usuarios_filtrados, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Éxito", f"Usuario '{sel_user}' eliminado correctamente.")
            win.destroy()
            self.adminusuarios()

        ctk.CTkButton(win, text="Eliminar", command=eliminar, width=160).pack(pady=18)

## Funciones del administrador de etiquetas del modulo de configuración

    def adminetiquetas(self):
        self.clearcontent()
        print("Entrando a adminetiquetas...")
        self.backbutt(self.content)

        ctk.CTkLabel(
            self.content,
            text="Administrar Etiquetas Contables",
            font=("Helvetica", 22, "bold"),
            text_color="#0D47A1"
        ).pack(pady=10)

        ctk.CTkLabel(
            self.content,
            text="Gestiona las etiquetas usadas en contabilidad, inventario y nómina.",
            font=("Helvetica", 13),
            text_color="gray30"
        ).pack(pady=(0, 15))

        try:
            with open("DBetiquetas.json", "r", encoding="utf-8") as f:
                etiquetas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            etiquetas = []

        if not etiquetas:
            ctk.CTkLabel(
                self.content,
                text="No hay etiquetas registradas aún.",
                font=("Helvetica", 14),
                text_color="gray50"
            ).pack(pady=40)
            etiquetas = []  # Evita errores posteriores

        table = ctk.CTkScrollableFrame(self.content, width=700, height=400, fg_color=self.colores[self.tema_actual]["content"])
        table.pack(pady=10)

        header = ctk.CTkFrame(table, fg_color=self.colores[self.tema_actual]["sidebar"])
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Nombre", text_color="white",
                    font=("Helvetica", 13, "bold"), width=200, anchor="w").pack(side="left", padx=30, pady=5)
        ctk.CTkLabel(header, text="Importe ($-%)", text_color="white",
                    font=("Helvetica", 13, "bold"), width=100, anchor="w").pack(side="left", padx=20, pady=5)
        ctk.CTkLabel(header, text="Módulo", text_color="white",
                    font=("Helvetica", 13, "bold"), width=150, anchor="w").pack(side="left", padx=20, pady=5)
        ctk.CTkLabel(header, text="Acciones", text_color="white",
                    font=("Helvetica", 13, "bold"), width=100, anchor="center").pack(side="right", padx=20, pady=5)

        for e in etiquetas:
            fila = ctk.CTkFrame(table, fg_color=self.colores[self.tema_actual]["content"])
            fila.pack(fill="x", pady=1)

            ctk.CTkLabel(fila, text=e.get("nombre", ""), width=200,
                        font=("Helvetica", 12), anchor="w").pack(side="left", padx=30, pady=3)
            ctk.CTkLabel(fila, text=str(e.get("taxes", "")), width=100,
                        font=("Helvetica", 12), anchor="w").pack(side="left", padx=20, pady=3)
            ctk.CTkLabel(fila, text=e.get("modulo", ""), width=150,
                        font=("Helvetica", 12), anchor="w").pack(side="left", padx=20, pady=3)

            menu_button = ctk.CTkButton(
                fila,
                text="⋮",
                width=30,
                height=30,
                corner_radius=8,
                fg_color="#90CAF9",
                hover_color="#64B5F6",
                text_color="#0D47A1",
                font=("Helvetica", 16, "bold"),
                command=lambda e=e: self.mostrar_menu_etiqueta(e)
            )
            menu_button.pack(side="right", padx=20, pady=3)

        buttons_frame = ctk.CTkFrame(
            self.content,
            fg_color=self.colores[self.tema_actual]["content"]
        )
        buttons_frame.pack(pady=20)

        btn_add = ctk.CTkButton(
            buttons_frame,
            text="➕ Agregar Etiqueta",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            width=180,
            command=self.addtags
        )
        btn_add.pack(side="left", padx=10)

        btn_help = ctk.CTkButton(
            buttons_frame,
            text="❔ Guía del Sistema",
            fg_color="#1565C0",
            hover_color="#0D47A1",
            width=180,
            command=self.guia_etiquetas
        )
        btn_help.pack(side="left", padx=10)

    def mostrar_menu_etiqueta(self, etiqueta):
        menu = ctk.CTkToplevel(self)
        menu.overrideredirect(True)
        menu.attributes("-topmost", True)

        menu.configure(fg_color=self.colores[self.tema_actual]["content"])

        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        menu.geometry(f"160x100+{x}+{y}")

        def cerrar_menu():
            menu.destroy()

        def eliminar():
            cerrar_menu()
            confirm = CTkMessagebox(
                title="Confirmar Eliminación",
                message=f"¿Seguro que quieres eliminar la etiqueta '{etiqueta['nombre']}'?",
                icon="warning",
                option_1="Sí",
                option_2="No"
            )

            if confirm.get() == "Sí":
                try:
                    with open("DBetiquetas.json", "r", encoding="utf-8") as f:
                        contenido = f.read().strip()
                        etiquetas = json.loads(contenido) if contenido else []
                except (FileNotFoundError, json.JSONDecodeError):
                    etiquetas = []

                etiquetas = [e for e in etiquetas if e.get("nombre") != etiqueta["nombre"]]

                with open("DBetiquetas.json", "w", encoding="utf-8") as f:
                    json.dump(etiquetas, f, indent=4, ensure_ascii=False)

                CTkMessagebox(
                    title="Etiqueta eliminada",
                    message=f"'{etiqueta['nombre']}' fue eliminada correctamente.",
                    icon="check"
                )
                self.adminetiquetas()  # Refresca la vista

        def editar():
            cerrar_menu()
            self.edittags()

        inner_frame = ctk.CTkFrame(
            menu,
            fg_color=self.colores[self.tema_actual]["content"],
            corner_radius=10
        )
        inner_frame.pack(expand=True, fill="both", padx=5, pady=5)

        ctk.CTkButton(
            inner_frame,
            text="✏️ Editar",
            width=130,
            command=editar,
            fg_color=self.colores[self.tema_actual]["boton"],
            hover_color=self.colores[self.tema_actual]["hover"],
            text_color="white"
        ).pack(pady=4)

        ctk.CTkButton(
            inner_frame,
            text="🗑️ Eliminar",
            width=130,
            command=eliminar,
            fg_color="#C62828",
            hover_color="#B71C1C",
            text_color="white"
        ).pack(pady=4)

        menu.bind("<FocusOut>", lambda e: menu.destroy())
        menu.focus_force()

    def guia_etiquetas(self):
        win = ctk.CTkToplevel(self)
        win.title("Guía del Sistema de Etiquetas")
        win.geometry("500x400")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        win.transient(self)
        win.grab_set()
        win.focus_force()

        win.update_idletasks()
        width = 360
        height = 380
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(win, text="📘 Guía del Sistema de Etiquetas Contables",
                    font=("Helvetica", 17, "bold"), text_color="#0D47A1").pack(pady=15)

        texto = (
            "Las etiquetas contables son categorías que permiten identificar "
            "y aplicar impuestos, tasas o reglas específicas en los diferentes módulos "
            "del sistema (Contabilidad, Inventario y Nómina).\n\n"
            "- Nombre de la Etiqueta:\n"
            "    Es el identificador del impuesto o categoría (ejemplo: IVA, Retención).\n\n"
            "- Taxes (%), o importe ($):\n"
            "    Representa el valor porcentual del impuesto o tasa aplicada.\n\n"
            "- Módulo:\n"
            "    Indica a qué área pertenece la etiqueta (Inventario, Contabilidad o Nómina).\n\n"
            "📌  Estas etiquetas pueden ser usadas posteriormente para cálculos automáticos "
            "en los módulos contables y reportes financieros."
        )

        text_box = ctk.CTkTextbox(win, width=460, height=280, wrap="word")
        text_box.pack(padx=15, pady=5)
        text_box.insert("1.0", texto)
        text_box.configure(state="disabled")

    def addtags(self):
        win = ctk.CTkToplevel(self)
        win.title("Agregar Etiqueta Contable")
        win.geometry("380x340")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        win.transient(self)
        win.grab_set()
        win.focus_force()
        win.update_idletasks()
        width, height = 380, 340
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(win, text="Nueva Etiqueta", font=("Helvetica", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(win, text="Nombre de la Etiqueta:").pack(pady=(10, 0))
        nombre_entry = ctk.CTkEntry(win, width=220)
        nombre_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Parametro ($ o %):").pack(pady=(10, 0))
        taxes_entry = ctk.CTkEntry(win, width=220)
        taxes_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Módulo:").pack(pady=(10, 0))
        modulos = ["Inventario", "Contabilidad", "Nómina"]
        modulo_menu = ctk.CTkOptionMenu(win, values=modulos)
        modulo_menu.pack(pady=5)
        modulo_menu.set("Contabilidad")

        def guardar():
            nombre = nombre_entry.get().strip()
            taxes = taxes_entry.get().strip()
            modulo = modulo_menu.get()

            if not nombre or not taxes:
                CTkMessagebox(
                    title="Campos Vacíos",
                    message="Debes llenar todos los campos.",
                    icon="warning"
                )
                return

            try:
                taxes_val = float(taxes)
            except ValueError:
                CTkMessagebox(
                    title="Error",
                    message="El campo 'Taxes' debe ser un número (puede tener decimales).",
                    icon="warning"
                )
                return

            try:
                with open("DBetiquetas.json", "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    etiquetas = json.loads(contenido) if contenido else []
            except (FileNotFoundError, json.JSONDecodeError):
                etiquetas = []

            etiquetas.append({
                "nombre": nombre,
                "taxes": taxes_val,
                "modulo": modulo
            })

            with open("DBetiquetas.json", "w", encoding="utf-8") as f:
                json.dump(etiquetas, f, indent=4, ensure_ascii=False)

            CTkMessagebox(
                title="Éxito",
                message=f"Etiqueta '{nombre}' agregada correctamente.",
                icon="check"
            )
            win.destroy()
            self.adminetiquetas()

        ctk.CTkButton(
            win,
            text="Guardar",
            command=guardar,
            width=160,
            fg_color="#1976D2"
        ).pack(pady=20)

    def edittags(self):
        try:
            with open("DBetiquetas.json", "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                etiquetas = json.loads(contenido) if contenido else []
        except (FileNotFoundError, json.JSONDecodeError):
            etiquetas = []

        if not etiquetas:
            CTkMessagebox(
                title="Sin Datos",
                message="No hay etiquetas registradas para editar.",
                icon="warning"
            )
            return

        win = ctk.CTkToplevel(self)
        win.title("Editar Etiqueta Contable")
        win.geometry("400x380")
        win.resizable(False, False)
        try:
            win.iconbitmap("ExodusIcon.ico")
        except Exception:
            pass

        win.transient(self)
        win.grab_set()
        win.focus_force()
        win.update_idletasks()

        width, height = 400, 380
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(
            win, text="Selecciona una etiqueta para editar",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        etiquetas_nombres = [e["nombre"] for e in etiquetas]
        etiqueta_menu = ctk.CTkOptionMenu(win, values=etiquetas_nombres)
        etiqueta_menu.pack(pady=10)
        etiqueta_menu.set(etiquetas_nombres[0])

        ctk.CTkLabel(win, text="Nuevo nombre (opcional):").pack(pady=(10, 0))
        nombre_entry = ctk.CTkEntry(win, width=250)
        nombre_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Nuevo Taxes (%):").pack(pady=(10, 0))
        taxes_entry = ctk.CTkEntry(win, width=250)
        taxes_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Nuevo Módulo:").pack(pady=(10, 0))
        modulos = ["Inventario", "Contabilidad", "Nómina"]
        modulo_menu = ctk.CTkOptionMenu(win, values=modulos)
        modulo_menu.pack(pady=5)
        modulo_menu.set("Contabilidad")

        def guardar_cambios():
            seleccion = etiqueta_menu.get()
            nuevo_nombre = nombre_entry.get().strip()
            nuevo_tax = taxes_entry.get().strip()
            nuevo_modulo = modulo_menu.get()

            for e in etiquetas:
                if e["nombre"] == seleccion:
                    if nuevo_nombre:
                        e["nombre"] = nuevo_nombre
                    if nuevo_tax:
                        try:
                            e["taxes"] = float(nuevo_tax)
                        except ValueError:
                            CTkMessagebox(
                                title="Error",
                                message="El campo 'Taxes' debe ser un número (puede tener decimales).",
                                icon="warning"
                            )
                            return
                    e["modulo"] = nuevo_modulo
                    break

            with open("DBetiquetas.json", "w", encoding="utf-8") as f:
                json.dump(etiquetas, f, indent=4, ensure_ascii=False)

            CTkMessagebox(
                title="Éxito",
                message=f"Etiqueta '{seleccion}' actualizada correctamente.",
                icon="check"
            )
            win.destroy()
            self.adminetiquetas()

        ctk.CTkButton(
            win,
            text="💾 Guardar Cambios",
            command=guardar_cambios,
            width=200,
            height=38,
            fg_color="#1976D2",
            hover_color="#0D47A1",
            font=("Helvetica", 14, "bold")
        ).pack(pady=20)

        def deltags(self):
            try:
                with open("DBetiquetas.json", "r", encoding="utf-8") as f:
                    etiquetas = json.load(f)
            except FileNotFoundError:
                etiquetas = []

            if not etiquetas:
                CTkMessagebox(title="Sin Datos",
                            message="No hay etiquetas registradas para eliminar.",
                            icon="warning")
                return

            win = ctk.CTkToplevel(self)
            win.title("Eliminar Etiqueta Contable")
            win.geometry("360x300")
            win.resizable(False, False)
            try:
                win.iconbitmap("ExodusIcon.ico")
            except Exception:
                pass

            win.transient(self)
            win.grab_set()
            win.focus_force()
            win.update_idletasks()
            width, height = 360, 300
            x = (win.winfo_screenwidth() // 2) - (width // 2)
            y = (win.winfo_screenheight() // 2) - (height // 2)
            win.geometry(f"{width}x{height}+{x}+{y}")

            ctk.CTkLabel(win, text="Selecciona una etiqueta para eliminar", font=("Helvetica", 14, "bold")).pack(pady=10)

            etiquetas_nombres = [e["nombre"] for e in etiquetas]
            etiqueta_menu = ctk.CTkOptionMenu(win, values=etiquetas_nombres)
            etiqueta_menu.pack(pady=10)
            etiqueta_menu.set(etiquetas_nombres[0])

        def eliminar():
            seleccion = etiqueta_menu.get()
            confirm = CTkMessagebox(title="Confirmar Eliminación",
                                    message=f"¿Eliminar la etiqueta '{seleccion}'?",
                                    icon="warning", option_1="Sí", option_2="No")

            if confirm.get() == "Sí":
                etiquetas_filtradas = [e for e in etiquetas if e["nombre"] != seleccion]
                with open("DBetiquetas.json", "w", encoding="utf-8") as f:
                    json.dump(etiquetas_filtradas, f, indent=4, ensure_ascii=False)
                CTkMessagebox(title="Éxito", message=f"Etiqueta '{seleccion}' eliminada correctamente.")
                win.destroy()
                self.adminetiquetas()

        ctk.CTkButton(win, text="Eliminar", command=eliminar,
                    fg_color="#C62828", hover_color="#B71C1C", width=160).pack(pady=20)


## Funciones del administrador de etiquetas contables

    def seeloginsusers(self):
        self.clearcontent()
        self.backbutt(self.content)

        ctk.CTkLabel(
            self.content,
            text="Monitoreo de Usuarios",
            font=("Helvetica", 22, "bold"),
            text_color=self.colores[self.tema_actual]["texto_titulo"]
        ).pack(pady=10)

        ctk.CTkLabel(
            self.content,
            text="Aquí se muestran los registros de inicio de sesión (datalogins.json).",
            font=("Helvetica", 13),
            text_color="gray70" if self.tema_actual == "oscuro" else "gray30"
        ).pack(pady=(0, 15))

        try:
            with open("datalogins.json", "r", encoding="utf-8") as f:
                registros = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            registros = []

        if not registros:
            ctk.CTkLabel(
                self.content,
                text="No hay registros de inicio de sesión.",
                font=("Helvetica", 13),
                text_color="gray70" if self.tema_actual == "oscuro" else "gray50"
            ).pack(pady=10)
            return

        table = ctk.CTkScrollableFrame(
            self.content,
            width=700,
            height=400,
            fg_color=self.colores[self.tema_actual]["content"]
        )
        table.pack(pady=10)

        header = ctk.CTkFrame(
            table,
            fg_color=self.colores[self.tema_actual]["sidebar"]
        )
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Usuario",
            text_color="white",
            font=("Helvetica", 13, "bold"),
            width=200,
            anchor="w"
        ).pack(side="left", padx=40, pady=5)

        ctk.CTkLabel(
            header,
            text="Fecha",
            text_color="white",
            font=("Helvetica", 13, "bold"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=40, pady=5)

        ctk.CTkLabel(
            header,
            text="Hora",
            text_color="white",
            font=("Helvetica", 13, "bold"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=40, pady=5)

        for r in registros:
            fila = ctk.CTkFrame(
                table,
                fg_color=self.colores[self.tema_actual]["content"]
            )
            fila.pack(fill="x", pady=1)

            ctk.CTkLabel(
                fila,
                text=r.get("usuario", ""),
                width=200,
                font=("Helvetica", 12),
                anchor="w",
                text_color=self.colores[self.tema_actual]["texto_titulo"]
            ).pack(side="left", padx=40, pady=3)

            ctk.CTkLabel(
                fila,
                text=r.get("fecha", ""),
                width=150,
                font=("Helvetica", 12),
                anchor="w",
                text_color=self.colores[self.tema_actual]["texto_titulo"]
            ).pack(side="left", padx=40, pady=3)

            ctk.CTkLabel(
                fila,
                text=r.get("hora", ""),
                width=150,
                font=("Helvetica", 12),
                anchor="w",
                text_color=self.colores[self.tema_actual]["texto_titulo"]
            ).pack(side="left", padx=40, pady=3)

        def exportar_logins():
            import os
            from datetime import datetime

            if not registros:
                CTkMessagebox(
                    title="Sin registros",
                    message="No hay registros para exportar.",
                    icon="warning"
                )
                return

            carpeta = "LogLogins"
            os.makedirs(carpeta, exist_ok=True)

            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            nombre_archivo = f"LogLogins_{fecha_actual}.txt"
            ruta = os.path.join(carpeta, nombre_archivo)

            with open(ruta, "a", encoding="utf-8") as f:
                if os.stat(ruta).st_size == 0:
                    f.write("REGISTRO DE INICIOS DE SESIÓN - EXODUS CONTABLE\n")
                    f.write("=" * 60 + "\n\n")
                for r in registros:
                    f.write(f"Usuario: {r.get('usuario','')}\n")
                    f.write(f"Fecha:   {r.get('fecha','')}\n")
                    f.write(f"Hora:    {r.get('hora','')}\n")
                    f.write("-" * 40 + "\n")
                f.write(f"\nExportación realizada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")

            with open("datalogins.json", "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

            CTkMessagebox(
                title="Exportación completa",
                message=f"Los registros se exportaron correctamente a:\n{ruta}\n\nEl historial ha sido limpiado.",
                icon="check"
            )

            self.seeloginsusers()

        buttons_frame = ctk.CTkFrame(
            self.content,
            fg_color=self.colores[self.tema_actual]["content"]
        )
        buttons_frame.pack(pady=20)

        ctk.CTkButton(
            buttons_frame,
            text="📤 Exportar registros y limpiar historial",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            width=320,
            height=40,
            font=("Helvetica", 14, "bold"),
            command=exportar_logins
        ).pack()

    def logout(self):
        self.destroy()
        subprocess.Popen([sys.executable, "Exodus_Login.py"])

    def exit(self):
        self.destroy()

def verificar_archivos_base():

    archivos = {
        "DBusuarios.json": [
            {
                "usuario": "adminis",
                "contraseña": "1234",
                "rol": "Administrador"
            }
        ],
        "DBetiquetas.json": [],
        "datalogins.json": [],
        "acountingdb.json": [],
        "inventorydb.json": [],
        "workersdb.json": [],
        "config.json": {
            "recordar_credenciales": True,
            "usuario": "",
            "clave": ""
        }
    }

    for nombre, contenido in archivos.items():
        if not os.path.exists(nombre):
            try:
                with open(nombre, "w", encoding="utf-8") as f:
                    json.dump(contenido, f, indent=4, ensure_ascii=False)
                print(f"Archivo creado: {nombre}")
            except Exception as e:
                print(f"Error al crear {nombre}: {e}")
        else:
            print(f"Archivo existente: {nombre}")


# Final por el momento (Faltan los modulos) Anoten grupo

if __name__ == "__main__":
    verificar_archivos_base()
    rol = sys.argv[1] if len(sys.argv) > 1 else "Operario"
    app = ExodusMain(rol)
    app.mainloop()
