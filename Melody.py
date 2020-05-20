from tkinter import *

root = Tk()
root.geometry('300x300')
root.title("Muzyk")
#root.iconbitmap(r'F://play_button_mS9_icon.ico')

text = Label(root, text='Melody')
text.pack()

def play_btn():
    print('None')

btn = Button(root, text='Play', command=play_btn)
btn.pack()

root.mainloop()
