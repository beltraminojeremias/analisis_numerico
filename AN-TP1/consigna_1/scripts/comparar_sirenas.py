#!/usr/bin/env python3
"""
consigna_1/scripts/comparar_sirenas.py
Compara sirena_1.wav y sirena_2.wav para captura de pantalla
"""

# 🔧 FIJAR IMPORT config DESDE DIRECTORIO PADRE
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pathlib import Path
from config import AUDIOS_DIR, IMG_DIR

def graficar_sirenas_juntas_comparacion(prefix='comparacion_sirenas'):
    """
    Genera gráfica comparativa sirena_1 vs sirena_2 
    con grids + títulos para informe TP
    """
    
    # 📁 RUTAS desde config.py
    audio_path1 = AUDIOS_DIR / 'sirena_1.wav'
    audio_path2 = AUDIOS_DIR / 'sirena_2.wav'
    img_path = IMG_DIR / f'{prefix}.png'
    
    # 🔍 CARGAR AUDIOS
    fs1, sirena1 = wavfile.read(audio_path1)
    fs2, sirena2 = wavfile.read(audio_path2)
    
    print(f"✅ sirena_1: {len(sirena1)/fs1:.1f}s ({len(sirena1)} samples)")
    print(f"✅ sirena_2: {len(sirena2)/fs2:.1f}s ({len(sirena2)} samples)")
    
    # ⏱️ TIEMPOS
    t1 = np.arange(len(sirena1)) / fs1
    t2 = np.arange(len(sirena2)) / fs2
    
    # 🎨 FIGURA GRANDE (15x12) con grids
    plt.style.use('default')
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), 
                            facecolor='white', dpi=100)
    
    # 1️⃣ SIRNA 1 - ESTÁTICA (AZUL)
    axes[0].plot(t1, sirena1, color='#00A8E8', linewidth=0.8, alpha=0.9)
    axes[0].set_title('🩼 sirena_1.wav - ESTÁTICA (sin Doppler)', 
                     fontsize=16, fontweight='bold', pad=20)
    axes[0].grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
    axes[0].set_ylabel('Amplitud', fontsize=12)
    axes[0].set_xlim(0, min(6, t1[-1]))
    
    # 2️⃣ SIRNA 2 - MÓVIL (ROJO)
    axes[1].plot(t2, sirena2, color='#FF4444', linewidth=0.8, alpha=0.9)
    axes[1].set_title('🚑 sirena_2.wav - MÓVIL (con efecto Doppler)', 
                     fontsize=16, fontweight='bold', pad=20)
    axes[1].grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
    axes[1].set_ylabel('Amplitud', fontsize=12)
    axes[1].set_xlim(0, min(6, t2[-1]))
    
    # 3️⃣ SUPERPUESTAS (0-5s)
    min_dur = min(5.0, t1[-1], t2[-1])
    mask1, mask2 = t1 <= min_dur, t2 <= min_dur
    
    axes[2].plot(t1[mask1], sirena1[mask1], color='#00A8E8', 
                linewidth=1.2, label='sirena_1 (estática)', alpha=0.9)
    axes[2].plot(t2[mask2], sirena2[mask2], color='#FF4444', 
                linewidth=1.2, label='sirena_2 (móvil)', alpha=0.9)
    axes[2].set_title('⚡ COMPARACIÓN sirena_1 vs sirena_2 (0-5 segundos)', 
                     fontsize=16, fontweight='bold', pad=20)
    axes[2].legend(fontsize=12, framealpha=0.9)
    axes[2].grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
    axes[2].set_ylabel('Amplitud', fontsize=12)
    axes[2].set_xlabel('Tiempo [s]', fontsize=12)
    
    plt.tight_layout(pad=2.0)
    
    # 👀 MOSTRAR EN PANTALLA (para captura)
    plt.show()
    
    # 💾 GUARDAR alta calidad
    plt.savefig(img_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"💾 Guardado: {img_path}")
    
    return fig

# 🚀 EJECUTAR DESDE consigna_1/
if __name__ == "__main__":
    print("🎨 Generando comparación sirena_1 vs sirena_2...")
    fig = graficar_sirenas_juntas_comparacion()
    print("✅ Listo para captura de pantalla!")
