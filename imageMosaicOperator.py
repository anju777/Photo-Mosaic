# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

# This module contains functions that performs most operations to the image,
# Including the creation of photo mosaics, etc.

from cmu_112_graphics import *
from PIL import Image, ImageColor
import os
import timesheets

####################### Sample Images (Remove Later) ########################
fileName = "Nagahama_Neru"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image1 = Image.open(imgPath)

fileName = "HKT"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image2 = Image.open(imgPath)

fileName = "Nature"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image3 = Image.open(imgPath)

sampleImages = os.listdir("C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\")
for i in range(len(sampleImages)):
    text = sampleImages[i]
    imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{text}"
    sampleImages[i] = Image.open(imgPath)
#############################################################################


############################ MAIN FUNCTION #########################
# Takes in an image object, and returns the image mosaic
def createMosaicFromImage(mainImage, sampleImages):
    'Replace later with rows/columns obtainer '
    rows =  50
    cols = 25

    sampleImages = sizeSampleImages(sampleImages, mainImage, rows, cols)
    sampleImagesRGB = getListOfRGBValues(sampleImages)
    griddedImages = gridImage(mainImage, rows, cols)

    for row in range(rows):
        for col in range(cols):
            avgRGB = getAverageRGB(griddedImages[row][col])
            indexOfSampleImage = findClosestValue(avgRGB, sampleImagesRGB)
            sampleImage = sampleImages[indexOfSampleImage]
            griddedImages[row][col] = sampleImage

    result = convertGridsToOriginal(griddedImages)
    return result



########################## sizeSampleImages ##############################
# Takes in list of images and returns the same list of images, but sized to 
# match the size of each grid if the mainImage was cut up in indicated rows/cols
def sizeSampleImages(sampleImages, mainImage, rows, cols):
    for i in range(len(sampleImages)):
        sampleImages[i] = sizeImage(sampleImages[i], mainImage, rows, cols)
    return sampleImages

# Takes in an image and returns the image, sized to match the size of each grid 
# if the mainImage was cut up in indicated rows/cols
def sizeImage(image, mainImage, rows, cols):
    '''Note: crops image (takes top left part) & resizes, so might need to 
    modify later if want better selection/compression (just skip to resize
    for latter), and fractal expansion'''
    gridWidth, gridHeight = mainImage.width//cols, mainImage.height//rows
    ratioHeight, ratioWidth = image.height/gridHeight, image.width/gridWidth
    baseRatio = min(ratioHeight, ratioWidth)
    targetWidth, targetHeight = gridWidth * baseRatio, gridHeight * baseRatio

    image = image.resize((gridWidth, gridHeight), 3, 
            (0, 0, targetWidth, targetHeight))
    return image

############################################################################

# Takes in list of images and returns list (same len) of tuples containing RGB
# values of each elements
def getListOfRGBValues(imageList):
    RGBList = []
    for image in imageList:
        RGBValue = getAverageRGB(image)
        RGBList.append(RGBValue)
    return RGBList

# Takes in an image and returns a 2D list of the image with indicated rows/cols
def gridImage(image, rows, cols):
    result = []
    gridWidth = image.width // cols
    gridHeight = image.height // rows
    for row in range(rows):
        result.append([])
        for col in range(cols):
            grid = image.crop((col*gridWidth, row*gridHeight, 
                    col*gridWidth + gridWidth, row*gridHeight + gridHeight))
            result[row].append(grid)
    return result

########################## getAverageRGB #################################
# Takes in an image object and returns a tuple of the average RGB of the image
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

# Takes in colorCount (list of tuples (count, paletteNumber)) & palette (list
# of RGB values (not separated by tuples, etc.)). 
# Returns new list in the format(count, (RGB Value))
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
#   Default return type is lists and integer divides, but can also specify
#   Mode: can integer divide ('int'), floor divide ('floor'), or 'float' divide
#   Target: Returns result in indicated object format (list, set, or tuples)
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

############################################################################

# Takes in target value and a list, and returns the index closest to the target
def findClosestValue(value, inputList):
    smallestDifference = None
    closestIndex = None
    for i in range(len(inputList)):
        difference = abs(value - inputList[i])
        if (smallestDifference == None or difference < smallestDifference):
            smallestDifference = difference
            closestIndex = i
    return closestIndex

# Takes in 2D list containing image objects, and returns the images put together
# Note: all sizes of images in the griddedImages must be the same
def convertGridsToOriginal(griddedImages):
    rows = len(gridedImages)
    cols = len(griddedImages[0])
    griddedImage = griddedImages[0][0]

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