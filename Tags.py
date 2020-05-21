import mutagen
import os
import csv
from tkinter import *
from tkinter.filedialog import askdirectory
import sys
# import librosa
import pygame

#File chooser
#root = Tk()
#root.minsize(300, 300)

list_of_songs = []
index = 0
current_file = "E:\\14 - Together In Electric Dreams.flac"
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
FOLDER_PATH = r'C:\Users\Lenovo PC\Documents\Sound-Traverse'


class song_tags:

    def __init__(self, name, title, artist, album, tr_num, date, genre, len, format):
        self.name = name
        self.title = title
        self.artist = artist
        self.album = album
        self.tr_num = tr_num
        self.date = date
        self.genre = genre
        self.len = len
        self.format = format

    #Creates tags base
    def make_base(self):
        try:
            open('tags_base.txt', "r")
        except FileNotFoundError:
            open(FOLDER_PATH + r'\\{}'.format('tags_base.txt'), 'w')

    #Read tags and adds song whth its tags to the base
    def info(currentFile):
        key_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
        curr_tags = {}
        current_audio = mutagen.File(currentFile)
        for key in key_tags:
            curr_key = key.strip('\'')
            try:
                curr_tags[curr_key] = str(current_audio[key])
            except KeyError:
                curr_tags[curr_key] = "None"
    #
    def update_track(path):
        pass

    def update_folder(path):
        pass

    def directory_chooser():
        directory = askdirectory()
        os.chdir(directory)

        for format in FORMATS:
            for files in os.listdir(directory):
                if files.endswith(format):
                    list_of_songs.append(files)


#directory_chooser()
#make_base()
#for rec in list_of_songs:
#    print(rec + "\n")


def directory_chooser():
    directory = askdirectory()
    os.chdir(directory)

    for format in FORMATS:
        for files in os.listdir(directory):
            if files.endswith(format):
                info(files)
                list_of_songs.append(files)

def info(currentFile):
    key_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    curr_tags = {}
    current_audio = mutagen.File(currentFile)
    for key in key_tags:
        curr_key = key.strip('\'')
        if key == 'name':
            try:
                curr_tags[curr_key] = str(currentFile)
            except KeyError:
                curr_tags[curr_key] = "None"
            except TypeError:
                print("Typ się wywalił z rowerka")
        else:
            try:
                curr_tags[curr_key] = str(current_audio[key])
            except KeyError:
                curr_tags[curr_key] = "None"
            except TypeError:
                print("Typ się wywalił z rowerka")
    print(curr_tags)
    print('\n')

directory_chooser()