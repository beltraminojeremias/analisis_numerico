# Añade esto al final del main, para ver la fase con un ejemplo clásico de traslado
from scipy.ndimage import shift
import numpy as np
from scipy.fft import fft2
import matplotlib.pyplot as plt
from matplotlib.colors import CenteredNorm

test_img = np.zeros((64, 64))
test_img[16:48, 16:48] = 1.0   # cuadrado

# Traslado
dx0, dy0 = 0, 6
test_img_tras = shift(test_img, (dy0, dx0), cval=0.0)

# FFT2
F1 = fft2(test_img)
F2 = fft2(test_img_tras)
phase1 = np.angle(F1)
phase2 = np.angle(F2)
phase_diff = phase1 - phase2

plt.figure(figsize=(14, 4))

plt.subplot(141); plt.imshow(test_img, cmap='gray'); plt.title('Cuadrado original')
plt.subplot(142); plt.imshow(test_img_tras, cmap='gray'); plt.title('Trasladado')
#
# plt.subplot(143); plt.imshow(phase_diff, cmap='RdBu_r', norm=CenteredNorm()); plt.title('Diferencia de fase (F1-F2)')
# plt.subplot(144); plt.plot(phase_diff[phase_diff.shape[0]//2, :]); plt.title('Corte u=0, v variable')
#
plt.tight_layout()
plt.show()
#
plt.figure(figsize=(11, 5))

plt.subplot(121)
plt.imshow(phase_diff, cmap='RdBu_r', norm=CenteredNorm())
plt.colorbar(label='Fase (radianes)')
plt.title('Diferencia de fase (F1-F2)')

plt.subplot(122)
plt.plot(phase_diff[phase_diff.shape[0]//2, :])
plt.grid(True)
plt.title('Corte horizontal (u variable, v=0)')
plt.ylabel('Fase (radianes)')
plt.xlabel('Frecuencia u')

plt.tight_layout()
plt.show()
