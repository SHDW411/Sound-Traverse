import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from scipy import signal
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import wave
import statistics
import threading

root = Tk()
TIME_BUFFER = 3 # Czas pomiaru
BUFFER = 1024 #Długość analizy
FORMAT = pyaudio.paFloat32
WINDOW = 'hamming' #Kształt okna
CHANNELS = 1  #Ilość kanałow
RATE = 44100  #Czestotliwość próbkowania
CARRIER = 3150

raw_frames_arr = np.empty(0)
spectrum = np.empty(0)
max_freq = 0.0

freq_var = StringVar()
freq_var.set(CARRIER)
time_var = StringVar()
time_var.set(TIME_BUFFER)
rate_var = StringVar()
rate_var.set(RATE)


def evaluate(event):
    global CARRIER
    global TIME_BUFFER
    global sampling_rate
    CARRIER = int(freq_ent.get())
    TIME_BUFFER = int(time_ent.get())
    sampling_rate = int(sr_ent.get())
    print(CARRIER)
    print(TIME_BUFFER)
    #print(sampling_rate)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

def fm_demod(x, df=1.0, fc=0.0):
    x = signal.hilbert(x)
    # Usuwanie nośnej
    n = np.arange(0,len(x))
    rx = x*np.exp(-1j*2*np.pi*fc*n)
    # Obliczanie fazy
    phi = np.arctan2(np.imag(rx), np.real(rx))
    # Obliczanie częstotliwości z fazy
    y = np.diff(np.unwrap(phi)/(2*np.pi*df))
    return y

def data_collecting():
    global raw_frames_arr
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER)
    for i in range(0, int(RATE / BUFFER * TIME_BUFFER)):
        wave = np.frombuffer(stream.read(BUFFER), dtype=np.float32)
        raw_frames_arr = np.append(raw_frames_arr,wave)
    stream.stop_stream()
    stream.close()
    p.terminate()

def spectrum_analisis():
    global spectrum
    global max_freq
    spectrum = abs(np.fft.rfft(raw_frames_arr * signal.get_window(WINDOW, len(raw_frames_arr)), RATE))
    max_freq = np.argmax(spectrum)
    return max_freq

def waf_demod():
    lowcut = max_freq-2500
    highcut = max_freq+2500
    raw_filterd = butter_bandpass_filter(raw_frames_arr, lowcut, highcut, RATE, order=6)
    spectrum2 = abs(np.fft.rfft(raw_filterd * signal.get_window(WINDOW, len(raw_frames_arr)), RATE))
    sig_demod = fm_demod(raw_filterd, max_freq, max_freq)
    one_sec = int(len(raw_filterd)/TIME_BUFFER)
    last_sec = one_sec*(TIME_BUFFER-1)
    final_cut = sig_demod[one_sec:last_sec]
    Mean = np.mean(final_cut)
    stdev = statistics.stdev(final_cut)
    sigma2 = 2*stdev
    final_value = (sigma2/Mean)*100
    statusbar['text'] = "Wynik: {5.3f}".format(final_value)

def waf_meas():
    global max_freq
    statusbar['text'] = "Uruchomiono pomiar o długości " + str(TIME_BUFFER) +" sekund."
    data_collecting()
    statusbar['text'] = "Koniec nagrywania - obliczanie wyniku"
    max_freq = spectrum_analisis()
    txt_f_mes_val['text'] = str(max_freq) + " Hz"
    waf_demod()


#root.geometry('400x300')
root.title("Miernik nierównomierności przesuwu")
root.iconbitmap(r'Icons/001_speaker_plus_sign_6xq_icon.ico')

title_text = Label(root, text='Miernik nierównomierności przesuwu', bg='white', fg='black', font='Arial 18 bold')
title_text.pack(pady=15)
txt_f_exp = Label(root, text='Oczekiwana częstotliwości fali nośnej')
txt_f_exp.pack(pady=5)
freq_ent = Entry(root, textvariable=freq_var)
freq_ent.pack(pady=5)
freq_ent.bind("<Return>", evaluate)
txt_time = Label(root, text='Czas akwizycji')
txt_time.pack(pady=5)
time_ent = Entry(root, textvariable=time_var)
time_ent.pack(pady=5)
time_ent.bind("<Return>", evaluate)
txt_time = Label(root, text='Długość analizy')
txt_time.pack(pady=5)
rate_ent = Entry(root, textvariable=rate_var)
rate_ent.pack(pady=5)
rate_ent.bind("<Return>", evaluate)
txt_time = Label(root, text='Czestotliwość próbkowania')
txt_time.pack(pady=5)
txt_time = Label(root, text='44100')
txt_time.pack(pady=5)
PlayBtn = Button(root, text='Uruchom pomiar', command=waf_meas)
PlayBtn.pack(padx=5, pady=5)
PlotBtn = Button(root, text='Narysuj wykres', command=waf_meas)
PlotBtn.pack(padx=5, pady=5)
txt_f_mes = Label(root, text='Zmierzona częstotliwość fali nośnej')
txt_f_mes.pack(pady=5)
txt_f_mes_val = Label(root, text='---- Hz')
txt_f_mes_val.pack(pady=3)
statusbar = Label(root, title_text,text="", relief = SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)


root.mainloop()