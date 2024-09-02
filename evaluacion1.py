import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
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
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
ventana = ctk.CTk()
ventana.title("Gestión de Ingredientes y Pedidos")
ventana.geometry("900x700")
tabview = ctk.CTkTabview(ventana)
tabview.pack(fill="both", expand=True)
tab_ingredientes = tabview.add("Ingreso de Ingredientes")
tab_pedido = tabview.add("Pedido")
frame_formulario = ctk.CTkFrame(tab_ingredientes)
frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frame_treeview = ctk.CTkFrame(tab_ingredientes)
frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)
label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
label_nombre.pack(pady=5)
entrada_nombre = ctk.CTkEntry(frame_formulario)
entrada_nombre.pack(pady=5)
label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
label_cantidad.pack(pady=5)
entrada_cantidad = ctk.CTkEntry(frame_formulario)
entrada_cantidad.pack(pady=5)
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
boton_agregar.pack(pady=10)
boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=eliminar_ingrediente)
boton_eliminar.pack(pady=10)
boton_generar_menu = ctk.CTkButton(tab_ingredientes, text="Generar Menú")
boton_generar_menu.pack(side="bottom", pady=20)
# Código de la pestaña "Pedido" (por implementar)
# Aquí es donde implementarías la funcionalidad de los menús, la gestión del pedido, y la generación de la boleta.
ventana.mainloop()