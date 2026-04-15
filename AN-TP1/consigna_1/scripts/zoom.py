import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks  # Esencial para picos
import matplotlib.pyplot as plt

def zoom_ventanas_audio(archivo, intervalos, win_dur=0.05, color='yellow', 
                       prominence=0.1, directorio='audios/'):
    """
    Grafica zooms de ventanas fijas en audio (1+ intervalos).
    
    Parameters:
    - intervalos: list/array, ej: [3] (solo 3s) o [0,1,2,3]
    - color: str, color línea (default 'yellow')
    """
    path = f"{directorio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    print(f"{archivo}: fs={fs} Hz, total={len(signal)/fs:.2f}s")
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    
    plt.figure(figsize=(15, 2 + len(intervalos)*1.5))
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal):
            print(f"Intervalo {t_start}s excede")
            continue
        
        ventana = signal[idx_start:idx_end]
        t_vent = np.arange(len(ventana)) / fs + t_start
        
        plt.subplot(len(intervalos), 1, i+1)
        plt.plot(t_vent, ventana, color=color, linewidth=1)
        plt.title(f'Zoom {win_dur}s en t={t_start:.1f}s')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3)
        plt.xlim(t_start, t_start + win_dur)
    
    plt.tight_layout()
    plt.show()
    
    return fs, signal


def zoom_ventanas_audio_con_contador(archivo, intervalos, win_dur=0.05, color='yellow', 
                       prominence=0.2, height=0.3, min_dist=10, directorio='audios/'):
    """
    Zoom robusto: filtra ruido con prominence/height/distancia.
    - prominence: 0.15-0.4 (altura pico vs valles)
    - height: 0.2-0.6 (amplitud mínima)
    - min_dist: muestras mín. entre picos (~fs/2*freq)
    """
    path = f"{directorio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    print(f"{archivo}: fs={fs} Hz, total={len(signal)/fs:.2f}s")
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    
    plt.figure(figsize=(15, 2.5 + len(intervalos)*1.8))
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal): continue
        
        ventana = signal[idx_start:idx_end]
        t_vent = np.arange(len(ventana)) / fs + t_start
        
        # find_peaks robusto (solo sirena)
        picos_idx, props = find_peaks(ventana, 
                                    prominence=prominence,
                                    height=height,
                                    distance=min_dist)
        n_picos = len(picos_idx)
        n_periodos = max(0, n_picos - 1)
        freq_est = n_periodos / win_dur if n_periodos > 0 else 0
        
        plt.subplot(len(intervalos), 1, i+1)
        plt.plot(t_vent, ventana, color=color, linewidth=1, label=f'{n_picos} picos ({freq_est:.0f} Hz)')
        
        if n_picos > 0:
            plt.plot(t_vent[picos_idx], ventana[picos_idx], 'ro', markersize=8)
            # for j, idx in enumerate(picos_idx):
                # plt.annotate(str(j+1), (t_vent[idx], ventana[idx]), 
                #            xytext=(8, 8), textcoords='offset points', 
                #            fontsize=12, fontweight='bold',
                #            bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
            for j, idx in enumerate(picos_idx):
                plt.text(t_vent[idx], ventana[idx]+0.02, str(j+1), 
                        fontsize=10, fontweight='bold', color='red',
                        ha='center', va='bottom', zorder=10)   
        
        plt.title(f'Ventana t={t_start:.1f}s | Picos: {n_picos} | Freq: {freq_est:.0f} Hz')
        plt.xlabel('Tiempo [s]'); plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3); plt.legend()
        plt.xlim(t_start, t_start + win_dur)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Paráms: prominence={prominence}, height={height}, dist={min_dist}")
    return fs, signal

# Uso optimizado para sirena ~1kHz (ajusta params)
# zoom_ventanas_audio_con_contador('sirena_2.wav', [3], prominence=0.25, height=0.35, min_dist=20)
# Uso (ajusta prominence según amplitud)

# Uso
# zoom_ventanas_audio('sirena_2.wav', [3])  # Solo 3s, amarillo default
# zoom_ventanas_audio('sirena_2.wav', [3], color='red')  # Solo 3s, rojo
# zoom_ventanas_audio('sirena_2.wav', [0, 3, 7], color='cyan')  # Múltiples, cyan
