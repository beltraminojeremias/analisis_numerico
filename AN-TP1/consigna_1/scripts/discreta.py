import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

def graficar_discreta(archivo, intervalos=[0], win_dur=0.05, directorio_img='imagenes/', 
                     directorio_audio='audios/', prefix='discreta', save=False):
    """
    Grafica señal DISCRETA en ventanas (stem plot SOLO LÍNEAS).
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    
    plt.figure(figsize=(15, 2 + len(intervalos)*1.5))
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal):
            print(f"Intervalo {t_start}s excede")
            continue
        
        t_zoom = np.arange(idx_end-idx_start) / fs + t_start
        signal_zoom = signal[idx_start:idx_end]
        
        plt.subplot(len(intervalos), 1, i+1)
        # STEM SOLO LÍNEAS GRIS (SIN PUNTOS)
        plt.stem(t_zoom, signal_zoom, 
                linefmt='gray',     # Líneas GRIS
                markerfmt=' ',      # SIN marcadores
                basefmt=' ')
        
        plt.title(f'Discreta t={t_start:.1f}s | {win_dur}s | fs={fs}Hz')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3)
        plt.xlim(t_start, t_start + win_dur)
    
    plt.tight_layout()
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}_{int(win_dur*1000)}ms.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✅ Guardado: {filename}")
        plt.close()
    else:
        plt.show()
    
    print(f"fs: {fs}Hz | Ventanas: {len(intervalos)}")
    return fs, signal

if __name__ == "__main__":
    graficar_discreta('sirena_1.wav', intervalos=[0], win_dur=0.5, save=True)
