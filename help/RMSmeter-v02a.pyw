# RMSmeter-v02a.py(w)  (14-10-2018) RMSmeter
# For Python version 3
# With external module pyaudio
# Made by Onno Hoekstra (pa2ohh)

import pyaudio
import math
import time

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font

# Values that can be modified
CANVASwidth = 500           # Width of the canvas
CANVASheight = 200          # Height of the canvas

SAMPLErate = 48000          # Sample rate of the soundcard 22050 44100 48000 88200 96000 192000
UPDATEspeed = 1.1           # Update speed, default 1.1, for slower PC's a higher value is perhaps required 

TIMEdiv1x = [0.2, 0.5, 1.0, 2.0, 5.0, 10.0] # Gate Time list in s/div
TIMEdiv = 1                 # index 1 from TIMEdiv1x  as initial value

# Colors that can be modified
COLORframes = "#000080"     # Color = "#rrggbb" rr=red gg=green bb=blue, Hexadecimal values 00 - ff 
COLORcanvas = "#404040"
COLORtext = "#ffffff"
COLORaudiobar = "#606060"
COLORaudiook = "#00ff00"
COLORaudiomax = "#ff0000"

# Fontsizes that can be modified
RMSfontsize = 48            # Size of RMS value text (Small=6, Large=48)
INFOfontsize = 8            # Size of info text (Small=6, Large=24)

# Button sizes that can be modified
Buttonwidth1 = 12
Buttonwidth2 = 8

AUDIOsignal1 = []           # Audio trace channel 1    
AUDIOdevin = None           # Audio device for input. None = Windows default
AUDIOdevout = None          # Audio device for output. None = Windows default

RUNstatus = 1               # 0 stopped, 1 start, 2 running, 3 stop and restart, 4 stop
AUDIOstatus = 1             # 0 audio off, 1 audio on

RMSch1 = 0.0                # RMS value channel 1

AUDIOlevel = 0.0            # Maximum value of CH1


# =================================== Start widgets routines ========================================
def Bnot():
    print("Routine not made yet")


def BAudiostatus():
    global AUDIOstatus
    
    if (AUDIOstatus == 0):
        AUDIOstatus = 1
    else:
        AUDIOstatus = 0

    UpdateScreen()          # UpdateScreen() call 

    
def BStart():
    global RUNstatus
    
    if (RUNstatus == 0):
        RUNstatus = 1

    UpdateScreen()          # UpdateScreen() call 


def BStop():
    global RUNstatus
    
    if (RUNstatus == 1):
        RUNstatus = 0
    elif (RUNstatus == 2):
        RUNstatus = 3
    elif (RUNstatus == 4):
        RUNstatus = 3

    UpdateScreen()          # UpdateScreen() call 


def BSoundcard():
    global SAMPLErate
    global RUNstatus
    
    s = simpledialog.askstring("Sample rate","Value: " + str(SAMPLErate) + "\n\nNew value:\n(48000, 96000, 192000)")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = ""), then v = 0
        v = int(s)
    except:
        v = 0

    if v != 0:
        SAMPLErate = v

    if (RUNstatus == 2):    # Restart if running
        RUNstatus = 4

    UpdateScreen()          # UpdateScreen() call 


def BTime1():
    global TIMEdiv
    global RUNstatus
    
    if (TIMEdiv >= 1):
        TIMEdiv = TIMEdiv - 1

    if (RUNstatus == 2):    # Restart if running
        RUNstatus = 4

    UpdateScreen()          # UpdateScreen() call 

    
def BTime2():
    global TIMEdiv1x
    global TIMEdiv
    global RUNstatus
    
    if (TIMEdiv < len(TIMEdiv1x) - 1):
        TIMEdiv = TIMEdiv + 1

    if (RUNstatus == 2):    # Restart if running
        RUNstatus = 4

    UpdateScreen()          # UpdateScreen() call 
    
# ============================================ Main routine ====================================================
    
