import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import noisereduce as nr
import sounddevice as sd

# -------------------------------
# Rutas de las grabaciones
# -------------------------------
rutas_audios = [
    r"C:\Users\Paola\Documents\Labs Señales\Lab 3 Señales\Microfono1.wav",
    r"C:\Users\Paola\Documents\Labs Señales\Lab 3 Señales\Microfono2.wav",
    r"C:\Users\Paola\Documents\Labs Señales\Lab 3 Señales\Microfono3.wav"
]

nombres = ["Micrófono 1", "Micrófono 2", "Micrófono 3"]

# -------------------------------
# Funciones auxiliares
# -------------------------------
def calcular_snr(signal):
    power_signal = np.mean(signal ** 2)
    stft = np.abs(librosa.stft(signal))
    noise_magnitude = np.percentile(stft, 10, axis=1)
    power_noise = np.mean(noise_magnitude ** 2)
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

def metricas_frecuencia(y, sr):
    N = len(y)
    T = 1.0 / sr
    fft_values = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, T)[:N // 2]
    magnitudes = np.abs(fft_values[:N // 2])

    freq_media = np.sum(freqs * magnitudes) / np.sum(magnitudes)
    freq_mediana = freqs[np.argsort(magnitudes.cumsum())[len(magnitudes)//2]]
    freq_std = np.sqrt(np.sum(((freqs - freq_media) ** 2) * magnitudes) / np.sum(magnitudes))

    return freq_media, freq_mediana, freq_std, freqs, magnitudes

# -------------------------------
# Procesamiento por cada micrófono
# -------------------------------
for i, ruta in enumerate(rutas_audios):
    if os.path.exists(ruta):
        y, sr = librosa.load(ruta, sr=None)

        # -------------------------------
        # Métricas señal original
        # -------------------------------
        media_orig = np.mean(y)
        std_orig = np.std(y)
        freq_media_orig, freq_mediana_orig, freq_std_orig, freqs_orig, mags_orig = metricas_frecuencia(y, sr)
        snr_orig = calcular_snr(y)

        print(f"\n--- {nombres[i]} ---")
        print(">> Señal Original:")
        print(f"Media (tiempo): {media_orig:.4f}")
        print(f"Desviación estándar (tiempo): {std_orig:.4f}")
        print(f"Frecuencia media: {freq_media_orig:.2f} Hz")
        print(f"Frecuencia mediana: {freq_mediana_orig:.2f} Hz")
        print(f"Desviación estándar espectral: {freq_std_orig:.2f} Hz")
        print(f"SNR original: {snr_orig:.2f} dB")

        # -------------------------------
        # Filtrado
        # -------------------------------
        y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=True)

        media_filt = np.mean(y_denoised)
        std_filt = np.std(y_denoised)
        freq_media_filt, freq_mediana_filt, freq_std_filt, freqs_filt, mags_filt = metricas_frecuencia(y_denoised, sr)
        snr_filt = calcular_snr(y_denoised)

        print("\n>> Señal Filtrada:")
        print(f"Media (tiempo): {media_filt:.4f}")
        print(f"Desviación estándar (tiempo): {std_filt:.4f}")
        print(f"Frecuencia media: {freq_media_filt:.2f} Hz")
        print(f"Frecuencia mediana: {freq_mediana_filt:.2f} Hz")
        print(f"Desviación estándar espectral: {freq_std_filt:.2f} Hz")
        print(f"SNR filtrado: {snr_filt:.2f} dB")

        # -------------------------------
        # Gráficas comparativas
        # -------------------------------
        plt.figure(figsize=(12, 8))
        plt.suptitle(f"{nombres[i]} - Comparación Original vs Filtrada", fontsize=14, fontweight="bold")

        # Tiempo original
        plt.subplot(2, 2, 1)
        librosa.display.waveshow(y, sr=sr)
        plt.title("Tiempo - Original")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)

        # Tiempo filtrado
        plt.subplot(2, 2, 2)
        librosa.display.waveshow(y_denoised, sr=sr, color="g")
        plt.title("Tiempo - Filtrada")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)

        # Frecuencia original
        plt.subplot(2, 2, 3)
        plt.semilogx(freqs_orig, mags_orig, color='r')
        plt.title("Frecuencia - Original")
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud")
        plt.grid(True)

        # Frecuencia filtrada
        plt.subplot(2, 2, 4)
        plt.semilogx(freqs_filt, mags_filt, color='m')
        plt.title("Frecuencia - Filtrada")
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud")
        plt.grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

        # -------------------------------
        # Guardar archivo filtrado
        # -------------------------------
        output_file = rf"C:\Users\Paola\Documents\Labs Señales\Lab 3 Señales\{nombres[i].replace(' ', '_')}_Filtrado.wav"
        sf.write(output_file, y_denoised, sr)
        print(f"Archivo filtrado guardado: {output_file}")

        # -------------------------------
        # Reproducir señal filtrada
        # -------------------------------
        print(f"\nReproduciendo señal filtrada de {nombres[i]}...")
        sd.play(y_denoised, sr)
        sd.wait()
        print("Reproducción terminada.")
    else:
        print(f"ERROR: No se encontró el archivo {ruta}")