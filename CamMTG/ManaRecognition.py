
import numpy
import cv2

class ManaImageClass:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.updateImageInfo()

    def updateImageInfo(self):
        # Read template
        self.image = cv2.imread(self.path, 0)

        self.__logoFound = self.image is not None

        if self.hasLogo():
            # Set logo size
            self.w,self.h = self.image.shape[::-1]

    
    def hasLogo(self):
        return self.__logoFound


def colorCheck(color_template, draw_color, img_gray, img_to_check):
    print("Something")

def identify():

    from os import listdir

    # Configuaration
    matchThreshold = 0.7

    logos = [ManaImageClass("Green",'Icons\Mana\green_mana.jpg'),
             ManaImageClass("Blue",'Icons\Mana\Blue-symbol.png'),
             ManaImageClass("Red",'Icons\Mana\red_mana.jpg'),
             ManaImageClass("White",'Icons\Mana\White-symbol.png'),
             ManaImageClass("Black",'Icons\Mana\black_mana.jpg'),
             ManaImageClass("Colorless",'Icons\Mana\Colorless-symbol.png'),]


    #if not all(singleLogo.hasLogo() == True for singleLogo in logos):
    #    print("At least one of the colours is NoneType")
    #    exit(0)

    # Temporary for Testing
    if not any(singleLogo.hasLogo() == True for singleLogo in logos):
        print("All of the colours is NoneType")
        exit(0)

