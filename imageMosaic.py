# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

from cmu_112_graphics import *
from imageScraper import keywordImageRetriever, convertUrlToImage
from imageMosaicOperator import imageMosaicCreator

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
        backgroundImageUrl = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        mode.backgroundImage = convertUrlToImage(backgroundImageUrl)
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
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.backgroundImage))
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
- Import: Can import files from your computer to create your customized photo mosaics!
\n\n\n\n\n
\t\t\t\tPress any key to go back.
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
        backgroundImageUrl = 'https://previews.123rf.com/images/mycteria/mycteria1512/mycteria151200044/49529679-abstract-frozen-background-of-ice.jpg'
        mode.backgroundImage = convertUrlToImage(backgroundImageUrl)
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
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.backgroundImage))
        canvas.create_text(cx, titley, text=mode.titleText, font=font, fill='Navy')
        for button in mode.buttons:
            mode.app.drawButton(mode, button, canvas)

class ImportSamplesMode(Mode):
    def appStarted(mode):
        mode.input = ''
        mode.createButtons()
        backgroundImageUrl = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        mode.backgroundImage = convertUrlToImage(backgroundImageUrl)
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
        nextButton = Button(mode.width*0.7, mode.height*0.8, mode.width*0.7+nextWidth,
            mode.height*0.8+40, 'Next', mode.app.ImportMainMode)
        mode.buttons = [keywordButton, importButton, nextButton]

    def mousePressed(mode, event):
        for button in mode.buttons:
            nextMode = button.isClicked(event.x, event.y)
            if (nextMode):
                if (button.content == ''):
                    mode.keywordBar = True
                elif (button.content == 'Import'):
                    mode.app.getUserInput('Choose Sample Image File')
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
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.backgroundImage))
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
        mode.mainImage = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        mode.mainImage = convertUrlToImage(mode.mainImage)
        mode.mosaic = imageMosaicCreator(mode.mainImage, mode.app.sampleImages)
    
    def redrawAll(mode, canvas):
        cx = mode.width//2
        cy = mode.height//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.mosaic))
        
'''
class LoadingMode(Mode):

class DisplayMode(Mode):
'''


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
        app.sampleImages = None
        app.setActiveMode(app.TitleMode)

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
def run(width=800, height=600):
    app = PhotoMosaicApp(width=width, height=height)

if __name__ == "__main__":
    run()
