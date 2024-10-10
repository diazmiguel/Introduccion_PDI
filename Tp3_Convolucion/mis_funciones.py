#En proceso :)
import numpy as np
#FUNCIONES DE TRANSFORMACION
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

#FUNCIONES DE CONVOLUCION

#Este es para convolucionar los 3 canales
def realizarConvolucion(imagen, kernel):
    Img_convol = convolucion(rgb2yiq(imagen),kernel)
    Img_convol = (yiq2rgb(Img_convol) * 255).astype(np.uint8)
    return Img_convol


def convolucion(img, kn):
    # Obtenemos las dimensiones de la imagen y el kernel por que no se puede operar con tuplas
    img_fila, img_columna,img_canal = img.shape #dimensiones de la imagen
    kn_dim = kn.shape[0]
    # Calculamos las dimensiones de la imagen transformada
    img_conv_fila = img_fila - kn_dim + 1
    img_conv_columna = img_columna - kn_dim + 1
    # Inicializamos la matriz de salida
    img_conv = np.zeros((img_conv_fila, img_conv_columna, img_canal))
    # Realizamos la convolución
    for k in range(img_canal):
      img_k = img[:,:,k]
      #print("canal ")
      for i in range(img_conv_fila):
          for j in range(img_conv_columna):
              #img_conv[i, j, k] = np.sum(img[i:i+kn_dim, j:j+kn_dim, k] * kn) #producto elem a elem y luego suma
              img_conv[i, j, k] = np.sum(img_k[i:i+kn_dim, j:j+kn_dim] * kn)
    return img_conv

"""

def convolucionar(img, kernel):
    imgConvolucionada = np.zeros((np.array(img.shape) - np.array(kernel.shape)+1))
    for x in range(imgConvolucionada.shape[0]):
        for y in range(imgConvolucionada.shape[1]):
            imgConvolucionada[x,y] = (img[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).sum() 
    return imgConvolucionada
    
def realizarConvolucion(imagen, kernel):
    # Convertir la imagen RGB a YIQ
    img_yiq = rgb2yiq(imagen)
    # Obtener el canal Y
    CanalY = img_yiq[:, :, 0]
    # Calcular el padding necesario para mantener el tamaño original
    pad_x = kernel.shape[0] // 2
    pad_y = kernel.shape[1] // 2
    # Aplicar padding con ceros al canal Y
    CanalY_padded = np.pad(CanalY, ((pad_x, pad_x), (pad_y, pad_y)), mode='constant', constant_values=0)
    # Aplicar la convolución usando la función original de convolucionar (sin cambios)
    CanalY_convolucionado = convolucionar(CanalY_padded, kernel)
    # Reasignar el canal Y convolucionado a la imagen YIQ
    img_yiq[:, :, 0] = CanalY_convolucionado[:imagen.shape[0], :imagen.shape[1]]
    # Convertir de nuevo a RGB y asegurarse de que los valores estén en el rango adecuado
    Img_convol = (yiq2rgb(img_yiq) * 255).astype(np.uint8)
    return Img_convol
"""
#Filtro llano
def kernel_plano(n):
  k = np.ones((n,n))
  k = k/ n**2
  return k

#Barlett  3x3, 5x5, 7x7
def kernel_bartlett(n):
  secuencia = np.arange(1,(n+1)//2+1) #Crece
  secuencia = np.concatenate([secuencia, secuencia[::-1][1:]]) #Decreciente
  matriz = secuencia * secuencia.reshape(n,1) #Producto vectorial
  matriz = matriz/np.sum(matriz) #Normalizacion
  return matriz

#Filtro de Gauss 5x5 y 7x7.
def gauss(size, sigma):
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    g = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return g / g.sum()

#Detectores de borde v4 y v8
def laplace(_type=4,normalize=False):
    if _type==4:
        kernel =  np.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])
    if _type==8:
        kernel =  np.array([[-1.,-1.,-1.],[-1.,8.,-1.],[-1.,-1.,-1.]])
    if normalize:
        kernel /= np.sum(np.abs(kernel))
    return kernel

#Filtro direccional
def sobel(direccion):
    if direccion == 'n':  # Norte (Y negativo)
        kernel = np.array([[ 1,  2,  1],[ 0,  0,  0],[-1, -2, -1]])
    elif direccion == 's':  # Sur (Y positivo)
        kernel = np.array([[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]])
    elif direccion == 'e':  # Este (X positivo)
        kernel = np.array([[-1,  0,  1],[-2,  0,  2],[-1,  0,  1]])
    elif direccion == 'o':  # Oeste (X negativo)
        kernel = np.array([[ 1,  0, -1],[ 2,  0, -2],[ 1,  0, -1]])
    elif direccion == 'ne':  # Noreste (diagonal)
        kernel = np.array([[ 0,  1,  2],[-1,  0,  1],[-2, -1,  0]])
    elif direccion == 'no':  # Noroeste (diagonal)
        kernel = np.array([[ 2,  1,  0],[ 1,  0, -1],[ 0, -1, -2]])
    elif direccion == 'se':  # Sureste (diagonal)
        kernel = np.array([[-2, -1,  0],[-1,  0,  1],[ 0,  1,  2]])
    elif direccion == 'so':  # Suroeste (diagonal)
        kernel = np.array([[ 0, -1, -2],[ 1,  0, -1],[ 2,  1,  0]])
    else:
        raise ValueError("Incorrecto. Debe ser: 'n', 's', 'e', 'o', 'ne', 'no', 'se', 'so'.")
    return kernel

#Filtro pasabanda
def dog(size,fs=1,cs=2):
    return gauss(size,fs)-gauss(size,cs)

#Filtropasalto
def identity_kernel(s):
    kernel = np.zeros(s)
    kernel[s[0]//2,s[1]//2] = 1.
    return kernel

def high_pass(low_pass):
    return identity_kernel(low_pass.shape) - low_pass