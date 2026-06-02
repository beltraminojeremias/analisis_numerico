"""
Configuración paths absolutos para Consigna 1.
"""

from pathlib import Path

# Raíz proyecto (dos niveles arriba de consigna_1/)
BASE_DIR = Path(__file__).parent.parent  # /tp-procesamiento-senales/
AUDIOS_DIR = BASE_DIR / 'audios'
IMG_DIR = BASE_DIR / 'imagenes' / 'consigna_4'

# Verificar existencia
if not AUDIOS_DIR.exists():
    raise FileNotFoundError(f"❌ Carpeta audios no encontrada: {AUDIOS_DIR}")

print(f"✅ Config: Audios={AUDIOS_DIR} | Imágenes={IMG_DIR}")
