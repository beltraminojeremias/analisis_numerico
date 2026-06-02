from common_tp3 import *

print("PASO 2 - FFT 2D y magnitud del espectro")
f1 = leer_gris(F1_PATH)
f5 = leer_gris(F5_PATH)
prep1, ventana, F1, M1, M1log = preparar_fft(f1)
prep5, _, F5, M5, M5log = preparar_fft(f5)
print("Formula conceptual: F(u,v) = sum_x sum_y f(x,y) exp(-j 2pi (ux/M + vy/N))")
print("Se resta el promedio, se aplica ventana Hann y se calcula FFT2 centrada con fftshift.")
print("Luego se obtiene |F| y para visualizar log(1 + |F|).")
guardar_img(ventana, "Ventana Hann 2D", "02_ventana_hann_2d.png")
guardar_par(prep1, prep5, "f1 preparada para FFT", "f5 preparada para FFT", "03_imagenes_preparadas_fft.png")
guardar_par(M1log, M5log, "log(1 + |FFT2(f1)|)", "log(1 + |FFT2(f5)|)", "04_magnitudes_fft_log.png")
