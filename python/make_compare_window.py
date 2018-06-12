########################################################################################
# This majority of this code is taken directly from NanoGUI example1.cpp:              #
#                                                                                      #
#     https://github.com/wjakob/nanogui/blob/master/src/example1.cpp                   #
#                                                                                      #
# Copyright (c) 2017 Wenzel Jakob <wenzel.jakob@epfl.ch>, All rights reserved.         #
#                                                                                      #
# Redistribution and use in source and binary forms, with or without                   #
# modification, are permitted provided that the following conditions are met:          #
#                                                                                      #
# 1. Redistributions of source code must retain the above copyright notice, this       #
#    list of conditions and the following disclaimer.                                  #
#                                                                                      #
# 2. Redistributions in binary form must reproduce the above copyright notice,         #
#    this list of conditions and the following disclaimer in the documentation         #
#    and/or other materials provided with the distribution.                            #
#                                                                                      #
# 3. Neither the name of the copyright holder nor the names of its contributors        #
#    may be used to endorse or promote products derived from this software             #
#    without specific prior written permission.                                        #
#                                                                                      #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND      #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED        #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE               #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE         #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL           #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR           #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER           #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,        #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE        #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                 #
#                                                                                      #
# You are under no obligation whatsoever to provide any bug fixes, patches, or         #
# upgrades to the features, functionality or performance of the source code            #
# ("Enhancements") to anyone; however, if you choose to make your Enhancements         #
# available either publicly, or directly to the author of this software, without       #
# imposing a separate written license agreement for such Enhancements, then you        #
# hereby grant the following license: a non-exclusive, royalty-free perpetual          #
# license to install, use, modify, prepare derivative works, incorporate into          #
# other computer software, distribute, and sublicense such enhancements or             #
# derivative works thereof, in binary and source code form.                            #
########################################################################################
from custom_theme import ThemeChoice

import nanogui
from nanogui import entypo, fontawesome

import math


