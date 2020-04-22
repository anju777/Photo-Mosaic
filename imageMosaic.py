# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

from cmu_112_graphics import *
from imageScraper import keywordImageRetriever, convertUrlToImage, retrieveImagesFromFile
from imageMosaicOperator import imageMosaicCreator

# Sample Main Images from: 
# https://wallpaperhd.wiki/wp-content/uploads/desktop-high-res-hd-wallpapers-hd-high-resolution-wallpaper-for-desktop
#   -wallpaper-hd-widescreen-high-quality-desktop-nature-12-wallpapers-hd-widescreen-high-quality-desktop-uyewRm.jpg
# https://i.pinimg.com/originals/99/28/73/9928737a3504c5fc8269377d8ba5a122.jpg 
# https://1.bp.blogspot.com/-lMg-uRzjXXQ/VWUVykvi6jI/AAAAAAAAAUA/SyND9ucVWU8/s1600/High%2BResolution%2BSpace%2BWallpaper.jpg
'''ToDo:
- Design Title Image Text
- Create background image (idea: photo mosaic)
- Figure out title text alignment (multi-line center option for help, etc.)
- Different modes and versions with similarities -> OOP (subclass)
'''

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
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.app.background))
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
Here you can create photo mosaics based on keyword input or by importing your own images and videos.
The basic features and their descriptions are listed below. Enjoy!

- Keyword Feature: Takes in keyword and imports images from the Internet to use.
- Import: Can import folder from your computer with all your favorite photos!
              * The imported photo can have multiple files inside, and skips non-image files!
\n\n\n\n\n
\t\t\t***Press any key to return***
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
        titley = mode.height*1/3
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.app.background))
        canvas.create_text(cx, titley, text=mode.titleText, font=font, fill='Navy')
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)

class ImportSamplesMode(Mode):
    def appStarted(mode):
        mode.input = ''
        mode.createButtons()
        mode.keywordBar = False
        mode.sampleImages = None
        mode.counter = 1

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

    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content == ''):
                    mode.keywordBar = True
                elif (button.content == 'Import'):
                    mode.app.sampleImagesFile = filedialog.askdirectory(title='Select file: ')
                    mode.app.sampleImages = retrieveImagesFromFile(mode.app.sampleImagesFile)
                elif (button.content == 'Next'):
                    if (mode.app.sampleImages):
                        mode.app.setActiveMode(nextMode)
                    else:
                        mode.app.showMessage('Please import sample images first')

    def keyPressed(mode, event):
        if (mode.keywordBar):
            if (event.key == 'Space'):
                mode.input += ' '
            elif (event.key == 'Backspace'):
                mode.input = mode.input[:-1]
            elif (event.key == 'Enter'):
                mode.app.sampleImages = keywordImageRetriever(mode.input)
            elif (len(event.key) == 1):
                mode.input += event.key

    def drawInput(mode, canvas):
        font = 'Arial 20 bold'
        mode.counter += 1
        blinkTime = 20
        inputX = mode.keywordMargin + 10
        if (mode.keywordBar and mode.counter%blinkTime < blinkTime//2):
            canvas.create_text(inputX, mode.keywordY, text=(mode.input + '|'), 
                anchor='w', fill='Black', font=font)
        canvas.create_text(inputX, mode.keywordY, text=mode.input, anchor='w', fill='Black', font=font)

    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        font='Arial 20 bold'
        fontColor = 'white'
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.app.background))
        canvas.create_text(cx, mode.height*0.1, text='Sample Images', fill=fontColor, font=font)
        canvas.create_text(cx, mode.height*0.3, text='Import with Keyword!\n(Press Enter to Search)', fill=fontColor, font=font)
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)
        mode.drawInput(canvas)
        canvas.create_text(cx, mode.height*0.6, text='Or Import from Computer!', fill=fontColor, font=font)

class ImportVideoSamplesMode(ImportSamplesMode):
    pass

class ImportMainMode(Mode):
    def appStarted(mode):
        path = 'C:\\Users\\anjua\\OneDrive\\Desktop\\Photo-Mosaic\\MainImages'
        mode.mainImages = retrieveImagesFromFile(path)
        mode.resizeMainImages() #destructive function
        mode.createButtons()
    
    def resizeMainImages(mode):
        for i in range(len(mode.mainImages)):
            mode.mainImages[i] = mode.app.frameImage(mode.mainImages[i], 
                (mode.width*0.2, mode.height*0.2))

    def createButtons(mode):
        importWidth = 150
        importHeight = 40
        importY = mode.height*0.7
        importButton = Button((mode.width//2)-(importWidth//2), importY-(importHeight//2),
            (mode.width//2)+(importWidth//2), importY+(importHeight//2), 'Import')

        nextWidth = 120
        mode.nextButton = Button(mode.width*0.7, mode.height*0.8, mode.width*0.7+nextWidth,
            mode.height*0.8+40, 'Next', mode.app.ImportMainMode, color='gray')
        
        mode.buttons = [importButton, mode.nextButton]

    def timerFired(mode):
        if (mode.app.mainImage):
            mode.nextButton.color = 'white'
    
    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content == 'Import'):
                    # Citation: filedialog.askdirectory modified version from cmu_112_graphics.py:
                    # https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py 
                    mode.app.mainImage = filedialog.askopenfile(title='Select file: ', 
                        filetypes=(('Image files', '*.png *.gif *.jpg'), ('Video files', '*.mp4 *.mov *.avi *.wmv *.flv')))
                elif (button.content == 'Next'):
                    if (mode.app.mainImage):
                        mode.app.setActiveMode(nextMode)
                    else:
                        mode.app.showMessage('Please select main image first')

    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        imageY = mode.height*0.4
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.app.background))
        canvas.create_text(cx, mode.height*0.2, font='Arial 12 bold', fill='white',
            text='Choose main image from below or import from your computer')
        canvas.create_image(mode.width//4, imageY, image=ImageTk.PhotoImage(mode.mainImages[0]))
        canvas.create_image(mode.width//2, imageY, image=ImageTk.PhotoImage(mode.mainImages[1]))
        canvas.create_image(mode.width*3//4, imageY, image=ImageTk.PhotoImage(mode.mainImages[2]))
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)
        
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
            mode.app.setActiveMode(mode.app.SaveMode)

    def redrawAll(mode, canvas):
        cx, cy = mode.width//2, mode.height//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.background))
        canvas.create_text(cx, cy, text='Loading', font='Georgia 24', fill='white')

class DisplayMode(Mode):
    def appStarted(mode):
        mode.app.mosaic = imageMosaicCreator(mode.mainImage, mode.app.sampleImages)
    
    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.app.mosaic))

