import TkinterGui
import tkinter
import feedparser
import threading
import time
import random

from tkinter import ttk

# Variables
TIME_LOOP = 5 # Seconds


def run_gui(*args):
    library = []
    for url in urls:
        library += feedparser.parse(url)
    random.shuffle(library)
    gui = TkinterGui.TkinterGui()
    cycle_thread = threading.Thread(target=cycle_news, args=[gui, library])
    cycle_thread.start()
    gui.start()

# This will loop through the library of URLs and show them in the gui 
def cycle_news(gui, library):
    while True:
        for item in library:
            gui.update(item[0], item[1])
            time.sleep(TIME_LOOP)


if __name__ == '__main__':
    urls = ['http://feeds.bbci.co.uk/news/rss.xml', 'http://rss.cnn.com/rss/cnn_topstories.rss']
    
    run_gui(urls)
    