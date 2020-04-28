# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

from cmu_112_graphics import *
from imageScraper import keywordImageRetriever, convertUrlToImage, retrieveImagesFromFile
from imageMosaicOperator import imageMosaicCreator

# Sample Main Images from: 
# https://i.pinimg.com/originals/54/a0/8f/54a08f440ac87229c787c4a7d4d7c2e1.jpg
# https://i.pinimg.com/originals/99/28/73/9928737a3504c5fc8269377d8ba5a122.jpg 
# https://1.bp.blogspot.com/-lMg-uRzjXXQ/VWUVykvi6jI/AAAAAAAAAUA/SyND9ucVWU8/s1600/High%2BResolution%2BSpace%2BWallpaper.jpg

class TitleMode(Mode):
    def appStarted(mode):
        mode.titleText = 'PHOTO MOSAIC\nCREATOR'
        mode.optionsText = ['Create', 'Help']
        mode.optionsDestination = [mode.app.ImportSamplesMode, mode.app.HelpMode]
        mode.buttonHeight = mode.height * 4/5
        mode.buttons = mode.app.createButtonsWithFixedY(mode, mode.optionsText, 
            mode.optionsDestination, mode.buttonHeight, 40, 200, 'rectangle', 'white')

    def mousePressed(mode, event):
        for button in mode.buttons:
            buttonClicked = button.isClicked(event.x, event.y)
            if (buttonClicked):
                nextMode = buttonClicked
                mode.app.previousMode = mode.app.TitleMode
                mode.app.setActiveMode(nextMode)

    def redrawAll(mode, canvas):
        font = 'Arial 40 bold'
        cx = mode.width//2
        cy = mode.height//2
        canvas.create_image(cx, cy, image=mode.app.background)
        canvas.create_text(cx, cy, text=mode.titleText, font=font, fill='White')
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)



class HelpMode(Mode):
    def appStarted(mode):
        mode.backgroundColor = 'Light Pink'
        mode.borderColor = 'Cyan'
        mode.space = 0
        mode.margin = 30
        mode.font = 'Arial 12'
        mode.text = '''Welcome to the Photo Mosaic Creator!\n\n
Here, you can create photo mosaics based on keyword input or by importing your own images and videos.
The basic features and their descriptions are listed below. Enjoy!


- Keyword Feature: Takes in keyword and imports images from the Internet to use.
              * Uses Selenium and incorporated threads so multiple folders can open at the same time ^^

- Import: Can import folder from your computer with all your favorite photos!
              * The imported photo can have multiple files inside (can have movie, etc. files inside)

- Main Image Selection: Choose from one of the provided images or import your own from your computer

- Optional Features:
        1. Rows/Cols: Choose the number of rows and cols that the final photo mosaic will be made up of
        2. Basic/Detailed: Choose the level of analysis of the images. 
            The higher the number, the better image created! (but takes longer time)
            Number indicates how many rows and cols each grid will be separated into for analysis
\n\n\n
\t\t\t               ***Press any key to return***
'''

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.previousMode)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(mode.space, 0, mode.width-mode.space, 
            mode.height, fill=mode.borderColor)
        canvas.create_rectangle(mode.space+mode.margin, mode.margin, 
            mode.width-mode.space-mode.margin, mode.height-mode.margin, 
            fill=mode.backgroundColor)
        canvas.create_text(mode.width//2, mode.height//2, text=mode.text, font=mode.font)



class SelectionMode(Mode):
    def appStarted(mode):
        mode.titleText = 'Selection'
        mode.createButtons()

    def createButtons(mode):
        buttonY = mode.height * 2/3
        marginSpace = 100
        buttonR = 100
        buttonShape = 'ellipse'
        buttonColor = 'white'
        buttonFont = 'Arial 20 bold'
        videoButton = Button(marginSpace, buttonY-buttonR, marginSpace+(buttonR*2), 
            buttonY+buttonR, 'Video', mode.app.ImportVideoSamplesMode,
            buttonShape, buttonColor, buttonFont)
        photoMosaicButton = Button(mode.width-marginSpace-buttonR*2, buttonY-buttonR, 
            mode.width-marginSpace, buttonY+buttonR, 'Photo Mosaic\n      Creator',
            mode.app.ImportSamplesMode, buttonShape, buttonColor, buttonFont)
        mode.buttons = [videoButton, photoMosaicButton]

    def mousePressed(mode, event):
        for button in mode.buttons:
            buttonClicked = button.isClicked(event.x, event.y)
            if (buttonClicked):
                nextMode = buttonClicked
                mode.app.previousMode = mode.app.TitleMode
                mode.app.setActiveMode(nextMode)

    def redrawAll(mode, canvas):
        font = 'Arial 40 bold'
        cx = mode.width//2
        cy = mode.height//2
        titleY = mode.height*1/3
        canvas.create_image(cx, cy, image=mode.app.background)
        canvas.create_text(cx, titleY, text=mode.titleText, font=font, fill='Navy')
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)



