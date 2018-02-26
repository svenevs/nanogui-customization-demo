################################################################################
# This file is part of an example repository for NanoGUI.  Use of this source  #
# code is governed by a BSD-style license that can be found in the             #
# LICENSE file:                                                                #
#                                                                              #
# https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE    #
################################################################################

import gc
import nanogui

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from custom_screen import CustomScreen
from custom_theme import ThemeChoice


if __name__ == "__main__":
    nanogui.init()
    screen = CustomScreen((800, 900))

    # manual demonstration
    window = nanogui.Window(screen, "Manual Labels")
    window.setLayout(nanogui.GroupLayout())
    pangram = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog."]
    # add the spirax font
    for text in pangram:
        nanogui.Label(window, text, "spirax").setFontSize(30)
    # add the membra font
    for text in pangram:
        nanogui.Label(window, text, "membra").setFontSize(24)

    # make one with the default theme
    window = screen.makeCompareWindow("Default Theme", ThemeChoice.Default)
    window.setPosition((150, 0))

    # make one with the custom theme
    window = screen.makeCompareWindow("Custom Theme", ThemeChoice.Custom)
    window.setPosition((475, 0))

    screen.performLayout()
    screen.drawAll()
    screen.setVisible(True)
    nanogui.mainloop()
    del screen
    gc.collect()
    nanogui.shutdown()
