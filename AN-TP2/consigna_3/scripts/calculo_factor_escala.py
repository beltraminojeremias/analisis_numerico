from common_tp3 import *
import numpy as np

print("PASO 5 - Conversion del desplazamiento log-radial a factor de escala")
f1 = leer_gris(F1_PATH)
f5 = leer_gris(F5_PATH)
_, _, _, _, M1log = preparar_fft(f1)
_, _, _, _, M5log = preparar_fft(f5)
LP1, centro, radio_maximo, nang, nrad = a_logpolar(M1log)
LP5, _, _, _, _ = a_logpolar(M5log)
shift, error, phasediff = phase_cross_correlation(LP1, LP5, upsample_factor=10)
delta_rho = float(shift[1])
k_log = nrad / np.log(radio_maximo)
factor = np.exp(delta_rho / k_log)
factor_inverso = 1.0 / factor
print(f"Delta_rho = {delta_rho:.3f}")
print(f"k_log = nrad / ln(radio_maximo) = {nrad} / ln({radio_maximo}) = {k_log:.6f}")
print(f"factor = exp(Delta_rho / k_log) = {factor:.6f}")
print(f"factor inverso para compensar = {factor_inverso:.6f}")
print(f"Interpretacion: f5 se estima escalada respecto de f1 por factor {factor:.4f}.")
