import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

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

# Ajustes de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Gestión de Ingredientes y Pedidos")
ventana.geometry("900x700")


tabview = ctk.CTkTabview(ventana)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

# Pestaña de Pedido
tab_pedido = tabview.add("Pedido")


tab_ingredientes = tabview.add("Ingreso de Ingredientes")

frame_ingredientes = ctk.CTkFrame(tab_ingredientes, corner_radius=15)
frame_ingredientes.pack(fill="both", expand=True, padx=20, pady=20)

label_nombre_ingrediente = ctk.CTkLabel(frame_ingredientes, text="Nombre del Ingrediente:", font=("Arial", 14))
label_nombre_ingrediente.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_nombre_ingrediente = ctk.CTkEntry(frame_ingredientes)
entry_nombre_ingrediente.grid(row=0, column=1, padx=10, pady=10)

label_cantidad_ingrediente = ctk.CTkLabel(frame_ingredientes, text="Cantidad:", font=("Arial", 14))
label_cantidad_ingrediente.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_cantidad_ingrediente = ctk.CTkEntry(frame_ingredientes)
entry_cantidad_ingrediente.grid(row=1, column=1, padx=10, pady=10)

def agregar_ingrediente():
    nombre = entry_nombre_ingrediente.get()
    cantidad = entry_cantidad_ingrediente.get()
    if nombre and cantidad:
        lista_ingredientes.insert("", "end", values=(nombre, cantidad))
        entry_nombre_ingrediente.delete(0, tk.END)
        entry_cantidad_ingrediente.delete(0, tk.END)

boton_agregar_ingrediente = ctk.CTkButton(frame_ingredientes, text="Agregar Ingrediente", command=agregar_ingrediente)
boton_agregar_ingrediente.grid(row=2, column=0, columnspan=2, padx=10, pady=20)


lista_ingredientes = ttk.Treeview(frame_ingredientes, columns=("nombre", "cantidad"), show="headings", height=8)
lista_ingredientes.column("nombre", anchor=tk.W, width=200)
lista_ingredientes.column("cantidad", anchor=tk.W, width=100)
lista_ingredientes.heading("nombre", text="Nombre del Ingrediente")
lista_ingredientes.heading("cantidad", text="Cantidad")
lista_ingredientes.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


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


treeview_precios = ttk.Treeview(frame_precios, columns=("menu", "cantidad", "precio"), show="headings", height=8)
treeview_precios.column("menu", anchor=tk.W, width=200)
treeview_precios.column("cantidad", anchor=tk.W, width=100)
treeview_precios.column("precio", anchor=tk.W, width=100)
treeview_precios.heading("menu", text="Nombre del Menú")
treeview_precios.heading("cantidad", text="Cantidad")
treeview_precios.heading("precio", text="Precio Unitario")
treeview_precios.pack(expand=True, fill="both", padx=10, pady=10)

def agregar_menu_seleccionado(imagen, nombre, precio):
    nuevo_menu = {'imagen': imagen, 'nombre': nombre, 'precio': precio}
    pedido.agregar_menu(nuevo_menu)
    actualizar_precios()

def actualizar_precios():
    for item in treeview_precios.get_children():
        treeview_precios.delete(item)
    for menu in pedido.listar_menus():
        treeview_precios.insert("", "end", values=(menu['nombre'], 1, f"${menu['precio']:.2f}"))
    actualizar_total()


frame_total = ctk.CTkFrame(tab_pedido)
frame_total.place(relx=0.55, rely=0.35, relwidth=0.4, relheight=0.1)

label_total = ctk.CTkLabel(frame_total, text="Total: $0.00", font=("Arial", 16))
label_total.pack(side="left", padx=20, pady=10)

boton_eliminar = ctk.CTkButton(frame_total, text="Eliminar Menú", fg_color="black", text_color="white", command=lambda: print("Eliminar menú"))
boton_eliminar.pack(side="right", padx=20, pady=10)

def actualizar_total():
    total = pedido.calcular_total()
    label_total.configure(text=f"Total: ${total:.2f}")


boton_generar_boleta = ctk.CTkButton(tab_pedido, text="Generar Boleta", font=("Arial", 14))
boton_generar_boleta.place(relx=0.4, rely=0.88, relwidth=0.2, relheight=0.07)

ventana.mainloop()