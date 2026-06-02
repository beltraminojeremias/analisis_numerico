from common_tp3 import *

print("PASO 1 - Carga de imagenes")
f1 = leer_gris(F1_PATH)
f5 = leer_gris(F5_PATH)
print(f"f1: {f1.shape[1]} x {f1.shape[0]} pixeles")
print(f"f5: {f5.shape[1]} x {f5.shape[0]} pixeles")
print("Cada imagen se transforma en una matriz de intensidades normalizadas en [0,1].")
guardar_par(f1, f5, "f1 - imagen de referencia", "f5 - imagen escalada", "01_imagenes_originales.png")
