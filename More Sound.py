from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
from pygame import mixer

FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
PAUSED = FALSE

mixer.init()  # initializing the mixer

root = Tk()

# Messagebox
def about_player():
    tkinter.messagebox.showinfo('About player', 'Version 0.1')

def browse_file():
    global filename
    filename = filedialog.askopenfilename()

# Menubar
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Play')
subMenu.add_command(label='Exit', command=root.destroy)
subMenu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Others', menu=subMenu2)
subMenu2.add_command(label='Open', command=about_player)

#root.geometry('300x300')
root.title("More Sound")
root.iconbitmap(r'Icons/001_speaker_plus_sign_6xq_icon.ico')

text = Label(root, text='More Sound')
text.pack()

#frame
middleframe = Frame(root)
middleframe.pack(padx=10, pady=10)

PlayPhoto = PhotoImage(file=r'Icons/002-play-right-arrow-triangle-outline.png')
StopPhoto = PhotoImage(file=r'Icons/008-square-outlined-shape.png')
PausePhoto = PhotoImage(file=r'Icons/002-two-vertical-parallel-lines.png')


def play_music():
    if PAUSED == TRUE:
        mixer.music.unpause()
        PASUED = FALSE
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
        except:
            browse_file()
            mixer.music.load(filename)
            mixer.music.play()
    statusbar['text']= 'Playing \"' + os.path.basename(filename) + '\"'

def pause_music():
    global PAUSED
    PAUSED = TRUE
    mixer.music.pause()
    statusbar['text'] = "Pause"

PlayBtn = Button(middleframe, image=PlayPhoto, command=play_music)
PlayBtn.grid(row=0, column=0, padx=10, pady=10 )

StopBtn = Button(middleframe, image=StopPhoto, command=lambda: mixer.music.stop())
StopBtn.grid(row=0, column=1, padx=10, pady=10)

PauseBtn = Button(middleframe, image=PausePhoto, command=pause_music)
PauseBtn.grid(row=0, column=2, padx=10, pady=10)

statusbar = Label(root, text,text="Welcome to More Sound", relief = SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

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
    volume = int(val) / 100
    mixer.music.set_volume(volume)

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.pack()

root.mainloop()
