# Name: Anju Ito

import requests, time, os
import bs4 as bs
from PIL import Image
from io import BytesIO
import threading
import time
from queue import Queue

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

# Inputs keyword that you want to look up, and returns list of sample images
# containing at least n pictures 

############################## MAIN FUNCTIONS #################################
def keywordImageRetriever(keyword, n=300):
    numThread = 50
    keywordDirectory = modifyKeywordForDirectory(keyword)
    path = f'C:/Users/anjua/OneDrive/Desktop/Photo-Mosaic/SampleImages/{keywordDirectory}'
    if (os.path.exists(path) and ((len(os.listdir(path)) + 50) > n)):
        imageList = retrieveImagesFromFile(path)
        return imageList
    htmlList = retrieveHtmlsFromGoogleImage(keyword)
    imageUrls = retrieveImageUrlsFromList(htmlList)
    imageList = convertUrlsToImagesAndSave(imageUrls, numThread
    
def convertUrlToImage(imageUrl):
    # Citation: Below 2 lines taken from loadImage() of cmu_112_graphics.py
    # Downloaded from: https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
    response = requests.request('GET', imageUrl)
    return Image.open(BytesIO(response.content)), path)
    return imageList
##############################################################################

######################## Global Variables (for threading) ####################

# Lock prevents List/variable from being edited at once
htmlList_lock = threading.Lock() 
i_lock = threading.Lock()
imageList_lock = threading.Lock()
###############################################################################

########################## modifyKeywordForDirectory #########################
def modifyKeywordForDirectory(keyword):
    illegalPunctuation = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}
    i = 0
    while (i < len(keyword)):
        if (keyword[i] in illegalPunctuation):
            keyword = keyword[:i] + keyword[i+1:]
        else: i += 1
    if (keyword == ''):
        return '_'
    return keyword
##############################################################################

######################## retrieveHtmlsFromGoogleImage ########################
# Use Selenium to search Google Image for keyword, and returns HTML of that page
def retrieveHtmlsFromGoogleImage(keyword, n=''):
    threads = []
    htmlList = []
    for n in range(13): # 13 is number of color filters + original page on Google Image
        if (n == 0): thread = threading.Thread(target=retrieveHtmlOfNormalImages,
            args=[keyword, htmlList])
        else: thread = threading.Thread(target=retrieveHtmlOfColorFilteredImages,
            args=[keyword, n, htmlList])
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return htmlList
        
def retrieveHtmlOfNormalImages(keyword, htmlList):
    chromeDriverPath = 'C:\\Users\\anjua\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\chromedriver_win32\\chromedriver.exe'
    with Chrome(chromeDriverPath) as driver:
        #driver.minimize_window()
        driver.get('http://image.google.com')
        assert 'Google Images' in driver.title
        elem = driver.find_element_by_name('q')
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.1)
        html = getHtmlOfGoogleImagePage(driver)
        with htmlList_lock:
            htmlList.append(html)

def retrieveHtmlOfColorFilteredImages(keyword, n, htmlList): # max of n is 12 (12 color options)
    chromeDriverPath = 'C:\\Users\\anjua\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\chromedriver_win32\\chromedriver.exe'
    with Chrome(chromeDriverPath) as driver:
        #driver.minimize_window()
        driver.get('http://image.google.com')
        assert 'Google Images' in driver.title
        elem = driver.find_element_by_name('q')
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.1)
        
        ### color selection: runs if there is any input for n
        driver.find_element_by_class_name('PNyWAd.ZXJQ7c').click() # Clicks on Tool
        time.sleep(0.3)
        driver.find_element_by_xpath("//div[@class='D0HoIc itb-h']/div[2]/div[1]/div[1]").click() # Clicks on Color Option
        time.sleep(0.3)
        if (n == 0): driver.find_element_by_class_name("sE24ib").click()
        else: driver.find_element_by_xpath(f"//div[@class='Ix6LGe']/div[1]/a[{n}]/div[1]/div[1]").click()                
        time.sleep(0.2)

        # returns html of page, completely loaded with all the images
        html = getHtmlOfGoogleImagePage(driver)
        with htmlList_lock:
            htmlList.append(html)

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
##############################################################################

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
    imgElems = html.find_all('img')
    for i in range(len(imgElems)):
        if (i == 0): continue
        imageLink = imgElems[i].get('src')
        if (imageLink and imageLink.startswith('http')): 
            # not empty string and not one of Google's stored image
            imageUrls.append(imageLink)
    return imageUrls
##############################################################################

############################ convertUrlsToImagesAndSave #######################
# Takes in a list of imageLinks and returns new list with Image objects of url
def convertUrlsToImagesAndSave(imageUrls, numThread, path):
    q = Queue()
    imageList = []
    threads = []
    i = -1
    if (not os.path.exists(path)): # creates folder to save images if not exist
        os.mkdir(path)
    for imageUrl in imageUrls:
        q.put(imageUrl)

    def imageToThreadThreader(imageList, path):
        while not q.empty():
            with i_lock: 
                nonlocal i
                i += 1
            imageUrl = q.get()
            AddImageUrlToListAndSave(imageUrl, i, imageList, path)
            q.task_done()

    for i in range(numThread):
        thread = threading.Thread(target=imageToThreadThreader, args=[imageList, path]) 
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    return imageList

def AddImageUrlToListAndSave(imageUrl, i, imageList, path, fileFormat='jpg'):
    response = requests.request('GET', imageUrl)
    # Adds appropriate extension to image file
    if (path.count('\\') > 0):
        imgPath = (f'{path}\\image{i}.{fileFormat}')
    else:
        imgPath = (f'{path}/image{i}.{fileFormat}')
    with open(imgPath, 'wb') as file:
        file.write(response.content) # response.content is in bytes
    with imageList_lock:
        imageList.append(Image.open(imgPath))

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