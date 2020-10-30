import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation
from scipy import signal
import scipy as sp
import matplotlib.pylab as pyl
import time


RATE = 44100
BUFFER = 1024

p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = RATE, input = True, output = False, frames_per_buffer = BUFFER)

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1)
line1 = ax2.plot([],[])[0]
line2 = ax1.plot([],[])[0]
line3 = ax3.plot([],[])[0]
line4 = ax4.plot([],[])[0]
line5 = ax5.plot([],[])[0]

sampling_period = RATE/BUFFER
r = range(0,int(RATE/2+1),int(RATE/BUFFER))
ts=pyl.arange(0,int(RATE/2),0.01)
r2 = range(0,1024)
r3=range(0,1023)
l = len(r)
#wave1 = np.frombuffer(stream.read(BUFFER), dtype=np.float32)
#yc=pyl.sin(2.0*pyl.pi*(3150.0/44100)*ts)
#plt.plot(ts,yc)


def fm_demod(x, df=1.0, fc=0.0):
    ''' Perform FM demodulation of complex carrier.

    Args:
        x (array):  FM modulated complex carrier.
        df (float): Normalized frequency deviation [Hz/V].
        fc (float): Normalized carrier frequency.

    Returns:
        Array of real modulating signal.
    '''

    # Remove carrier.
    n = np.arange(len(x))
    rx = x*np.exp(-1j*2*np.pi*fc*n)

    # Extract phase of carrier.
    phi = np.arctan2(np.imag(rx), np.real(rx))

    # Calculate frequency from phase.
    y = np.diff(np.unwrap(phi)/(2*np.pi*df))

    return y



def init_line():
        line1.set_data(r, l)
        line2.set_data(r, l)
        line2.set_data(r, l)
        line4.set_data(r, l)
        line5.set_data(r, l)
        return (line1,line2,line4,line5,)

def update_line(i):
    try:
        wave = np.frombuffer(stream.read(BUFFER), dtype=np.float32)
        data = np.fft.rfft(wave*signal.get_window('hamming',1024),1024)

    except IOError:
        pass
    data2 = np.log10(np.sqrt(np.real(data)**2+np.imag(data)**2) / BUFFER) * 10
    line1.set_data(r, data2)
    line2.set_data(r2, wave)
    line3.set_data(r, data2)
    #n=np.arange(len(wave))
    #rx=wave*sp.exp(-1j*2*sp.pi*)
    demo = np.array(fm_demod(wave, df=30.0 ,fc=3150.0))
    print(len(demo))
    line4.set_data(r3, demo)
    #print(signal.find_peaks_cwt(demo))
    #line5.
    time.sleep(0.1)
    return (line1,line2, line3, line4,line5)



ax1.set_xlim(0, 1024)
ax1.set_ylim(-1, 1)
ax1.set_xlabel('Frequency')
ax1.set_ylabel('dB')
ax1.set_title('Spectrometer')
ax1.grid()

ax2.set_xlim(20, 20000)
ax2.set_ylim(-60, 20)
ax2.set_xlabel('Frequency')
ax2.set_ylabel('dB')
ax2.set_title('Spectrometer')
ax2.set_xscale('symlog')
ax2.grid()


ax3.set_xlim(2500, 3500)
ax3.set_ylim(-60, 0)
ax3.set_xlabel('Frequency')
ax3.set_ylabel('dB')
ax3.set_title('Spectrometer')
ax3.grid()

ax4.set_xlim(0, 1024)
ax4.set_ylim(-0.25, 0.25)
ax4.set_xlabel('Frequency')
ax4.set_ylabel('dB')
ax4.set_title('Spectrometer')
ax4.grid()

line_ani = matplotlib.animation.FuncAnimation(fig, update_line, init_func=init_line, interval=0, blit=True)
plt.show()