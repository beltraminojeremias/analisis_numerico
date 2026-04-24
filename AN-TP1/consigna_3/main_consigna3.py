#!/usr/bin/env python3
"""
TP Procesamiento Señales - CONSIGNA 3: FFT Sirena2
"""

from config import AUDIOS_DIR, IMG_DIR
from scripts.fft_sirena2 import fft_larga_sirena2, fft_corta_sirena2

def main():
    print("🔬 === CONSIGNA 3: FFT SIRENA2 (Larga vs Corta) ===")
    
    # 1. FFT VENTANAS LARGAS (2s)
    print("\n📏 1. FFT Ventanas LARGAS (2s)...")
    fft_larga_sirena2('sirena_2.wav', win_dur=2.0,
                     directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR),
                     prefix='c3_fft_larga_sirena2', save=True)
    
    # 2. FFT VENTANAS CORTAS (0.1s)
    print("\n📐 2. FFT Ventanas CORTAS (0.1s)...")
    fft_corta_sirena2('sirena_2.wav', win_dur=0.1,
                     directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR),
                     prefix='c3_fft_corta_sirena2', save=True)
    
    print("\n🔍 ANÁLISIS CONSIGNA 3:")
    print("• FFT LARGA: Pico ~borroso (promedia chirp rápido)")
    print("• FFT CORTA: Picos MÓVILES (850→1100Hz)")
    print("• FENÓMENO: MOVIMIENTO RÁPIDO (Doppler cambia f continua)")
    print("• IMPIDE medición: frecuencia NO estacionaria")

if __name__ == "__main__":
    main()
