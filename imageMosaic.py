# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

from cmu_112_graphics import *
from imageScraper import keywordImageRetriever, convertUrlToImage

'''ToDo:
- Design Title Image Text
- Create background image (idea: 112-related background: logo/Prof. Kosbie)
- Figure out title text alignment (multi-line center option for help, etc.)
- Different modes and versions with similarities -> OOP (subclass)
'''

class TitleMode(Mode):
    def appStarted(mode):
        mode.titleText = 'PHOTO MOSAIC\nCREATOR'
        mode.optionsText = ['Create', 'Help']
        mode.optionsDestination = [mode.app.SelectionMode, mode.app.HelpMode]
        backgroundImageUrl = 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/03/22/16/istock-644053990.jpg?w968h681'
        mode.backgroundImage = convertUrlToImage(backgroundImageUrl)
        mode.buttonHeight = mode.height * 4/5
        mode.buttons = mode.app.createButtonsWithFixedY(mode, mode.optionsText, 
            mode.optionsDestination, mode.buttonHeight, 20, 100, 'rectangle', 'white')

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
        mode.space = mode.width * 1/5
        mode.margin = 30
        mode.text = '''Welcomee to the Photo Mosaic Creator!
Here, you can create photo mosaics based on keyword input or by importing your own images and videos.
The basic features and their descriptions are listed below. Enjoy!

- Keyword Feature: Takes in keyword and imports images from the Internet to use.
- Import: Can import files from your computer to create your customized photo mosaics!
'''

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.previousMode)

    def redrawAll(mode, canvas):
        mode.app.previousMode
        canvas.create_rectangle(mode.space, 0, mode.width-mode.space, 
            mode.height, fill=mode.borderColor)
        canvas.create_rectangle(mode.space+mode.margin, mode.margin, 
            mode.width-mode.space-mode.margin, mode.height-mode.margin, 
            fill=mode.backgroundColor)

class SelectionMode(Mode):
    pass

'''
class ImportSamplesMode(mode):

class ImportMainMode(mode):

class LoadingMode(mode):

class DisplayMode(mode):
'''


class Button(object):
    def __init__(self, x1, y1, x2, y2, content, targetMode, buttonType='rectangle', 
            color='white', font='Arial 20 bold'):
        typeOptions = {'rectangle', 'ellipse', 'hexagon', 'circle', 'rounded rectangle'}
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.content = content
        self.targetMode = targetMode
        self.type = buttonType
        self.color = color
        self.font = font
        self.rx = (x2 - x1)//2
        self.ry = (y2 - y1)//2
        self.cx = x1 + self.rx
        self.cy = y1 + self.ry

    def isClicked(self, x, y):
        if (self.type=='rectangle'):
            if (self.x1 < x and x < self.x2 and self.y1 < y and y < self.y2):
                return self.targetMode
            else: return None
        elif (self.type == 'ellipse'):
            if ((x**2//self.rx**2 + y**2//self.ry**2) < 1):
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
        app.setActiveMode(app.TitleMode)

    @staticmethod
    def drawButton(app, button, canvas):    # button is of object Button
        if (button.type == 'ellipse'):
            canvas.create_ellipse(button.x1, button.y1, button.x2, 
                button.y2, fill=button.color)
            if (isinstance(button.content, str)):
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font)
            '''Add Image option too'''
        elif (button.type == 'rectangle'):
            canvas.create_rectangle(button.x1, button.y1, button.x2, 
                button.y2, fill=button.color)
            if (isinstance(button.content, str)):
                canvas.create_text(button.cx, button.cy, text=button.content,
                    font=button.font)

    # Takes in dictionary of buttons
    @staticmethod
    def createButtonsWithFixedY(app, buttonTexts, buttonDestinations, y, height=40, width=100, shape='rectangle', color='white'):
        cellWidth = app.width//(1 + len(buttonTexts))
        result = []
        for i in range(len(buttonTexts)):
            button = Button(cellWidth*(i+1)-width, y-height, cellWidth*(i+1)+width, y+height,
                    buttonTexts[i], buttonDestinations[i], shape, color)
            result.append(button)
        return result

def run(width=800, height=600):
    app = PhotoMosaicApp(width=width, height=height)

if __name__ == "__main__":
    run()
