# -*- coding: utf-8 -*-

import xbmcgui
import xbmc
import xbmcaddon
import json
from PIL import Image

__addon__           = xbmcaddon.Addon()
__addon_id__        = __addon__.getAddonInfo('id')
__addonname__       = __addon__.getAddonInfo('name')
__icon__            = __addon__.getAddonInfo('icon')
__addonpath__       = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__lang__            = __addon__.getLocalizedString
__path_img__        = __addonpath__ + "/images"

class ShowImage:
    def __init__(self):
        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        if window.getProperty('ShowImage') != 'true':
            display = windowImage()
            display .doModal()
            del display
            window.setProperty('ShowImage', 'false')
        else:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Input.ExecuteAction", "params":["back"]},"id":1}')

class windowImage(xbmcgui.WindowDialog):
    def __init__(self):
    
        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        window.setProperty('ShowImage', 'true')
        
        # check arg getting from settings
        try:
            idImage = str(sys.argv[1])
        except:
            idImage = '0'

        imagePath = __addon__.getSetting('image'+idImage)
        
        # set max height and margin to background
        xImageRes = 660
        yImageRes = 400
        yMax = 660
        margin = 10
        
        if idImage == '0':
            msg = __lang__(32100)    
        elif imagePath == '':
            msg = __lang__(32101)
        else:
            try:
                image = Image.open(imagePath)
                msg = ''
            except:
                msg = __lang__(32102)
            else:
                imageSize = image.size
                xImageRes = imageSize[0]
                yImageRes = imageSize[1]
        
        # scale if image is too big
        if yImageRes > yMax:
            scale = (xImageRes) / float(yImageRes)
            
            xImageRes = int(scale * yMax)
            yImageRes = yMax

        # set size
        xImagePos = ((1280 - xImageRes) / 2)
        yImagePos = ((720 - yImageRes) / 2) - margin
        xBgRes = xImageRes + (margin * 2)
        yBgRes = yImageRes + (margin * 4)
        xBgPos = xImagePos - margin
        yBgPos = yImagePos - margin
        
        # create window
        self.bg = xbmcgui.ControlImage(xBgPos,yBgPos,xBgRes,yBgRes, __path_img__ + '//bg.png')
        self.addControl(self.bg)
        if msg == '':
            self.image = xbmcgui.ControlImage(xImagePos,yImagePos,xImageRes,yImageRes, imagePath)
            self.addControl(self.image)
        else:
            self.label = xbmcgui.ControlLabel(xImagePos,yImagePos,xImageRes,yImageRes, msg, 'font13', alignment=6)
            self.addControl(self.label)

    def onAction(self, action):
        self.close()
        
    def onControl(self, control):
        self.close()

ShowImage()

