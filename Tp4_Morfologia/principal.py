import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import imageio
import mis_funciones as mf
from tkinter import filedialog
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Crear ventana principal
ventana = tk.Tk()
ventana.geometry("1000x600")
ventana.title("IPDI")
ventana.config(bg="#333333") 

# Crear figura de Matplotlib para mostrar la imagen en el cuadro izquierdo
fig1, ax1 = plt.subplots(figsize=(4.5, 4))  # Tamaño de la figura similar al canvas
ax1.axis('off') 
canvas1 = FigureCanvasTkAgg(fig1, master=ventana)  # Crear el canvas de Matplotlib
canvas1.get_tk_widget().place(x=40, y=50)  # Posicionar el canvas de Matplotlib en la ventana

# Crear figura de Matplotlib para mostrar una suma 
fig2, ax2 = plt.subplots(figsize=(4.5, 4))  # Tamaño de la figura similar al canvas
ax2.axis('off') 
canvas2 = FigureCanvasTkAgg(fig2, master=ventana)  # Crear el canvas de Matplotlib
canvas2.get_tk_widget().place(x=510, y=50)  # Posicionar el canvas de Matplotlib en la ventana

# Configuracion que evita el fondo blanco por matplotlib
fig1.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig2.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Variables para guardar las imágenes
imagen_inicio = None # imagen que mostrara al principio
imagen_final = None # imagen que mostrara al final

#FUNCIONES PARA TRABAJAR CON ELLAS (Deberia modularizarse)

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

def cargar2daImagen():
    ruta = filedialog.askopenfilename(defaultextension=".png", filetypes=[("Image files", "*.png ; *.bmp ; *.jpg")])
    if ruta:
        imagen2da = imageio.v2.imread(ruta)  #Reemplazar por lectura de imageio
        return imagen2da

def pintar2Canvas(img):
    global imagen_final
    imagen_final = img
    ax2.clear();  # Limpiar el contenido anterior de la figura
    ax2.imshow(imagen_final,"gray");  # Mostrar la imagen
    ax2.axis('off');  # Ocultar los ejes
    canvas2.draw();  # Dibujar la imagen en el canvas de Matplotlib

#FUNCIONES DEL TP 4
def erosion3():
    global imagen_inicio
    pintar2Canvas(mf.im_erode(imagen_inicio[:,:,0], np.ones((3,3))))

def erosion5():
    global imagen_inicio
    pintar2Canvas(mf.im_erode(imagen_inicio[:,:,0], np.ones((5,5))))
    
def dilatar3():
    global imagen_inicio
    pintar2Canvas(mf.im_dilate(imagen_inicio[:,:,0], np.ones((3,3))))

def dilatar5():
    global imagen_inicio
    pintar2Canvas(mf.im_dilate(imagen_inicio[:,:,0], np.ones((5,5))))

def apertura3(): #No se resta, se hace las operaciones consecutivas
    global imagen_inicio
    pintar2Canvas(mf.apertura(imagen_inicio[:,:,0], np.ones((3,3))))

def apertura5(): #No se resta, se hace las operaciones consecutivas
    global imagen_inicio
    pintar2Canvas(mf.apertura(imagen_inicio[:,:,0], np.ones((5,5))))
    
def cierre3():
    global imagen_inicio
    pintar2Canvas(mf.cierre(imagen_inicio[:,:,0], np.ones((3,3))))

def cierre5():
    global imagen_inicio
    pintar2Canvas(mf.cierre(imagen_inicio[:,:,0], np.ones((5,5))))

def bordeExterno():
    global imagen_inicio
    pintar2Canvas(mf.im_border_ext(imagen_inicio[:,:,0], np.ones((3,3))))

def bordeInterno():
    global imagen_inicio
    pintar2Canvas(mf.im_border_int(imagen_inicio[:,:,0], np.ones((3,3))))

def mediana3():
    global imagen_inicio
    pintar2Canvas(mf._convolution(imagen_inicio[:,:,0], np.ones((3,3))))

def ejecutar_opcion():
    funcion_seleccionada = operaciones[opcion.get()]
    funcion_seleccionada()

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
            
# Diccionario de funciones
operaciones = {
    " Dilatar 3x3 ": dilatar3,
    " Dilatar 5x5 ": dilatar5,
    " Erosionar 3x3 ": erosion3,
    " Erosionar 5x5 ": erosion5,
    " Apertura 3x3": apertura3,
    " Apertura 5x5": apertura5,
    " Cierre   3x3": cierre3,
    " Cierre   5x5": cierre5,
    " Borde Interno": bordeInterno,
    " Borde Externo": bordeExterno,
    " Mediana 3x3  ": mediana3
}
# Variable para almacenar la opción seleccionada
opcion = tk.StringVar()
opcion.set(" Erosionar 3x3 ")  # Valor inicial

# Crear botones 
boton_abrir = tk.Button(ventana, text="Abrir ", command= abrir_imagen, bg="#1dd767", font=("Roboto", 11))
boton_abrir.place(x=200, y=500)

# menú desplegable (OptionMenu)
menu_opciones = tk.OptionMenu(ventana, opcion, *operaciones.keys())
menu_opciones.place(x=300, y=500)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen, bg="#1dd767",font=("Roboto", 11))
boton_guardar.place(x=550, y=500)

boton_volver = tk.Button(ventana, text="Volver", command=volver, bg="#1dd767",font=("Roboto", 11))
boton_volver.place(x=200, y=550)

# Crear el botón y vincularlo a la función de solicitud de datos
boton_ejecutar = tk.Button(ventana, text="Ejecutar Operación", command=ejecutar_opcion, bg="#1dd767", font=("Roboto", 11))
boton_ejecutar.place(x=550, y=550)

# Iniciar el loop de la ventana
ventana.mainloop()