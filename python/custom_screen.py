################################################################################
# This file is part of an example repository for NanoGUI.  Use of this source  #
# code is governed by a BSD-style license that can be found in the             #
# LICENSE file:                                                                #
#                                                                              #
# https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE    #
################################################################################

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
from nanogui import entypo, fontawesome
from custom_theme import CustomTheme, FontawesomeTheme, ThemeChoice

class CustomScreen(nanogui.Screen):
    def __init__(self, size):
        super(CustomScreen, self).__init__(size, "Customization Demo")
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
        self.imageData = np.array(image.getdata()).reshape(*image.size, 4)

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

    def makeCompareWindow(self, title, themeChoice):
        window = nanogui.Window(self, title)

        # By setting the theme now *BEFORE* any children are added, this means that
        # all new children created will inherit a reference to this custom theme.
        #
        # When you call setTheme after-the-fact, the same will occur -- calling
        # setTheme on a widget propagates that theme to all children.
        if themeChoice == ThemeChoice.Custom:
            window.setTheme(self.customTheme)
        elif themeChoice == ThemeChoice.Fontawesome:
            window.setTheme(self.fontawesomeTheme)

        # The remainder of the code here is largely irrelevant, the setTheme is the
        # important part.  Everything added below exists as a testing suite to make
        # sure that all widgets that draw fonts are obeying the new theme's default
        # font selections as defined by CustomTheme::defaultFont and
        # CustomTheme::defaultBoldFont overrides (see custom_theme.py).
        window.setLayout(nanogui.GroupLayout(15, 6, 6))

        # test text box fonts
        nanogui.Label(window, "Text Boxes")
        wrapper = nanogui.Widget(window)
        grid_layout = nanogui.GridLayout()
        grid_layout.setColAlignment([nanogui.Alignment.Maximum, nanogui.Alignment.Fill])
        wrapper.setLayout(grid_layout)
        nanogui.Label(wrapper, "TextBox : ")
        nanogui.TextBox(wrapper, "Some Text").setEditable(True)
        nanogui.Label(wrapper, "IntBox : ")
        nanogui.IntBox(wrapper).setSpinnable(True)
        nanogui.Label(wrapper, "FloatBox : ")
        nanogui.FloatBox(wrapper).setSpinnable(True)

        # test ImageView fonts (needs callback, scroll up on image to see)
        nanogui.Label(window, "Image View (Mouse Over Image and Scroll Up)")
        # NOTE: self.icons loaded in constructor!
        imageView = nanogui.ImageView(window, self.icons[0][0])
        imageView.setGridThreshold(20)
        imageView.setPixelInfoThreshold(20)

        def img_view_cb(index):
            stringData = ""
            channelSum = 0.0
            pixel = self.imageData[index[1], index[0]]
            for i in range(4):
                channelData = pixel[i]
                channelSum += float(channelData)
                stringData += "{0}\n".format(channelData)
            intensity = (255.0 - (channelSum / 4.0)) / 255.0
            # print(intensity, pixel)
            if intensity > 0.5:
                colorScale = (intensity + 1.0) / 2.0
            else:
                colorScale = intensity / 2.0
            textColor = nanogui.Color(colorScale, 1.0)
            return (stringData, textColor)

        imageView.setPixelInfoCallback(img_view_cb)

        # Message dialogs
        def message_cb(result):
            print("Dialog result: {0}".format(result))

        nanogui.Label(window, "Message Dialogues")
        tools = nanogui.Widget(window)
        tools.setLayout(nanogui.BoxLayout(nanogui.Orientation.Horizontal,
                                          nanogui.Alignment.Middle, 0, 6))

        dialogTheme = None
        if themeChoice == ThemeChoice.Custom:
            dialogTheme = self.customTheme
        elif themeChoice == ThemeChoice.Fontawesome:
            dialogTheme = self.fontawesomeTheme

        def info_cb():
            dlg = nanogui.MessageDialog(
                self,
                nanogui.MessageDialog.Type.Information,
                "Title",
                "This is an information message",
                theme=dialogTheme
            )
            dlg.setCallback(message_cb)

        b = nanogui.Button(tools, "Info")
        b.setCallback(info_cb)

        def warn_cb():
            dlg = nanogui.MessageDialog(
                self,
                nanogui.MessageDialog.Type.Warning,
                "Title",
                "This is a warning message",
                theme=dialogTheme
            )
            dlg.setCallback(message_cb)

        b = nanogui.Button(tools, "Warn")
        b.setCallback(warn_cb)

        def ask_cb():
            dlg = nanogui.MessageDialog(
                self,
                nanogui.MessageDialog.Type.Question,
                "Title",
                "This is a question message",
                "Yes",
                "No",
                True,
                dialogTheme
            )
            dlg.setCallback(message_cb)

        b = nanogui.Button(tools, "Ask")
        b.setCallback(ask_cb)

        # TabWidget used to test TabHeader and others while keeping the size manageable
        nanogui.Label(window, "Tab Widget")
        tabWidget = nanogui.TabWidget(window)

        # test button and checkbox fonts
        layer = tabWidget.createTab("Button Like")
        layer.setLayout(nanogui.GroupLayout())

        # regular buttons
        button = nanogui.Button(layer, "PushButton")
        button = nanogui.Button(layer, "RadioButton 1")
        button.setFlags(nanogui.Button.Flags.RadioButton)
        button = nanogui.Button(layer, "RadioButton 2")
        button.setFlags(nanogui.Button.Flags.RadioButton)
        button = nanogui.Button(layer, "ToggleButton")
        button.setFlags(nanogui.Button.Flags.ToggleButton)

        # combobox
        cb = nanogui.ComboBox(
            layer, ["Combo box item 1", "Combo box item 2", "Combo box item 3"]
        )
        if themeChoice != ThemeChoice.Default:
            cb.setSide(nanogui.Popup.Side.Left)

        icon = entypo.ICON_EXPORT
        if themeChoice == ThemeChoice.Fontawesome:
            icon = fontawesome.ICON_SOLID_SHARE_SQUARE
        # popup button
        popupBtn = nanogui.PopupButton(layer, "Popup", icon)
        popup = popupBtn.popup()
        # making sure the popup button for the custom theme stays in bounds
        if themeChoice == ThemeChoice.Custom or themeChoice == ThemeChoice.Fontawesome:
            popupBtn.setSide(nanogui.Popup.Side.Left)
        popup.setLayout(nanogui.GroupLayout())
        nanogui.Label(popup, "Arbitrary widgets can be placed here")
        nanogui.CheckBox(popup, "A check box")
        # popup right
        icon = entypo.ICON_FLASH
        if themeChoice == ThemeChoice.Fontawesome:
            icon = fontawesome.ICON_SOLID_BOLT
        popupBtn = nanogui.PopupButton(popup, "Recursive popup", icon)
        popupRight = popupBtn.popup()
        popupRight.setLayout(nanogui.GroupLayout())
        nanogui.CheckBox(popupRight, "Another check box")
        # popup left
        popupBtn = nanogui.PopupButton(popup, "Recursive popup", icon)
        popupBtn.setSide(nanogui.Popup.Side.Left)
        popupLeft = popupBtn.popup()
        popupLeft.setLayout(nanogui.GroupLayout())
        nanogui.CheckBox(popupLeft, "Another check box")

        # checkbox (top level)
        nanogui.CheckBox(layer, "A CheckBox")

        # test the graph widget fonts
        layer = tabWidget.createTab("Graph")
        layer.setLayout(nanogui.GroupLayout())

        # Same as nanogui python/example1.py
        nanogui.Label(layer, "Function Graph Widget")
        graph = nanogui.Graph(layer, "Some Function")

        graph.setHeader("E = 2.35e-3")
        graph.setFooter("Iteration 89")
        values = [0.5 * (0.5 * math.sin(i / 10.0) +
                         0.5 * math.cos(i / 23.0) + 1)
                  for i in range(100)]
        graph.setValues(values)

        # Dummy tab used to represent the last tab button.
        tabWidget.createTab("+")

        def tab_cb(index):
            if index == (tabWidget.tabCount()-1):
                if themeChoice != ThemeChoice.Default:
                    counter = self.manual_counter
                else:
                    counter = self.default_counter
                # When the "+" tab has been clicked, simply add a new tab.
                tabName  = "Dynamic {0}".format(counter)
                layerDyn = tabWidget.createTab(index, tabName)
                layerDyn.setLayout(nanogui.GroupLayout())
                nanogui.Label(layerDyn, "Function graph widget", "spectral-bold")
                graphDyn = nanogui.Graph(layerDyn, "Dynamic function")

                graphDyn.setHeader("E = 2.35e-3")
                graphDyn.setFooter("Iteration {0}".format(index*counter))
                valuesDyn = [0.5 * abs((0.5 * math.sin(i / 10.0 + counter)) +
                                       (0.5 * math.cos(i / 23.0 + 1 + counter)))
                             for i in range(100)]
                graphDyn.setValues(valuesDyn)
                if themeChoice != ThemeChoice.Default:
                    self.manual_counter += 1
                else:
                    self.default_counter += 1
                # We must invoke perform layout from the screen instance to keep everything in order.
                # This is essential when creating tabs dynamically.
                self.performLayout()
                # Ensure that the newly added header is visible on screen
                tabWidget.ensureTabVisible(index)

        tabWidget.setCallback(tab_cb)
        tabWidget.setActiveTab(0)

        return window
