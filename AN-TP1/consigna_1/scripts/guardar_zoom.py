import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

def guardar_zooms_png(archivo, intervalos, win_dur=0.05, prefix='zoom', 
                     directorio_img='imagenes/', color='yellow', 
                     directorio_audio='audios/', show=False):
    """
    GUARDA zooms SIN PICOS como PNG individuales (señal limpia).
    """
    os.makedirs(directorio_img, exist_ok=True)
    
    path_audio = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path_audio)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    print(f"Guardando {len(intervalos)} zooms SIN PICOS de {archivo}...")
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal): 
            print(f"Skip {t_start}s")
            continue
        
        ventana = signal[idx_start:idx_end]
        t_vent = np.arange(len(ventana)) / fs + t_start
        
        # Figura limpia SIN picos
        plt.figure(figsize=(10, 4))
        plt.plot(t_vent, ventana, color=color, linewidth=1.5)
        
        plt.title(f'{prefix}_{i} | t={t_start:.1f}s | fs={fs}Hz')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3)
        plt.xlim(t_start, t_start + win_dur)
        
        filename = f"{directorio_img}/{prefix}_{i}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ Guardado: {filename}")
    
    print(f"¡Completado! {len(intervalos)} zooms limpios en {directorio_img}")

# Uso
