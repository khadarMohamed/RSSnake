from urllib.request import urlopen
from urllib.error import HTTPError
import random
import time
from bs4 import BeautifulSoup # pip install beautifulsoup4



def parse(url):
    """ Parse the URL to XML and return list of headlines and urls like a key value pair """
    counter = 0
    while True:
        try:
            parsed_url = urlopen(url)
            page = parsed_url.read()
            parsed_url.close()
            # By default BS parses documents as HTML, to parse as XML, pass in as arg
            return build_library(BeautifulSoup(page, "xml")) # pip install lxml
        except HTTPError:
            if(counter >= 3):
                print("Something Went Wrong. Check Feeds.txt for invalid / Expired urls")
                break
            print("Too many Requests, retrying.")
            time.sleep(3)
            counter += 1
            continue
        except ValueError:
            print("Invalid url found, consider correcting.")
            return " "
        else:
            break
    


def build_library(page):
    """ Puts headlines and associated urls into a list """
    library = []
    top_stories = page.find_all("item") # "item" instead of "a" because all the links are in div id="item"
    for item in top_stories:
        lib_item = [item.title.text, item.link.text]
        library.append(lib_item)
    random.shuffle(library)
    return library
                                        