def AUDIOin():   # Read the audio from the stream and store the data into the arrays
    global AUDIOsignal1
    global AUDIOdevin
    global AUDIOdevout
    global RUNstatus
    global AUDIOstatus
    global TIMEdiv1x
    global TIMEdiv
    global SAMPLErate
    global UPDATEspeed
     
    while (True):                                           # Main loop
        PA = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16                            # Audio format 16 levels and 2 channels
        CHUNK = int( float(SAMPLErate) * TIMEdiv1x[TIMEdiv])

        # RUNstatus = 1 : Open Stream
        if (RUNstatus == 1):
            if UPDATEspeed < 1:
                UPDATEspeed = 1.0
            if UPDATEspeed > 5:
                UPDATEspeed = 5.0

            TRACESopened = 1

            try:
                chunkbuffer = int(UPDATEspeed * CHUNK)

                if chunkbuffer < SAMPLErate / 10:            # Prevent buffer overload if small number of samples
                    chunkbuffer = int(SAMPLErate / 10)

                stream = PA.open(format = FORMAT,
                    channels = TRACESopened, 
                    rate = SAMPLErate, 
                    input = True,
                    output = True,
                    frames_per_buffer = int(chunkbuffer),
                    input_device_index = AUDIOdevin,
                    output_device_index = AUDIOdevout)
                RUNstatus = 2
            except:                                         # If error in opening audio stream, show error
                RUNstatus = 0
                txt = "Sample rate: " + str(SAMPLErate) + ", try a lower sample rate.\nOr another audio device."
                messagebox.showerror("Cannot open Audio Stream", txt)

            UpdateScreen()                                  # UpdateScreen() call        

        
        # RUNstatus = 2: Reading audio data from soundcard
        if (RUNstatus == 2):
            signals = []
            try:
                signals = stream.read(chunkbuffer)          # Read samples from the buffer
            except:
                RUNstatus = 4

            if (AUDIOstatus == 1):                          # Audio on 
                stream.write(signals, chunkbuffer)

            # Start conversion audio samples to values -32762 to +32767 (one's complement)
            Lsignals = len(signals)                         # Lenght of signals array
            AUDIOsignal1 = []                               # Clear the AUDIOsignal1 array for trace 1

            Sbuffer = Lsignals / 2                          # Sbuffer is number of values (2 bytes per audio sample value, 1 channel is 2 bytes)
            i = 2 * int(Sbuffer - CHUNK)                    # Start value, first part is skipped due to possible distortions

            if i < 0:                                       # Prevent negative values of i
                i = 0
                
            s = Lsignals - 1       
            while (i < s):
                v = (signals[i]) + 256 * (signals[i+1])
                if v > 32767:                               # One's complement correction
                    v = v - 65535
                AUDIOsignal1.append(v)                      # Append the value to the trace 1 array 
                i = i + 2                                   # 2 bytes per sample value and 1 trace is 2 bytes totally

            UpdateAll()                                     # Update Data, trace and screen

        # RUNstatus = 3: Stop
        # RUNstatus = 4: Stop and restart
        if (RUNstatus == 3) or (RUNstatus == 4):
            stream.stop_stream()
            stream.close()
            PA.terminate()
            if RUNstatus == 3:
                RUNstatus = 0                               # Status is stopped 
            if RUNstatus == 4:          
                RUNstatus = 1                               # Status is (re)start

            UpdateScreen()                                  # Update screen with text  

        # Update tasks and screens by TKinter 
        root.update_idletasks()
        root.update()                                       # Activate updated screens 


def UpdateAll():        # Update Data, trace and screen
    CalculateRMS()      # RMS calculation
    UpdateScreen()      # Update screen with text


def UpdateScreen():     # Update screen with text
    MakeScreen()        # Update the text
    root.update()       # Activate updated screens    


def CalculateRMS():                 # Calculate the RMS on channel 1
    global AUDIOsignal1
    global SAMPLErate
    global RMSch1                   # The RMSvalue
    global AUDIOlevel               # Maximum value
    
    TRACEsize = len(AUDIOsignal1)   # Set the trace length
    if TRACEsize == 0:
        return()

    # Zero offset correction routine only for trace 1
    AD1 = 0
    t = 0
    
    Vmin = 0
    Vmax = 0
    while t < TRACEsize:
        V = AUDIOsignal1[t]
        AD1 = AD1 + V
        if V > Vmax:
            Vmax = V
        if V < Vmin:
            Vmin = V
        t = t + 1

    Vmin = -1 * Vmin        # Delete the minus sign

    AUDIOlevel = float(Vmin)
    if Vmax > AUDIOlevel:
        AUDIOlevel = float(Vmax)

    AUDIOlevel = AUDIOlevel / 32000
    if AUDIOlevel > 1.0:
        AUDIOlevel = 1.0            
    
    AD1 = int(AD1 /  TRACEsize)      

    # RMS calculation, only for trace 1
    RMSch1 = 0.0

    t = 0
    while t < TRACEsize:
        v1 = AUDIOsignal1[t] - AD1
        RMSch1 = RMSch1 + v1 * v1
        t = t + 1

    RMSch1 = math.sqrt(RMSch1 / TRACEsize) # RMSvalue in steps of the AD converter
     
    
