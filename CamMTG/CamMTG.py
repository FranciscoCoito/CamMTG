
import cv2
import numpy

from os import listdir

# Configuaration
matchThreshold = 0.7

# Read templates
green = cv2.imread('mana_icons\green_mana.jpg',0)
blue = cv2.imread('mana_icons\blue_mana.jpg',0)
red = cv2.imread('mana_icons\red_mana.jpg',0)
white = cv2.imread('mana_icons\white_mana.jpg',0)
black = cv2.imread('mana_icons\black_mana.jpg',0)

if green is None or blue is None or red is None or white is None or black is None:
    print("At least one of the colours is NoneType")
    exit(0)
# All logos should be the same size
something = green.shape
w,h=green.shape[::-1]