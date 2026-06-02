import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from PIL import Image
import os
import tifffile

# ============================
# Utilidades
# ============================

def guardar_gris(img, path):
    """Guarda una imagen en escala de grises [0,1] como PNG/JPG."""
    img_clipped = np.clip(img, 0, 1)
    img_uint8 = (img_clipped * 255).astype(np.uint8)
    Image.fromarray(img_uint8).save(path)

def metrica_nitidez(img):
    """
    Métrica de nitidez: magnitud del gradiente promedio.
    """
    gx = ndimage.sobel(img, axis=1, mode='reflect')
    gy = ndimage.sobel(img, axis=0, mode='reflect')
    grad_mag = np.hypot(gx, gy)
    return np.mean(grad_mag)

def buscar_k_optimo(magnitud, fase, k_min=0.01, k_max=1.0, k_step=0.01, verbose=False):
    """
    Recorre valores de k en [k_min, k_max] y devuelve:
    - k_opt: valor de k que maximiza la nitidez
    - I_best: imagen reconstruida con k_opt
    - max_nitidez: valor máximo de la métrica de nitidez
    """
    k_vals = np.arange(k_min, k_max + k_step, k_step)
    mejor_k = k_min
    max_nitidez = -np.inf
    I_best = None

    for k in k_vals:
        fase_k = k * fase
        F_k = magnitud * np.exp(1j * fase_k)
        I_k = np.fft.ifft2(F_k)
        I_k = np.abs(I_k)

        nitidez = metrica_nitidez(I_k)

        if verbose:
            print(f"k = {k:.3f}, nitidez = {nitidez:.6f}")

        if nitidez > max_nitidez:
            max_nitidez = nitidez
            mejor_k = k
            I_best = I_k

    return mejor_k, I_best, max_nitidez

def cargar_y_procesar_par(f6_path, f7_path, k_min=0.01, k_max=1.0, k_step=0.01, verbose=False):
    """
    Carga f6 y f7, calcula FFT2, separa magnitud y fase,
    busca k óptimo y devuelve (k_opt, imagen_recuperada).
    Suponemos:
    - magnitud: de f6
    - fase: de f7 (fase comprimida por k)
    """
    # Determinar si es TIF o JPG (por extensión)
    ext6 = f6_path.lower()
    ext7 = f7_path.lower()

    # Cargar f6
    if ext6.endswith(".tif") or ext6.endswith(".tiff"):
        img6 = tifffile.imread(f6_path).astype(np.float64)
    else:
        img6 = np.array(Image.open(f6_path).convert("L"), dtype=np.float64)

    # Cargar f7
    if ext7.endswith(".tif") or ext7.endswith(".tiff"):
        img7 = tifffile.imread(f7_path).astype(np.float64)
    else:
        img7 = np.array(Image.open(f7_path).convert("L"), dtype=np.float64)

    # Normalizar [0,1]
    img6 = img6 / 255.0
    img7 = img7 / 255.0

    # Asegurar mismo tamaño
    if img6.shape != img7.shape:
        raise ValueError(f"Las imágenes deben tener el mismo tamaño. "
                         f"f6: {img6.shape}, f7: {img7.shape}")

    print(f"Procesando par:\n  magnitud = {f6_path}\n  fase     = {f7_path}")

    # FFT2D
    F6 = np.fft.fft2(img6)
    F7 = np.fft.fft2(img7)

    magnitud = np.abs(F6)
    fase = np.angle(F7)

    # Buscar k óptimo
    k_opt, I_best, max_nit = buscar_k_optimo(magnitud, fase,
                                             k_min=k_min, k_max=k_max,
                                             k_step=k_step,
                                             verbose=verbose)

    print(f"  k_opt = {k_opt:.4f}, nitidez = {max_nit:.6f}")
    return k_opt, I_best

# ============================
# Script principal
# ============================

if __name__ == "__main__":
    # Características TIF / JPG
    base_dir = "./img"
    out_dir = "./output"
    os.makedirs(out_dir, exist_ok=True)

    # Rutas de entrada
    f6_tif = os.path.join(base_dir, "imagen6.tif")   # magnitud
    f7_tif = os.path.join(base_dir, "imagen7.tif")   # fase
    f6_jpg = os.path.join(base_dir, "imagen6.jpg")   # magnitud
    f7_jpg = os.path.join(base_dir, "imagen7.jpg")   # fase

    # Rango de k
    k_min = 0.01
    k_max = 1.0
    k_step = 0.01

    # ---- Formato TIF ----
    print("\n=== TIF ===")
    k_tif, img_tif = cargar_y_procesar_par(f6_tif, f7_tif,
                                           k_min=k_min, k_max=k_max,
                                           k_step=k_step,
                                           verbose=False)

    out_tif_path = os.path.join(out_dir, f"recuperada_TIF_k_{k_tif:.2f}.png")
    guardar_gris(img_tif, out_tif_path)
    print(f"Imagen TIF recuperada guardada en: {out_tif_path}")

    # ---- Formato JPG ----
    print("\n=== JPG ===")
    k_jpg, img_jpg = cargar_y_procesar_par(f6_jpg, f7_jpg,
                                           k_min=k_min, k_max=k_max,
                                           k_step=k_step,
                                           verbose=False)

    out_jpg_path = os.path.join(out_dir, f"recuperada_JPG_k_{k_jpg:.2f}.png")
    guardar_gris(img_jpg, out_jpg_path)
    print(f"Imagen JPG recuperada guardada en: {out_jpg_path}")

    print(f"\nResultado TIF: k_opt = {k_tif:.4f}")
    print(f"Resultado JPG: k_opt = {k_jpg:.4f}")

    # Mostrar resultados
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img_tif, cmap="gray")
    axes[0].set_title(f"TIF: imagen recuperada (k = {k_tif:.2f})")
    axes[0].axis("off")

    axes[1].imshow(img_jpg, cmap="gray")
    axes[1].set_title(f"JPG: imagen recuperada (k = {k_jpg:.2f})")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()
