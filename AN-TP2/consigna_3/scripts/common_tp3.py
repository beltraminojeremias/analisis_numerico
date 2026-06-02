from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.transform import warp_polar
from skimage.registration import phase_cross_correlation

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "salida_punto3"
OUT_DIR.mkdir(exist_ok=True)
F1_PATH = BASE_DIR / "imagen1.jpg"
F5_PATH = BASE_DIR / "imagen5.jpg"

def leer_gris(path):
    """Lee una imagen como matriz de intensidades normalizadas en [0,1]."""
    return np.array(Image.open(path).convert("L")).astype(np.float32) / 255.0

def guardar_par(a,b,t1,t2,nombre,cmap="gray",aspect=None,axis_off=True):
    fig, axs = plt.subplots(1,2,figsize=(11,5))
    axs[0].imshow(a,cmap=cmap,aspect=aspect); axs[0].set_title(t1)
    axs[1].imshow(b,cmap=cmap,aspect=aspect); axs[1].set_title(t2)
    if axis_off:
        axs[0].axis("off"); axs[1].axis("off")
    else:
        axs[0].set_xlabel("x"); axs[0].set_ylabel("y")
        axs[1].set_xlabel("x"); axs[1].set_ylabel("y")
    plt.tight_layout()
    ruta = OUT_DIR / nombre
    plt.savefig(ruta, dpi=180)
    plt.show()
    return ruta

def guardar_img(a,titulo,nombre,cmap="gray",aspect=None,axis_off=True,mark=None):
    fig, ax = plt.subplots(figsize=(7,5))
    ax.imshow(a,cmap=cmap,aspect=aspect); ax.set_title(titulo)
    if mark is not None:
        fila, col = mark
        ax.scatter([col],[fila],s=150,marker="x")
    if axis_off:
        ax.axis("off")
    else:
        ax.set_xlabel("columna"); ax.set_ylabel("fila")
    plt.tight_layout()
    ruta = OUT_DIR / nombre
    plt.savefig(ruta, dpi=180)
    plt.show()
    return ruta

def preparar_fft(img):
    """Resta promedio, aplica ventana Hann, calcula FFT2 centrada y magnitudes."""
    h,w = img.shape
    ventana = np.outer(np.hanning(h), np.hanning(w))
    preparada = (img - img.mean()) * ventana
    F = np.fft.fftshift(np.fft.fft2(preparada))
    magnitud = np.abs(F)
    magnitud_log = np.log1p(magnitud)
    return preparada, ventana, F, magnitud, magnitud_log

def a_logpolar(magnitud_log):
    h,w = magnitud_log.shape
    centro = (h/2, w/2)
    radio_maximo = min(h,w)//2
    muestras_angulares = 360
    muestras_radiales = radio_maximo
    lp = warp_polar(
        magnitud_log,
        center=centro,
        radius=radio_maximo,
        output_shape=(muestras_angulares, muestras_radiales),
        scaling="log"
    )
    return lp, centro, radio_maximo, muestras_angulares, muestras_radiales

def correlacion_fase_manual(A,B):
    FA = np.fft.fft2(A)
    FB = np.fft.fft2(B)
    producto = FA * np.conj(FB)
    normalizado = producto / (np.abs(producto) + 1e-12)
    corr = np.abs(np.fft.ifft2(normalizado))
    return corr
