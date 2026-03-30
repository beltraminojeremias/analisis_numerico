import numpy as np
from scipy.io import wavfile

def guardar_audio(nombre_archivo, fs, senal):
    # 1. Normalizar la señal para que el máximo sea 1.0 (evita saturación)
    # Usamos el valor absoluto máximo para mantener la simetría
    senal_norm = senal / np.max(np.abs(senal))
    
    # 2. Convertir a formato de 16 bits (PCM_16)
    # Esto escala el rango [-1, 1] al rango de enteros [-32768, 32767]
    senal_int16 = (senal_norm * 32767).astype(np.int16)
    
    # 3. Escribir el archivo
    wavfile.write(nombre_archivo, fs, senal_int16)
    print(f"Archivo guardado exitosamente como: {nombre_archivo}")

# Ejemplo de uso con las variables del paso anterior:
#guardar_audio('sirena1_filtrada.wav', fs, data_filtrada)