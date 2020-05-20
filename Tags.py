import mutagen
import os
from tkinter import *
from tkinter.filedialog import askdirectory
import sys
# import librosa
import pygame

#File chooser
root = Tk()
root.minsize(300, 300)

listOfSongs = []
index = 0

def directoryChooser():
    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".flac"):
            listOfSongs.append(files)

#directoryChooser()

currentFile = "F:\\02 - Les chants magnetiques II.flac"

# Tags base
def make_base():
    try:
        open('tags_base.txt', 'r')
    except IOError:
        createList()


def addToBase():
    for i in selectFolder:
        pass


def updateMeta(filepath):
    pass


def currentFileInfo(currentFile):
    current_tags = []
    current_audio = mutagen.File(currentFile)
    try:
        artist = str(current_audio["artist"])
    except KeyError:
        artist = "None"
    try:
        album = str(current_audio["album"])
    except KeyError:
        album = "None"
    """try:
        year = current_audio["year"]
    except IOError:
        year = "None"""""

    print(artist + '\n')
    print(album + '\n')
    # print("\n" + str(current_audio["title"]) + "\n" + str(current_audio["artist"]) + "\n" + str(current_audio) + "\n" + str(current_audio['album']) + "\n")


#currentFileInfo(currentFile)
basepath = 'F:'
for entry in os.listdir(basepath):
    if os.path.isdir(os.path.join(basepath, entry)):
        print(entry)