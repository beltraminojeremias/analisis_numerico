#!/usr/bin/env python3
"""
consigna_1/scripts/discreta.py
FIX: config.py desde directorio padre + Pathlib
"""

# 🔧 FIJAR IMPORT config DESDE DIRECTORIO PADRE
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pathlib import Path
from config import AUDIOS_DIR, IMG_DIR

def graficar_discreta(archivo, intervalos=[0], win_dur=0.05, 
                     prefix='discreta', save=False):
    """
    Grafica señal DISCRETA en ventanas (stem plot SOLO LÍNEAS).
    
    Args:
        archivo: 'sirena_1.wav'
        intervalos: [0, 0.5, 1] segundos
        win_dur: 0.05 segundos (50ms)
        prefix: 'c1_sirena1_disc_zoom'
        save: True guarda PNGs
    """
    # 📁 PATHS con config.py
    audio_path = AUDIOS_DIR / archivo
    img_path = IMG_DIR / f"{prefix}_{int(win_dur*1000)}ms.png"
    
    # 🔍 CARGAR AUDIO
    fs, signal = wavfile.read(audio_path)
    signal = signal.astype(np.float32) / np.max(np.abs(signal))
    
    win_samples = int(win_dur * fs)
    intervalos = np.array(intervalos)
    
    # 🎨 FIGURA adaptativa
    fig, axes = plt.subplots(len(intervalos), 1, 
                            figsize=(12, 4 + len(intervalos)*1.5),
                            facecolor='white')
    if len(intervalos) == 1:
        axes = [axes]
    
    print(f"✅ {archivo}: fs={fs}Hz | Duración={len(signal)/fs:.1f}s")
    
    for i, t_start in enumerate(intervalos):
        idx_start = int(t_start * fs)
        idx_end = min(idx_start + win_samples, len(signal))
        
        if idx_start >= len(signal):
            print(f"⚠️ Intervalo {t_start}s excede duración")
            continue
        
        t_zoom = np.arange(idx_end-idx_start) / fs + t_start
        signal_zoom = signal[idx_start:idx_end]
        
        # 📊 STEM DISCRETO (solo líneas GRIS)
        axes[i].stem(t_zoom, signal_zoom, 
                    linefmt='gray',      # Líneas GRIS finas
                    markerfmt=' ',       # SIN puntos/marcadores
                    basefmt=' ')
        
        axes[i].set_title(f'Discreta | t={t_start:.2f}s | Δt={win_dur:.0f}ms | fs={fs:,}Hz', 
                         fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Tiempo [s]')
        axes[i].set_ylabel('Amplitud normalizada')
        axes[i].grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
        axes[i].set_xlim(t_start, t_start + win_dur)
    
    plt.tight_layout(pad=1.5)
    
    if save:
        # 💾 GUARDAR PNG alta calidad
        img_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(img_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ Guardado: {img_path}")
        plt.close()
    else:
        plt.show()
    
    print(f"📊 fs: {fs:,}Hz | Ventanas: {len(intervalos)} | {win_samples:,} samples")
    return fs, signal

if __name__ == "__main__":
    # 🎯 EJEMPLO uso desde consigna_1/
    graficar_discreta('sirena_1.wav', intervalos=[0], 
                     win_dur=0.003, prefix='c1_sirena1_disc_zoom', save=True)
