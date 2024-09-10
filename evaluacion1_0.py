# falta : arglar pdf ya que no c parecen al del video y el tema de los iconos ademas de lo del boton de generar menu
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from fpdf import FPDF
from customtkinter import CTkImage
from PIL import Image
from datetime import datetime

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

    def hay_ingredientes(self):
        return len(self.ingredientes) > 0

class Pedido:
    def __init__(self):
        self.menus = []

    def agregar_menu(self, menu):
        self.menus.append(menu)

    def listar_menus(self):
        return self.menus

    def eliminar_todos_los_menus(self):
        self.menus = []

    def calcular_total(self):
        total = sum(menu['precio'] * menu['cantidad'] for menu in self.menus)
        return total

def seleccionar_imagen(ruta):
    imagen = Image.open(ruta)
    imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(imagen)

def generar_boleta():
    if not pedido.listar_menus():
        CTkMessagebox(title="Error", message="No hay menús en el pedido para generar una boleta.", icon="warning")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    

    # Información del restaurante
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Nombre del Restaurante: Mi Restaurante", ln=True)
    pdf.cell(0, 10, txt="Razón Social: Restaurante S.A.", ln=True)
    pdf.cell(0, 10, txt="RUT: 12345678-9", ln=True)
    pdf.cell(0, 10, txt="Dirección: Calle Falsa 123", ln=True)
    pdf.cell(0, 10, txt="Teléfono: +56 9 1234 5678", ln=True)
    pdf.ln(10)  # Espacio entre la información del restaurante y el contenido de la boleta

    # Fecha
    pdf.set_font("Arial", size=10)
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 10, txt=f"Fecha: {fecha_actual}", ln=True, align='R')
    pdf.ln(10)  # Espacio entre la fecha y la tabla de artículos



    # Título
    pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align='C')
    pdf.ln(10)



    # Agregar detalles del pedido
    total_sin_iva = 0
    pdf.cell(100, 10, txt="Nombre del Menú", border=1, align='C')
    pdf.cell(30, 10, txt="Cantidad", border=1, align='C')
    pdf.cell(30, 10, txt="Precio Unitario", border=1, align='C')
    pdf.cell(30, 10, txt="Total", border=1, ln=True, align='C')

    for menu in pedido.listar_menus():
        cantidad = menu['cantidad']
        precio_unitario = menu['precio']
        total_item = cantidad * precio_unitario
        total_sin_iva += total_item

        pdf.cell(100, 10, txt=menu['nombre'], border=1)
        pdf.cell(30, 10, txt=str(cantidad), border=1, align='C')
        pdf.cell(30, 10, txt=f"${precio_unitario:.0f}", border=1, align='C')
        pdf.cell(30, 10, txt=f"${total_item:.0f}", border=1, ln=True, align='C')

    # Calcular IVA (19%)
    iva = total_sin_iva * 0.19
    total_con_iva = total_sin_iva + iva

    # Total sin IVA
    pdf.ln(10)
    pdf.cell(160, 10, txt="Subtotal:", border=1)
    pdf.cell(30, 10, txt=f"${total_sin_iva:.0f}", border=1, ln=True, align='C')

    # IVA
    pdf.cell(160, 10, txt="IVA (19%):", border=1)
    pdf.cell(30, 10, txt=f"${iva:.0f}", border=1, ln=True, align='C')

    # Total con IVA
    pdf.cell(160, 10, txt="Total:", border=1)
    pdf.cell(30, 10, txt=f"${total_con_iva:.0f}", border=1, ln=True, align='C')

    # Guardar PDF
    pdf_output = "boleta_pedido.pdf"
    pdf.output(pdf_output)

    CTkMessagebox(title="Éxito", message=f"Boleta generada exitosamente y guardada como {pdf_output}.", icon="check")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Gestión de Ingredientes y Pedidos")
ventana.geometry("900x700")

tabview = ctk.CTkTabview(ventana)
tabview.pack(fill="both", expand=True)

