########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

# Developer note: need to make a change to this file?
# Please raise an Issue on GitHub describing what needs to change.  This file
# was generated, so the scripts that generated it need to update as well.

import gc

import nanogui
from nanogui import Screen, Window, Widget, GridLayout, VScrollPanel, Button, TextBox, BoxLayout, Orientation, Theme
from nanogui import fontawesome


class FontawesomeTheme(nanogui.Theme):
    def __init__(self, ctx):
        super(FontawesomeTheme, self).__init__(ctx)
        # override default icon font globally
        self.mDefaultIconFont = "fontawesome";
        # load the fontawesome font into memory
        self.mFontawesomeFont = nanogui.createFontMem(ctx, "fontawesome", "fontawesome.ttf")
        if self.mFontawesomeFont == -1:
            raise RuntimeError("Could not load the fontawesome font!")

        # TODO: you need to override the following default icon choices in your
        #       own application!  See documentation for nanogui::Theme.
        # self.mCheckBoxIcon             = entypo.ICON_CHECK
        # self.mCheckBoxIconExtraScale   = self.defaultCheckBoxIconExtraScale()
        # self.mMessageInformationIcon   = entypo.ICON_INFO_WITH_CIRCLE
        # self.mMessageQuestionIcon      = entypo.ICON_HELP_WITH_CIRCLE
        # self.mMessageWarningIcon       = entypo.ICON_WARNING
        # self.mMessageAltButtonIcon     = entypo.ICON_CIRCLE_WITH_CROSS
        # self.mMessagePrimaryButtonIcon = entypo.ICON_CHECK
        # self.mPopupChevronRightIcon    = entypo.ICON_CHEVRON_RIGHT
        # self.mPopupChevronLeftIcon     = entypo.ICON_CHEVRON_LEFT
        # self.mPopupIconExtraScale      = self.defaultPopupIconExtraScale()
        # self.mTabHeaderLeftIcon        = entypo.ICON_ARROW_BOLD_LEFT
        # self.mTabHeaderRightIcon       = entypo.ICON_ARROW_BOLD_RIGHT
        # self.mTextBoxUpIcon            = entypo.ICON_CHEVRON_UP
        # self.mTextBoxDownIcon          = entypo.ICON_CHEVRON_DOWN
        # self.mTextBoxIconExtraScale    = self.defaultTextBoxIconExtraScale()


class EscapeScreen(nanogui.Screen):
    def __init__(self, size, title, resizable):
        super(EscapeScreen, self).__init__(size, title, resizable)

    # allow <ESCAPE> to exit
    def keyboardEvent(self, key, scancode, action, modifiers):
        if key == nanogui.glfw.KEY_ESCAPE and modifiers == 0:
            self.setVisible(False)
            return True

        return super(EscapeScreen, self).keyboardEvent(key, scancode, action, modifiers)


class IconBox(nanogui.Widget):
    def __init__(self, parent, name, icon, width):
        super(IconBox, self).__init__(parent)

        self.setLayout(nanogui.BoxLayout(nanogui.Orientation.Horizontal))

        b = nanogui.Button(self, "", icon)
        b.setFixedWidth(40)

        text = nanogui.TextBox(self, name)
        text.setDefaultValue(name)
        text.setEditable(True)
        # Return false essentially makes it not possible to actually edit this text
        # box, but keeping it editable=true allows selection for copy-paste.  If the
        # text box is not editable, then the user cannot highlight it.
        text.setCallback(lambda x: False)
        text.setFont("mono-bold")
        text.setFixedWidth(width - 40)


if __name__ == "__main__":
    nanogui.init()

    width      = 1000
    half_width = width // 2
    height     = 800

    # create a fixed size screen with one window
    screen = EscapeScreen((width, height), "NanoGUI Fontawesome Icons", False)

    # NOTE: if doing a custom screen derived class, for some reason if you
    #       load a custom theme object and call setTheme in the constructor
    #       of the derived theme class it will not work.  You can load the
    #       theme in the constructor, but just make sure to call setTheme
    #       after the constructor is finished (as we are doing here)
    #
    #       Setting the theme of the screen means that all children created
    #       after this point will use this as their theme (rather than the
    #       default NanoGUI theme).
    theme = FontawesomeTheme(screen.nvgContext())
    screen.setTheme(theme)
    window = Window(screen, "")
    window.setPosition((0, 0))
    window.setFixedSize((width, height))

    # attach a vertical scroll panel
    vscroll = VScrollPanel(window)
    vscroll.setFixedSize((width, height))

    # vscroll should only have *ONE* child. this is what `wrapper` is for
    wrapper = Widget(vscroll)
    wrapper.setFixedSize((width, height))
    wrapper.setLayout(GridLayout())  # defaults: 2 columns

    # NOTE: don't __dict__ crawl in real code!
    # this is just because it's more convenient to do this for enumerating all
    # of the icons -- see cpp example for alternative...
    for key in fontawesome.__dict__.keys():
        if key.startswith("ICON_"):
            IconBox(wrapper, key, fontawesome.__dict__[key], half_width)

    screen.performLayout()
    screen.drawAll()
    screen.setVisible(True)

    nanogui.mainloop()

    del screen
    gc.collect()

    nanogui.shutdown()
