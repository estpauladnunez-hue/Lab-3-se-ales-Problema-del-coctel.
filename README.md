
#  Fiesta de Cóctel
 ## Introducción
En este trabajo desarrollaremos la práctica de “la fiesta de cóctel”, esta consiste en grabar diferentes conversaciones desde diferentes micrófonos en una reunión, en nuestro caso hicimos uso de la aplicación grabadora de voz desde los celulares, en un cuarto a una distancia de aproximadamente 2 metros cada uno de los micrófonos que se encontraban en un punto central, esto permitió la captura de tres audios guardados desde tres diferentes celulares de aproximadamente 50 segundos cada audio. 
## Preparacion y Calculos 
![Imagen de WhatsApp 2025-09-25 a las 10 31 17_5ec5b131](https://github.com/user-attachments/assets/c66bc535-34e9-4c40-870a-9b1568f0355e)
![Imagen de WhatsApp 2025-09-25 a las 08 47 01_a822fd87](https://github.com/user-attachments/assets/3d2d0d23-2ef8-4642-9b31-caee67cd0a54)

# Marco Teorico.
## Tranformada rápida de Fourier
La Transformación rápida de Fourier, FFT para abreviar, es un importante método de medición en la tecnología de medición de audio y acústica. Descompone una señal en sus componentes espectrales individuales y así proporciona información sobre su composición. Los FFT se utilizan para el análisis de errores, el control de calidad y la monitorización de las condiciones de las máquinas o sistemas. 
## ¿Qué es ICA?
El análisis de componentes independientes es un método probabilístico para aprender una transformación lineal de un vector aleatorio. El objetivo es encontrar componentes que sean máximamente independientes y no gaussianos (no normales). Su diferencia fundamental con los métodos estadísticos multivariantes clásicos radica en el supuesto de no gaussianidad, lo que permite la identificación de componentes originales subyacentes, en contraste con los métodos clásicos.
## ¿Qué es Beamforming?
Esta es una técnica que permite mejorar la captación de señal en una dirección específica y reducir el ruido o interferencias que puedan provenir de otras direcciones, esto es posible si se utiliza un arreglo de sensores siendo micrófonos o antenas que reciben la misma señal con algunas diferencias de tiempo, después estas señales se ajustan aplicando retrasos y pesos (retrasos y pesos) antes de ser sumados lo que refuerza la señal deseada atenuando las de más. Existen varios métodos para la implementación de beamforming, podríamos hablar de lo convencional el cual usa retrasos (Delays) fijos para cada sensor, en el adaptativo que ajusta dinámicamente los parámetros mediante algoritmos de adaptación siendo esta técnica utilizada en las comunicaciones inalámbricas, procesamiento de voz y en biomédica hablaríamos de la detección del latido fetal.
## Diferencia entre ICA y BEAMFORMING
Podemos decir que ICA intenta separar múltiples señales que han sido mezcladas mientras que beamforming se enfoca en mejorar la señal desde una dirección específica. La siguiente tabla explica mucho mejor lo anterior mencionado.
 ![{9636A8FF-1E1A-44F0-98B7-2692BC0D1C35}](https://github.com/user-attachments/assets/74c10c3d-5310-40d1-80ec-72967d3cf53d)
 # Desarrollo.
En este laboratorio se trabajó con tres grabaciones de voz capturadas por distintos micrófonos, con el fin de realizar un análisis en el dominio del tiempo y en el dominio de la frecuencia. Además, se aplicó una técnica de beamforming para combinar las señales y mejorar la calidad del audio final mediante reducción de ruido.

Como primera parte,se cargaron las grabaciones desde archivos .wav usando la librería librosa. A cada señal se le calculó su SNR (Signal-to-Noise Ratio) para medir la calidad del audio en dB.
```python
y, sr = librosa.load(ruta, sr=None)
snr = calcular_snr(y)
print(f"SNR de {nombres[i]}: {snr:.2f} dB")
```
En donde los resultados obtenidos fueron:

<img width="206" height="46" alt="image" src="https://github.com/user-attachments/assets/db47b1f6-f302-47d5-a398-d484b76decd9" />

Luego, cada señal fue graficada enh dos representaciones utilizando nuestra parte del codigo:
```python
plt.subplot(2,1,1)
librosa.display.waveshow(y, sr=sr)
plt.title("Forma de onda")

N = len(y)
T = 1.0 / sr
fft_values = np.fft.fft(y)
freqs = np.fft.fftfreq(N, T)[:N//2]
plt.subplot(2,1,2)
plt.semilogx(freqs, np.abs(fft_values[:N//2]))
plt.title("Espectro de Frecuencia")
```
1.Forma de onda en el tiempo → permite observar cómo varía la amplitud de la señal con el tiempo.

2.Espectro de frecuencias (FFT) → muestra la distribución de la energía en función de las frecuencias presentes en la señal.

De esto obtuvimos como resultado una imagen con dos gráficas por cada micrófono (forma de onda y espectro de frecuencia) y de las cuales pudimos observar cómo cada grabación presentaba diferentes características de amplitud y contenido en frecuencia.
<img width="1189" height="593" alt="image" src="https://github.com/user-attachments/assets/0130dc15-c414-46d6-b915-d7b7e92002d5" />
La señal capturada por el micrófono 1 tiene una duración aproximada de 50 segundos y corresponde a una grabación de voz humana en un ambiente controlado. En el dominio del tiempo se observan variaciones de amplitud propias del habla, con picos más marcados en los instantes de mayor intensidad y pausas intermedias que reflejan los silencios naturales. La señal no presenta saturación, lo cual indica que la grabación se realizó con un nivel adecuado de ganancia.

En el dominio de la frecuencia, el espectro obtenido mediante la Transformada Rápida de Fourier (FFT) muestra la mayor concentración de energía entre los 100 Hz y 3 kHz, rango característico de la voz humana. Se distinguen picos pronunciados alrededor de 100–300 Hz que corresponden al fundamental y primeros armónicos de la voz, mientras que las frecuencias más altas representan consonantes y fricativas con menor magnitud. El nivel de ruido fuera de la banda principal es bajo, lo cual evidencia una buena relación señal/ruido gracias a la proximidad del hablante (~38 cm) y a las condiciones del recinto.

<img width="1189" height="593" alt="image" src="https://github.com/user-attachments/assets/bb3fefdc-8cc6-46b4-87c9-92fc3801726e" />
La señal registrada por el micrófono 2 muestra una duración cercana a los 55 segundos, con actividad marcada desde los primeros segundos y una amplitud consistente a lo largo de la grabación. Se evidencian variaciones de intensidad y pausas cortas, propias del habla continua. En el dominio de la frecuencia, la FFT revela un pico de energía dominante alrededor de los 100–300 Hz, correspondiente al fundamental de la voz, acompañado de armónicos distribuidos hasta aproximadamente los 3 kHz. La magnitud espectral en este micrófono es más elevada que en el micrófono 1, lo cual indica una mayor captación de energía, posiblemente por la cercanía del hablante (32,5 cm). En conclusión, la señal del micrófono 2 presenta una buena calidad, alta energía y un espectro claro para análisis y separación de fuentes.


<img width="1189" height="593" alt="image" src="https://github.com/user-attachments/assets/68e1dab4-b662-4c67-83fe-f5735ef87254" />
La señal capturada por el micrófono 3 tiene también una duración aproximada de 50 segundos, pero su amplitud es más baja en comparación con los micrófonos 1 y 2. Esto se debe a la mayor distancia con respecto al hablante (66 cm), lo que genera una señal más débil y con menor relación señal/ruido. En el dominio de la frecuencia, la energía se concentra igualmente entre 100 Hz y 3 kHz, con varios picos que reflejan la estructura armónica de la voz. Sin embargo, la magnitud general es menor, lo que evidencia atenuación por la distancia y mayor presencia de ruido relativo. En conclusión, la señal del micrófono 3, aunque útil para análisis, requiere mayor procesamiento (ej. filtrado o beamforming) para alcanzar la misma claridad que los otros dos micrófonos.



Para mejorar la señal de voz, se aplicó un método de beamforming simple, que consiste en promediar las tres señales después de recortarlas a la misma duración. Posteriormente, se aplicó un filtro de reducción de ruido (noisereduce), gracias a esta parte de nuestro codigo:
```python
muestras_beamformed = np.mean(muestras_recortadas, axis=0)
muestras_beamformed_denoised = nr.reduce_noise(
    y=muestras_beamformed, sr=sample_rate, stationary=True)
```
Que nos dio como resultados la señal combinada con mejor relacion señal-ruido y el archivo final exportado como .wav para escuchar la señal filtrada.

Para la parte final usamos esta parte del codigo:
```python
plt.figure(figsize=(12, 6))
plt.plot(muestras_beamformed, label="Señal Beamformed Original", alpha=0.7)
plt.plot(muestras_beamformed_denoised, label="Señal Beamformed Denoised", alpha=0.7)
plt.title("Comparación de Señal Original y Señal Procesada")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.legend()
plt.grid()
plt.show()
```
El cual nos permitio realizar una gráfica comparando la señal original (promedio simple) contra la señal procesada (beamformed denoised).
<img width="1017" height="546" alt="image" src="https://github.com/user-attachments/assets/9eabc573-5a4a-4b7d-a966-834087fff500" />

Y obtuvimos la reproducción del archivo final para verificar la mejora perceptual en la calidad del audio con nuestro codigo:
```python
import sounddevice as sd

print("\nReproduciendo la señal aislada...")
sd.play(muestras_beamformed_denoised, sample_rate)
sd.wait()  # Se queda esperando hasta que acabe el audio
print("Reproducción terminada.")
```
