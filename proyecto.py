import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

class Stock:
    def __init__(self):
        self.ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        for ingr in self.ingredientes:
            if ingr.nombre == ingrediente.nombre:
                ingr.cantidad += ingrediente.cantidad
                return
        self.ingredientes.append(ingrediente)

    def eliminar_ingrediente(self, nombre_ingrediente):
        for ingrediente in self.ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                self.ingredientes.remove(ingrediente)
                return True
        return False

    def listar_ingredientes(self):
        return self.ingredientes

class Pedido:
    def __init__(self):
        self.menus = []

    def agregar_menu(self, menu):
        self.menus.append(menu)

    def listar_menus(self):
        return self.menus

    def calcular_total(self):
        return sum(menu['precio'] for menu in self.menus)

def seleccionar_imagen(ruta):
    imagen = Image.open(ruta)
    imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(imagen)

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

ventana = ctk.CTk()
ventana.title("Gestión de Ingredientes y Pedidos")
ventana.geometry("900x700")


tabview = ctk.CTkTabview(ventana)
tabview.pack(fill="both", expand=True, padx=20, pady=20)


tab_ingredientes = tabview.add("Ingreso de Ingredientes")
tab_pedido = tabview.add("Pedido")


frame_formulario = ctk.CTkFrame(tab_ingredientes, corner_radius=15)
frame_formulario.pack(side="left", fill="both", expand=True, padx=20, pady=20)

frame_treeview = ctk.CTkFrame(tab_ingredientes, corner_radius=15)
frame_treeview.pack(side="right", fill="both", expand=True, padx=20, pady=20)

label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:", font=("Arial", 16))
label_nombre.pack(pady=10)

entrada_nombre = ctk.CTkEntry(frame_formulario, font=("Arial", 14))
entrada_nombre.pack(pady=10)

label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:", font=("Arial", 16))
label_cantidad.pack(pady=10)

entrada_cantidad = ctk.CTkEntry(frame_formulario, font=("Arial", 14))
entrada_cantidad.pack(pady=10)

stock = Stock()

def agregar_ingrediente():
    nombre = entrada_nombre.get().strip()
    cantidad = entrada_cantidad.get().strip()
    if not nombre or not cantidad:
        CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="warning")
        return
    if not validar_nombre(nombre):
        CTkMessagebox(title="Error", message="El nombre del ingrediente debe contener solo letras y espacios.", icon="warning")
        return
    if not validar_cantidad(cantidad):
        CTkMessagebox(title="Error", message="La cantidad debe ser un número entero positivo.", icon="warning")
        return
    nuevo_ingrediente = Ingrediente(nombre, int(cantidad))
    stock.agregar_ingrediente(nuevo_ingrediente)
    actualizar_treeview()
    limpiar_entradas()

def eliminar_ingrediente():
    seleccion = treeview.selection()
    if not seleccion:
        CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
        return
    item = treeview.item(seleccion)
    nombre = item['values'][0]
    if stock.eliminar_ingrediente(nombre):
        actualizar_treeview()
    else:
        CTkMessagebox(title="Error", message="El ingrediente no se encontró en el stock.", icon="warning")
    limpiar_entradas()

def actualizar_treeview():
    for item in treeview.get_children():
        treeview.delete(item)
    for ingrediente in stock.listar_ingredientes():
        treeview.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

def limpiar_entradas():
    entrada_nombre.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)

def validar_nombre(nombre):
    return nombre.replace(" ", "").isalpha()

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0


treeview = ttk.Treeview(frame_treeview, columns=("nombre", "cantidad"), show="headings", height=20)
treeview.column("nombre", anchor=tk.W, width=250)
treeview.column("cantidad", anchor=tk.W, width=150)
treeview.heading("nombre", text="Nombre del Ingrediente")
treeview.heading("cantidad", text="Cantidad")
treeview.pack(expand=True, fill="both", padx=10, pady=10)


boton_agregar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente", command=agregar_ingrediente)
boton_agregar.pack(pady=15)

boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=eliminar_ingrediente)
boton_eliminar.pack(pady=15)

boton_generar_menu = ctk.CTkButton(tab_ingredientes, text="Generar Menú")
boton_generar_menu.pack(side="bottom", pady=20)


frame_opciones = ctk.CTkFrame(tab_pedido, corner_radius=15)
frame_opciones.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.4)

frame_precios = ctk.CTkFrame(tab_pedido, corner_radius=15)
frame_precios.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.35)

pedido = Pedido()


imagenes = [
    seleccionar_imagen("icono_cola_64x64.png"),
    seleccionar_imagen("icono_hamburguesa_negra_64x64.png"),
    seleccionar_imagen("icono_papas_fritas_64x64.png"),
    seleccionar_imagen("icono_hotdog_sin_texto_64x64.png")
]



def agregar_menu_seleccionado(imagen, nombre, precio):
    nuevo_menu = {'imagen': imagen, 'nombre': nombre, 'precio': precio}
    pedido.agregar_menu(nuevo_menu)
    actualizar_precios()

def actualizar_precios():
    for item in treeview_precios.get_children():
        treeview_precios.delete(item)
    for menu in pedido.listar_menus():
        treeview_precios.insert("", "end", values=(menu['nombre'], f"${menu['precio']:.2f}"))

# Treeview para mostrar los precios en la parte inferior
treeview_precios = ttk.Treeview(frame_precios, columns=("menu", "cantidad", "precio"), show="headings", height=8)
treeview_precios.column("menu", anchor=tk.W, width=200)
treeview_precios.column("cantidad", anchor=tk.W, width=100)
treeview_precios.column("precio", anchor=tk.W, width=100)
treeview_precios.heading("menu", text="Nombre del Menú")
treeview_precios.heading("cantidad", text="Cantidad")
treeview_precios.heading("precio", text="Precio Unitario")
treeview_precios.pack(expand=True, fill="both", padx=10, pady=10)

for i, imagen in enumerate(imagenes):
    nombre_menu = ["Papas Fritas", "Completo", "Pepsi", "Hamburguesa"][i]
    precio_menu = (i+1) * 10
    boton_menu = ctk.CTkButton(
        frame_opciones, 
        text=nombre_menu, 
        image=imagen, 
        compound="top", 
        font=("Arial", 14), 
        command=lambda img=imagen, nom=nombre_menu, pre=precio_menu: agregar_menu_seleccionado(img, nom, pre))
    boton_menu.grid(row=i//2, column=i%2, padx=10, pady=10)

frame_total = ctk.CTkFrame(tab_pedido)
frame_total.place(relx=0.55, rely=0.35, relwidth=0.4, relheight=0.1)

label_total = ctk.CTkLabel(frame_total, text="Total: $0.00", font=("Arial", 16))
label_total.pack(side="left", padx=20, pady=10)


def actualizar_precios():
    total = 0
    for item in treeview_precios.get_children():
        treeview_precios.delete(item)
    for menu in pedido.listar_menus():
        treeview_precios.insert("", "end", values=(menu['nombre'], f"${menu['precio']:.2f}"))
        total += menu['precio']
    label_total.configure(text=f"Total: ${total:.2f}")


ventana.mainloop()
