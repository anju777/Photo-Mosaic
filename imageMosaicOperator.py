# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

# This module contains functions that performs most operations to the image,
# Including the creation of photo mosaics, etc.

from cmu_112_graphics import *
from PIL import Image, ImageColor
import timesheets

####################### Sample Images (Remove Later) ########################
fileName = "Nagahama_Neru"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image1 = Image.open(imgPath)

fileName = "hkt"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image2 = Image.open(imgPath)

fileName = "planetEarth"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image3 = Image.open(imgPath)
#############################################################################

# Takes in an image object, and returns the image mosaic
# Main function of the module
def createMosaicFromImage(mainImage, listOfSampleImages):
    ####### Replace later with rows/columns obtainer ##########
    rows =  50
    columns = 25
    ###########################################################
    sampleRGBValues = getListOfRGBValues(listOfSampleImages)
    griddedImage = gridImage(mainImage, rows, columns)

    for grid in range(len(griddedImage)):
        avgRGB = getAverageRGB(griddedImage[grid])
        indexOfSampleImage = findClosestValueFromList(avgRGB, sampleRGBValues)
        sampleImage = listOfSampleImages[indexOfSampleImage]
        griddedImage[grid] = sampleImage

    result = convertGridsToOriginal(griddedImage)
    return result

# Takes in an image object and obtains the average RGB in the image
def getAverageRGB(image):
    # Modifies image so that it can be represented with 256 colors
    image = image.quantize()
    colorList = image.getcolors()
    colorPalette = image.getpalette()
    colorList = combineListAndPalette(colorList, colorPalette)
    avgRGB = [0, 0, 0]

    # Takes sum of all individual colors in that image
    for count, RGBValue in colorList:
        for i in range(len(RGBValue)):
            avgRGB[i] += (RGBValue[i]*count)
    # Divides each element by total number of pixels to obtain average
    pixelCount = image.width * image.height
    avgRGB = divideElements(avgRGB, pixelCount, 'int', tuple())
    return avgRGB 

# Takes in colorCount & palette. Returns new list of (count, (RGB Value))
def combineListAndPalette(colorList, colorPalette):
    for i in range(len(colorList)):
        count = colorList[i][0]
        paletteNumber = colorList[i][1]
        redIndex = paletteNumber*3
        RGBList = colorPalette[redIndex:redIndex + 3]
        RGBTuple = tuple(RGBList)
        colorList[i] = (count, RGBTuple)        
    return colorList

# Takes in element and returns element with each element divided by divisor
# Default return type is lists and integer divides, but can also specify
# Mode: can integer divide ('int'), floor divide ('floor'), or 'float' divide
# target: takes in object (list, tuple, or set) and returns result of that type
def divideElements(L, divisor, mode='int', target=list()):
    mode = mode.lower()
    if (mode != 'int' and mode != 'floor' and mode != 'float'):
        return 'Mode only takes in "int", "floor", or "float"'
    result = []
    for elem in L:
        if (mode == 'int'):
            quotient = int(elem // divisor)
        elif (mode == 'floor'):
            quotient = elem // divisor
        elif (mode == 'float'):
            quotient = elem / divisor 
        result.append(quotient)
    if isinstance(target, list):
        return result
    elif isinstance(target, tuple):
        return tuple(result)
    elif isinstance(target, set):
        return set(result)
    else:
        return 'Error: Target type must be object of type list, tuple, or set'


def testGetAverageRGB():
    print('Testing getAverageRGB... ', end='')
    assert(getAverageRGB(image1) == (172, 169, 122))
    assert(getAverageRGB(image2) == (137, 109, 107))
    assert(getAverageRGB(image3) == (122, 117, 68))
    print('Passed!!')

def main():
    testGetAverageRGB()

if __name__ == '__main__':
    main()
'''
size sample image with image.crop()
grid.paste(sampleImage, box)
image3 = image3.quantize(256)
colorList = image3.getcolors()
image3.show('title')
image3.close()
'''