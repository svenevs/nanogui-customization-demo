########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

# For the pixel info callback, we need to have the host image loaded
try:
    from PIL import Image
except:
    import sys
    if sys.version[0] == "3":
        pip = "pip3"
    else:
        pip = "pip"
    sys.stderr.write("Please install Pillow: `sudo -H {pip} install Pillow`\n".format(pip=pip))
    sys.exit(1)

import math
import numpy as np

import nanogui
from custom_theme import CustomTheme, FontawesomeTheme, ThemeChoice

class CustomScreen(nanogui.Screen):
    def __init__(self, size, title="NanoGUI Customization Demo"):
        super(CustomScreen, self).__init__(size, title)
        self.customTheme = CustomTheme(self.nvgContext())
        self.fontawesomeTheme = FontawesomeTheme(self.nvgContext())

        # Doing GLTexture in Python is not convenient, instead (as done in Example1)
        # just load all of the images
        try:
            self.icons = nanogui.loadImageDirectory(self.nvgContext(), "../icons")
        except:
            raise RuntimeError("Could not load the image icons!")

        # load the PNG for host data for setting up the pixel info callback
        image = Image.open("../icons/icon1.png")
        # reshape: take a (width*height)x4 rgba image and reshape to be
        # (width,height,4).  image.size returns a tuple, in this case (255,255),
        # so we're reshaping 65535x4 to be (256,256,4)
        self.imageData = np.array(image.getdata()).reshape(image.size[0], image.size[1], 4)

        # Simple counters, used for dynamic tab creation with TabWidget callback
        self.default_counter = 1 # for the default theme widget
        self.manual_counter  = 1 # for the manual theme widget

    def keyboardEvent(self, key, scancode, action, modifiers):
        ''' Allow <ESCAPE> to exit the application. '''
        if super(CustomScreen, self).keyboardEvent(key, scancode, action, modifiers):
            return True

        if key == nanogui.glfw.KEY_ESCAPE and action == nanogui.glfw.PRESS:
            self.setVisible(False)
            return True

        return False
