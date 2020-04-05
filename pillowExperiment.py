from PIL import Image

fileName = "Nagahama_Neru"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image1 = Image.open(imgPath)

fileName = "hkt"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image2 = Image.open(imgPath)

fileName = "planetEarth"
imgPath = f"C:\\Users\\anjua\\OneDrive\\Pictures\\15112_TP\\{fileName}.jpg"
image3 = Image.open(imgPath)

'''
image3.show() -> opens the image
bands = image3.getbands() -> get bands of input image
image3 = image3.crop((x1, y1, x2, y2))
image.getcolors()
'''