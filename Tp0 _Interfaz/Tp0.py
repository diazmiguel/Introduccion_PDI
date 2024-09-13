import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import imageio
import numpy as np
import matplotlib.pyplot as plt

# Crear ventana principal
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("IPDI")

ventana.config(bg="#1dd767") 

# Crear espacios para las imágenes
canvas1 = tk.Canvas(ventana, width=300, height=300, bg="lightgray")
canvas1.place(x=50, y=50)  # Cuadrado izquierdo

canvas2 = tk.Canvas(ventana, width=300, height=300, bg="lightgray")
canvas2.place(x=450, y=50)  # Cuadrado derecho

# Variables para guardar las imágenes
imagen_inicio = None # imagen que mostrara al principio
imagen_final = None # imagen que mostrara al final
imagen = None #imagen con la que trabajaremos

#FUNCIONES PARA TRABAJAR CON ELLAS
def rgb2yiq(imagen):
    imagen = np.clip(imagen /255.,0.,1.) #Normalizamos los valores
    yiq= np.zeros(imagen.shape)
    yiq[:,:,0] = np.clip(0.299 * imagen[:,:,0] + 0.587 * imagen[:,:,1] + 0.114 * imagen[:,:,2], 0., 1.)
    yiq[:,:,1] = np.clip(0.595716 * imagen[:,:,0] - 0.274453 * imagen[:,:,1] - 0.321263 * imagen[:,:,2], -0.5957, 0.5957)
    yiq[:,:,2] = np.clip(0.211456 * imagen[:,:,0] - 0.522591 * imagen[:,:,1] + 0.311135 * imagen[:,:,2], -0.5226, 0.5226)
    return yiq 

def yiq2rgb(imagen):
    imagen = np.clip(imagen /255.,0.,1.) #normalizo los valores
    rgb = np.zeros(imagen.shape)
    rgb[:,:,0] = np.clip(imagen[:,:,0] + 0.9663 * imagen[:,:,1] + 0.6210 * imagen[:,:,2], 0., 1.)
    rgb[:,:,1] = np.clip(imagen[:,:,0] - 0.2721 * imagen[:,:,1] - 0.6474 * imagen[:,:,2], 0., 1.)
    rgb[:,:,2] = np.clip(imagen[:,:,0] - 1.1070 * imagen[:,:,1] + 1.7046 * imagen[:,:,2], 0., 1.)
    return rgb

# FUNCIONES DE INTERFAZ
#filetypes=[("Image files", "*.jpg;*.png")] Este no funciona
def abrir_imagen():
    global imagen_inicio, imagen
    ruta = filedialog.askopenfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if ruta:
        imagen_inicio = Image.open(ruta) #imagen objeto de libreria PIL
        imagen = np.array(imagen_inicio) # transformamos a un array para trabajarlo
        #Esta parte es para mostrar la imagen al inicio
        imagen_abierta = imagen_inicio.resize((300, 300))
        img = ImageTk.PhotoImage(imagen_abierta)
        canvas1.create_image(150, 150, image=img)
        canvas1.image = img

# Función para transformar la imagen de RGB a YIQ
def transformar_a_yiq():
    global imagen, imagen_final
    if imagen_inicio:
        # Transformar la imagen Aqui
        imagen = rgb2yiq(imagen)
        # Convertimos luego de normalizar a un rango de 0 a 255 que maneja pil
        imagen = (imagen * 255).astype(np.uint8)
        #Esta parte es para mostrar la imagen resultante
        imagen_final = Image.fromarray(imagen) #transformamos a un objeto que maneja PIL
        img = ImageTk.PhotoImage(imagen_final.resize((300, 300)))
        canvas2.create_image(150, 150, image=img)
        canvas2.image = img

# Función para transformar la imagen de YIQ a RGB
def transformar_a_rgb():
    global imagen, imagen_final
    if imagen_inicio:
        # Transformar la imagen Aqui
        imagen = yiq2rgb(imagen)
        # Convertimos luego de normalizar a un rango de 0 a 255 que maneja pil
        imagen = (imagen * 255).astype(np.uint8)
        #Esta parte es para mostrar la imagen resultante
        imagen_final = Image.fromarray(imagen) #transformamos a un objeto que maneja PIL
        img = ImageTk.PhotoImage(imagen_final.resize((300, 300)))
        canvas2.create_image(150, 150, image=img)
        canvas2.image = img

def luminancia_saturacion():
    global imagen, imagen_final
    if imagen_inicio:
        imagen = np.clip(imagen /255.,0.,1.) #normalizo los valores
        luminancia = 0.7
        saturacion = 0.4
        imagen[:,:,0] *=luminancia
        imagen[:,:,1] *=saturacion
        imagen[:,:,2] *=saturacion
        # Convertimos luego de normalizar a un rango de 0 a 255 que maneja pil
        imagen = (imagen * 255).astype(np.uint8)
        #Esta parte es para mostrar la imagen resultante
        imagen_final = Image.fromarray(imagen) #transformamos a un objeto que maneja PIL
        img = ImageTk.PhotoImage(imagen_final.resize((300, 300)))
        canvas2.create_image(150, 150, image=img)
        canvas2.image = img

# Función para guardar la imagen transformada
def guardar_imagen():
    if imagen_final:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if ruta_guardado:
            imagen_final.save(ruta_guardado)

# Crear botones
boton_abrir = tk.Button(ventana, text="Abrir", command=abrir_imagen, bg="#ff1d28",font=("Roboto", 11))
boton_abrir.place(x=200, y=400)

boton_transformar = tk.Button(ventana, text="Transformar a YIQ", command=transformar_a_yiq, bg="#ff1d28",font=("Roboto", 11))
boton_transformar.place(x=300, y=400)

boton_transformar = tk.Button(ventana, text="Transformar a RGB", command=transformar_a_yiq, bg="#ff1d28",font=("Roboto", 11))
boton_transformar.place(x=300, y=450)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen, bg="#ff1d28",font=("Roboto", 11))
boton_guardar.place(x=500, y=400)

boton_guardar = tk.Button(ventana, text="Luminancia", command=luminancia_saturacion, bg="#ff1d28",font=("Roboto", 11))
boton_guardar.place(x=500, y=450)

# Iniciar el loop de la ventana
ventana.mainloop()
