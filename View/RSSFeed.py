from bs4 import BeautifulSoup
from tkinter import *
from urllib.request import urlopen
import webbrowser
import lxml

def cyclelink(x):
    entry = news_list[x]
    link = Label(root, text=entry.link.title)
    link.pack()
    link.bind("<Button-1>" ,lambda event, link=entry.link.text: callback(event, link))
    x = x + 1
def quit():
    root.destroy()
def callback(event, article_link):
    webbrowser.open_new(article_link)
    
parse_xml_url = urlopen("http://feeds.bbci.co.uk/news/rss.xml?edition=us")
xml_page = parse_xml_url.read()
parse_xml_url.close()
feed = BeautifulSoup(xml_page, "xml")
news_list = feed.findAll("item")


root = Tk()
text = Text(root)
x = 0
root.overrideredirect(True)
entry = news_list[x]
link = Label(root, text=entry.link.title)
link.pack(side=LEFT)
link.bind("<Button-1>" ,lambda event, link=entry.link.text: callback(event, link))
button = Button(root, text = 'Click and Quit', command=quit)
button.pack()
root.after(1000, cyclelink(x))    
root.mainloop()



    