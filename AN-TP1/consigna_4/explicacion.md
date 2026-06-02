EXPLICACIÓN con MANZANAS: PASO 1 🍎
NO son 1024 partes por segundo. Es diferente:

```text
fs = 44100 Hz  → 44,100 **muestras** por segundo
ventana = 1024 **muestras** → 1024/44100 = **0.023 SEGUNDOS** (23ms)

```

Analogía MANZANAS:

```text

Imagina una CINTA CONTINUA de manzanas (tu audio sirena2):
🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎... (44,100 manzanas/segundo)

1️⃣ Tomamos **1024 manzanas seguidas** ← ventana1 (23ms)
🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎... (1024 manzanas)

2️⃣ Nos movemos **256 manzanas adelante** (75% overlap)
     🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎... ← ventana2

3️⃣ Repetimos hasta el final → **~170 ventanas**
```

CÓDIGO paso a paso:

```python
# 1. Tomar ventana1 (muestras 0-1023)
ventana1 = signal[0:1024]

# 2. FFT ventana1 → frecuencias de esas 1024 manzanas
yf1 = fft(ventana1)

# 3. Ventana2 (muestras 256-1279) ← 75% overlap
ventana2 = signal[256:1280]

# 4. FFT ventana2 → frecuencias ventana2
yf2 = fft(ventana2)

```

VISUAL:

```text
Tiempo →→→
0ms    23ms   46ms   69ms
 |-----|-----|-----| ← ventanas (1024 muestras)
  \---/ \---/     ← 75% overlap (768 muestras)
  
Cada |---| → 1 columna espectrograma

```
