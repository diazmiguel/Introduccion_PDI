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
def rgb2yiq(imagen):
    imagen = np.clip(imagen/255.,0.,1.) # imagen = imagen/255.
    #print("rgb2yiq: ",imagen.shape,imagen.dtype, "tamaño: ", imagen.min(),imagen.max())
    yiq= np.zeros(imagen.shape)
    yiq[:,:,0] = np.clip(0.299 * imagen[:,:,0] + 0.587 * imagen[:,:,1] + 0.114 * imagen[:,:,2], 0., 1.)
    yiq[:,:,1] = np.clip(0.595716 * imagen[:,:,0] - 0.274453 * imagen[:,:,1] - 0.321263 * imagen[:,:,2], -0.5957, 0.5957)
    yiq[:,:,2] = np.clip(0.211456 * imagen[:,:,0] - 0.522591 * imagen[:,:,1] + 0.311135 * imagen[:,:,2], -0.5226, 0.5226)
    return yiq

def yiq2rgb(imagen):
    #imagen = np.clip(imagen/255.,0.,1.)
    rgb = np.zeros(imagen.shape)
    rgb[:,:,0] = np.clip(imagen[:,:,0] + 0.9663 * imagen[:,:,1] + 0.6210 * imagen[:,:,2], 0., 1.)
    rgb[:,:,1] = np.clip(imagen[:,:,0] - 0.2721 * imagen[:,:,1] - 0.6474 * imagen[:,:,2], 0., 1.)
    rgb[:,:,2] = np.clip(imagen[:,:,0] - 1.1070 * imagen[:,:,1] + 1.7046 * imagen[:,:,2], 0., 1.)
    return rgb

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
        luminancia = simpledialog.askfloat("Entrada", "Ingrese el valor de luminancia:") 
        saturacion = simpledialog.askfloat("Entrada", "Ingrese el valor de saturacion:")
        yiq = rgb2yiq(imagen_inicio)
        yiq[:,:,0] *=luminancia
        yiq[:,:,1] *=saturacion
        yiq[:,:,2] *=saturacion
        yiq_normalized = (yiq - yiq.min()) / (yiq.max() - yiq.min())
        imagen_final = (yiq_normalized * 255).astype(np.uint8)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib

def transformar_a_rgb():
    global imagen_inicio, imagen_final
    if imagen_inicio is not None:
        # Transformar la imagen Aqui
        rgb = yiq2rgb(imagen_inicio/255.)
        imagen_final = (rgb * 255).astype(np.uint8)
        #print(imagen_final.dtype)
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib


def cambiarLuminanciaSaturacion():
    global imagen_inicio, imagen_final
    if imagen_inicio is not None:
        # Transformar la imagen
        luminancia = simpledialog.askfloat("Entrada", "Ingrese el valor de luminancia:") 
        saturacion = simpledialog.askfloat("Entrada", "Ingrese el valor de saturacion:")
        yiq = rgb2yiq(imagen_inicio)
        yiq[:,:,0] *=luminancia
        yiq[:,:,1] *=saturacion
        yiq[:,:,2] *=saturacion
        imagen_final = (yiq2rgb(yiq) * 255).astype(np.uint8)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        ax2.clear()  # Limpiar el contenido anterior de la figura
        ax2.imshow(imagen_final)  # Mostrar la imagen
        ax2.axis('off')  # Ocultar los ejes
        canvas2.draw()  # Dibujar la imagen en el canvas de Matplotlib

def cargar2daImagen():
    ruta = filedialog.askopenfilename(defaultextension=".png", filetypes=[("Image files", "*.png ; *.bmp ; *.jpg")])
    if ruta:
        imagen2da = imageio.v2.imread(ruta)  #Reemplazar por lectura de imageio
        return imagen2da

def pintar2Canvas(img):
    global imagen_final
    imagen_final = img
    ax2.clear();  # Limpiar el contenido anterior de la figura
    ax2.imshow(imagen_final);  # Mostrar la imagen
    ax2.axis('off');  # Ocultar los ejes
    canvas2.draw();  # Dibujar la imagen en el canvas de Matplotlib

def cuasi_suma_clampeada():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        sumaImg = np.clip(imagen_inicio+img2,0,255) #Operacion que sumara las matrices
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        pintar2Canvas(sumaImg)
        
def cuasi_suma_promediada():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        sumaImg = (imagen_inicio+img2) //2
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        pintar2Canvas(sumaImg)       

