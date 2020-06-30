from tkinter import *

root = Tk()
root.geometry('300x300')
root.title("More Sound")
root.iconbitmap(r'001_speaker_plus_sign_6xq_icon.ico')

text = Label(root, text='More Sound')
text.pack()

photo = PhotoImage(file=r'002-play-right-arrow-triangle-outline.png')


def play_btn():
    print('None')

btn = Button(root, image=photo, command=play_btn)
btn.pack()

root.mainloop()
