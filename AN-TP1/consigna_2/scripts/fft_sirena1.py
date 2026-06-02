import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import os

def fft_global_sirena1(archivo, directorio_audio='audios/', directorio_img='imagenes/', 
                      prefix='fft_global', save=True):
    """
    FFT GLOBAL sirena1 (señal completa).
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    # FFT completa
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1/fs)[:N//2]
    mag_fft = 20 * np.log10(np.abs(yf[:N//2]) + 1e-10)
    
    plt.figure(figsize=(14, 5))
    plt.plot(xf, mag_fft)
    plt.title(f'FFT GLOBAL - {archivo} (fs={fs}Hz)')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 3000)
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✅ FFT Global guardado: {filename}")
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
    
    # Pico dominante
    idx_pico = np.argmax(mag_fft)
    f_pico = xf[idx_pico]
    print(f"🌊 PICO DOMINANTE: {f_pico:.0f} Hz")
    
    return fs, xf, mag_fft, f_pico

def fft_ventanas_sirena1(archivo, intervalos=[0], win_dur=0.5, directorio_audio='audios/', 
                        directorio_img='imagenes/', prefix='fft_ventana', save=True):
    """
    FFT en ventanas 0.5s sirena1.
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    
    plt.figure(figsize=(15, 2 + len(intervalos)*2))
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        if idx_start >= len(signal): continue
        
        ventana = signal[idx_start:idx_end]
        N = len(ventana)
        yf = fft(ventana)
        xf = fftfreq(N, 1/fs)[:N//2]
        mag_fft = 20 * np.log10(np.abs(yf[:N//2]) + 1e-10)
        
        plt.subplot(len(intervalos), 1, i+1)
        plt.plot(xf, mag_fft)
        plt.title(f'FFT Ventana t={t_start:.1f}s ({win_dur}s)')
        plt.xlabel('Frecuencia [Hz]'); plt.ylabel('Magnitud [dB]')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 3000)
        
        # Pico dominante ventana
        idx_pico = np.argmax(mag_fft)
        f_pico = xf[idx_pico]
        plt.axvline(f_pico, color='red', linestyle='--', alpha=0.7, 
                   label=f'Pico: {f_pico:.0f}Hz')
        plt.legend()
    
    plt.tight_layout()
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✅ FFT Ventanas guardado: {filename}")
        plt.close()
    else:
        plt.show()
    
    print(f"fs: {fs}Hz | Ventanas: {len(intervalos)}")
    return fs

def calcular_velocidad_constante(f_observada, f_emision=1000, c_sonido=343):
    """Velocidad Doppler (sirena1 constante)."""
    delta_f = f_observada - f_emision
    v = (c_sonido * delta_f) / f_emision
    return abs(v * 3.6)  # km/h

# Uso directo
if __name__ == "__main__":
    fft_global_sirena1('sirena_1.wav')
    fft_ventanas_sirena1('sirena_1.wav', intervalos=[0, 2, 4])