def cuasi_resta_clampeada():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        print("img2")
        restaImg = np.clip(imagen_inicio - img2,0,255) #Operacion que restara las matrices
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        #print(restaImg)
        pintar2Canvas(restaImg)
        
def cuasi_resta_promediada():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        restaImg = (imagen_inicio - img2) //2
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        pintar2Canvas(restaImg)  
        
def suma_clampeada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = rgb2yiq(imagen_inicio)
        img2 = rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip(img1[:,:,0]+img2[:,:,0], 0.,1.)# YA + YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] + img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA + YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] + img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA + YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = (yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)

def resta_clampeada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = rgb2yiq(imagen_inicio)
        img2 = rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip(img1[:,:,0]-img2[:,:,0], 0.,1.)# YA - YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] - img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA - YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] - img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA - YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = sumaImg = (yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)

def suma_promediada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = rgb2yiq(imagen_inicio)
        img2 = rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip((img1[:,:,0]+img2[:,:,0])/2, 0.,1.)# YA + YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] + img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA + YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] + img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA + YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = (yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)


def resta_promediada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = rgb2yiq(imagen_inicio)
        img2 = rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip((img1[:,:,0]-img2[:,:,0])/2, 0.,1.)# YA - YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] - img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA - YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] - img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA - YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = sumaImg = (yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)
"""
def convolucionar(img, kernel):
    imgConvolucionada = np.zeros((np.array(img.shape) - np.array(kernel.shape)+1))
    for x in range(imgConvolucionada.shape[0]):
        for y in range(imgConvolucionada.shape[1]):
            imgConvolucionada[x,y] = (img[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).sum() 
    return imgConvolucionada
"""


def realizarConvolucionBarlett():
    global imagen_inicio
    kernel = mf.kernel_bartlett(5)
    Img_convol = mf.convolucion(rgb2yiq(imagen_inicio), kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    pintar2Canvas(Img_convol)

def realizarConvolucionPascal():
    global imagen_inicio
    kernel = mf.pascal(7)
    Img_convol = mf.convolucion(rgb2yiq(imagen_inicio), kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    pintar2Canvas(Img_convol)


def realizarConvolucionGauss():
    global imagen_inicio
    kernel = mf.gauss(5,2)
    Img_convol = mf.convolucion(rgb2yiq(imagen_inicio), kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    pintar2Canvas(Img_convol)

def realizarConvolucionLaplace():
    global imagen_inicio
    kernel = mf.laplace(4)
    Img_convol = mf.convolucion(rgb2yiq(imagen_inicio), kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    pintar2Canvas(Img_convol)

def realizarConvolucionDog():
    global imagen_inicio
    kernel = mf.dog(7)
    Img_convol = mf.convolucion(rgb2yiq(imagen_inicio), kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    pintar2Canvas(Img_convol)

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
    "   Transformar a YIQ ": transformar_a_yiq,
    "   Transformar a RGB ": transformar_a_rgb,
    " Convolucion Barlett 5x5": realizarConvolucionBarlett,
    " Convolucion Pascal 7x7": realizarConvolucionPascal,
    " Convolucion Gauss ": realizarConvolucionGauss,
    " Convolucion Laplace 4x4": realizarConvolucionLaplace,
    " Convolucion Dog ": realizarConvolucionDog
}
# Variable para almacenar la opción seleccionada
opcion = tk.StringVar()
opcion.set("   Transformar a YIQ ")  # Valor inicial

# Crear botones 
boton_abrir = tk.Button(ventana, text="Abrir ", command= abrir_imagen, bg="#1dd767", font=("Roboto", 11))
boton_abrir.place(x=200, y=500)

# menú desplegable (OptionMenu)
menu_opciones = tk.OptionMenu(ventana, opcion, *operaciones.keys())
menu_opciones.place(x=300, y=500)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen, bg="#1dd767",font=("Roboto", 11))
boton_guardar.place(x=500, y=500)

boton_volver = tk.Button(ventana, text="Volver", command=volver, bg="#1dd767",font=("Roboto", 11))
boton_volver.place(x=200, y=550)

# Crear el botón y vincularlo a la función de solicitud de datos
boton_ejecutar = tk.Button(ventana, text="Ejecutar Operación", command=ejecutar_opcion, bg="#1dd767", font=("Roboto", 11))
boton_ejecutar.place(x=500, y=550)

# Iniciar el loop de la ventana
ventana.mainloop()