def MakeScreen():                       # Update the screen with text
    global AUDIOsignal1
    global RUNstatus
    global AUDIOstatus
    global TIMEdiv1x
    global TIMEdiv
    global SAMPLErate
    global AUDIOlevel                   # Maximum audio value
    global RMSch1
    global RMSfont
    global INFOfont
    global COLORaudiobar
    global COLORaudiook 
    global COLORaudiomax
    global CANVASwidth
    global CANVASheight

    # Delete all items on the screen
    de = ca.find_enclosed ( 0, 0, CANVASwidth+1000, CANVASheight+1000)   
    for n in de: 
        ca.delete(n)


    # General information on top of the screen
    if (AUDIOstatus == 1):
        txt = "Audio on "
    else:
        txt = "Audio off"

    x = 10
    y = 20
    idTXT = ca.create_text (x, y, text=txt, font=INFOfont, anchor=W, fill=COLORtext)


    # RMS value printing
    if RMSch1 > 0.000001:                                     # Prevent log(0)
        txt = str(20 * math.log10(RMSch1)) + "000000"
        txt = txt[:6] + " dB"
    else:
        txt = "No signal"

    x = 60
    y = CANVASheight / 2
    idTXT = ca.create_text(x, y, text=txt, font=RMSfont, anchor=W, fill=COLORtext)


    # Time gating information
    vx = TIMEdiv1x[TIMEdiv]
    if vx >= 1:
        txt = str(int(vx))
    elif vx >= 0.1:
        txt ="0." + str(int(vx * 10))
    elif vx >= 0.01:
        txt ="0.0" + str(int(vx * 100))

    txt = txt + " sec."
    if (RUNstatus == 0) or (RUNstatus == 3):
        txt = txt + "    stop"
       
    x = 10
    y = CANVASheight-50
    idTXT = ca.create_text (x, y, text=txt, font=INFOfont, anchor=W, fill=COLORtext)


    # Soundcard level bargraph
    txt1 = "||||||||||||||||||||"   # Bargraph
    le = len(txt1)                  # length of bargraph

    t = int(math.sqrt(AUDIOlevel) * le)

    n = 0
    txt = ""
    while(n < t and n < le):
        txt = txt + "|"
        n = n + 1

    x = 10
    y = CANVASheight-20
    
    idTXT = ca.create_text (x, y, text=txt1, anchor=W, fill=COLORaudiobar)

    if AUDIOlevel >= 1.0:
        idTXT = ca.create_text (x, y, text=txt, anchor=W, fill=COLORaudiomax)
    else:
        idTXT = ca.create_text (x, y, text=txt, anchor=W, fill=COLORaudiook)


def SELECTaudiodevice():        # Select an audio device
    global AUDIOdevin
    global AUDIOdevout

    PA = pyaudio.PyAudio()
    ndev = PA.get_device_count()

    n = 0
    ai = ""
    ao = ""
    while n < ndev:
        s = PA.get_device_info_by_index(n)
        # print(n, s)
        if s['maxInputChannels'] > 0:
            ai = ai + str(s['index']) + ": " + s['name'] + "\n"
        if s['maxOutputChannels'] > 0:
            ao = ao + str(s['index']) + ": " + s['name'] + "\n"
        n = n + 1
    PA.terminate()

    AUDIOdevin = None
    
    s = simpledialog.askstring("Device","Select audio INPUT device:\nPress Cancel for Windows Default\n\n" + ai + "\n\nNumber: ")
    if (s != None):         # If Cancel pressed, then None
        try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
            v = int(s)
        except:
            s = "error"

        if s != "error":
            if v < 0 or v > ndev:
                v = 0
            AUDIOdevin = v

    AUDIOdevout = None

    s = simpledialog.askstring("Device","Select audio OUTPUT device:\nPress Cancel for Windows Default\n\n" + ao + "\n\nNumber: ")
    if (s != None):         # If Cancel pressed, then None
        try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
            v = int(s)
        except:
            s = "error"

        if s != "error":
            if v < 0 or v > ndev:
                v = 0
            AUDIOdevout = v


# ================ Make Screen ==========================

root=Tk()
root.title("RMS meter V01a.py(w) (14-10-2018)")

root.minsize(100, 100)

frame1 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame1.pack(side=TOP, expand=1, fill=X)

frame2 = Frame(root, background="black", borderwidth=5, relief=RIDGE)
frame2.pack(side=TOP, expand=1, fill=X)

frame3 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame3.pack(side=TOP, expand=1, fill=X)

ca = Canvas(frame2, width=CANVASwidth, height=CANVASheight, background=COLORcanvas)
ca.pack(side=TOP)

b = Button(frame1, text="Audio on/off", width=Buttonwidth1, command=BAudiostatus)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="Soundcard", width=Buttonwidth1, command=BSoundcard)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="Start", width=Buttonwidth2, command=BStart)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="Stop", width=Buttonwidth2, command=BStop)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="-Time", width=Buttonwidth2, command=BTime1)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="+Time", width=Buttonwidth2, command=BTime2)
b.pack(side=LEFT, padx=5, pady=5)

# Fonts, after initialisation of the tk screen! 
RMSfont = font.Font(size=RMSfontsize)
# FREQfont = font.Font(family="Helvetica", size=FREQfontsize, weight="bold")
INFOfont = font.Font(size=INFOfontsize)
# INFOfont = font.Font(family="Helvetica", size=INFOfontsize, weight="bold")

# ================ Call main routine ===============================
root.update()               # Activate updated screens
SELECTaudiodevice()
AUDIOin()
 


