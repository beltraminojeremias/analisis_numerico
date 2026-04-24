import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import os

def fft_larga_sirena2(archivo, win_dur=2.0, directorio_audio='audios/', 
                     directorio_img='imagenes/', prefix='fft_larga', save=True):
    """
    FFT VENTANA LARGA sirena2 (promedia chirp Doppler).
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.arange(0, len(signal)/fs, win_dur)[:3]  # 3 ventanas largas
    
    plt.figure(figsize=(15, 8))
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        ventana = signal[idx_start:idx_end]
        
        N = len(ventana)
        yf = fft(ventana)
        xf = fftfreq(N, 1/fs)[:N//2]
        mag_fft = 20 * np.log10(np.abs(yf[:N//2]) + 1e-10)
        
        plt.subplot(3, 1, i+1)
        plt.plot(xf, mag_fft)
        plt.title(f'FFT LARGA t={t_start:.1f}-{t_start+win_dur:.1f}s')
        plt.xlabel('Frecuencia [Hz]'); plt.ylabel('Magnitud [dB]')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 3000)
    
    plt.tight_layout()
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✅ FFT Larga guardado: {filename}")
        plt.close()
    else:
        plt.show()
    
    print("OBSERVACIÓN: Pico central ~borroso (promedio chirp)")
    return fs

def fft_corta_sirena2(archivo, win_dur=0.1, directorio_audio='audios/', 
                     directorio_img='imagenes/', prefix='fft_corta', save=True):
    """
    FFT VENTANA CORTA sirena2 (múltiples frecuencias).
    """
    path = f"{directorio_audio}/{archivo}"
    fs, signal = wavfile.read(path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.arange(0, 5, 0.5)  # 10 ventanas cortas
    
    plt.figure(figsize=(15, 12))
    
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
        plt.title(f'FFT CORTA t={t_start:.2f}-{t_start+win_dur:.2f}s')
        plt.xlabel('Frecuencia [Hz]'); plt.ylabel('Magnitud [dB]')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 3000)
        
        # Pico dominante
        idx_pico = np.argmax(mag_fft)
        f_pico = xf[idx_pico]
        plt.axvline(f_pico, color='red', linestyle='--', alpha=0.7,
                   label=f'{f_pico:.0f}Hz')
        plt.legend(fontsize=8)
    
    plt.tight_layout()
    
    if save:
        os.makedirs(directorio_img, exist_ok=True)
        filename = f"{directorio_img}/{prefix}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✅ FFT Corta guardado: {filename}")
        plt.close()
    else:
        plt.show()
    
    print("OBSERVACIÓN: Picos cambian posición (Doppler)")
    return fs

# Uso directo
if __name__ == "__main__":
    fft_larga_sirena2('sirena_2.wav', win_dur=2.0)
    fft_corta_sirena2('sirena_2.wav', win_dur=0.1)
