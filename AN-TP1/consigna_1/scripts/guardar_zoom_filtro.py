import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks, firwin
import matplotlib.pyplot as plt
import os

def guardar_zooms_filtrada(archivo, intervalos, win_dur=0.05, prefix='zoom_filt', 
                          directorio_img='imagenes/', low_cut=300, high_cut=3000,
                          color_orig='orange', color_filt='#00AAFF', prominence=0.25,
                          directorio_audio='audios/', show=False):
    """
    GUARDA zooms ORIGINAL + FILTRADA (FIR pasa-banda) lado a lado.
    """
    os.makedirs(directorio_img, exist_ok=True)
    
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal_orig = signal.astype(np.float32) / np.max(np.abs(signal))
    
    # Filtro FIR pasa-banda
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    numtaps = 201
    fir_filt = firwin(numtaps, [low, high], pass_zero=False)
    signal_filt = np.convolve(signal_orig, fir_filt, mode='same')
    signal_filt /= np.max(np.abs(signal_filt))  # Renormalizar
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    print(f"Filtrado {low_cut}-{high_cut}Hz | Guardando {len(intervalos)} zooms...")
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal_orig))
        if idx_start >= len(signal_orig): continue
        
        # Ventanas
        t_vent = np.arange(idx_end-idx_start) / fs + t_start
        orig_win = signal_orig[idx_start:idx_end]
        filt_win = signal_filt[idx_start:idx_end]
        
        # Picos FILTRADA (más limpia)
        # picos_idx, _ = find_peaks(filt_win, prominence=prominence)
        # n_picos = len(picos_idx)
        # n_periodos = max(0, n_picos - 1)
        # freq_est = n_periodos / win_dur if n_periodos > 0 else 0
        
# Nuevo bloque de figura (reemplaza en guardar_zooms_filtrada):
        plt.figure(figsize=(12, 6))

        plt.plot(t_vent, orig_win, color=color_orig, linewidth=1.5, label=f'Original', alpha=0.8)
        plt.plot(t_vent, filt_win, color=color_filt, linewidth=2, label=f'Filtrada {low_cut}-{high_cut}Hz')

        plt.title(f'{prefix}_{i} | t={t_start:.1f}s | Original vs Filtrada')
        plt.xlabel('Tiempo [s]'); plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(t_start, t_start + win_dur)

# Guardar
        filename = f"{directorio_img}{prefix}_{i}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Guardado: {filename}")
    
    if show: plt.show()
    print(f"¡Listo! Filtro {low_cut}-{high_cut}Hz aplicado.")

# Uso
# guardar_zooms_filtrada('sirena_2.wav', [0,1,2,3,4,5], prefix='sirena2_filt',
#                       low_cut=200, high_cut=3500, color_orig='orange', color_filt='cyan')
