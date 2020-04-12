from bs4 import BeautifulSoup
from tkinter import *
from urllib.request import urlopen
import webbrowser
import lxml
from pip._internal import self_outdated_check

class Feed:
    def __init__(self, parent):
        
        parse_xml_url = urlopen("http://rss.cnn.com/rss/cnn_topstories.rss")
        xml_page = parse_xml_url.read()
        parse_xml_url.close()
        
        self.source = BeautifulSoup(xml_page, "xml")
        self.news_list = self.source.findAll("item")
        self.entrynum = 0
        entry = self.news_list[self.entrynum]
       
        self.label = Label(parent, text=entry.title.contents)
        self.label.bind("<Button-1>" ,lambda event, link=entry.link.text: self.callback(event, link))
        self.label.pack(side=LEFT)
        self.button = Button(root, text = 'Click and Quit', command=self.quit)
        self.button.pack()
        # start the timer
        self.label.after(3000, self.refresh_label)

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the entry
        self.entrynum += 1
        # display the new entry
        entry = self.news_list[self.entrynum]
        self.label.config(text="%s" % entry.title.contents)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label.after(3000, self.refresh_label)
    def quit(self):
        root.destroy()
    def callback(self, event, article_link):
        webbrowser.open_new(article_link)

if __name__ == "__main__":
    root = Tk()
    timer = Feed(root)
    root.overrideredirect(True)
    root.mainloop()