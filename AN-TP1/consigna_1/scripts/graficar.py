import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def graficar_tiempo(archivo, dur_show=None, directorio='audios/', filtrada=False):
    """
    Grafica señal de audio en dominio tiempo (completa o primeros Xs).
    
    Parameters:
    - archivo: str, nombre .wav
    - dur_show: float, duración mostrar [s] (None=total)
    - directorio: str, path base
    - filtrada: bool, si es versión filtrada (título)
    """
    path = f"{directorio}{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    t_total = len(signal) / fs
    if dur_show is None:
        dur_show = t_total
        idx_max = len(signal)
    else:
        idx_max = min(int(dur_show * fs), len(signal))
    
    t = np.arange(idx_max) / fs
    
    plt.figure(figsize=(12, 4))
    plt.plot(t, signal[:idx_max])
    plt.title(f'{archivo} - Dominio Tiempo {"(Filtrada)" if filtrada else "(Original)"}')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud normalizada')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, dur_show)
    plt.tight_layout()
    plt.show()
    
    print(f"fs: {fs} Hz | Duración mostrada: {dur_show:.2f}s / Total: {t_total:.2f}s")
    return fs, signal[:idx_max]

# Uso
# Original completa primeros 10s
graficar_tiempo('sirena_1.wav', dur_show=10)

# Filtrada total
# graficar_tiempo('sirena_1_filtrada.wav', filtrada=True)
