import sounddevice as sd
import soundfile as sf
import datetime
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

def record_audio(duration, gain=1.0, device_id=2):
    # Query the device to get its info
    device_info = sd.query_devices(device_id, 'input')
    channels = device_info['max_input_channels']  # Number of channels supported by the input device
    print(f"channels: {channels}")

    # Set the sample rate
    sample_rate = int(device_info['default_samplerate'])
    sample_rate = sample_rate*2
    print(f"sample_rate: {sample_rate}")

    # Calculate the number of samples to record
    num_samples = int(duration * sample_rate)

    # Start recording audio
    recording = sd.rec(num_samples, samplerate=sample_rate, channels=channels, device=device_id)

    # Wait for the recording to complete
    sd.wait()

    # Apply gain to the recording
    recording *= gain

    # Generate a filename based on the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recordings/{current_time}.wav"

    # Save the recording as a WAV file
    sf.write(filename, recording, sample_rate)

    # Create a spectrogram
    f, t, Sxx = signal.spectrogram(recording[:, 0], sample_rate)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram')
    plt.colorbar(label='Intensity [dB]')
    plt.savefig(f"recordings/{current_time}_spectrogram.png")
    plt.show()

if __name__ == "__main__":
    # Record audio for specified duration and number of recordings
    duration_s = int(input("Enter the duration of the recording in seconds: "))

    # Ask for the device ID if the user wants to specify one
    device_id_input = input("Enter the device ID (Press Enter to use default): ")
    device_id = int(device_id_input) if device_id_input else 2  # Convert to integer or use default (2)

    # Ask for the gain
    gain = float(input("Enter the gain (e.g., 1.0 for no change): "))

    print("Recording...")
    record_audio(duration_s, gain, device_id)

