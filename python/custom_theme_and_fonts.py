########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

import gc
import nanogui

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from custom_screen import CustomScreen
from custom_theme import ThemeChoice
from make_compare_window import makeCompareWindow


if __name__ == "__main__":
    nanogui.init()
    screen = CustomScreen((800, 900))

    # manual demonstration
    window = nanogui.Window(screen, "Manual Labels")
    window.setLayout(nanogui.GroupLayout())

    def add_pangram(font, fontSize):
        pangram = "The quick brown fox jumps over the lazy dog."
        l = nanogui.Label(window, pangram, font, fontSize)
        l.setFixedWidth(110)

    add_pangram("spirax", 33)
    add_pangram("membra", 23)

    # make one with the default theme
    window = makeCompareWindow(screen, "Default Theme", ThemeChoice.Default)
    window.setPosition((150, 0))

    # make one with the custom theme
    window = makeCompareWindow(screen, "Custom Theme", ThemeChoice.Custom)
    window.setPosition((475, 0))

    screen.performLayout()
    screen.drawAll()
    screen.setVisible(True)
    nanogui.mainloop()
    del screen
    gc.collect()
    nanogui.shutdown()
