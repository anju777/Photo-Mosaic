# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

# This module contains functions that performs most operations on the image,
# Including the creation of photo mosaics, etc.

from cmu_112_graphics import *
from PIL import Image, ImageColor
from imageScraper import convertUrlToImage
from io import BytesIO
import numpy as np

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
#############################################################################

############################### MAIN FUNCTION ###############################
# Takes in an image object, and returns the image mosaic
def imageMosaicCreator(mainImage, sampleImages, rowCol=None):
    # Allows function to take in imageUrl as mainImage as well
    if (isinstance(mainImage, str) and mainImage.startswith('http')):
        mainImage = convertUrlToImage(mainImage)
    if (rowCol == None):
        rows, cols = obtainRowsCols(mainImage)
    elif (isinstance(rowCol, tuple)):
        rows, cols = rowCol
    sampleImages = sizeSampleImages(sampleImages, mainImage, rows, cols)
    sampleImagesRGB = getListOfRGBValues(sampleImages)
    griddedImages = gridImage(mainImage, rows, cols)
    avgRGBMain = getAverageRGB(mainImage)

    for row in range(rows):
        for col in range(cols):
            avgRGB = getAverageRGB(griddedImages[row][col])
            indexOfSampleImage = findClosestRGB(avgRGB, sampleImagesRGB)
            sampleImage = sampleImages[indexOfSampleImage]
            griddedImages[row][col] = sampleImage

    result = convertGridsToOriginal(griddedImages, avgRGBMain)
    return result
#############################################################################

# Takes in image and ratio (default = 4:3), and returns rows/cols that would
# be optimal to split the image into
def obtainRowsCols(image, ratio=(4, 3), minLength=30):
    base = min(ratio)
    multiplier = minLength / base
    ratio = multiplyElement(ratio, multiplier)
    rows = int(image.height / ratio[1])
    cols = int(image.width / ratio[0])
    return rows, cols

############################# sizeSampleImages ##############################
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
#############################################################################

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

def getRGBGridded(image, rows=3, cols=3):
    griddedImages = gridImage(mainImage, rows, cols)
    result = np.zeros((rows, cols))
    for row in range(rows):
        for col in range(cols):
            grid = griddedImages[row][col]
            avgRGB = 

############################# getAverageRGB #################################
# Takes in an image object and returns a tuple of the average RGB of the image
def getAverageRGB(image):
    # Modifies image so that it can be represented with 256 (limited) colors
    image = image.quantize()
    colorList = np.array(image.getcolors()) # 2D Array: count, palette number
    colorPalette = np.array(image.getpalette()) # Array of RGB w/o separation
    colorList = combineListAndPalette(colorList, colorPalette)
    multiplier = np.array([colorList[:, 0]]).transpose()
    rgbValues = np.stack(colorList[:, 1])
    # Multiplies all elements by  count, adds them up, and divides to take avg
    result = np.multiply(multiplier, rgbValues) 
    result = np.sum(result.T, axis=-1) 
    pixelCount = image.width * image.height
    #avgRGB = np.divide(result, pixelCount, dtype=int)
    avgRGB = result // pixelCount
    return avgRGB

# Takes in colorCount (list of (count, paletteNumber)) & palette (list of RGB 
# values without categorization. Returns new list as (count, (RGB Value))
def combineListAndPalette(colorList, colorPalette):
    countList = colorList[:, 0]
    paletteNum = colorList[:, 1]
    colorPalette = np.array(np.split(colorPalette, len(colorPalette)//3))
    result = np.array([[countList[0], colorPalette[paletteNum[0]]]])
    for i in range(1, len(colorList)):
        row = np.array([[countList[i], colorPalette[paletteNum[i]]]])
        result = np.concatenate((result, row))
    return result   #2D matrix in numpy

# Takes in set/list/tuple and returns with each element multiplied by multiplier
#   Default return type is lists and normal multipliacation, but can specify
#   Mode: can return elements consisting of 'int' or 'float' (regular)
#   Target: Returns result in indicated object format (list, set, or tuples)
def multiplyElement(L, multiplier, mode='float', target=list()):
    mode = mode.lower()
    if (mode != 'int' and mode != 'floor' and mode != 'float'):
        return 'Mode only takes in "int" or "float"'
    result = []
    for elem in L:
        if (mode == 'int'):
            product = int(elem * multiplier)
        elif (mode == 'float'):
            product = elem * multiplier 
        result.append(product)
    if isinstance(target, list):
        return result
    elif isinstance(target, tuple):
        return tuple(result)
    elif isinstance(target, set):
        return set(result)
    else:
        return 'Error: Target type must be object of type list, tuple, or set'

# Takes in element and returns element with each element divided by divisor
#   Default return type is lists and integer divides, but can also specify
#   Mode: can integer divide ('int'), floor divide ('floor'), or 'float' divide
#   Target: Returns result in indicated object format (list, set, or tuples)
def divideElement(L, divisor, mode='int', target=list()):
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
############################################################################

############################# findClosestRGB ###############################
# Takes in target RGB (tuple) and list of RGB Values (tuples), and returns 
# the indexof the RGB value in the list closest to the target 
def findClosestRGB(targetRGB, RGBList):
    smallestDifference = None
    closestIndex = None
    targetRed, targetGreen, targetBlue = targetRGB
    for i in range(len(RGBList)):
        red, green, blue= RGBList[i]
        redDifference = abs(targetRed - red)
        greenDifference = abs(targetGreen - green)
        blueDifference = abs(targetBlue - blue)
        avgDifference = (redDifference + greenDifference + blueDifference)/3
        if (smallestDifference == None or avgDifference < smallestDifference):
            smallestDifference = avgDifference
            closestIndex = i
    return closestIndex

# Takes in 2D list containing image objects, and returns the images put together
# Note: all sizes of images in the griddedImages must be the same
def convertGridsToOriginal(griddedImages, backgroundColor=0):
    rows = len(griddedImages)
    cols = len(griddedImages[0])
    griddedImage = griddedImages[0][0]
    gridWidth, gridHeight = griddedImage.size
    resultWidth, resultHeight = gridWidth * cols, gridHeight * rows
    result = Image.new('RGB', (resultWidth, resultHeight), backgroundColor)
    for row in range(rows):
        for col in range(cols):
            griddedImage = griddedImages[row][col]
            x1, y1 = gridWidth * col, gridHeight * row
            x2, y2 = x1 + griddedImage.width, y1 + griddedImage.height
            result.paste(griddedImage, (x1, y1, x2, y2))
    return result
############################################################################