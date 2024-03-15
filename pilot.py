from testsoundrec import get_input_devices, record_audio, save_wave_file
import sounddevice as sd
import datetime as dt
#settings
length = 5


def get_filename(filename,recnumber):
    return filename + dt.datetime.now().strftime("%H-%M-%S") + "_rec" + str(recnumber)

    
def main():
    get_input_devices()
    device = int(input("Enter the input device index: "))
    duration = length # in second
    filename = input("Enter the id to save the recording: (f.ex 'big tank, no fish')")

    for i in range(10):
        record_data = record_audio(duration, device)
        save_name = get_filename(filename, i+1)
        save_wave_file(save_name, record_data)
    

main()
