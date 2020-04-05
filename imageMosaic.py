# Name: Anju Ito 
# Term Project 15-112: Photo Mosaic

from cmu_112_graphics import *
import requests, time

class MyApp(App):
    def appStarted(self):
        path = 'https://cdn.mos.cms.futurecdn.net/vChK6pTy3vN3KbYZ7UU7k3.jpg'
        # Graphics/open up 
