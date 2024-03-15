import sounddevice as sd
import numpy as np
import wave
import matplotlib.pyplot as plt
import datetime as dt
from scipy.signal import spectrogram

samplerate = 44100  # Hertz

def record_audio(duration, samplerate=samplerate, channels=2):
    """
    Record audio with the given parameters.
    
    :param duration: Duration of the recording in seconds
    :param samplerate: Sampling rate in samples/second
    :param channels: Number of audio channels
    :return: Numpy array with recorded data
    """
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    return recording

def save_wave_file(filename, data, samplerate=44100, channels=2):
    """
    Save recorded data to a WAV file.
    
    :param filename: Path to save the WAV file
    :param data: Numpy array with audio data
    :param samplerate: Sampling rate in samples/second
    :param channels: Number of audio channels
    """
    
    if not filename.endswith('.wav'):
        filename += '.wav'

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # Number of bytes, int16 -> 2 bytes
        wf.setframerate(samplerate)
        wf.writeframes(data)



def draw_log_spectrogram(audio_data, samplerate,filename):
    """
    Draws a spectrogram on a logarithmic scale focusing on lower frequencies.

    :param audio_data: Numpy array containing the audio data.
    :param samplerate: The samplerate of the audio data.
    """
    # Compute the spectrogram
    print("Trying to create spectrogram")
    f, t, Sxx = spectrogram(audio_data, fs=samplerate, window='hann', nperseg=1024, noverlap=512)
    
    # Convert Sxx to dB, avoiding log of zero by adding a small epsilon
    Sxx_dB = 10 * np.log10(Sxx + np.finfo(float).eps)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, Sxx_dB, shading='gouraud')
    
    # Set the y-axis to logarithmic scale, focusing around 400 Hz
    plt.yscale('symlog', linthresh=400, linscale=0.5)
    plt.ylim(20, 500)  # Display from 20 Hz to Nyquist frequency
    
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Logarithmic Spectrogram')
    plt.colorbar(label='Intensity [dB]')
   #no need to show plt.show()

    plt.savefig(filename + ".png")
    print("spectrogram created")

# Example usage (uncomment and replace `audio_data` and `samplerate` with actual values)
# audio_data = np.random.randn(44100)  # Example random noise, replace with actual audio data
# samplerate = 44100  # Example sample rate, replace with actual sample rate of the audio
# draw_log_spectrogram(audio_data, samplerate)

def get_input_devices():
    """
    Print the available input devices.
    """
    print("Available input devices:")
    print(sd.query_devices())


def get_filename(filename,recnumber):
    return filename + dt.datetime.now().strftime("%H-%M-%S") + "_rec" + str(recnumber)

def print_time_now():
    print(dt.datetime.now().strftime("%H-%M-%S"))

def main():
    get_input_devices()
    device = int(input(f"Enter the input device index: "))
    duration = 300
    filename = input("Enter the filename to save the recording: ")
    
    # Set the device
    sd.default.device = device
    
    # Record audio
    #recorded_data = record_audio(duration)
    #save_wave_file(filename, recorded_data)

    for i in range(12):
        print(f"TIME={print_time_now()}  Recording {i+1} of 12")
        record_data = record_audio(duration)
        print("Recording finished.")
        save_name = get_filename(filename, i+1)
        print(f"Saving to {save_name}")
        save_wave_file(save_name, record_data)
        print(f"Saved to {save_name}")
        print(".....")
        

main()
    # Draw the spectrogram
    #draw_log_spectrogram(recorded_data[:, 0], samplerate, filename)



