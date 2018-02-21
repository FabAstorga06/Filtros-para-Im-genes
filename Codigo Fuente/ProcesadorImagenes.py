# coding=utf-8
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, misc

#Carga una imagen al programa mediante una entrada
#desde la consola.
def cargarImagen(img):
    return Image.open(img, mode='r')

#Transforma un objeto imagen a un arreglo mediante
#la biblioteca numpy.
def acomodaFilasImg(lista):
    fila = []
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            fila += [lista[i][j]]
    return fila

def TransformarImagenAArreglo(img):
    arr_img = np.array(img)
    nuevo_arr = []
    for i in range(len(arr_img)):
        nuevo_arr += [acomodaFilasImg(arr_img[i])]
    return nuevo_arr

#Muestra la imagen resultante mediante la
#biblioteca matplotlib.
def mostrarImagen(original, filtrada, titulo):
    fig = plt.figure(titulo)
    fig.set_facecolor('black')
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.imshow(original)
    ax2.imshow(filtrada)
    plt.axis('off')
    plt.show()

# Aplicación mediante las bibliotecas scipy/numpy para la
#aplicación de algún otro filtro (opcional).
def rankFiltro(img, width, height):
    filtrada = ndimage.rank_filter(img, rank=42, size=20)
    redimensionaImg = misc.imresize(filtrada, (height, width))
    return redimensionaImg

# Transforma un arreglo de numeros que representa una imagen
# a un objeto imagen mediante la biblioteca PIL.
def TransformarArregloAImagen(imgFiltrada):
    img = Image.fromarray(imgFiltrada.astype('uint8'))
    return img

#Guarda en formato png la imagen con filtro
def guardarImagen(nuevaImg, dir, nombre):
    nuevaImg.save(dir + "/" + nombre + ".png")

#Aplicación manual del filtro Gaussian Blur mediante métodos
#matemáticos.

#Realiza el cálculo de la nueva tupla RGB de cada pixel de la imagen mediante
#los valores del pixel a evaluar y los pixeles del kernel 5x5.
def evaluaPixel(eval_pixel, otros_pixeles):
    r = 0
    g = 0
    b = 0
    # Kernel 5x5
    valores_kernel = [0, 1, 2, 1, 0, 1, 3, 5, 3, 1, 2, 5, 5, 2, 1, 3, 5, 3, 1, 0, 1, 2, 1, 0]
    centro_kernel = 9
    prom_kernel = 57

    #Convolución
    for i in range(len(valores_kernel)):
        r += valores_kernel[i] * otros_pixeles[i][0]
        g += valores_kernel[i] * otros_pixeles[i][1]
        b += valores_kernel[i] * otros_pixeles[i][2]

    #Valores del pixel modificado
    R = (r + (eval_pixel[0] * centro_kernel)) / prom_kernel
    G = (g + (eval_pixel[1] * centro_kernel)) / prom_kernel
    B = (b + (eval_pixel[2] * centro_kernel)) / prom_kernel

    return ((int(R), int(G), int(B)))

#Se modifican los 24 pixeles utilizados para el filtro
def setPixeles(pixeles, esUno, ancho):
    # Se suman uno a los pixeles
    if (esUno):
        for i in range(len(pixeles)):
            pixeles[i] += 1
    #Se inicializan los pixeles con sus valores iniciales
    else:
        pixeles += [0]
        pixeles += [1]
        pixeles += [2]
        pixeles += [3]
        pixeles += [4]
        pixeles += [ancho]
        pixeles += [ancho + 1]
        pixeles += [ancho + 2]
        pixeles += [ancho + 3]
        pixeles += [ancho + 4]
        pixeles += [ancho * 2]
        pixeles += [(ancho * 2) + 1]
        pixeles += [(ancho * 2) + 3]
        pixeles += [(ancho * 2) + 4]
        pixeles += [(ancho * 3)]
        pixeles += [(ancho * 3) + 1]
        pixeles += [(ancho * 3) + 2]
        pixeles += [(ancho * 3) + 3]
        pixeles += [(ancho * 3) + 4]
        pixeles += [(ancho * 4)]
        pixeles += [(ancho * 4) + 1]
        pixeles += [(ancho * 4) + 2]
        pixeles += [(ancho * 4) + 3]
        pixeles += [(ancho * 4) + 4]
    return pixeles

