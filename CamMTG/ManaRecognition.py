
import numpy
import cv2
import imutils
from os import listdir, path


# Configuaration
matchThreshold = .3
TestCasePath = "TestImages/Source/SingleCards_2"
ResultPath = "TestImages/result_Files"



class ManaImageClass:
    _CONST_ICON = '[ICON]'
    _CONST_MANAPATH = 'Icons\TemplateMana\\' + _CONST_ICON + '-symbol.png'
    #_CONST_MANAPATH = 'Icons\TemplateMana\\' + _CONST_ICON + '-symbol.png'
    #_CONST_MANAPATH = 'Icons\Mana2\\' + _CONST_ICON + '-symbol.jpg'

    def __init__(self, name, colorTuple):
        self.name = name
        self.path = ManaImageClass._CONST_MANAPATH.replace(ManaImageClass._CONST_ICON,name)
        self.colorTuple = colorTuple
        self.updateImageInfo()

    def updateImageInfo(self):
        # Read template
        self.image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)#cv2.IMREAD_GRAYSCALE)
        self.__logoFound = self.image is not None

        if self.hasLogo():
            transMask = self.image[:,:,3] == 0
            self.image[transMask] = [255,255,255,255]
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.Canny(self.image,100,200)
            filename = path.join(ResultPath,self.name)
            print(filename)
            cv2.imwrite(filename + ".png",self.image)

            # Set logo size
            self.w,self.h = self.image.shape[::-1]

    
    def hasLogo(self):
        return self.__logoFound

    def checkColor(self,img_gray):
        scaleValue = 0
        for scale in numpy.linspace(0.05,1,20):
            resized = imutils.resize(self.image,width = int(self.image.shape[1] * scale))
            results = cv2.matchTemplate(img_gray, resized,cv2.TM_CCOEFF_NORMED)
            locations = numpy.where(results >= matchThreshold)

            val = len(list(zip(*locations[::-1])))
            wasIdentified = len(list(zip(*locations[::-1]))) > 0
            if wasIdentified:
                scaleValue = scale
                break

        return wasIdentified, locations, scaleValue

def markOnImage(locations, manaImageClass, originalImage,scale):
    for pt in zip(*locations[::-1]):
        pt2 = (pt[0] + round(manaImageClass.w * scale),pt[1] + round(manaImageClass.h * scale))
        cv2.rectangle(originalImage,pt,pt2,manaImageClass.colorTuple,2)



def clearFolder(folderPath):
    from os import unlink
    from shutil import rmtree

    for filename in listdir(folderPath):
        filePath = path.join(folderPath,filename)
        try:
            if path.isfile(filePath) or path.islink(filePath):
                unlink(filePath)
            elif path.isdir(filePath):
                rmtree(filePath)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (filePath, e))


def identify():


    logos = [#ManaImageClass("Black",(0,0,0)),
        ManaImageClass("Blue",(255,0,0)),
        #ManaImageClass("Green",(0,255,0)),
        #ManaImageClass("Red",(0,0,255)),
        #ManaImageClass("White",(255,255,255)),
        #ManaImageClass("Colorless",(125,125,125)),
        ]

    #clearFolder(ResultPath)


    if not all(singleLogo.hasLogo() == True for singleLogo in logos):
        print("At least one of the colours is NoneType")
        exit(0)

    for f in listdir(TestCasePath):
        fullPath = path.join(TestCasePath,f)

        if path.isfile(fullPath):
            print("File: " + fullPath)
            cardImage = cv2.imread(fullPath)
            
            # Change into Grayscale to compare with templte
            grayCardImage = cv2.cvtColor(cardImage, cv2.COLOR_BGR2GRAY)
            
            edgeCardImage = cv2.Canny(grayCardImage,100,200)
            
            filename = path.join(ResultPath,"ed_" + f)
            print(filename)
            cv2.imwrite(filename,edgeCardImage)

            atLeastOne = False
            for logo in logos:
                wasChecked,location,scale = logo.checkColor(edgeCardImage)
                if wasChecked:
                    print("Checked for " + logo.name)
                    markOnImage(location,logo,cardImage,scale)

                    atLeastOne|=wasChecked

            if atLeastOne:
                filename = path.join(ResultPath,f)
                print(filename)
                cv2.imwrite(filename,cardImage)

        elif path.isdir(fullPath):
            print("Directory: " + fullPath)
        else:
            print("Unknown: " + fullPath)


