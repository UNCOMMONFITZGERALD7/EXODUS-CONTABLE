#Exodus Login 1.0

import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import subprocess, sys, os, time, json
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

exodus = ctk.CTk()
ctk.set_widget_scaling(1.2)
exodus.title("Exodus Contable Pre-Alpha")
exodus.geometry("400x600")
ctk.set_appearance_mode("Dark")
exodus.iconbitmap("iconexodark.ico")
ancho = 400
alto = 600
pant_ancho = exodus.winfo_screenwidth()
pant_alto = exodus.winfo_screenheight()
x = int((pant_ancho / 2) - (ancho / 2))
y = int((pant_alto / 2) - (alto / 2))
exodus.geometry(f"{ancho}x{alto}+{x}+{y}")

imagen_fondo = ctk.CTkImage(
    light_image=Image.open("soporte_icon.png"),
    dark_image=Image.open("soporte_icon.png"),
    size=(20, 20)
)

imagen_logobg = Image.open("BG_Logo_Ex.png").convert("RGBA")

alpha = 0.25  # valores entre 0.1 y 1.0 — 0.4 da una transparencia elegante
r, g, b, a = imagen_logobg.split()
a = a.point(lambda p: p * alpha)
img_fondo = Image.merge("RGBA", (r, g, b, a))

fondologobg_ctk = ctk.CTkImage(
    light_image=img_fondo,
    dark_image=img_fondo,
    size=(250, 250)
)

label_fondo = ctk.CTkLabel(exodus, image=fondologobg_ctk, text="")
label_fondo.place(relx=0.5, y=150, anchor="center")
label_fondo.lower()

# Database (Usamos archivos .json)

dbusuarios = "DBusuarios.json"

def creararusuarios():
    if not os.path.exists(dbusuarios):
        usuario_inicial = [{
            "usuario": "adminis",
            "contraseña": "1234",
            "rol": "Administrador"
        }]
        with open(dbusuarios, "w", encoding="utf-8") as f:
            json.dump(usuario_inicial, f, indent=4)

