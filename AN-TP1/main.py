import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import convolve, firwin
import guardarSenal


# 1. Cargar señal
fs, data = wavfile.read('audios/sirena_1.wav')

# 2. Definir un filtro Pasa-Banda (FIR) por convolución
num_taps = 101  # Longitud del filtro
f_low, f_high = 400, 2000
# Crear los coeficientes del filtro
coeficientes = firwin(num_taps, [f_low, f_high], pass_zero=False, fs=fs)

# 3. Aplicar el filtro mediante convolución
data_filtrada = convolve(data, coeficientes, mode='same')
guardarSenal.guardar_audio('sirena1_filtrada.wav', fs, data_filtrada)

# 4. Graficar
t = np.linspace(0, len(data)/fs, len(data))
plt.figure(figsize=(12, 4))
plt.plot(t, data, label='Original (con ruido)', alpha=0.5)
plt.plot(t, data_filtrada, label='Filtrada', color='red')
plt.title("Señal en el Dominio del Tiempo")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.legend()
plt.show()

print(f"La frecuencia de muestreo es: {fs} Hz")