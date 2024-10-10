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
    ax2.imshow(imagen_final);  # Mostrar la imagen
    ax2.axis('off');  # Ocultar los ejes
    canvas2.draw();  # Dibujar la imagen en el canvas de Matplotlib

# Función para transformar la imagen de RGB a YIQ
def transformar_a_yiq():
    global imagen_inicio
    if imagen_inicio is not None:
        # Transformar la imagen
        luminancia = simpledialog.askfloat("Entrada", "Ingrese el valor de luminancia:") 
        saturacion = simpledialog.askfloat("Entrada", "Ingrese el valor de saturacion:")
        yiq = mf.rgb2yiq(imagen_inicio)
        yiq[:,:,0] *=luminancia
        yiq[:,:,1] *=saturacion
        yiq[:,:,2] *=saturacion
        yiq_normalized = (yiq - yiq.min()) / (yiq.max() - yiq.min())
        pintar2Canvas((yiq_normalized * 255).astype(np.uint8))

def transformar_a_rgb():
    global imagen_inicio
    if imagen_inicio is not None:
        # Transformar la imagen Aqui
        rgb = mf.yiq2rgb(imagen_inicio/255.)
        pintar2Canvas((rgb * 255).astype(np.uint8))


def cambiarLuminanciaSaturacion(): #Te cambia la luminosidad, saturacion transformando en el canal yiq
    global imagen_inicio
    if imagen_inicio is not None:
        # Transformar la imagen
        luminancia = simpledialog.askfloat("Entrada", "Ingrese el valor de luminancia:") 
        saturacion = simpledialog.askfloat("Entrada", "Ingrese el valor de saturacion:")
        yiq = mf.rgb2yiq(imagen_inicio)
        yiq[:,:,0] *=luminancia
        yiq[:,:,1] *=saturacion
        yiq[:,:,2] *=saturacion
        pintar2Canvas((mf.yiq2rgb(yiq) * 255).astype(np.uint8))
        

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
        img1 = mf.rgb2yiq(imagen_inicio)
        img2 = mf.rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip(img1[:,:,0]+img2[:,:,0], 0.,1.)# YA + YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] + img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA + YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] + img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA + YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = (mf.yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)

def resta_clampeada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = mf.rgb2yiq(imagen_inicio)
        img2 = mf.rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip(img1[:,:,0]-img2[:,:,0], 0.,1.)# YA - YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] - img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA - YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] - img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA - YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = sumaImg = (mf.yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)

def suma_promediada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = mf.rgb2yiq(imagen_inicio)
        img2 = mf.rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip((img1[:,:,0]+img2[:,:,0])/2, 0.,1.)# YA + YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] + img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA + YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] + img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA + YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = (mf.yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)


def resta_promediada_yiq():
    global imagen_inicio
    img2 = cargar2daImagen()
    if img2 is not None:
        #Obtenemos YIQ
        img1 = mf.rgb2yiq(imagen_inicio)
        img2 = mf.rgb2yiq(img2)
        yiq= np.zeros(img1.shape)
        yiq[:,:,0] = np.clip((img1[:,:,0]-img2[:,:,0])/2, 0.,1.)# YA - YB; If YC > 1 then YC:=1
        yiq[:,:,1] = (img1[:,:,0]*img1[:,:,1] - img2[:,:,0]*img2[:,:,1]) / (img1[:,:,0]+img2[:,:,0]) #(YA * IA - YB * IB) / (YA + YB)
        yiq[:,:,2] = (img1[:,:,0]*img1[:,:,2] - img2[:,:,0]*img2[:,:,2]) / (img1[:,:,0]+img2[:,:,0])  #(YA * QA - YB * QB) / (YA + YB)
        # Mostrar la imagen en el canvas derecho utilizando Matplotlib
        sumaImg = sumaImg = (mf.yiq2rgb(yiq) * 255).astype(np.uint8)
        pintar2Canvas(sumaImg)

#Plano
def realizarConvolucionPlano():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.kernel_plano(3)))
#Barlett
def realizarConvolucionBarlett3():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.kernel_bartlett(3)))
def realizarConvolucionBarlett5():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.kernel_bartlett(5)))
def realizarConvolucionBarlett7():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.kernel_bartlett(7)))

#Gauss
def realizarConvolucionGauss5():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.gauss(5,2)))
def realizarConvolucionGauss7():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.gauss(7,2)))
#Laplace
def realizarConvolucionLaplace4():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.laplace(4)))
def realizarConvolucionLaplace8():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.laplace(8)))
#Direccional
def realizarConvolucionDireccional():
    global imagen_inicio
    direccion = simpledialog.askstring("Entrada","Ingrese Direccion [n,s,e,o,ne,no,se,so]:") 
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.sobel(direccion)))
#Dog
def realizarConvolucionDog():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.dog(5)))
#PasaAlto
def realizarPasaAlto():
    global imagen_inicio
    pintar2Canvas(mf.realizarConvolucion(imagen_inicio, mf.high_pass(mf.gauss(5, 1))))

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
    " Convolucion Plano ": realizarConvolucionPlano,
    " Convolucion Barlett 3x3": realizarConvolucionBarlett3,
    " Convolucion Barlett 5x5": realizarConvolucionBarlett5,
    " Convolucion Barlett 7x7": realizarConvolucionBarlett7,
    " Convolucion Gauss 5x5 ": realizarConvolucionGauss5,
    " Convolucion Gauss 7x7 ": realizarConvolucionGauss7,
    " Convolucion Laplace 4x4": realizarConvolucionLaplace4,
    " Convolucion Laplace 8x8": realizarConvolucionLaplace8,
    " Convolucion Direccional": realizarConvolucionDireccional,
    " Convolucion Dog ": realizarConvolucionDog,
    " Convolucion PasaAlto ": realizarPasaAlto
}
# Variable para almacenar la opción seleccionada
opcion = tk.StringVar()
opcion.set(" Convolucion Plano ")  # Valor inicial

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