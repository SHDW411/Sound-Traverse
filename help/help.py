import numpy as np
import sounddevice as sd
from numpy import linalg as LA

duration = 10 #in seconds

def audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   print("|" * int(volume_norm))


stream = sd.InputStream(callback=audio_callback)
with stream:
   sd.sleep(duration * 1000)

#########

duration = 10  # seconds


def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(int(volume_norm))


with sd.Stream(callback=print_sound):
    sd.sleep(duration * 1000)