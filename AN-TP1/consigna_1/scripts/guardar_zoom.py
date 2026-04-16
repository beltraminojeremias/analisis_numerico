
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import os

def guardar_zooms_png(archivo, intervalos, win_dur=0.05, prefix='zoom', 
                     directorio_img='imagenes/', color='yellow', prominence=0.25, 
                     height=0.35, min_dist=20, directorio_audio='audios/', show=False):
    """
    GUARDA zooms como PNG individuales (no muestra).
    
    - prefix: str, ej 'sirena2' → sirena2_0.png, sirena2_1.png...
    - directorio_img: guarda aquí
    - show=True: preview antes guardar
    """
    # Crear directorio
    os.makedirs(directorio_img, exist_ok=True)
    
    path_audio = f"{directorio_audio}{archivo}"
    fs, signal = wavfile.read(path_audio)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    print(f"Guardando {len(intervalos)} zooms de {archivo}...")
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal): 
            print(f"Skip {t_start}s")
            continue
        
        ventana = signal[idx_start:idx_end]
        t_vent = np.arange(len(ventana)) / fs + t_start
        
        # Picos
        picos_idx, _ = find_peaks(ventana, prominence=prominence, height=height, distance=min_dist)
        n_picos = len(picos_idx)
        n_periodos = max(0, n_picos - 1)
        freq_est = n_periodos / win_dur if n_periodos > 0 else 0
        
        # Figura individual
        plt.figure(figsize=(10, 4))
        plt.plot(t_vent, ventana, color=color, linewidth=1, label=f'{n_picos} picos ({freq_est:.0f} Hz)')
        
        if n_picos > 0:
            plt.plot(t_vent[picos_idx], ventana[picos_idx], 'ro', markersize=3)
            for j, idx in enumerate(picos_idx):
                plt.text(t_vent[idx], ventana[idx]+0.02, str(j+1), fontsize=10, 
                        fontweight='normal', color='black', ha='center', va='bottom')
        
        plt.title(f'{prefix}_{i} | t={t_start:.1f}s | {n_picos} picos | {freq_est:.0f} Hz')
        plt.xlabel('Tiempo [s]'); plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3); plt.legend()
        plt.xlim(t_start, t_start + win_dur)
        
        # Guardar
        filename = f"{directorio_img}{prefix}_{i}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()  # Cierra figura (no memoria)
        
        print(f"Guardado: {filename}")
    
    if show:
        plt.show()  # Solo si quieres preview
    
    print(f"¡Completado! Imágenes en {directorio_img}")

# Uso
# guardar_zooms_png('sirena_2.wav', [0,1,2,3,4,5], prefix='sirena2_zooms', show=False)
# → imagenes/sirena2_zooms_0.png ... sirena2_zooms_5.png