class SaveMode(Mode):
    def appStarted(mode):
        margin = 20
        mode.frameWidth, mode.frameHeight = mode.width-mode.buttonWidth-(2*margin), mode.height-(2*margin)
        mode.mosaicForDisplay = mode.app.frameImage(mode.app.mosaic, (frameWidth, frameHeight))
        mode.createButtons()
    
    def createButtons(mode):
        mode.buttonWidth = 120
        mode.buttonHeight = 40
        margin = 10
        saveButton = Button(mode.width-margin-mode.buttonWidth, mode.height*0.7-mode.buttonHeight//2, 
            mode.width-margin, mode.height*0.7+mode.buttonheight//2, content='Save')
        homeButton = Butotn(mode.width-margin-mode.buttonWidth, mode.height*0.3-mode.buttonHeight//2,
            mode.width-margin, mode.height*0.7+mode.buttonHeight//2, content='Back to Home',
            targetMode=mode.app.TitleMode)
        
        mode.buttons = [saveButton, homeButton]

    def mouseClicked(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (content=='Save'):
                    filedialog.asksaveasfilename(mode.app.mosaic)
                else:
                    mode.app.setActiveMode(nextMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width//2, mode.height//2, image=ImageTk.PhotoImage(mode.app.background))
        # Mosaic already sized at appropriate size
        canvas.create_image((mode.frameWidth-80)//2, mode.height//2, image=ImageTk.PhotoImage(mode.mosaicForDisplay))
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)

class Button(object):
    def __init__(self, x1, y1, x2, y2, content='', targetMode=True, buttonType='rectangle', 
            color='white', font='Arial 20 bold', fill='black'):
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
        '''
        elif (self.type == 'hexagon'):
            if (not inRect(x, y, self.x1+self.cy, self.y1, self.x2-self.cy, self.y2)):
                return False
            if (self.x1 < x and x < (self.x1 + self.cy) and self. y < )
        '''

    def __repr__(self):
        return f'<Button object ({self.x1}, {self.y1}), ({self.x2}, {self.y2}), shape: {self.type}'

class PhotoMosaicApp(ModalApp):
    def appStarted(app):
        app.TitleMode = TitleMode()
        app.HelpMode = HelpMode()
        app.SelectionMode = SelectionMode()
        app.ImportSamplesMode = ImportSamplesMode()
        app.ImportVideoSamplesMode = ImportVideoSamplesMode()
        app.ImportMainMode = ImportMainMode()
        app.LoadingMode = LoadingMode()
        app.DisplayMode = DisplayMode()
        app.SaveMode = SaveMode()
        
        app.background = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        app.background = convertUrlToImage(app.background)
        app.sampleImages = None
        app.mainImage = None 
        app.mosaic = None
        app.setActiveMode(app.TitleMode)

    ########################## Helper Functions ###########################
    @staticmethod
    def drawButton(app, button, canvas):    # button is of object Button
        if (button.type == 'ellipse'):
            canvas.create_oval(button.x1, button.y1, button.x2, 
                button.y2, fill=button.color)
            if (isinstance(button.content, str)):
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font, fill=button.fill)
            '''Add Image option too'''
        elif (button.type == 'rectangle'):
            canvas.create_rectangle(button.x1, button.y1, button.x2, 
                button.y2, fill=button.color)
            if (isinstance(button.content, str)):
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font, fill=button.fill)

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
    ''' Don't really use right now
    @staticmethod
    def createButtonsWithFixedX(app, buttonTexts, buttonDestinations, x, yStart, yEnd, height=80, width=100, shape='rectangle', color='white'):
        cellHeight = ((yEnd-yStart)//(1 + len(buttonTexts)))
        result = []
        for i in range(len(buttonTexts)):
            button = Button(x-(width//2), yStart+cellHeight*(i+1)-(height//2), x+(width//2),
                yStart+cellHeight*(i+1)+(height//2), buttonTexts[i], buttonDestinations[i], shape, color)
            result.append(button)
        return result
    '''

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