# Pestaña de Ingredientes
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
        CTkMessagebox(title="Error", message="El nombre debe contener solo letras y espacios.", icon="warning")
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

def generar_menu():
    tabview.set("Pedido")  # Cambia a la pestaña de Pedido
    actualizar_precios()  # Actualiza la tabla de precios cuando se cambie de pestaña
    actualizar_total()  # Asegúrate de que el total también se actualice

boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=eliminar_ingrediente)
boton_eliminar.pack(pady=10)

treeview = ttk.Treeview(frame_treeview, columns=("nombre", "cantidad"), show="headings", height=20)
treeview.column("nombre", anchor=tk.W, width=250)
treeview.column("cantidad", anchor=tk.W, width=150)
treeview.heading("nombre", text="Nombre del Ingrediente")
treeview.heading("cantidad", text="Cantidad")
treeview.pack(expand=True, fill="both", padx=10, pady=10)

boton_agregar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente", command=agregar_ingrediente)
boton_agregar.pack(pady=10)

boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", command=generar_menu)
boton_generar_menu.pack(side="bottom", pady=20)

# Pestaña de Pedido
frame_opciones = ctk.CTkFrame(tab_pedido)
frame_opciones.pack(side="top", fill="x", padx=10, pady=10)

frame_precios = ctk.CTkFrame(tab_pedido)
frame_precios.pack(side="bottom", fill="both", padx=10, pady=10)

pedido = Pedido()

# Seleccionar imágenes
imagenes = [
    seleccionar_imagen("icono_cola_64x64.png"),
    seleccionar_imagen("icono_hamburguesa_negra_64x64.png"),
    seleccionar_imagen("icono_papas_fritas_64x64.png"),
    seleccionar_imagen("icono_hotdog_sin_texto_64x64.png")
]


# Ingredientes necesarios para cada menú
ingredientes_necesarios = {
    "Hamburguesa": {"pan": 1, "queso": 1, "churrasco": 1},
    "Papas Fritas": {"papas": 5},
    "Completo": {"pan": 1, "vienesa": 1, "tomate": 1, "palta": 1},
    "Pepsi": {"bebida": 1}
}

def agregar_menu_seleccionado(imagen, nombre, precio):
    if not stock.hay_ingredientes():
        CTkMessagebox(title="Error", message="No hay ingredientes en stock. No se puede hacer el pedido.", icon="warning")
        return

    disponible, faltantes = verificar_y_descontar_ingredientes(nombre)
    if not disponible:
        CTkMessagebox(title="Error", message=f"Faltan los siguientes ingredientes para {nombre}: {faltantes}", icon="warning")
        return

    for menu in pedido.menus:
        if menu['nombre'] == nombre:
            menu['cantidad'] += 1
            actualizar_precios()
            return

    nuevo_menu = {'imagen': imagen, 'nombre': nombre, 'precio': precio, 'cantidad': 1}
    pedido.agregar_menu(nuevo_menu)
    actualizar_precios()

# Función para verificar si hay suficientes ingredientes
# Modificar la función para verificar y descontar ingredientes
def verificar_y_descontar_ingredientes(menu):
    if menu not in ingredientes_necesarios:
        return True, ""
    
    ingredientes_faltantes = []
    
    # Verificar si hay suficientes ingredientes
    for ingrediente, cantidad_necesaria in ingredientes_necesarios[menu].items():
        for stock_ingrediente in stock.ingredientes:
            if stock_ingrediente.nombre == ingrediente:
                if stock_ingrediente.cantidad >= cantidad_necesaria:
                    break
                else:
                    ingredientes_faltantes.append(ingrediente)
        else:
            ingredientes_faltantes.append(ingrediente)

    if ingredientes_faltantes:
        return False, ", ".join(ingredientes_faltantes)
    
    # Si hay suficientes ingredientes, se descuentan del stock
    for ingrediente, cantidad_necesaria in ingredientes_necesarios[menu].items():
        for stock_ingrediente in stock.ingredientes:
            if stock_ingrediente.nombre == ingrediente:
                stock_ingrediente.cantidad -= cantidad_necesaria
                break

    return True, ""

