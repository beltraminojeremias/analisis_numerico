TP2 - Punto 3 - Desarrollo paso a paso

Archivos incluidos:
- imagen1.jpg
- imagen5.jpg
- scripts/common_tp3.py
- scripts/01_carga_imagenes.py
- scripts/02_fft_magnitud.py
- scripts/03_transformacion_logpolar.py
- scripts/04_correlacion_fase.py
- scripts/05_calculo_factor_escala.py
- scripts/06_pipeline_completo.py
- resultados_generados/ con las imagenes usadas en el apunte

Como ejecutar en Windows desde esta carpeta:
py -3.13 scripts/01_carga_imagenes.py
py -3.13 scripts/02_fft_magnitud.py
py -3.13 scripts/03_transformacion_logpolar.py
py -3.13 scripts/04_correlacion_fase.py
py -3.13 scripts/05_calculo_factor_escala.py

Dependencias:
py -3.13 -m pip install numpy matplotlib pillow scikit-image

Resultado esperado:
Factor de escala estimado: 1.2989
Factor inverso para compensar: 0.7699
