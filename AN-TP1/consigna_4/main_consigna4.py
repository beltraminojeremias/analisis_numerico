from config import AUDIOS_DIR, IMG_DIR
from scripts.espectrograma import espectrograma_sirena2, calcular_velocidad_doppler

def main():
    print("🔬 === CONSIGNA 4: ESPECTROGRAMA STFT SIRENA4 ===")
    
    # STFT sirena2
    f, t, S_db, fs = espectrograma_sirena2('sirena_2.wav',
                                         directorio_audio=str(AUDIOS_DIR),
                                         directorio_img=str(IMG_DIR),
                                         prefix='c2_stft_sirena2',
                                         save=True)
    
    # MANUAL: mide freq media punto medio oscilación (ej: 950Hz)
    f_promedio = 1100  # ← RASTREA VISUALMENTE espectrograma
    v_kmh = calcular_velocidad_doppler(f_promedio)
    print(f"🚑 VELOCIDAD: {v_kmh:.1f} km/h (f_promedio={f_promedio}Hz)")

if __name__ == "__main__":
    main()
