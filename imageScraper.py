# Name: Anju Ito

import requests, time
import bs4 as bs
from PIL import Image
from io import BytesIO

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

# Inputs keyword that you want to look up, and returns list of sample images
# containing at least n pictures 
def keywordImageRetriever(keyword, n=300):
    html = retrieveHtmlFromGoogleImage(keyword)
    imageUrls = retrieveImageUrls(html)
    imageList = convertUrlsToImages(imageUrls)
    return imageList

# Use Selenium to search Google Image for keyword, and returns HTML of that page
def retrieveHtmlFromGoogleImage(keyword):
    chromeDriverPath = 'C:\\Users\\anjua\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\chromedriver_win32\\chromedriver.exe'
    with Chrome(chromeDriverPath) as driver:
        '''driver.minimize_window()'''
        driver.get('http://image.google.com')
        assert 'Google Images' in driver.title
        elem = driver.find_element_by_name('q')
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.1)
        # Scrolls down the page to obtain HTML code with more images loaded
        for i in range(35):
            start = i*1080
            # Citation: modified code from below URL for driver.execute_script
            # https://www.edureka.co/community/4578/possible-scroll-webpage-selenium-webdriver-programmed-python
            driver.execute_script(f"window.scrollTo({start},{start + 1080});") 
            time.sleep(0.05)
        html = driver.page_source
        '''url = driver.current_url'''
        return html

'''
def getHtmlOfUrls(urls):
    htmlList = []
    for url in urls:
        request = requests.get(url)
        html = bs.BeautifulSoup(request.content, 'html.parser')
        htmlList.append(html)
    return htmlList
'''

def retrieveImageUrls(html):
    imageUrls = []
    html = bs.BeautifulSoup(html, 'lxml')
    for imageTag in html.find_all('img'):
        imageLink = imageTag.get('src')
        if (imageLink and imageLink.startswith('http')): 
            # not empty string and not Google's stored image
            imageUrls.append(imageLink)
    return imageUrls

def convertUrlsToImages(imageUrls):
    imageList = []
    for imageUrl in imageUrls:
        # Citation: Below 2 lines taken from loadImage() of cmu_112_graphics.py
        # Downloaded from: https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
        response = requests.request('GET', imageUrl)
        image = Image.open(BytesIO(response.content))
        imageList.append(image)
    return imageList