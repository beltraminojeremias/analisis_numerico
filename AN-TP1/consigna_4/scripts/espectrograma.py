import numpy as np
from scipy.io import wavfile
from scipy.signal import stft
import matplotlib.pyplot as plt
import os
from pathlib import Path

def espectrograma_sirena2(archivo, nperseg=1024, noverlap=512, directorio_img='imagenes/', 
                         directorio_audio='audios/', prefix='stft_sirena2', save=True):
    """
    Espectrograma STFT sirena2 + rastreo frecuencia fundamental.
    
    Parámetros óptimos:
    - nperseg=1024: ventana Hann ~23ms (buen compromiso tiempo-frec)
    - noverlap=512: 50% overlap (suave)
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    # STFT
    f, t, Zxx = stft(signal, fs=fs, nperseg=nperseg, noverlap=noverlap, 
                     window='hann', nfft=nperseg)
    
    # Espectrograma (dB)
    S_db = 20 * np.log10(np.abs(Zxx) + 1e-10)
    
    plt.figure(figsize=(15, 6))
    plt.pcolormesh(t, f/1000, S_db, shading='gouraud', cmap='viridis')
    plt.title(f'Espectrograma STFT - {archivo} (nperseg={nperseg}, overlap={noverlap/ nperseg*100:.0f}%)')
    plt.ylabel('Frecuencia [kHz]')
    plt.xlabel('Tiempo [s]')
    plt.colorbar(label='Intensidad [dB]')
    plt.ylim(0, 3)  # Zoom 0-3kHz (sirena)
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}.png"
        plt.savefig(filename, dpi=200, bbox_inches='tight')
        print(f"✅ Espectrograma guardado: {filename}")
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
    
    # Rastreo visual frecuencia fundamental (MANUAL)
    print("📊 ANÁLISIS:")
    print(f"fs: {fs}Hz | Duración: {len(signal)/fs:.1f}s")
    print(f"Freq bins: 0-{fs/2/1000:.0f}kHz | Tiempo: {t[-1]:.1f}s")
    print("🔍 RASTREA VISUALMENTE: ridge central sirena ~1kHz → punto medio oscilación")
    
    return f, t, S_db, fs

def calcular_velocidad_doppler(f_promedio, f_emision=1000, c_sonido=343):
    """
    Velocidad móvil Doppler (aprox).
    f_promedio: freq media observada (punto medio oscilación)
    f_emision: freq nominal sirena (~1000Hz)
    """
    delta_f = f_promedio - f_emision
    v = (c_sonido * delta_f) / f_emision  # Aprox. v << c
    return v * 3.6  # m/s → km/h

# Uso
if __name__ == "__main__":
    espectrograma_sirena2('sirena_2.wav', nperseg=1024, noverlap=512)