#Se realiza un desplazamiento de 4 a cada pixel
def desplazarPixeles(pixeles):
    desplazamiento = 4
    for i in range(len(pixeles)):
        pixeles[i] += desplazamiento
    return pixeles

#Filtro de Gauss hecho con un kernel de 5x5 para realizar filtros
#en imagenes.
def gaussBlurFiltro(img):
    #Se establecen valores iniciales y constantes
    vals = list(img.getdata())
    vals_finales = []
    width = img.width
    height = img.height
    pix = []
    pix = setPixeles(pix, False, width)
    izq = width * 2
    der = (width * 3) - 2
    x = (width * 2) + 2
    sup = width * 2
    inf = -width * 2

    #Se crea una copia pixel por pixel al borde superior
    for valor in vals[:sup]:
        vals_finales.append(valor)

    #Se crea una copia pixel por pixel al borde izquierdo
    for i in range(height - 4):
        vals_finales.append(vals[izq])
        vals_finales.append(vals[izq + 1])

        for j in range(x, der):
            #Se escogen los valores indicados de pixeles de la imagen para evaluar
            #el pixel inicial.
            pixeles = []
            for index in range(24):
                pixeles.insert(index, vals[pix[index]])

            # Se llama la funcion de Gauss y se agrega el resultado del nuevo pixel al conjunto de datos
            # de la imagen filtrada.
            nuevoPixel = evaluaPixel(vals[j], pixeles)
            vals_finales.append(nuevoPixel)
            pix = setPixeles(pix, True, 0)

        pix = desplazarPixeles(pix)

        #Se crea una copia pixel por pixel al borde derecho
        vals_finales.append(vals[der])
        vals_finales.append(vals[der + 1])
        x += width
        der += width
        izq += width


    #Se crea una copia pixel por pixel al borde inferior
    for i in vals[inf:]:
        vals.append(i)

    return vals_finales

#Funcion que contiene la lógica principal del programa.
def main():
    print "---------------------------------------------------"
    print "PROCESADOR DE IMAGENES"
    print "---------------------------------------------------"

    while True:
        try:
            #Carga la imagen
            nombreImagen = str(input("Inserte el nombre de la imagen que desea manipular: "))
            if(nombreImagen == "salir"):
                break
            else:
                img = cargarImagen(nombreImagen + ".png")
                width, height = img.size
                imagenFiltrada = []
                grafico = ""
                #El usuario escoge alguno de los dos filtros
                tipoFiltro = str(input("¿Desea agregar un filtro a su imagen? "))
                if (tipoFiltro == "si" or tipoFiltro == "Si"):
                    arr_img = TransformarImagenAArreglo(img)
                    print ("Inserte el filtro que desea:")
                    print ("1. Gaussian Blur.")
                    filtro = int(input("2. Rank. "))
                    if (filtro == 1):
                        #Se aplica el filtro 'gaussian blur' a la imagen.
                        gaussianResultado = gaussBlurFiltro(img)
                        resGaussian = Image.new(img.mode, img.size)
                        resGaussian.putdata(gaussianResultado)
                        grafico = "GAUSSIAN BLUR"
                        # Se muestra la imagen filtrada
                        mostrarImagen(img, resGaussian, grafico)

                    elif (filtro == 2):
                        #Se aplica rank filtro.
                        imagenFiltrada = rankFiltro(arr_img, width, height)
                        grafico = "RANK"
                        # Se muestra la imagen filtrada
                        mostrarImagen(img, imagenFiltrada, grafico)
                    else:
                        break

                    # Se guarda la imagen
                    guardar_img = str(input("¿Desea guardar la imagen con filtro? "))
                    if (guardar_img == "si" or guardar_img == "Si"):
                        dir = str(input("Indique el directorio donde desea guardar la imagen: "))
                        nombreArchivo = str(input("Indique el nombre de la imagen: "))
                        if (filtro == 1):
                            guardarImagen(resGaussian, dir, nombreArchivo)
                        else:
                            nuevaImg = TransformarArregloAImagen(imagenFiltrada)
                            guardarImagen(nuevaImg, dir, nombreArchivo)
                        print "Su imagen " + nombreArchivo + ".png se guardó exitosamente en " + dir

                else:
                    print ("Puede añadir un filtro a alguna imagen si desea...")

        except:
            print("Hubo algún problema al procesar la imagen, por favor inténtelo de nuevo.")
    print ("¡Adiós!")

#Se inicializa el programa
main()



