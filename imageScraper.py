# Name: Anju Ito

import requests, time, os
import bs4 as bs
from PIL import Image
from io import BytesIO

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

# Inputs keyword that you want to look up, and returns list of sample images
# containing at least n pictures 

############################## MAIN FUNCTIONS #################################
def keywordImageRetriever(keyword, n=300):
    path = f'C:/Users/anjua/OneDrive/Desktop/Photo-Mosaic/SampleImages/{keyword}'
    if (os.path.exists(path) and ((len(os.listdir(path)) + 50) > n)):
        imageList = retrieveImagesFromFile(path)
        return imageList
    htmlList = retrieveHtmlsFromGoogleImage(keyword)
    imageUrls = retrieveImageUrlsFromList(htmlList)
    imageList = convertUrlsToImages(imageUrls)
    imageList.pop(0)
    saveImageList(imageList, path)
    return imageList
##############################################################################

######################## retrieveHtmlsFromGoogleImage ########################
# Use Selenium to search Google Image for keyword, and returns HTML of that page
def retrieveHtmlsFromGoogleImage(keyword):
    chromeDriverPath = 'C:\\Users\\anjua\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\chromedriver_win32\\chromedriver.exe'
    htmlList = []
    with Chrome(chromeDriverPath) as driver:
        #driver.minimize_window()
        driver.get('http://image.google.com')
        assert 'Google Images' in driver.title
        elem = driver.find_element_by_name('q')
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.1)
        html = getHtmlOfGoogleImagePage(driver)
        htmlList.append(html)
        '''driver.execute_script("location.reload();")
        time.sleep(0.1)
        driver.find_element_by_class_name('PNyWAd.ZXJQ7c').click() # Clicks on Tool
        time.sleep(1)
        nColor = 12
        for n in range(nColor):
            driver.find_element_by_xpath("//div[@class='D0HoIc itb-h']/div[2]/div[1]/div[1]").click() # Clicks on Color Option
            time.sleep(1)
            if (n == 0): driver.find_element_by_class_name("sE24ib").click()
            else: driver.find_element_by_xpath(f"//div[@class='Ix6LGe']/div[1]/a[{n}]/div[1]/div[1]").click()
            time.sleep(0.2)
            html = getHtmlOfGoogleImagePage(driver)
            htmlList.append(html)'''
        return htmlList
        
# Assumes that element is already at top of Google Image page, and retrieves html
# of the page with all the Google Image loaded
def getHtmlOfGoogleImagePage(driver):
    # Scrolls down so that more image is loaded for use
    endLocation = scrollDown(driver)
    time.sleep(0.5)
    # Returns list of length 1
    loadMoreButton = driver.find_elements_by_class_name('mye4qd')
    loadMoreButton[0].click()
    time.sleep(0.5)
    scrollDown(driver, endLocation)
    html = driver.page_source
    return html

# Run on selenium browser and scrolls page fully scrolled down n times
def scrollDown(driver, startOffset=0, n=35, webSize=1080):
    for i in range(n):
        start = i*webSize + startOffset
        # Citation: modified code from below URL for driver.execute_script
        # https://www.edureka.co/community/4578/possible-scroll-webpage-selenium-webdriver-programmed-python
        driver.execute_script(f"window.scrollTo({start},{start + webSize});") 
        time.sleep(0.1)
    return start + webSize

########################### retrieveImageUrlsFromList ########################
# Takes in list of html link and takes out all the image links inside
def retrieveImageUrlsFromList(htmlList):
    result = []
    for html in htmlList:
        imageUrls = retrieveImageUrlsFromHtml(html)
        result.extend(imageUrls)
    return result

def retrieveImageUrlsFromHtml(html):
    imageUrls = []
    html = bs.BeautifulSoup(html, 'lxml')
    for imageTag in html.find_all('img'):
        imageLink = imageTag.get('src')
        if (imageLink and imageLink.startswith('http')): 
            # not empty string and not one of Google's stored image
            imageUrls.append(imageLink)
    return imageUrls
##############################################################################

############################## convertUrlsToImages ###########################
# Takes in a list of imageLinks and returns new list with Image objects of url
def convertUrlsToImages(imageUrls):
    imageList = []
    for imageUrl in imageUrls:
        image = convertUrlToImage(imageUrl)
        imageList.append(image)
    return imageList

def convertUrlToImage(imageUrl):
    # Citation: Below 2 lines taken from loadImage() of cmu_112_graphics.py
    # Downloaded from: https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
    response = requests.request('GET', imageUrl)
    return Image.open(BytesIO(response.content))
##############################################################################

############################### SaveImageList ################################
# Takes in list of PIL Images and saves it into indicated path with file format
def saveImageList(imageList, path, fileFormat='jpg'):
    if (not os.path.exists(path)):
        os.mkdir(path)
        for i in range(len(imageList)): # First image always Google
            imageList[i] = imageList[i].convert(mode='RGB')
            if (path.count('\\') > 0):
                imageList[i].save(f'{path}\\image{i}.{fileFormat}')
            else:
                imageList[i].save(f'{path}/image{i}.{fileFormat}')
##############################################################################

########################### retrieveImagesFromFile ###########################
def retrieveImagesFromFile(path):
    if os.path.isfile(path):
        if (path.lower().endswith('jpg') or path.lower().endswith('png')):
            return [Image.open(path)]
    else:
        imageList = []
        for item in os.listdir(path):
            if (path.count('\\') > 0 and not path.endswith('\\')):
                innerPath = f'{path}\\{item}'
            elif (not path.endswith('/')):
                innerPath = f'{path}/{item}'
            else:
                innerPath = f'{path}{item}'
            images = retrieveImagesFromFile(innerPath)
            imageList += images
    return imageList
##############################################################################