import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import imageio

# Crear ventana principal
ventana = tk.Tk()
ventana.geometry("850x600")
ventana.title("IPDI")
ventana.config(bg="#333333") 

# Crear figura de Matplotlib para mostrar la imagen en el cuadro izquierdo
fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))  # Tamaño de la figura similar al canvas
ax1.axis('off') 
canvas1 = FigureCanvasTkAgg(fig1, master=ventana)  # Crear el canvas de Matplotlib
canvas1.get_tk_widget().place(x=50, y=50)  # Posicionar el canvas de Matplotlib en la ventana

# Crear figura de Matplotlib para mostrar la imagen en el cuadro derecho
fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))  # Tamaño de la figura similar al canvas
ax2.axis('off') 
canvas2 = FigureCanvasTkAgg(fig2, master=ventana)  # Crear el canvas de Matplotlib
canvas2.get_tk_widget().place(x=450, y=50)  # Posicionar el canvas de Matplotlib en la ventana

# Configuracion que evita el fondo blanco por matplotlib
fig1.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig2.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Variables para guardar las imágenes
imagen_inicio = None # imagen que mostrara al principio
imagen_final = None # imagen que mostrara al final
imagen = None #imagen con la que trabajaremos

#FUNCIONES PARA TRABAJAR CON ELLAS (Deberia modularizarse)
def rgb2yiq(imagen):
    imagen = np.clip(imagen/255.,0.,1.) # imagen = imagen/255.
    #print("rgb2yiq: ",imagen.shape,imagen.dtype, "tamaño: ", imagen.min(),imagen.max())
    yiq= np.zeros(imagen.shape)
    yiq[:,:,0] = np.clip(0.299 * imagen[:,:,0] + 0.587 * imagen[:,:,1] + 0.114 * imagen[:,:,2], 0., 1.)
    yiq[:,:,1] = np.clip(0.595716 * imagen[:,:,0] - 0.274453 * imagen[:,:,1] - 0.321263 * imagen[:,:,2], -0.5957, 0.5957)
    yiq[:,:,2] = np.clip(0.211456 * imagen[:,:,0] - 0.522591 * imagen[:,:,1] + 0.311135 * imagen[:,:,2], -0.5226, 0.5226)
    luminancia, saturacion = preguntar_luminosidad()
    yiq[:,:,0] *=luminancia
    yiq[:,:,1] *=saturacion
    yiq[:,:,2] *=saturacion
    yiq_normalized = (yiq - yiq.min()) / (yiq.max() - yiq.min())
    return yiq_normalized 

def yiq2rgb(imagen):
    imagen = np.clip(imagen/255.,0.,1.) #imagen /255.
    rgb = np.zeros(imagen.shape)
    rgb[:,:,0] = np.clip(imagen[:,:,0] + 0.9663 * imagen[:,:,1] + 0.6210 * imagen[:,:,2], 0., 1.)
    rgb[:,:,1] = np.clip(imagen[:,:,0] - 0.2721 * imagen[:,:,1] - 0.6474 * imagen[:,:,2], 0., 1.)
    rgb[:,:,2] = np.clip(imagen[:,:,0] - 1.1070 * imagen[:,:,1] + 1.7046 * imagen[:,:,2], 0., 1.)
    return rgb
def preguntar_luminosidad():
    luminancia = simpledialog.askfloat("Entrada", "Ingrese el valor de luminancia:")
    saturacion = simpledialog.askfloat("Entrada", "Ingrese el valor de saturacion:")
    return luminancia, saturacion

# FUNCIONES DE INTERFAZ (Tambien deberia modularizarse)
def abrir_imagen():
    global imagen_inicio
    ruta = filedialog.askopenfilename(defaultextension=".png", filetypes=[("Image files", "*.png ; *.bmp ; *.jpg")])
    if ruta:
        imagen_inicio = imageio.v2.imread(ruta)  #Reemplazar por lectura de imageio
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        ax1.clear()  # Limpiar el contenido anterior de la figura
        ax1.imshow(imagen_inicio)  # Mostrar la imagen
        ax1.axis('off')  # Ocultar los ejes
        canvas1.draw()  # Dibujar la imagen en el canvas de Matplotlib

# Función para transformar la imagen de RGB a YIQ
def transformar_a_yiq():
    global imagen_inicio, imagen_final
    if imagen_inicio is not None:
        # Transformar la imagen
        imagen_final = rgb2yiq(imagen_inicio)
        imagen_final = (imagen_final * 255).astype(np.uint8)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib

def transformar_a_rgb():
    global imagen_inicio, imagen_final
    if imagen_inicio is not None:
        # Transformar la imagen Aqui
        imagen_final = yiq2rgb(imagen_inicio)
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib


def luminancia():
    global imagen_inicio, imagen_final
    if imagen_inicio is not None:
        luminancia,saturacion = preguntar_luminosidad()
        if imagen_final is not None:
            imagen_final = np.clip(imagen_final /255.,0.,1.) #normalizo los valores
        else:
            imagen_final = np.clip(imagen_inicio /255.,0.,1.) #normalizo los valores
        imagen_final[:,:,0] *=luminancia
        imagen_final[:,:,1] *=saturacion
        imagen_final[:,:,2] *=saturacion
        # Convertimos luego de normalizar a un rango de 0 a 255 que maneja pil
        imagen_final = (imagen_final * 255).astype(np.uint8)
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib
        

def volver():
    global imagen_inicio, imagen_final
    if imagen_final is not None: #reemplazar por imagen_final
        imagen_final= imagen_inicio
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib
        
def guardar_imagen():
    global imagen_final
    if imagen_final is not None:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if ruta_guardado:
            imageio.imwrite(ruta_guardado, imagen_final)
            

# Crear botones 
boton_abrir = tk.Button(ventana, text="Abrir", command= abrir_imagen, bg="#1dd767", font=("Roboto", 11))
boton_abrir.place(x=200, y=450)

boton_transformar = tk.Button(ventana, text="Transformar a YIQ", command=transformar_a_yiq, bg="#1dd767",font=("Roboto", 11))
boton_transformar.place(x=300, y=450)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen, bg="#1dd767",font=("Roboto", 11))
boton_guardar.place(x=500, y=450)

boton_volver = tk.Button(ventana, text="Volver", command=volver, bg="#1dd767",font=("Roboto", 11))
boton_volver.place(x=200, y=500)

boton_transformar = tk.Button(ventana, text="Transformar a RGB", command=transformar_a_rgb, bg="#1dd767",font=("Roboto", 11))
boton_transformar.place(x=300, y=500)

boton_luminancia = tk.Button(ventana, text="Luminancia", command=luminancia, bg="#1dd767",font=("Roboto", 11))
boton_luminancia.place(x=500, y=500)

# Iniciar el loop de la ventana
ventana.mainloop()