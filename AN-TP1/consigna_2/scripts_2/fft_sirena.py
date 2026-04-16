import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

def fft(filename, ventana=0, xinf=500, xsup=3500, yinf=0, ysup=None):
    # Cargar el archivo de audio
    fs, data = wavfile.read(filename)
    if data.ndim > 1:
        data = data[:, 0]  # Solo canal izquierdo si es estéreo
    N = len(data)

    if ventana == 0:
        yf = np.fft.fft(data)
        xf = np.fft.fftfreq(N, 1/fs)
        plt.figure(figsize=(10, 5))
        plt.plot(xf[:N//2], np.abs(yf[:N//2]))
        
        # --- AGREGAR ESTA LÍNEA PARA EL ZOOM ---
        plt.ylim(yinf, ysup)
        plt.xlim(xinf, xsup)
        # ---------------------------------------
        
        plt.title('FFT de toda la señal')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud')
        plt.grid()
        
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'imagenes'))
        os.makedirs(img_dir, exist_ok=True)
        img_path = os.path.join(img_dir, 'c2_fft_entera.png')
        plt.savefig(img_path)
        print(f"Imagen guardada en: {os.path.abspath(img_path)}")
        plt.show()
    else:
        muestras_ventana = int(ventana * fs)
        n_ventanas = N // muestras_ventana
        for i in range(n_ventanas):
            start = i * muestras_ventana
            end = start + muestras_ventana
            segmento = data[start:end]
            yf = np.fft.fft(segmento)
            xf = np.fft.fftfreq(muestras_ventana, 1/fs)
            plt.figure(figsize=(10, 5))
            plt.plot(xf[:muestras_ventana//2], np.abs(yf[:muestras_ventana//2]))
            
            plt.ylim(yinf, ysup)
            plt.xlim(xinf, xsup)
            
            plt.title(f'FFT ventana {i+1} ({start/fs:.2f}-{end/fs:.2f} s)')
            plt.xlabel('Frecuencia [Hz]')
            plt.ylabel('Magnitud')
            plt.grid()
            plt.show()

if __name__ == "__main__":
    # Ajusta la ruta a tu archivo sirena_1.wav
    audio_path = os.path.join(os.path.dirname(__file__), '..', 'audios', 'sirena_1.wav')
    # Prueba con ventana=0.5 para ver el efecto en los fragmentos
    fft(audio_path, ventana=0.5)