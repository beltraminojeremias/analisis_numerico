"""
TP Procesamiento Señales - CONSIGNA 2
"""


from scripts_2.fft_sirena import fft




def main():
    print("CONSIGNA 2: DOMINIO FRECUENCIA + FFT ===")
    # Aplicar filtro y graficar
    sirena_1="AN-TP1/audios/sirena_1.wav"
    
    # Aplicar FFT y graficar
    inf = 0
    sup = 3500
    fft(sirena_1, ventana=0, xinf=inf, xsup=sup, yinf=0, ysup=None)
    fft(sirena_1, ventana=0.5, xinf=inf, xsup=sup, yinf=0, ysup=None)


if __name__ == "__main__":
    main()
