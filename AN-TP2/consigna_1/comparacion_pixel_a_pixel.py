import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift
import time
from PIL import Image

def desplazamiento_pixel_wise(I1, I2, max_d):
    """
    Estima el desplazamiento (dx, dy) de I2 respecto de I1
    buscando el par (dx, dy) que minimiza el error cuadrático medio
    en la zona de solapamiento.
    """
    M, N = I1.shape
    best_dx = 0
    best_dy = 0
    min_error = float('inf')

    for dy in range(-max_d, max_d + 1):
        for dx in range(-max_d, max_d + 1):
            # Zona de solapamiento
            y_src_start = max(0, -dy)
            y_src_end   = min(M, M - dy)
            x_src_start = max(0, -dx)
            x_src_end   = min(N, N - dx)

            if y_src_start >= y_src_end or x_src_start >= x_src_end:
                continue

            I1_crop = I1[y_src_start:y_src_end, x_src_start:x_src_end]
            I2_crop = I2[y_src_start+dy:y_src_end+dy,
                         x_src_start+dx:x_src_end+dx]

            diff = I1_crop - I2_crop
            error = np.mean(diff**2)

            if error < min_error:
                min_error = error
                best_dx = dx
                best_dy = dy

    return best_dx, best_dy, min_error

def desplazamiento_fft_phase_correlation(I1, I2):
    """
    Estima el desplazamiento (dx, dy) usando correlación de fase con FFT2D.
    """
    M, N = I1.shape

    # Zero-padding (opcional pero recomendable)
    pad_M = 2 * M
    pad_N = 2 * N
    pad_y = pad_M // 2
    pad_x = pad_N // 2

    I1_pad = np.pad(I1, ((pad_y, pad_y), (pad_x, pad_x)))
    I2_pad = np.pad(I2, ((pad_y, pad_y), (pad_x, pad_x)))

    # FFT2D
    F1 = fft2(I1_pad)
    F2 = fft2(I2_pad)

    # Correlación de fase normalizada
    eps = 1e-8
    G = F1 * np.conj(F2) / (np.abs(F1) * np.abs(F2) + eps)

    # Inversa -> mapa de correlación
    corr = np.abs(fftshift(ifft2(G)))

    # Pico de correlación
    yy, xx = np.unravel_index(np.argmax(corr), corr.shape)
    cy = corr.shape[0] // 2
    cx = corr.shape[1] // 2

    dy = yy - cy
    dx = xx - cx

    # Ojo: este (dx, dy) es el desplazamiento para alinear I2 con I1,
    # así que el desplazamiento real de I2 respecto de I1 es el opuesto:
    real_dx = -dx
    real_dy = -dy

    return real_dx, real_dy, corr
def cargar_gris(path):
    """Carga una imagen y la convierte a escala de grises float32 normalizada."""
    img = Image.open(path).convert("L")  # L = grayscale
    arr = np.array(img, dtype=np.float32)
    # opcional: normalizar a [0,1]
    arr /= 255.0
    return arr
if __name__ == "__main__":
    # 1) Crear imagen sintética
    # M, N = 256, 256
    # img1 = np.zeros((M, N), dtype=float)
    # Un rectángulo blanco en el centro
    # img1[80:120, 100:150] = 1.0

    # 2) Definir un desplazamiento conocido
    true_dx = 40   # derecha
    true_dy = 10   # abajo

    # 3) Crear imagen trasladada
    # img2 = trasladar_imagen(img1, true_dx, true_dy)
    img1 = cargar_gris("img/imagen1.jpg")
    img2 = cargar_gris("img/imagen2.jpg")

    # 4) Estimar desplazamiento por comparación pixel a pixel
    max_d = 128  # rango de búsqueda
    t0 = time.time()
    pw_dx, pw_dy, pw_err = desplazamiento_pixel_wise(img1, img2, max_d=max_d)
    t1 = time.time()

    # 5) Estimar desplazamiento por correlación de fase (FFT2D)
    t2 = time.time()
    fft_dx, fft_dy, corr = desplazamiento_fft_phase_correlation(img1, img2)
    t3 = time.time()

    print("Desplazamiento real   : dx = {}, dy = {}".format(true_dx, true_dy))
    print("Pixel-wise estimado   : dx = {}, dy = {}, error = {:.6f}, tiempo = {:.3f} s"
          .format(pw_dx, pw_dy, pw_err, t1 - t0))
    print("FFT fase estimado     : dx = {}, dy = {}, tiempo = {:.3f} s"
          .format(fft_dx, fft_dy, t3 - t2))

    # 6) Mostrar las imágenes y el mapa de correlación (opcional)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title('Imagen 1')
    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title('Imagen 2 (trasladada)')
    axes[2].imshow(corr, cmap='hot')
    axes[2].set_title('Mapa de correlación (FFT)')
    for ax in axes:
        ax.axis('off')
    plt.tight_layout()
    plt.show()
