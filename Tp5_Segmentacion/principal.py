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
    ax2.imshow(imagen_final, "gray");  # Mostrar la imagen
    ax2.axis('off');  # Ocultar los ejes
    canvas2.draw();  # Dibujar la imagen en el canvas de Matplotlib

#FUNCIONES DEL TP 5
def umbralizarGlobalmente():
    global imagen_inicio
    imagen_yiq = mf.rgb2yiq(imagen_inicio)
    imagen_yiq[:,:,0] = mf.umbralGlobal(imagen_yiq[:,:,0],np.mean(imagen_yiq[:,:,0]))
    porcentaje = np.sum(imagen_yiq[:,:,0] == 0) / (imagen_yiq[:,:,0].shape[0] * imagen_yiq[:,:,0].shape[1]) * 100
    print(f"Umbral Global: Porcentaje de píxeles negros: {porcentaje:.2f}%")
    pintar2Canvas((imagen_yiq[:,:,0] * 255).astype(np.uint8))

def umbralizarLocalmente():
    global imagen_inicio
    imagen_yiq = mf.rgb2yiq(imagen_inicio)
    imagen_yiq[:,:,0] = mf.umbralLocal(imagen_yiq[:,:,0],50)
    porcentaje = np.sum(imagen_yiq[:,:,0] == 0) / (imagen_yiq[:,:,0].shape[0] * imagen_yiq[:,:,0].shape[1]) * 100
    print(f"Umbral Local: Porcentaje de píxeles negros: {porcentaje:.2f}%")
    pintar2Canvas((imagen_yiq[:,:,0] * 255).astype(np.uint8))
    
def umbralizarPorDistanciaMinima():
    global imagen_inicio
    imagen_yiq = mf.rgb2yiq(imagen_inicio)
    canalYBinarizado = mf.binarizacionDistanciaMinima(imagen_yiq[:,:,0],0.5,0.9)
    imagen_yiq = mf.colocarCanalaImg(imagen_yiq,canalYBinarizado)
    porcentaje = np.sum(imagen_yiq[:,:,0] == 0) / (imagen_yiq[:,:,0].shape[0] * imagen_yiq[:,:,0].shape[1]) * 100
    print(f"Distancia Minima: Porcentaje de píxeles negros: {porcentaje:.2f}%")
    pintar2Canvas((imagen_yiq[:,:,0] * 255).astype(np.uint8))

def umbralizarOtsu():
    global imagen_inicio
    imagen_yiq = mf.rgb2yiq(imagen_inicio) #Transformamos a yiq
    umbral, imagen_bin_Otsu = mf.umbralOtsu(imagen_yiq[:,:,0]) #Aplicamos Otsu obteniendo el umbral calculado, y el canal bin
    imagen_yiq = mf.colocarCanalaImg(imagen_yiq,imagen_bin_Otsu) #Insertamos el canal Y binarizado en la imagen yiq
    porcentaje = np.sum(imagen_yiq[:,:,0] == 0) / (imagen_yiq[:,:,0].shape[0] * imagen_yiq[:,:,0].shape[1]) * 100 #Calculo px negro
    print("Umbral óptimo (Otsu):", umbral)
    print(f"Umbral Otsu: Porcentaje de píxeles negros: {porcentaje:.2f}%")
    pintar2Canvas((imagen_yiq[:,:,0] * 255).astype(np.uint8))
#Laplace
def realizarConvolucionLaplace4():
    global imagen_inicio
    img = mf.realizarConvolucion(imagen_inicio, mf.laplace(4))
    porcentaje = np.sum(img[:,:,0] == 0) / (img[:,:,0].shape[0] * img[:,:,0].shape[1]) * 100
    print(f"Laplace 4x4: Porcentaje de píxeles negros {porcentaje:.2f}%")
    pintar2Canvas(img[:,:,0])

def realizarConvolucionLaplace8():
    global imagen_inicio
    img = mf.realizarConvolucion(imagen_inicio, mf.laplace(8))
    porcentaje = np.sum(img[:,:,0] == 0) / (img[:,:,0].shape[0] * img[:,:,0].shape[1]) * 100
    print(f"Laplace 8x8: Porcentaje de píxeles negros {porcentaje:.2f}%")
    pintar2Canvas(img[:,:,0])



def bordeExterno():
    global imagen_inicio
    img=mf.im_border_ext(imagen_inicio[:,:,0], np.ones((3,3)))
    pintar2Canvas(img)

def bordeInterno():
    global imagen_inicio
    img=mf.im_border_int(imagen_inicio[:,:,0], np.ones((3,3)))
    pintar2Canvas(img)

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
    "Umbralizar globalmente": umbralizarGlobalmente,
    "Umbralizar Localmente": umbralizarLocalmente,
    "Umbralizar Distancia Min.": umbralizarPorDistanciaMinima,
    "Umbralizar Por Otsu": umbralizarOtsu,
    " Convolucion Laplace 4x4": realizarConvolucionLaplace4,
    " Convolucion Laplace 8x8": realizarConvolucionLaplace8,
    " Borde Interno": bordeInterno,
    " Borde Externo": bordeExterno
}
# Variable para almacenar la opción seleccionada
opcion = tk.StringVar()
opcion.set("Umbralizar globalmente")  # Valor inicial

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