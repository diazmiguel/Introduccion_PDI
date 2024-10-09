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

def kernel_bartlett(n):
  secuencia = np.arange(1,(n+1)//2+1) #Crece
  secuencia = np.concatenate([secuencia, secuencia[::-1][1:]]) #Decreciente
  matriz = secuencia * secuencia.reshape(n,1) #Producto vectorial
  matriz = matriz/np.sum(matriz) #Normalizacion
  return matriz

def pascal(s=3):
    def pascal_triangle(steps,last_layer = np.array([1])):
        if steps==1:
            return last_layer
        next_layer = np.array([1,*(last_layer[:-1]+last_layer[1:]),1])
        return pascal_triangle(steps-1,next_layer)
    a = pascal_triangle(s)
    k = np.outer(a,a.T)
    return k / k.sum()

def laplace(_type=4,normalize=False):
    if _type==4:
        kernel =  np.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])
    if _type==8:
        kernel =  np.array([[-1.,-1.,-1.],[-1.,8.,-1.],[-1.,-1.,-1.]])
    if normalize:
        kernel /= np.sum(np.abs(kernel))
    return kernel

# Función para crear un kernel gaussiano
def gauss(size, sigma):
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    g = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return g / g.sum()

# Función para crear el kernel DoG
def dog(size, fs=1, cs=2):
    return gauss(size, fs) - gauss(size, cs)