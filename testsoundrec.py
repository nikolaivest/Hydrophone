import sounddevice as sd
import soundfile as sf
import datetime

def record_audio(duration):
    # Set the sample rate and number of channels
    sample_rate = 44100
    channels = 1

    # Calculate the number of samples to record
    num_samples = int(duration * sample_rate)

    # Start recording audio
    recording = sd.rec(num_samples, samplerate=sample_rate, channels=channels)

    # Wait for the recording to complete
    sd.wait()

    # Generate a filename in a folder for every day and give file name based on the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recordings/{current_time}.wav"

    



    # Save the recording as a WAV file
    sf.write(filename, recording, sample_rate)

# Record audio for 30 seconds

duration_m= int(input("Enter the duration of the recording in minutes: "))
duration_s = duration_m 
duration_per_recording = input("Enter the duration of each recording in seconds (if NAN duration = 10 sec): ")
if duration_per_recording == "":
    duration_per_recording = 10

duration_per_recording = int(duration_per_recording)
num_recordings = duration_s // duration_per_recording
for i in range(num_recordings):
    print(f"Recording {i+1} of {num_recordings}...")
    record_audio(duration_per_recording)
    print("Finished recording.")
    print(f"Recording found at recording/{filename}")

print("Finished recording all audio.")



