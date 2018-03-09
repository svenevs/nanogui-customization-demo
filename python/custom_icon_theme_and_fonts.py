########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

import gc
import nanogui
from nanogui import entypo, fontawesome

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
    window.setLayout(nanogui.GridLayout())
    nanogui.Label(window, "Entypo+")
    nanogui.Label(window, "Awesome")

    # just some similar icons to compare with
    icons = [
        (        entypo.ICON_INFO_WITH_CIRCLE,    fontawesome.ICON_SOLID_INFO_CIRCLE),
        (                    entypo.ICON_HOME,           fontawesome.ICON_SOLID_HOME),
        (              entypo.ICON_LIGHT_BULB,            fontawesome.ICON_LIGHTBULB),
        (                    entypo.ICON_LINK,           fontawesome.ICON_SOLID_LINK),
        (                     entypo.ICON_EYE,            fontawesome.ICON_SOLID_EYE),
        (           entypo.ICON_EYE_WITH_LINE,      fontawesome.ICON_SOLID_EYE_SLASH),
        (                 entypo.ICON_COMPASS,              fontawesome.ICON_COMPASS),
        (entypo.ICON_CONTROLLER_FAST_BACKWARD,  fontawesome.ICON_SOLID_FAST_BACKWARD),
        ( entypo.ICON_CONTROLLER_FAST_FORWARD,   fontawesome.ICON_SOLID_FAST_FORWARD),
        (entypo.ICON_CONTROLLER_JUMP_TO_START,  fontawesome.ICON_SOLID_STEP_BACKWARD),
        (         entypo.ICON_CONTROLLER_NEXT,   fontawesome.ICON_SOLID_STEP_FORWARD),
        (         entypo.ICON_CONTROLLER_PAUS,          fontawesome.ICON_SOLID_PAUSE),
        (         entypo.ICON_CONTROLLER_PLAY,           fontawesome.ICON_SOLID_PLAY),
        (       entypo.ICON_CONTROLLER_RECORD,         fontawesome.ICON_SOLID_CIRCLE),
        (         entypo.ICON_CONTROLLER_STOP,           fontawesome.ICON_SOLID_STOP),
        (                    entypo.ICON_CROP,           fontawesome.ICON_SOLID_CROP),
        (                entypo.ICON_DOWNLOAD,       fontawesome.ICON_SOLID_DOWNLOAD),
        (               entypo.ICON_CLIPBOARD,      fontawesome.ICON_SOLID_CLIPBOARD),
        (                   entypo.ICON_CLOCK,                fontawesome.ICON_CLOCK),
        (               entypo.ICON_THUMBS_UP,      fontawesome.ICON_SOLID_THUMBS_UP),
        (             entypo.ICON_THUMBS_DOWN,    fontawesome.ICON_SOLID_THUMBS_DOWN),
        (             entypo.ICON_PAPER_PLANE,    fontawesome.ICON_SOLID_PAPER_PLANE),
        (                  entypo.ICON_ROCKET,         fontawesome.ICON_SOLID_ROCKET),
        (                     entypo.ICON_KEY,            fontawesome.ICON_SOLID_KEY),
        (                   entypo.ICON_GAUGE, fontawesome.ICON_SOLID_TACHOMETER_ALT)
    ]
    for entypo_icon, fontawesome_icon in icons:
        # add some vertical spacing (two widgets per row)
        nanogui.Label(window, " ")
        nanogui.Label(window, " ")
        # add the entypo icon
        nanogui.Label(window, nanogui.utf8(entypo_icon), "icons")
        # add the fontawesome icon
        nanogui.Label(window, nanogui.utf8(fontawesome_icon), "fontawesome")

    # add some vertical spacing (two widgets per row)
    nanogui.Label(window, " ")
    nanogui.Label(window, " ")
    window.setFixedWidth(125)

    # make one with the default theme
    window = makeCompareWindow(screen, "Default Theme", ThemeChoice.Default)
    window.setPosition((150, 0))

    # make one with the custom theme
    window = makeCompareWindow(screen, "Fontawesome Icon Theme", ThemeChoice.Fontawesome)
    window.setPosition((475, 0))

    screen.performLayout()
    screen.drawAll()
    screen.setVisible(True)
    nanogui.mainloop()
    del screen
    gc.collect()
    nanogui.shutdown()
