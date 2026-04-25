import sys
import os

# Agregamos la carpeta raíz del proyecto al path
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

from consigna_2.scripts_2.fft_sirena import fft
def main():
    print("CONSIGNA 3: FFT ")
    # Aplicar filtro y graficar
    sirena_2="AN-TP1/audios/sirena_2.wav"
    
    # Aplicar FFT y graficar
    xinf = 250
    xsup = 1600
    yinf=0
    ysup=None
    fft(sirena_2, ventana=0, xinf=xinf, xsup=xsup, yinf=yinf, ysup=ysup)
    fft(sirena_2, ventana=2, xinf=xinf, xsup=xsup, yinf=yinf, ysup=ysup)


if __name__ == "__main__":
    main()