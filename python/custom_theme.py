import nanogui
from nanogui import entypo, fontawesome

# A quasi-enum (not using real enum to support python 2.x)
class ThemeChoice:
    Default     = 0 # The default NanoGUI Theme
    Custom      = 1 # The 'CustomTheme' class
    Fontawesome = 2 # The 'FontawesomeTheme' class

class CustomTheme(nanogui.Theme):

    # The ``"spectral"`` font.  Overriding this method is what informs NanoGUI to use it.
    def defaultFont(self):
        return "spectral"

    # The ``"spectral-bold"`` font.  Overriding this method is what informs NanoGUI to use it.
    def defaultBoldFont(self):
        return "spectral-bold"

    def __init__(self, ctx):
        super(CustomTheme, self).__init__(ctx)
        # two additional fonts loaded that are not defaults, but can be used
        # independently e.g. new Label(parent, "label", "spirax")
        self.mSpiraxFont = nanogui.createFontMem(ctx, "spirax", "Spirax-Regular.ttf")
        self.mMembraFont = nanogui.createFontMem(ctx, "membra", "membra.ttf")

        if self.mSpiraxFont == -1 or self.mMembraFont == -1:
            raise RuntimeError("Could not load the `spirax` or `membra` fonts!")

        # load the default fonts for this theme
        self.mSpectralFont     = nanogui.createFontMem(ctx, "spectral", "SpectralSC-Regular.ttf")
        self.mSpectralBoldFont = nanogui.createFontMem(ctx, "spectral-bold", "SpectralSC-Bold.ttf")

        if self.mSpectralFont == -1 or self.mSpectralBoldFont == -1:
            raise RuntimeError("Could not load the `spectral` fonts!")

        # a not-well-thought-out quasi-light scheme.  This was mostly just inverting
        # colors set in nanogui/theme.cpp.  note that for things like
        # `mWindowHeaderGradientTop`, since we are in the derived class if you change
        # `mButtonGradientTopUnfocused`, and still want the window and button to have
        # the same colors, you need to *RESET* it.  there's no requirement to do so
        # of course!
        self.mDropShadow                 = nanogui.Color(100, 128)
        self.mTransparent                = nanogui.Color(100, 0)
        self.mBorderDark                 = nanogui.Color(111, 255)
        self.mBorderLight                = nanogui.Color(202, 255)
        self.mBorderMedium               = nanogui.Color(185, 255)
        self.mTextColor                  = nanogui.Color(33, 230)
        self.mDisabledTextColor          = nanogui.Color(83, 230)
        self.mTextColorShadow            = nanogui.Color(53, 0)
        self.mIconColor                  = self.mTextColor

        self.mButtonGradientTopFocused   = nanogui.Color(192, 255)
        self.mButtonGradientBotFocused   = nanogui.Color(172, 255)
        self.mButtonGradientTopUnfocused = nanogui.Color(202, 255)
        self.mButtonGradientBotUnfocused = nanogui.Color(182, 255)
        self.mButtonGradientTopPushed    = nanogui.Color(161, 255)
        # also affects inactive TabWidget icon, looks best when same as mBorderDark
        self.mButtonGradientBotPushed    = nanogui.Color(111, 255)

        # Window-related
        self.mWindowFillUnfocused        = nanogui.Color(150, 230)
        self.mWindowFillFocused          = nanogui.Color(155, 230)
        self.mWindowTitleUnfocused       = nanogui.Color(83, 230)
        self.mWindowTitleFocused         = nanogui.Color(33, 230)

        self.mWindowHeaderGradientTop    = self.mButtonGradientTopUnfocused
        self.mWindowHeaderGradientBot    = self.mButtonGradientBotUnfocused
        self.mWindowHeaderSepTop         = self.mBorderLight
        self.mWindowHeaderSepBot         = self.mBorderDark

        self.mWindowPopup                = nanogui.Color(150, 255)
        self.mWindowPopupTransparent     = nanogui.Color(150, 0)

        # overriding some default icons as demonstration
        # default: ``entypo.ICON_CHECK``
        self.mCheckBoxIcon = entypo.ICON_CROSS
        self.mCheckBoxIconExtraScale = 1.3
        # default: ``entypo.ICON_CHEVRON_RIGHT``
        self.mPopupChevronRightIcon = entypo.ICON_TRIANGLE_RIGHT
        # default: ``entypo.ICON_CHEVRON_LEFT``
        self.mPopupChevronLeftIcon = entypo.ICON_TRIANGLE_LEFT
        self.mPopupIconExtraScale = 0.8
        # default: ``entypo.ICON_ARROW_BOLD_LEFT``
        self.mTabHeaderLeftIcon = entypo.ICON_ARROW_WITH_CIRCLE_LEFT
        # default: ``entypo.ICON_ARROW_BOLD_RIGHT``
        self.mTabHeaderRightIcon = entypo.ICON_ARROW_WITH_CIRCLE_RIGHT
        # default: ``entypo.ICON_CHEVRON_UP``
        self.mTextBoxUpIcon = entypo.ICON_TRIANGLE_UP
        # default: ``entypo.ICON_CHEVRON_DOWN``
        self.mTextBoxDownIcon = entypo.ICON_TRIANGLE_DOWN
        self.mTextBoxIconExtraScale = 0.6


class FontawesomeTheme(nanogui.Theme):
    def defaultIconFont(self):
        return "fontawesome"

    def __init__(self, ctx):
        super(FontawesomeTheme, self).__init__(ctx)
        self.mFontAwesomeFont = nanogui.createFontMem(ctx, "fontawesome", "fontawesome.ttf")
        if self.mFontAwesomeFont == -1:
            raise RuntimeError("Could not load the fontawesome font!")

        # Since our dfault icon font is "fontawesome", we *must* override the
        # icon defaults for various widgets!
        self.mCheckBoxIcon             = fontawesome.ICON_SOLID_CHECK
        self.mCheckBoxIconExtraScale   = 0.7
        self.mMessageInformationIcon   = fontawesome.ICON_SOLID_INFO_CIRCLE
        self.mMessageQuestionIcon      = fontawesome.ICON_SOLID_QUESTION_CIRCLE
        self.mMessageWarningIcon       = fontawesome.ICON_SOLID_EXCLAMATION_CIRCLE
        self.mMessageAltButtonIcon     = fontawesome.ICON_SOLID_TIMES_CIRCLE
        self.mMessagePrimaryButtonIcon = fontawesome.ICON_SOLID_CHECK_CIRCLE
        self.mPopupChevronRightIcon    = fontawesome.ICON_SOLID_CHEVRON_CIRCLE_RIGHT
        self.mPopupChevronLeftIcon     = fontawesome.ICON_SOLID_CHEVRON_CIRCLE_LEFT
        self.mPopupIconExtraScale      = 0.7
        self.mTabHeaderLeftIcon        = fontawesome.ICON_SOLID_ARROW_ALT_CIRCLE_LEFT
        self.mTabHeaderRightIcon       = fontawesome.ICON_SOLID_ARROW_ALT_CIRCLE_RIGHT
        self.mTextBoxUpIcon            = fontawesome.ICON_SOLID_CHEVRON_UP
        self.mTextBoxDownIcon          = fontawesome.ICON_SOLID_CHEVRON_DOWN
        self.mTextBoxIconExtraScale    = 0.6
