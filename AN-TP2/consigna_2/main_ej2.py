import numpy as np
import cv2
import matplotlib.pyplot as plt  # <-- Acuérdate de agregar esta línea
from scipy.fft import fft2, fftshift
from skimage.transform import warp_polar
from skimage.registration import phase_cross_correlation

def graficar_espectros(imagen3, f3_fs, imagen4, f4_fs):

    plt.figure(figsize=(10, 6))

    # Imagen 3 y su FFT
    plt.subplot(2, 2, 1)
    plt.imshow(imagen3, cmap='gray')
    plt.title('Imagen 3 (Original)')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    # Usamos 'viridis' o 'magma' para que resalten más las frecuencias
    plt.imshow(f3_fs, cmap='magma') 
    plt.title('Espectro FFT 3')
    plt.axis('off')

    # Imagen 4 y su FFT
    plt.subplot(2, 2, 3)
    plt.imshow(imagen4, cmap='gray')
    plt.title('Imagen 4 (Rotada)')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(f4_fs, cmap='magma')
    plt.title('Espectro FFT 4')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def main():
    # 1. Cargar imágenes
    imagen3 = cv2.imread("AN-TP2/consigna_2/imagenes/imagen3.jpg", cv2.IMREAD_GRAYSCALE)
    imagen4 = cv2.imread("AN-TP2/consigna_2/imagenes/imagen4.jpg", cv2.IMREAD_GRAYSCALE)
    #imagenWeb= cv2.imread("AN-TP2/consigna_2/imagenes/imagenWeb.png", cv2.IMREAD_GRAYSCALE)
    
    # Calculamos la magnitud con el logaritmo directo (limpié un poco tu código duplicado)
    f3_fs = np.log(np.abs(fftshift(fft2(imagen3)))+1)
    f4_fs = np.log(np.abs(fftshift(fft2(imagen4)))+1)
    #fWeb_fs = np.log(np.abs(fftshift(fft2(imagenWeb)))+1)
    
 
    graficar_espectros(imagen3, f3_fs, imagen4, f4_fs)
   # graficar_espectros(imagenWeb, fWeb_fs, imagen4, f4_fs)

    # Mapeo a Coordenadas Polares
    radius = f3_fs.shape[0] / 2
    f3_polar = warp_polar(f3_fs, radius=radius)
    f4_polar = warp_polar(f4_fs, radius=radius)

    # Correlación de Fase
    resultado, error, diffase = phase_cross_correlation(f3_polar, f4_polar)

    # Convertir a grados
    angulo_detectado = resultado[0]

    if angulo_detectado == 0:
        angulo_detectado = resultado[1]

    print(f"El ángulo de rotación detectado es: {angulo_detectado} grados")

if __name__ == "__main__":
    main()