class ImportSamplesMode(Mode):
    def appStarted(mode):
        mode.createButtons()

    def modeActivated(mode):
        mode.app.input = ''
        mode.app.keywordBar = False
        mode.counter = 1
        mode.nextButton.color = 'gray'

    def createButtons(mode):
        mode.keywordMargin = 150
        mode.keywordY = mode.height*0.4
        keywordHeight = 40
        keywordButton = Button(mode.keywordMargin, mode.keywordY-(keywordHeight//2), 
            mode.width-mode.keywordMargin, mode.keywordY+(keywordHeight//2))

        importWidth = 150
        importHeight = 40
        importY = mode.height*0.7
        importButton = Button((mode.width//2)-(importWidth//2), importY-(importHeight//2),
            (mode.width//2)+(importWidth//2), importY+(importHeight//2), 'Import')

        nextWidth = 120
        mode.nextButton = Button(mode.width*0.7, mode.height*0.8, mode.width*0.7+nextWidth,
            mode.height*0.8+40, 'Next', mode.app.ImportMainMode, color='gray')

        mode.buttons = [keywordButton, importButton, mode.nextButton]
    
    def timerFired(mode):
        if (mode.app.sampleImages):
            mode.nextButton.color = 'white'
        else: mode.nextButton.color = 'gray'

    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content == ''):
                    mode.app.keywordBar = True
                elif (button.content == 'Import'):
                    mode.app.sampleImagesFile = filedialog.askdirectory(title='Select folder: ')
                    if (mode.app.sampleImagesFile):
                        mode.app.sampleImages = retrieveImagesFromFile(mode.app.sampleImagesFile)
                elif (button.content == 'Next'):
                    if (mode.app.sampleImages):
                        mode.app.setActiveMode(nextMode)
                    else:
                        mode.app.showMessage('Please import sample images first')

    def keyPressed(mode, event):
        if (mode.app.keywordBar):
            if (event.key == 'Space'):
                mode.app.input += ' '
            elif (event.key == 'Backspace'):
                mode.app.input = mode.app.input[:-1]
            elif (event.key == 'Enter'):
                mode.app.sampleImages = keywordImageRetriever(mode.app.input)
                mode.app.keywordBar = False
            elif (len(event.key) == 1):
                mode.app.input += event.key

    def drawInput(mode, canvas):
        font = 'Arial 20 bold'
        mode.counter += 1
        blinkTime = 20
        inputX = mode.keywordMargin + 10
        if (mode.app.keywordBar and mode.counter%blinkTime < blinkTime//2):
            canvas.create_text(inputX, mode.keywordY, text=(mode.app.input + '|'), 
                anchor='w', fill='Black', font=font)
        canvas.create_text(inputX, mode.keywordY, text=mode.app.input, anchor='w', fill='Black', font=font)

    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        font='Arial 20 bold'
        fontColor = 'white'
        canvas.create_image(cx, cy, image=mode.app.background)
        canvas.create_text(cx, mode.height*0.1, text='Sample Images', fill=fontColor, font=font)
        canvas.create_text(cx, mode.height*0.3, text='Import with Keyword!\n(Press Enter to Search)', fill=fontColor, font=font)
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)
        mode.drawInput(canvas)
        canvas.create_text(cx, mode.height*0.6, text='Or Import from Computer!', fill=fontColor, font=font)



class ImportMainMode(Mode):
    def appStarted(mode):
        # Citation: main images taken from URL in functions below
        mode.main1 = convertUrlToImage('https://i.pinimg.com/originals/54/a0/8f/54a08f440ac87229c787c4a7d4d7c2e1.jpg')
        mode.main2 = convertUrlToImage('https://i.pinimg.com/originals/99/28/73/9928737a3504c5fc8269377d8ba5a122.jpg')
        mode.main3 = convertUrlToImage('https://1.bp.blogspot.com/-lMg-uRzjXXQ/VWUVykvi6jI/AAAAAAAAAUA/SyND9ucVWU8/s1600/High%2BResolution%2BSpace%2BWallpaper.jpg')
        mode.mainImages = [mode.main1, mode.main2, mode.main3]
        mode.createButtons()
        mode.leverLevels = 6
        mode.segment = (mode.levsX2-mode.levsX1)//(mode.leverLevels-1)

    def modeActivated(mode):
        mode.app.rowsInput = mode.app.colsInput = ''
        mode.app.rowsBar = mode.app.colsBar = False
        mode.app.rowCol = None
        mode.counter = 0
        mode.app.currLevel = 3

    def createButtons(mode):
        importWidth = 150
        importHeight = 40
        importY = mode.height*0.7
        importButton = Button((mode.width//2)-(importWidth//2), importY-(importHeight//2),
            (mode.width//2)+(importWidth//2), importY+(importHeight//2), 'Import')

        nextWidth = 120
        mode.nextButton = Button(mode.width*0.7, mode.height*0.8, mode.width*0.7+nextWidth,
            mode.height*0.8+40, 'Next', mode.app.LoadingMode, color='gray')

        mode.imageX = mode.width//4
        mode.imageY = mode.height*0.4
        main1Button = Button(mode.imageX-mode.width*0.2//2, mode.imageY-mode.height*0.2//2,
                mode.imageX+mode.width*0.2//2, mode.imageY+mode.height*0.2//2,
                content=mode.mainImages[0], width=0)
        main2Button = Button(mode.imageX*2-mode.width*0.2//2, mode.imageY-mode.height*0.2//2,
                mode.imageX*2+mode.width*0.2//2, mode.imageY+mode.height*0.2//2,
                content=mode.mainImages[1], width=0)
        main3Button = Button(mode.imageX*3-mode.width*0.2//2, mode.imageY-mode.height*0.2//2,
                mode.imageX*3+mode.width*0.2//2, mode.imageY+mode.height*0.2//2,
                content=mode.mainImages[2], width=0)

        mode.rowColWidth = 60
        mode.rowColHeight = 30
        mode.rowColX = mode.width*0.15
        mode.rowY = mode.height*0.74
        mode.colY = mode.height*0.82
        rowsButton = Button(mode.rowColX, mode.rowY, mode.rowColX+mode.rowColWidth,
            mode.rowY+mode.rowColHeight, color='light gray', title='rows')
        colsButton = Button(mode.rowColX, mode.colY, mode.rowColX+mode.rowColWidth, 
            mode.colY+mode.rowColHeight, color='light gray', title='cols')
        mode.levsX1 = mode.width*0.07
        mode.levsX2 = mode.width*0.33
        mode.levsButton = Button(mode.levsX1, mode.height*0.88, mode.levsX2, 
            mode.height*0.9, fill='white', title='lever')

        mode.buttons = [importButton, mode.nextButton, main1Button, main2Button, 
            main3Button, rowsButton, colsButton, mode.levsButton]

    def timerFired(mode):
        if (mode.app.mainImage):
            mode.nextButton.color = 'white'
        else: mode.nextButton.color = 'gray'
    
    def keyPressed(mode, event):
        if (mode.app.rowsBar):
            if (event.key == 'Backspace'):
                mode.app.rowsInput = mode.app.rowsInput[:-1]
            elif (event.key == 'Enter'):
                if (mode.app.rowsInput.isdigit()):
                    mode.app.rowsBar = False
                else:
                    mode.app.showMessage('Please enter an integer')
            elif (len(event.key) == 1 and len(mode.app.rowsInput) < 5):
                mode.app.rowsInput += event.key
        elif (mode.app.colsBar):
            if (event.key == 'Backspace'):
                mode.app.colsInput = mode.app.colsInput[:-1]
            elif (event.key == 'Enter'):
                if (mode.app.colsInput.isdigit()):
                    mode.app.colsBar = False
                else:
                    mode.app.showMessage('Please enter an integer')
            elif (len(event.key) == 1 and len(mode.app.colsInput) < 5):
                mode.app.colsInput += event.key

    def drawInput(mode, canvas):
        font = 'Arial 20 bold'
        mode.counter += 1
        blinkTime = 15
        inputX = mode.rowColX + 5
        if (mode.app.rowsBar and mode.counter%blinkTime < blinkTime//2):
            canvas.create_text(inputX, mode.rowY+mode.rowColHeight//2, 
                text=(mode.app.rowsInput + '|'), anchor='w', fill='Black', font=font)
        canvas.create_text(inputX, mode.rowY+mode.rowColHeight//2, 
            text=mode.app.rowsInput, anchor='w', fill='Black', font=font)
        if (mode.app.colsBar and mode.counter%blinkTime < blinkTime//2):
            canvas.create_text(inputX, mode.colY+mode.rowColHeight//2, 
                text=(mode.app.colsInput + '|'), anchor='w', fill='Black', font=font)
        canvas.create_text(inputX, mode.colY+mode.rowColHeight//2, 
            text=mode.app.colsInput, anchor='w', fill='Black', font=font)

    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content == 'Import'):
                    # Citation: filedialog.askdirectory modified version from cmu_112_graphics.py:
                    # https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py 
                    mainImagePath = filedialog.askopenfilename(title='Select file: ', 
                        filetypes=(('Image files', '*.png *.gif *.jpg'), ('Video files', '*.mp4 *.mov *.avi *.wmv *.flv')))
                    if (mainImagePath):
                        mode.app.mainImage = Image.open(mainImagePath)
                elif (button.content == 'Next'):
                    if (mode.app.mainImage):
                        if ((not mode.app.rowsInput == '' and not mode.app.colsInput == '') and
                            (not mode.app.rowsInput.isdigit() or not mode.app.colsInput.isdigit())):
                            mode.app.showMessage('Please enter integers to Rows/Cols')
                        if (mode.app.rowsInput == '' and mode.app.colsInput == ''):
                            mode.nextButton.color = 'gray'
                        elif (mode.app.rowsInput.isdigit() and mode.app.colsInput.isdigit()):
                            mode.app.rowCol = (int(mode.app.rowsInput), int(mode.app.colsInput))
                        elif (mode.app.rowsInput.isdigit() and mode.app.colsInput == ''):
                            mode.app.rowCol = (int(mode.app.rowsInput), int(mode.app.rowsInput))
                        elif (mode.app.rowsInput == '' and mode.app.colsInput.isdigit()):
                            mode.app.rowCol = (int(mode.app.colsInput), int(mode.app.colsInput))
                        mode.app.setActiveMode(nextMode)
                    else:
                        mode.app.showMessage('Please select main image first')
                elif (button.title == 'rows'): 
                    mode.app.rowsBar = True
                elif (button.title == 'cols'):
                    mode.app.colsBar = True
                elif (button.title == 'lever'):
                    mode.app.currLevel = round((event.x-button.x1)/mode.segment) + 1
                elif (type(button.content) == type(mode.mainImages[0])):
                    mode.app.mainImage = button.content
    
    def drawLever(mode, canvas):
        cx = (mode.app.currLevel-1)*mode.segment + mode.levsX1
        cy = mode.levsButton.cy
        r = mode.levsButton.ry + 1
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='white')

    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        canvas.create_image(cx, cy, image=mode.app.background)
        canvas.create_text(cx, mode.height*0.1, font='Arial 20 bold', fill='white',
            text='Main Images')
        canvas.create_rectangle(mode.width*0.05, mode.height*0.65, mode.width*0.35,
            mode.height*0.95, fill='#404040')
        canvas.create_text(cx, mode.height*0.25, font='Arial 16 bold', fill='white',
            text='Choose Main Image from the Samples Below:')
        canvas.create_text(cx, mode.height*0.6, font='Arial 16 bold', fill='white',
            text='...Or Import from your Computer!')
        canvas.create_text(mode.width*0.07, mode.height*0.7, font='Arial 16 bold',
            fill='white', anchor='w', text='Optional Settings:')
        canvas.create_text(mode.width*0.07, mode.height*0.8, font='Arial 16 bold',
            fill='white', anchor='w', text='Rows:\n\nCols:')
        canvas.create_line(mode.width*0.07, mode.height*0.89, mode.width*0.33, mode.height*0.89,
            fill='white', width=3)
        canvas.create_text(mode.width*0.07, mode.height*0.92, font='Arial 12 bold',
            fill='white', anchor='w', text=f'Basic (1)\t              Detailed ({mode.leverLevels})')
        for button in mode.buttons:    
            if (button.title == 'lever'): mode.drawLever(canvas)
            else: mode.app.drawButton(mode, button, canvas)
        mode.drawInput(canvas)



class LoadingMode(Mode):
    def appStarted(mode):
        mode.counter = 1
        mode.background = mode.app.fullScreenColor(mode, (0, 0, 0))
        #mode.gifImages = mode.app.loadGifFromUrl('https://upload.wikimedia.org/wikipedia/commons/c/c7/Loading_2.gif')
        #mode.gifCounter = 0

    def timerFired(mode):
        mode.counter += 1
        #mode.gifCounter = (mode.gifCounter + 1) % len(mode.gifImages)
        if (mode.counter % 10 == 0):
            mode.app.mosaic = imageMosaicCreator(mode.app.mainImage, 
                mode.app.sampleImages, keywordDirectory=mode.app.input, rowCol=mode.app.rowCol, analysisLevel=mode.app.currLevel)
            mode.frameWidth, mode.frameHeight = mode.width-80, mode.height-80
            mode.app.mosaicForDisplay = mode.app.frameImage(mode.app.mosaic, (mode.frameWidth, mode.frameHeight))
            mode.app.setActiveMode(mode.app.SaveMode)

    def redrawAll(mode, canvas):
        cx, cy = mode.width//2, mode.height//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.background))
        canvas.create_text(cx, cy, text='Loading', font='Georgia 24', fill='white')



class SaveMode(Mode):
    def appStarted(mode):
        mode.buttonWidth = 120
        mode.buttonHeight = 40
        mode.createButtons()
    
    def modeDeactivated(mode):
        mode.app.sampleImages = None
        mode.app.mainImage = None 
        mode.app.mosaic = None

    def createButtons(mode):
        margin = 10
        saveButton = Button(mode.width*0.3-mode.buttonWidth//2, mode.height*0.9-mode.buttonHeight//2, 
            mode.width*0.3+mode.buttonWidth//2, mode.height*0.9+mode.buttonHeight//2, content='Save')
        homeButton = Button(mode.width*0.7-mode.buttonWidth//2, mode.height*0.9-mode.buttonHeight//2,
            mode.width*0.7+mode.buttonWidth//2, mode.height*0.9+mode.buttonHeight//2, content='Home',
            targetMode=mode.app.TitleMode)
        
        mode.buttons = [saveButton, homeButton]

    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content=='Save'):
                    savePath = filedialog.asksaveasfile(title='Save file: ', 
                        filetypes=(('jpg File', '*.jpg'), ('png File', '*.png')), 
                        defaultextension=('jpg File', '*.jpg'))
                    if (savePath): mode.app.mosaic.save(savePath)
                elif (button.content=='Home'):
                    mode.app.setActiveMode(nextMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width//2, mode.height//2, image=mode.app.background)
        # Mosaic already sized at appropriate size
        canvas.create_image(mode.width//2, (mode.height*0.9-mode.buttonHeight//2)//2, image=ImageTk.PhotoImage(mode.app.mosaicForDisplay))
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)

class Button(object):
    def __init__(self, x1, y1, x2, y2, content='', targetMode=True, buttonType='rectangle', 
            color='white', font='Arial 20 bold', fill='black', width=1, title=None):
        typeOptions = {'rectangle', 'ellipse', 'hexagon', 'rounded rectangle'}
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.content = content
        self.targetMode = targetMode
        self.type = buttonType
        self.color = color
        self.font = font
        self.fill = fill
        self.width = width
        self.title = title
        self.rx = (x2 - x1)//2
        self.ry = (y2 - y1)//2
        self.cx = x1 + self.rx
        self.cy = y1 + self.ry

    # Returns True if clicked and mode not specified. Else, None
    def isClicked(self, x, y):
        if (self.type=='rectangle'):
            if (self.x1 < x and x < self.x2 and self.y1 < y and y < self.y2):
                return self.targetMode
            else: return None
        elif (self.type == 'ellipse'): # only works for circles
            if (((self.cx-x)**2  + (self.cy-y)**2)**0.5 < self.rx):
                return self.targetMode
            else: return None

    def __repr__(self):
        return f'<Button object ({self.x1}, {self.y1}), ({self.x2}, {self.y2}), shape: {self.type}'

class PhotoMosaicApp(ModalApp):
    def appStarted(app):
        app.TitleMode = TitleMode()
        app.HelpMode = HelpMode()
        app.SelectionMode = SelectionMode()
        app.ImportSamplesMode = ImportSamplesMode()
        app.ImportMainMode = ImportMainMode()
        app.LoadingMode = LoadingMode()
        app.SaveMode = SaveMode()
        
        # Citation: B
        # ackground Image taken from below URL
        app.background = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        app.background = ImageTk.PhotoImage(convertUrlToImage(app.background))
        app.sampleImages = None
        app.mainImage = None 
        app.mosaic = None
        app.setActiveMode(app.TitleMode)

    ########################## Helper Functions ###########################
    @staticmethod
    def drawButton(app, button, canvas):    # button is of object Button
        if (button.type == 'ellipse'):
            canvas.create_oval(button.x1, button.y1, button.x2, 
                button.y2, fill=button.color, width=button.width)
            if (isinstance(button.content, str)):
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font, fill=button.fill)
        elif (button.type == 'rectangle'):
            if (isinstance(button.content, str)):
                canvas.create_rectangle(button.x1, button.y1, button.x2, 
                    button.y2, fill=button.color, width=button.width)
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font, fill=button.fill)
            else:
                try:
                    smallImage = PhotoMosaicApp.frameImage(button.content, (button.x2-button.x1, button.y2-button.y1))
                    canvas.create_image(button.cx, button.cy, image=ImageTk.PhotoImage(smallImage))
                except: pass

    # Takes in dictionary of buttons
    @staticmethod
    def createButtonsWithFixedY(app, buttonTexts, buttonDestinations, y, height=80, width=200, shape='rectangle', color='white'):
        cellWidth = app.width//(1 + len(buttonTexts))
        result = []
        for i in range(len(buttonTexts)):
            button = Button(cellWidth*(i+1)-(width//2), y-(height//2), cellWidth*(i+1)+(width//2), 
            y+(height//2), buttonTexts[i], buttonDestinations[i], shape, color)
            result.append(button)
        return result

    # The GIF in GIF List is an instance of Tkinter Image
    @staticmethod
    def loadGifFromUrl(GIFUrl):
        # Citation: GIF taken from wikiMedia Commons from below
        # https://upload.wikimedia.org/wikipedia/commons/c/c7/Loading_2.gif
        gif = convertUrlToImage(GIFUrl)
        gifImage = []
        i = 0
        while True:
            try:
                gif.seek(i)
                i += 1
                gifImage.append(ImageTk.PhotoImage(gif))
            except:
                break
        return gifImage

    # Creates solid color background that fills up the whole screen
    # Color can be imputted as tuple(R, G, B) or actual input of Image.new (need to specify mode)
    @staticmethod
    def fullScreenColor(app, color=0, mode='RGB'):
        if (isinstance(color, tuple) and mode=='RGB'):
            color = 'rgb' + str(color)
        image = Image.new(mode, (app.width, app.height), color)
        return image

    @staticmethod
    # Resizes object so that it fits in the frame
    # Input: image type: Image, frame: tuple(width, height) or any object with attribute width & height
    # Output: Image (that they took in, but resized. Nondestructive)
    def frameImage(image, frame):
        if (isinstance(frame, tuple)):
            frameWidth, frameHeight = frame
        else:
            frameWidth, frameHeight = frame.width, frame.height
        ratioWidth, ratioHeight = frameWidth/image.width, frameHeight/image.height
        baseRatio = min(ratioWidth, ratioHeight)
        targetWidth, targetHeight = int(image.width*baseRatio), int(image.height*baseRatio)
        return image.resize((targetWidth, targetHeight))
    #######################################################################

def run(width=800, height=600):
    app = PhotoMosaicApp(width=width, height=height)

if __name__ == "__main__":
    run()