import numpy as np
import tifffile as tiff
from PIL import Image
from scipy.optimize import minimize_scalar
import os

def guardar_imagen_png(matriz_imagen, nombre_archivo):
    """
    Normaliza una matriz de imagen (float) al rango [0, 255], 
    la convierte a uint8 y la guarda en formato .png dentro de la carpeta 'output'.
    """
    # 1. Asegurar que la carpeta 'output' exista
    carpeta_destino = 'output'
    os.makedirs(carpeta_destino, exist_ok=True)
    
    # 2. Clonar la matriz para no modificar la original y tomar el valor absoluto por seguridad
    img_procesada = np.abs(matriz_imagen.copy())
    
    # 3. Normalizar los valores al rango 0 - 255
    min_val = np.min(img_procesada)
    max_val = np.max(img_procesada)
    
    if max_val - min_val > 1e-5:
        # Escala lineal de los datos existentes al rango completo [0, 255]
        img_norm = 255.0 * (img_procesada - min_val) / (max_val - min_val)
    else:
        img_norm = np.zeros_like(img_procesada)
        
    # 4. Convertir a tipo entero de 8 bits (requerido para imágenes estándar)
    img_uint8 = img_norm.astype(np.uint8)
    
    # 5. Crear la ruta completa del archivo y guardarlo
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    
    # Asegurar que el nombre termine en .png
    if not ruta_completa.lower().endswith('.png'):
        ruta_completa += '.png'
        
    imagen_pil = Image.fromarray(img_uint8)
    imagen_pil.save(ruta_completa)
    print(f"Imagen guardada exitosamente en: {ruta_completa}")
def calcular_nitidez(imagen):
    """
    Calcula la nitidez basada en la magnitud del gradiente espacial (Sobel/Diferencias finitas).
    A mayor magnitud del gradiente, mayor nitidez (bordes más limpios).
    """
    gy, gx = np.gradient(imagen)
    magnitud_gradiente = np.sqrt(gx**2 + gy**2)
    return np.sum(magnitud_gradiente)

def reconstruir_imagen(magnitud, fase_alterada, k):
    """
    Reconstruye la imagen combinando la magnitud de f6 y la fase corregida de f7 (fase / k).
    """
    # 1. Corregir la fase deshaciendo el factor de compresión k
    # Evitamos división por cero si k es extremadamente cercano a 0
    if np.abs(k) < 1e-5: 
        return np.zeros_like(magnitud)
    
    fase_corregida = fase_alterada / k
    
    # 2. Recomponer el espectro complejo: F = |F| * exp(i * fase)
    espectro_complejo = magnitud * np.exp(1j * fase_corregida)
    
    # 3. Transformada Inversa de Fourier para volver al dominio espacial
    imagen_reconstruida = np.fft.ifft2(np.fft.ifftshift(espectro_complejo))
    
    # Nos quedamos con la parte real (por errores numéricos de precisión flotante)
    return np.real(imagen_reconstruida)

def optimizar_k(magnitud, fase_alterada):
    """
    Busca el factor k que maximiza la nitidez de la imagen reconstruida.
    Como minimize_scalar minimiza, pasamos la nitidez con signo negativo.
    """
    def funcion_objetivo(k):
        img = reconstruir_imagen(magnitud, fase_alterada, k)
        # Queremos maximizar la nitidez, por lo tanto minimizamos (-nitidez)
        return -calcular_nitidez(img)
    
    # Asumimos que k está en un rango razonable, por ejemplo entre 0.1 y 10
    resultado = minimize_scalar(funcion_objetivo, bounds=(0.1, 10.0), method='bounded')
    return resultado.x

# ==========================================
# PROCESAMIENTO PARA IMÁGENES TIF
# ==========================================
print("--- Procesando formato TIF ---")

# Leer imágenes TIF con tifffile
f6_tif = tiff.imread('./img/imagen6.tif').astype(float)
f7_tif = tiff.imread('./img/imagen7.tif').astype(float)

# Obtener magnitud de f6 y fase de f7
# Nota: Asumimos que f6 y f7 ya son las componentes de Fourier, u obtenemos su FFT si son espaciales.
# Si f6 y f7 son imágenes espaciales ordinarias, primero aplicamos FFT2:
F6_tif = np.fft.fftshift(np.fft.fft2(f6_tif))
F7_tif = np.fft.fftshift(np.fft.fft2(f7_tif))

magnitud_tif = np.abs(F6_tif)
fase_alterada_tif = np.angle(F7_tif)

# Búsqueda automática de k
k_optimo_tif = optimizar_k(magnitud_tif, fase_alterada_tif)
imagen_rec_tif = reconstruir_imagen(magnitud_tif, fase_alterada_tif, k_optimo_tif)

print(print(f"Factor k óptimo encontrado para TIF: {k_optimo_tif:.4f}"))
# Guardar el resultado en la carpeta output
guardar_imagen_png(imagen_rec_tif, 'resultado_recuperado_tif.png')
# Guardar o mostrar resultado (puedes usar matplotlib para visualizarlas)
# tiff.imwrite('recuperada_假tif.tif', imagen_rec_tif.astype(np.float32))

# ==========================================
# PROCESAMIENTO PARA IMÁGENES JPG
# ==========================================
print("\n--- Procesando formato JPG ---")

# Leer imágenes JPG usando Pillow y convertir a escala de grises
f6_jpg = np.array(Image.open('./img/imagen6.jpg').convert('L')).astype(float)
f7_jpg = np.array(Image.open('./img/imagen7.jpg').convert('L')).astype(float)

F6_jpg = np.fft.fftshift(np.fft.fft2(f6_jpg))
F7_jpg = np.fft.fftshift(np.fft.fft2(f7_jpg))

magnitud_jpg = np.abs(F6_jpg)
fase_alterada_jpg = np.angle(F7_jpg)

k_optimo_jpg = optimizar_k(magnitud_jpg, fase_alterada_jpg)
imagen_rec_jpg = reconstruir_imagen(magnitud_jpg, fase_alterada_jpg, k_optimo_jpg)

print(f"Factor k óptimo encontrado para JPG: {k_optimo_jpg:.4f}")
# Guardar el resultado en la carpeta output
guardar_imagen_png(imagen_rec_jpg, 'resultado_recuperado_jpg.png')
