#!/usr/bin/env python3
"""
TP Procesamiento Señales - CONSIGNA 2: FFT Sirena1
"""

from config import AUDIOS_DIR, IMG_DIR
from scripts.fft_sirena1 import fft_global_sirena1, fft_ventanas_sirena1, calcular_velocidad_constante

def main():
    print("🔬 === CONSIGNA 2: FFT SIRENA1 ===")
    
    # 1. FFT GLOBAL sirena1
    print("\n📈 1. FFT Global...")
    fs, xf, mag_fft, f_pico_global = fft_global_sirena1('sirena_1.wav',
                                                       directorio_audio=str(AUDIOS_DIR),
                                                       directorio_img=str(IMG_DIR),
                                                       prefix='c2_fft_global_sirena1',
                                                       save=True)
    
    # 2. FFT Ventanas 0.5s
    print("\n🪟 2. FFT Ventanas 0.5s...")
    fft_ventanas_sirena1('sirena_1.wav', intervalos=[0, 1, 2, 3, 4],
                        directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR),
                        prefix='c2_fft_ventanas_sirena1', save=True)
    
    # 3. Velocidad (f_promedio ~999Hz → constante)
    f_promedio = 999  # (941+1057)/2 de picos observados
    velocidad = calcular_velocidad_constante(f_promedio)
    
    print("\n🚑 RESULTADOS CONSIGNA 2:")
    print(f"• Pico global dominante: {f_pico_global:.0f} Hz")
    print(f"• Frecuencia promedio: {f_promedio} Hz")
    print(f"• VELOCIDAD ambulancia: {velocidad:.1f} km/h (constante)")
    print(f"• Efecto físico ventanas cortas: mayor variabilidad por ruido")

if __name__ == "__main__":
    main()
