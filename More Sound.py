from tkinter import *
from tkinter.filedialog import askdirectory
import os
from pygame import mixer

FORMATS = ['.mp3', '.wav', '.ogg', '.flac']

mixer.init() #initializing the mixer

root = Tk()


root.geometry('300x300')
root.title("More Sound")
root.iconbitmap(r'Icons/001_speaker_plus_sign_6xq_icon.ico')

text = Label(root, text='More Sound')
text.pack()

PlayPhoto = PhotoImage(file=r'Icons/002-play-right-arrow-triangle-outline.png')
StopPhoto = PhotoImage(file=r'Icons/008-square-outlined-shape.png')
PausePhoto = PhotoImage(file=r'Icons/008-square-outlined-shape.png')

def play_music():
    mixer.music.load("D:\Muzyka\Elton John-Diamonds-2CD\CD1\\107-elton_john-saturday_nights_alright_(for_fighting).mp3")
    if mixer.music.pause():
        mixer.music.unpause()
    else:
        mixer.music.play()

PlayBtn = Button(root, image=PlayPhoto, command=play_music)
PlayBtn.pack()

StopBtn = Button(root, image=StopPhoto, command=lambda: mixer.music.stop())
StopBtn.pack()

PauseBtn = Button(root, image=PausePhoto, command=lambda: mixer.music.pause())
PauseBtn.pack()

def directory_chooser():
    directory = askdirectory()
    os.chdir(directory)

    current_path = directory

    list_of_paths = []

    for format in FORMATS:
        for files in os.listdir(directory):
            if files.endswith(format):
                list_of_paths.append(directory + files)

    return list_of_paths

def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
scale.pack()

root.mainloop()
