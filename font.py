from tkinter import *
import tkinter.font as font

gui = Tk(className='Python Examples - Button')
gui.geometry("200x100")

# define font
myFont = font.Font(family='Helvetica', size=20, weight='bold')

# create button
button = Button(gui, text='My Button', bg='white', fg='black')
# apply font to the button label
button['font'] = myFont
# add button to gui window
button.pack()

gui.mainloop()