def makeCompareWindow(screen, title, themeChoice):
    window = nanogui.Window(screen, title)

    # By setting the theme now *BEFORE* any children are added, this means that
    # all new children created will inherit a reference to this custom theme.
    #
    # When you call setTheme after-the-fact, the same will occur -- calling
    # setTheme on a widget propagates that theme to all children.
    if isinstance(themeChoice, nanogui.Theme): # theme builder bypass
        window.setTheme(themeChoice)
    else:
        if themeChoice == ThemeChoice.Custom:
            window.setTheme(screen.customTheme)
        elif themeChoice == ThemeChoice.Fontawesome:
            window.setTheme(screen.fontawesomeTheme)


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
    if not isinstance(themeChoice, nanogui.Theme):
        nanogui.Label(window, "Image View (Mouse Over Image and Scroll Up)")
        # NOTE: screen.icons loaded in constructor!  On Linux the ordering is
        #       not alphanumeric (it seems to be by image size?), hence the loop
        imageView = None
        for identifier, basename in screen.icons:
            if "icon1" in basename:
                imageView = nanogui.ImageView(window, identifier)
                imageView.setGridThreshold(20)
                imageView.setPixelInfoThreshold(20)
                break

        if imageView is None:
            raise RuntimeError("Critical error: icon1 not found in CustomScreen.icons!")

        def img_view_cb(index):
            stringData = ""
            channelSum = 0.0
            pixel = screen.imageData[index[1], index[0]]
            for i in range(4):
                channelData = pixel[i]
                channelSum += float(channelData)
                stringData += "{0}\n".format(channelData)
            intensity = (255.0 - (channelSum / 4.0)) / 255.0

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
    if isinstance(themeChoice, nanogui.Theme): # theme builder bypass
        dialogTheme = themeChoice
    else:
        if themeChoice == ThemeChoice.Custom:
            dialogTheme = screen.customTheme
        elif themeChoice == ThemeChoice.Fontawesome:
            dialogTheme = screen.fontawesomeTheme

    def info_cb():
        dlg = nanogui.MessageDialog(
            screen,
            nanogui.MessageDialog.Type.Information,
            "Title",
            "This is an information message",
        )
        if dialogTheme:
            dlg.setTheme(dialogTheme)
        dlg.setCallback(message_cb)

    b = nanogui.Button(tools, "Info")
    b.setCallback(info_cb)

    def warn_cb():
        dlg = nanogui.MessageDialog(
            screen,
            nanogui.MessageDialog.Type.Warning,
            "Title",
            "This is a warning message"
        )
        if dialogTheme:
            dlg.setTheme(dialogTheme)
        dlg.setCallback(message_cb)

    b = nanogui.Button(tools, "Warn")
    b.setCallback(warn_cb)

    def ask_cb():
        dlg = nanogui.MessageDialog(
            screen,
            nanogui.MessageDialog.Type.Question,
            "Title",
            "This is a question message",
            "Yes",
            "No",
            True
        )
        if dialogTheme:
            dlg.setTheme(dialogTheme)
        dlg.setCallback(message_cb)

    b = nanogui.Button(tools, "Ask")
    b.setCallback(ask_cb)

    # TabWidget used to test TabHeader and others while keeping the size manageable
    nanogui.Label(window, "Tab Widget")
    tabWidget = nanogui.TabWidget(window)

    # test button and checkbox fonts
    layer = tabWidget.createTab("Button Like")
    layer.setLayout(nanogui.GroupLayout())

    # green color, produces white chevron at start
    cp = nanogui.ColorPicker(layer, nanogui.Color(0.28573, 0.56702, 0.25104, 1.0))
    if isinstance(themeChoice, nanogui.Theme) or themeChoice != ThemeChoice.Default:
        cp.setSide(nanogui.Popup.Side.Left)

    def cp_cb(col):
        print("Color: {0}, {1}, {2}, {3}".format(col.r, col.g, col.b, col.w))
    cp.setFinalCallback(cp_cb)

    # combobox
    cb = nanogui.ComboBox(
        layer, ["Combo box item 1", "Combo box item 2", "Combo box item 3"]
    )
    if isinstance(themeChoice, nanogui.Theme) or themeChoice != ThemeChoice.Default:
        cb.setSide(nanogui.Popup.Side.Left)

    icon = entypo.ICON_EXPORT
    if not isinstance(themeChoice, nanogui.Theme) and themeChoice == ThemeChoice.Fontawesome:
        icon = fontawesome.ICON_SOLID_SHARE_SQUARE
    # popup button
    popupBtn = nanogui.PopupButton(layer, "Popup", icon)
    popup = popupBtn.popup()
    # making sure the popup button for the custom theme stays in bounds
    if isinstance(themeChoice, nanogui.Theme) or themeChoice == ThemeChoice.Custom or themeChoice == ThemeChoice.Fontawesome:
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

    # regular buttons
    button = nanogui.Button(layer, "PushButton")

    # test that non-bold fonts for buttons work (applying to radio buttons)
    if isinstance(themeChoice, nanogui.Theme):
        radio_font = themeChoice.mDefaultFont
    else:
        # dynamic theme case, this will just be 'sans'
        radio_font = nanogui.Theme.GlobalDefaultFonts.Normal
    button = nanogui.Button(layer, "Radio1 (Hover for Tooltip)")
    button.setFont(radio_font)
    button.setFlags(nanogui.Button.Flags.RadioButton)
    button.setTooltip("Short tooltip!")

    button = nanogui.Button(layer, "Radio2 (Hover for Tooltip)")
    button.setFont(radio_font)
    button.setFlags(nanogui.Button.Flags.RadioButton)
    button.setTooltip(
        "This is a much longer tooltip that will get wrapped automatically!"
    )
    button = nanogui.Button(layer, "ToggleButton")
    button.setFlags(nanogui.Button.Flags.ToggleButton)

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
                counter = screen.manual_counter
            else:
                counter = screen.default_counter

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
                screen.manual_counter += 1
            else:
                screen.default_counter += 1
            # We must invoke perform layout from the screen instance to keep everything in order.
            # This is essential when creating tabs dynamically.
            screen.performLayout()
            # Ensure that the newly added header is visible on screen
            tabWidget.ensureTabVisible(index)

    tabWidget.setCallback(tab_cb)
    tabWidget.setActiveTab(0)

    return window