def leeratusuarios():
    creararusuarios()
    with open(dbusuarios, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
    return usuarios

def mostrar_error_login():
    CTkMessagebox(
        title="Error de autenticación",
        message="Usuario o contraseña incorrectos.",
        icon="cancel"  # Puedes usar: "info", "warning", "cancel", "question"
    )

def verificarlogdb():
    usuarios = leeratusuarios()
    usuario = Dato_nom.get()
    contraseña = Dato_pas.get()

    for u in usuarios:
        if u["usuario"] == usuario and u["contraseña"] == contraseña:
            timestamp_login(u["usuario"])
            print(f"¡Usuario autenticado!: {u['usuario']} ({u['rol']})")
            timestamp_login(usuario)
            exodus.destroy()
            subprocess.Popen([sys.executable, "Exodus_Main.py", u["rol"]])
            return
    mostrar_error_login()
    print("¡Usuario o contraseña incorrectos!")

#Fondo

bglogin = ctk.CTkFrame(exodus, width=500, height=400, fg_color="#1E1E2E", corner_radius=15, bg_color="transparent")
bglogin1 = ctk.CTkFrame(bglogin, width=280, height=380, fg_color="#2A2A3D", corner_radius=10, bg_color="transparent")

#Entrada de Datos 

credenciales = {"usuario": "", "contraseña": ""}

def limpiar_uguia(event):
    if Dato_nom.get() == "Ingrese su usuario":
        Dato_nom.delete(0, ctk.END)

def restaurar_uguia(event):
    if Dato_nom.get() == "":
        Dato_nom.insert(0, "Ingrese su usuario")

def limpiar_pguia(event):
    if Dato_pas.get() == "Ingrese su contraseña":
        Dato_pas.delete(0, ctk.END)
        Dato_pas.config(show="*")

def restaurar_pguia(event):
    if Dato_pas.get() == "":
        Dato_pas.insert(0, "Ingrese su contraseña")
        Dato_pas.config(show="")

def ojoabiertopas(event):
    Dato_pas.config(show="")

def ojocerradopas(event):
    if Dato_pas.get() not in ("", "Ingrese su contraseña"):
        Dato_pas.config(show="*")

def keepinventory():
    credenciales["usuario"] = Dato_nom.get()
    credenciales["contraseña"] = Dato_pas.get()
    print("Credenciales guardadas", credenciales)

def timestamp_login(usuario):
    archivo_log = "datalogins.json"
    now = datetime.now()
    registro = {
        "usuario": usuario,  # o como se llame tu variable de usuario actual
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S")
    }

    try:
        with open("datalogins.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []

    datos.append(registro)

    with open("datalogins.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

    print(f"[LOG] Se registró el inicio de sesión de {usuario} a las {now.strftime('%Y-%m-%d %H:%M:%S')}")

Dato_nom = ctk.CTkEntry(bglogin1, placeholder_text="Ingrese su usuario", width=200)

Dato_pas = ctk.CTkEntry(bglogin1, placeholder_text="Ingrese su contraseña", show="*", width=200)

Dato_nom.bind("<Return>", lambda event: verificarlogdb())
Dato_pas.bind("<Return>", lambda event: verificarlogdb())

#Recordar Usuario

vcontrol = ctk.BooleanVar(value=False)

configurjs = "config.json"

def guardarcredenciales():
    usuario = Dato_nom.get()
    contraseña = Dato_pas.get()
    reccredenciales = bool(vcontrol.get())
    saveconfig(usuario, contraseña, reccredenciales)
    print("Configuración actualizada.", usuario, contraseña, reccredenciales)

def readconfig():
    if not os.path.exists(configurjs):
        with open(configurjs, "w") as f:
            json.dump({"recordar_credenciales": False, "usuario": "", "clave": ""}, f, indent=4)
    with open(configurjs, "r") as f:
        return json.load(f)

def saveconfig(usuario, contraseña, reccredenciales):
    with open(configurjs, "w") as f:
        json.dump({
            "recordar_credenciales": reccredenciales,
            "usuario": usuario if reccredenciales else "",
            "clave": contraseña if reccredenciales else ""
        }, f, indent=4)

def addconfig():
    config = readconfig()
    if config["recordar_credenciales"]:
        Dato_nom.delete(0, ctk.END)
        Dato_nom.insert(0, config["usuario"])
        Dato_pas.delete(0, ctk.END)
        Dato_pas.insert(0, config["clave"])
        Dato_pas.configure(show="*")
        vcontrol.set(1)

reminduser = ctk.CTkCheckBox(bglogin1, text="Recordar credenciales", variable=vcontrol, command=guardarcredenciales,
                             font=("Helvetica", 10, "bold"), text_color="white")

addconfig()
 
#ayuda ¿? HAY QUE COLOCAR UNA AYUDA ADECUADA, sugieran grupo
from tkinter import messagebox

def helpie():
    messagebox.showinfo("¿No puedes entrar?", "Si no puedes entrar a tu espacio,\ncomunicate con el administrador\nde tu empresa para solucionar\nel problema.")
buttonhelp = ctk.CTkButton(
    exodus,
    width=15,
    height=26,
    text="Información",
    fg_color="#3B3B4D",
    hover_color="dodgerblue2",
    command=helpie,
    font=("Helvetica", 11, "bold"),
    bg_color="transparent",
    corner_radius=10, 
    text_color="white"
)
buttonhelp.place(x=25, y=25)

bTlogin = ctk.CTkButton(
    bglogin1,
    text="Iniciar Sesión",
    fg_color="#0A84FF",
    hover_color="skyblue3",
    text_color="black",
    font=("Helvetica", 12, "bold"),
    corner_radius=8,
    command=verificarlogdb
)

def supportchat():
    messagebox.showinfo("Contactenos", "Si tiene problemas o inquietudes comuniquese al siguiente correo:\njperezbnegocios@gmail.com")

buttonsupport = ctk.CTkButton(exodus, text="", bg_color="transparent", width=20, height=20, image=imagen_fondo, compound="left", fg_color="#3B3B4D", hover_color="dodgerblue2", command=supportchat)
buttonsupport.place(x=115, y=25)

bTexit = ctk.CTkButton(
    bglogin1,
    text="Salir",
    fg_color="#3B3B4D",
    hover_color="gray30",
    text_color="white",
    font=("Helvetica", 12, "bold"),
    corner_radius=8,
    command=exodus.destroy
)

#Labels (Etiquetas)

conteXT = ctk.CTkLabel(
    bglogin1,
    text="¡Bienvenido a Exodus Contable!\n",
    text_color="white",
    font=("Helvetica", 16, "bold")
)

conteXT2 = ctk.CTkLabel(
    bglogin1,
    text="Inicia sesión para continuar",
    text_color="lightgray",
    font=("Helvetica", 11, "bold")
)

#Reloj - lO USARÉ PARA HACER LOS TIME STAMP DE INICIOS DE SESION, COMO UN HISTORIAL.

FondoReloj = ctk.CTkLabel(exodus, text="00:00:00", text_color="white", font=("Helvetica", 12, "bold"))

def funcionamientoreloj():
    FondoReloj.configure(text=time.strftime("%H:%M:%S"))
    exodus.after(1000, funcionamientoreloj)

funcionamientoreloj()

##################################################################################
##################################################################################

#fondos
bglogin.place(relx=0.5, rely=0.5, anchor="center")
bglogin1.pack()
#Titulo 1
conteXT.pack(pady= 5, padx= 10)
conteXT2.pack()
#Entrada de datos 1
Dato_nom.pack(pady=5)
Dato_pas.pack(pady=3)
reminduser.pack(pady=3)
#Textos y botones 2
bTlogin.pack(pady=5)
bTexit.pack(pady= 5)
#Cosmeticos
FondoReloj.place(relx= 0.45, y= 600)

exodus.mainloop()