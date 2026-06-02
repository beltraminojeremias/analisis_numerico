#!/usr/bin/env python3
"""
Carga imágenes JPG desde img/ y calcula traslación
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
from scipy.fft import fft2, ifft2, fftshift
from matplotlib.colors import CenteredNorm
from scipy.signal import fftconvolve

# 📁 Directorio imágenes
IMG_DIR = Path('img/')

def cargar_imagenes(arch1, arch2):
    """
    Carga 2 imágenes JPG → escala de grises float [0,1]
    """
    img1 = np.array(Image.open(IMG_DIR / arch1).convert('L'))
    img2 = np.array(Image.open(IMG_DIR / arch2).convert('L'))
    
    # Normalizar [0,1]
    img1 = img1.astype(float) / 255
    img2 = img2.astype(float) / 255
    
    print(f"✅ {arch1}: {img1.shape}")
    print(f"✅ {arch2}: {img2.shape}")
    return img1, img2

def correlacion_fase(Img1, Img2):
    """
    Traslación por correlación de fase (FFT)
    """
    # Padding evitar wrap-around
    M, N = Img1.shape
    pad_M = 2*M; pad_N = 2*N
    Img1_pad = np.pad(Img1, ((pad_M//2,pad_M//2),(pad_N//2,pad_N//2)))
    Img2_pad = np.pad(Img2, ((pad_M//2,pad_M//2),(pad_N//2,pad_N//2)))
    
    # FFT2
    F1 = fft2(Img1_pad)
    F2 = fft2(Img2_pad)
    
    # Correlación de fase normalizada
    G = F1 * np.conj(F2) / (np.abs(F1) * np.abs(F2) + 1e-8)
    
    # Inversa → correlación
    corr = np.abs(fftshift(ifft2(G)))
    
    # Pico = traslación (centrar)
    yy, xx = np.unravel_index(np.argmax(corr), corr.shape)
    dx = xx - corr.shape[1]//2
    dy = yy - corr.shape[0]//2

    mostrar_correlacion_fase(F1, F2)
    
    return dx, dy, corr

def mostrar_correlacion_fase(F1, F2):
# 📊 Visualizar fase y diferencia de fase
    fig, axes = plt.subplots(2, 2, figsize=(11, 10))

    # Fase de la original (centrada)
    phase1 = np.angle(F1)
    axes[0,0].imshow(fftshift(phase1), cmap='hsv', interpolation='none') # hsv va bien para fase
    axes[0,0].set_title('Fase img. original (F1)')

    # Fase de la trasladada (centrada)
    phase2 = np.angle(F2)
    axes[0,1].imshow(fftshift(phase2), cmap='hsv', interpolation='none')
    axes[0,1].set_title('Fase img. trasladada (F2)')

    # Diferencia de fase (F1 - F2, centrada)
    diff_phase = np.angle(F1) - np.angle(F2)   # lineal si es solo traslación
    axes[1,0].imshow(fftshift(diff_phase), cmap='RdBu_r', interpolation='none', norm=CenteredNorm())
    axes[1,0].set_title('Diferencia de fase (F1 - F2)')

    # Fase de la correlación de fase (G)
    G = F1 * np.conj(F2) / (np.abs(F1) * np.abs(F2) + 1e-8)
    phase_G = np.angle(G)
    axes[1,1].imshow(fftshift(phase_G), cmap='hsv', interpolation='none')
    axes[1,1].set_title('Fase de G = F1·F2* (corr. de fase)')

    plt.tight_layout()
    plt.show()

# 🚀 USAR TUS IMÁGENES JPG
if __name__ == "__main__":
    # ⚠️ CAMBIÁ por tus archivos JPG
    img_orig, img_tras = cargar_imagenes('imagen1.jpg', 'imagen2.jpg')
    
    # FFT → correlación fase
    dx_fft, dy_fft, corr_map = correlacion_fase(img_orig, img_tras)
    
    # MOSTRAR RESULTADO
    plt.figure(figsize=(15, 5))
    plt.subplot(131); plt.imshow(img_orig, cmap='gray'); plt.title('Original')
    plt.subplot(132); plt.imshow(img_tras, cmap='gray'); plt.title('Trasladada')
    plt.subplot(133); plt.imshow(corr_map, cmap='hot')
    plt.plot(dx_fft+len(img_orig)//2, dy_fft+len(img_orig)//2, 'r*', ms=15)
    plt.title(f'Traslación FFT: dx={dx_fft}, dy={dy_fft}')
    plt.colorbar(); plt.tight_layout()
    plt.savefig('traslacion_fft.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"🎯 Traslación detectada: dx={dx_fft}, dy={dy_fft}")