def cambiar_color_fondo(event):
    boton = event.widget
    boton.configure(fg_color="blue")

def restaurar_color_fondo(event):
    boton = event.widget
    boton.configure(fg_color="green")

# Los botones y las imágenes de los menús ya están definidos
for i, imagen in enumerate(imagenes):
    nombre_menu = ["Pepsi", "Hamburguesa", "Papas Fritas", "Completo"][i]
    
    # Asignar los precios correctos
    if nombre_menu == "Pepsi":
        pre_menu = 1100
    elif nombre_menu == "Hamburguesa":
        pre_menu = 3500
    elif nombre_menu == "Papas Fritas":
        pre_menu = 500
    elif nombre_menu == "Completo":
        pre_menu = 1800

    boton_menu = ctk.CTkButton(
        frame_opciones, 
        text=nombre_menu, 
        image=imagen, 
        compound="top", 
        font=("Arial", 12), 
        fg_color="#2B2B2B",  # Color de fondo inicial
        border_width=2,  # Ancho del borde
        border_color="green", 
        command=lambda img=imagen, nom=nombre_menu, pre=pre_menu: agregar_menu_seleccionado(img, nom, pre)
    )
    
    boton_menu.bind("<ButtonPress-1>", cambiar_color_fondo)
    boton_menu.bind("<ButtonRelease-1>", restaurar_color_fondo)
    
    boton_menu.grid(row=i//2, column=i%2, padx=10, pady=10)



treeview_precios = ttk.Treeview(frame_precios, columns=("menu", "cantidad", "precio"), show="headings", height=8)
treeview_precios.column("menu", anchor=tk.W, width=200)
treeview_precios.column("cantidad", anchor=tk.W, width=100)
treeview_precios.column("precio", anchor=tk.W, width=100)
treeview_precios.heading("menu", text="Nombre del Menú")
treeview_precios.heading("cantidad", text="Cantidad")
treeview_precios.heading("precio", text="Precio Unitario")
treeview_precios.pack(expand=True, fill="both", padx=10, pady=10)

# Actualiza la tabla de precios para reflejar las cantidades acumuladas
def actualizar_precios():
    # Limpiar el treeview antes de insertar nuevos valores
    for item in treeview_precios.get_children():
        treeview_precios.delete(item)
    
    # Insertar los menús con su nombre, cantidad y precio
    for menu in pedido.listar_menus():
        treeview_precios.insert("", "end", values=(menu['nombre'], menu['cantidad'], f"${menu['precio']:.0f}"))
    
    # Actualizar el total
    actualizar_total()




# Calcular el total multiplicando el precio por la cantidad
def actualizar_total():
    total = pedido.calcular_total()
    label_total.configure(text=f"Total: ${total:.0f}")

# Funcion para eliminar todos los menús y reiniciar la interfaz
def eliminar_todos_los_menus_y_reiniciar():
    pedido.eliminar_todos_los_menus()
      # Eliminar todos los menús
    actualizar_precios()  # Actualizar la tabla de precios
    actualizar_total()  # Reiniciar el total a $0

# Boton para eliminar todos los menús
frame_total = ctk.CTkFrame(tab_pedido)
frame_total.place(relx=0.55, rely=0.35, relwidth=0.4, relheight=0.1)

label_total = ctk.CTkLabel(frame_total, text="Total: $0", font=("Arial", 16))
label_total.pack(side="right", padx=0, pady=10)

boton_eliminar = ctk.CTkButton(frame_total, text="Eliminar Menú", fg_color="black", text_color="white", command=eliminar_todos_los_menus_y_reiniciar)
boton_eliminar.pack(side="right", padx=20, pady=10)

# Agregar botón para generar boleta
boton_generar_boleta = ctk.CTkButton(frame_total, text="Generar Boleta", fg_color="black", text_color="white", command=generar_boleta)
boton_generar_boleta.pack(side="right", padx=0, pady=10)



ventana.mainloop()
