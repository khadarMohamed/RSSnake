"""
This program will display a Tkinter GUI
"""

import tkinter
import webbrowser
import Controller.feedparser
import random
from tkinter import *

class TkinterGui:
    def __init__(self, TIME_LOOP, argv):
        self.root = Tk()
        self.argv = argv
        if (len(self.argv) > 2 and len(self.argv) != 3):
            print("Args were found, but invalid. Correct usage: (--top / --bottom) (--left / --right) i.e --top --right")
        self.TIME_LOOP = TIME_LOOP
        self.library = []
        urls = self.readfeeds()
        for url in urls:
            self.library += Controller.feedparser.parse(url)
            random.shuffle(self.library)
        self.entrynum = 0
        
        
        self.build()
        
       
    def build(self):
        #initialize a few variables for runtime
        self.inverse = False
        headline = "No RSS Feeds Found!"
        url = None
        self.waiting = False
        
        #try to read in URL's
        try:
            entry = self.library[self.entrynum]
            headline = entry[0]
            url = entry[1]
        except IndexError:
            print("No valid URL's found, update and retry.")
            self.popup()
            self.waiting = True
        
        #Create widgets to display
        self.label = Label(self.root, text=headline, font = "Arial 12")
        self.resize()
        if(self.inverse):
            self.label.pack(side=LEFT)
        else:
            self.label.pack(side=RIGHT)
        photo = PhotoImage(file = "Assets/cog.png")
        photosized = photo.subsample(8, 8)
        self.button = Button(self.root, image = photosized, command=self.popup)
        self.button.image = photosized #It literally does not work without this reference.
        
        #Depending on if we open to the left or right side,
        #adjust the layout accordingly.
        if(self.inverse):
            self.button.pack(side=LEFT)
        else:
            self.button.pack(side=RIGHT)
        
        # start the timer to refresh the label.
        # if we're waiting on user input (when no RSS feeds are present), 
        # do nothing.
        if(not self.waiting):
            self.label.after(0, self.refresh_label)
        self.root.overrideredirect(True)
        self.root.mainloop()
        
    def resize(self):
        self.root.update_idletasks() # Ensures winfo gives the correct widths and heights.
        clientWidth = self.root.winfo_screenwidth()
        clientHeight = self.root.winfo_screenheight()
        windowWidth = self.root.winfo_width()
        windowHeight = self.root.winfo_height()
        height_diff = clientHeight - windowHeight
        width_diff = clientWidth - windowWidth

        if(len(self.argv) == 3):
            if(self.argv[1] == "--top"):
                if(self.argv[2] == "--right"):
                    self.root.geometry("+{0}+{1}".format((width_diff), 0))
                    self.inverse = True
            if(self.argv[1] == "--bottom"):
                if(self.argv[2] == "--right"):
                    self.root.geometry("+{0}+{1}".format(width_diff, height_diff - 40))
                    self.inverse = True
                if(self.argv[2] == "--left"):
                    self.root.geometry("+{0}+{1}".format(0, height_diff - 40))
        else:
            self.root.geometry("+0+0")
        
    def refresh_label(self):
        """ refresh the content of the label every second """
        #if we've reached the end of our list, cycle back to the start
        if(self.entrynum < len(self.library) - 1):
            # increment the entry
            self.entrynum += 1
        else:
            self.entrynum = 0
            
        # display the new entry
        entry = self.library[self.entrynum]
        headline = entry[0]
        url = entry[1]
        self.label.config(text="%s" % headline)
        self.label.bind("<Button-1>" ,lambda event, link=url: self.callback(event, link))
        self.resize()
        # request tkinter to call self.refresh after TIME_LOOP (the delay is given in ms)
        self.label.after(self.TIME_LOOP, self.refresh_label)
        
    def popup(self):
        settings = Toplevel()
        settings.title("RSSnake Settings Menu")
        settings.geometry("600x600")


        quitbutton = Button(settings, text = "quit and close", command=lambda:[settings.quit(), self.quit()])
        poplabel = Label(settings, text="Add an RSS / Atom Feed URL:")
        dataentry = Text(settings)
        for line in self.readfeeds():
            dataentry.insert(END, line + "\n")
        databutton = Button(settings, text = "Enter", command = lambda:[
             self.writefeeds(dataentry.get("1.0", END)),
             dataentry.config(state=DISABLED, highlightthickness = 0, bg = 'grey90'),
             self.quit(),
             TkinterGui(self.TIME_LOOP, self.argv)
            ])
        
        quitbutton.pack(side=BOTTOM)
        poplabel.pack()
        dataentry.pack()
        databutton.pack()
    def readfeeds(self):
        text = [line.strip() for line in open("Assets/Feeds.txt", "r")]
        while("" in text) : 
            text.remove("")
        return text
    def writefeeds(self, content):
        file = open("Assets/Feeds.txt", "w")
        file.write(content)
        file.close
    def quit(self):
        self.root.destroy()
    def callback(self, event, article_link):
        webbrowser.open_new(article_link)
        
        
        
    



