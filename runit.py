import sys
from View.TkinterGui import TkinterGui

# Variables
TIME_LOOP = 5000 # Seconds
    

# This will loop through the library of URLs and show them in the gui 
if __name__ == '__main__':
    feed = TkinterGui(TIME_LOOP, sys.argv)

    
    