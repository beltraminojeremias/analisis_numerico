#!/usr/bin/env python3
"""
TP Procesamiento Señales - CONSIGNA 1
"""

from config import AUDIOS_DIR, IMG_DIR
from scripts.discreta import graficar_discreta
from scripts.guardar_zoom_filtro import guardar_zooms_filtrada
from scripts.zoom import zoom_ventanas_audio_con_contador
from scripts.guardar_zoom import guardar_zooms_png

def main():
    print("🚀 === CONSIGNA 1: DOMINIO TIEMPO + FILTRO ===")
    
    # 1. DISCRETA
    print("\n📊 1. Representación Discreta...")
# Discreta ZOOM (3 ventanas)
    graficar_discreta('sirena_1.wav', intervalos=[0,], win_dur=0.05,
                    directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR),
                    save=False, prefix='c1_sirena1_disc_zoom')
    
    # 2. ZOOM + PICOS
    print("\n🔍 2. Análisis Picos...")
    zoom_ventanas_audio_con_contador('sirena_1.wav', [0,1,2], win_dur=0.05,
                                   directorio=str(AUDIOS_DIR),
                                   color='blue', prominence=0.25, height=0.35, min_dist=20)
    
    # 3. ORIGINAL vs FILTRADA hyperzoom
    print("\n🎨 3. Original vs Filtrada...")
    guardar_zooms_filtrada('sirena_1.wav', [0], prefix='c1_sirena1_hyperzoom',
                          low_cut=500, high_cut=1500, color_orig='#00A8E8',
                          color_filt='orange', win_dur=0.005,
                          directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR))



    guardar_zooms_png('sirena_1.wav', [0,1,2,3,4], prefix='c1_sirena1_ruido', win_dur=0.001, color='#00A8E8',
                 directorio_audio=str(AUDIOS_DIR), directorio_img=str(IMG_DIR))
    
    print("\n✅ Consigna 1 completada!")

if __name__ == "__main__":
    main()
