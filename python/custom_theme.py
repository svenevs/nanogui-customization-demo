########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

import nanogui
from nanogui import entypo, fontawesome

# A quasi-enum (not using real enum to support python 2.x)
class ThemeChoice:
    Default     = 0 # The default NanoGUI Theme
    Custom      = 1 # The 'CustomTheme' class
    Fontawesome = 2 # The 'FontawesomeTheme' class

class CustomTheme(nanogui.Theme):
    '''
    Colors loosely inspired by Solarized Light: http://ethanschoonover.com/solarized

    The JSON for this class::

        {
          "mStandardFontSize":                  16.0,
          "mButtonFontSize":                    20.0,
          "mTextBoxFontSize":                   20.0,
          "mWindowFontSize":                    18.0,
          "mIconScale":                         0.7699999809265137,

          "mWindowCornerRadius":                2,
          "mWindowHeaderHeight":                30,
          "mWindowDropShadowSize":              10,
          "mButtonCornerRadius":                2,
          "mTabBorderWidth":                    0.75,
          "mTabInnerMargin":                    5,
          "mTabMinButtonWidth":                 20,
          "mTabMaxButtonWidth":                 160,
          "mTabControlWidth":                   20,
          "mTabButtonHorizontalPadding":        10,
          "mTabButtonVerticalPadding":          2,

          "mDropShadow":                        [0.0, 0.16862745583057404, 0.21176475286483765, 1.0],
          "mTransparent":                       [0.0, 0.0, 0.0, 0.0],
          "mBorderDark":                        [0.4627450406551361, 0.5333333015441895, 0.5568627119064331, 0.9019607901573181],
          "mBorderLight":                       [0.6431373953819275, 0.6901960968971252, 0.7058823108673096, 0.9019607901573181],
          "mBorderMedium":                      [0.564706027507782, 0.6196078658103943, 0.6392157077789307, 0.9019607901573181],
          "mTextColor":                         [0.34117648005485535, 0.42745086550712585, 0.4509802758693695, 1.0],
          "mDisabledTextColor":                 [0.6078431010246277, 0.658823549747467, 0.6745098233222961, 0.9019607901573181],
          "mTextColorShadow":                   [0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181],
          "mIconColor":                         [0.34117648005485535, 0.42745086550712585, 0.4509802758693695, 1.0],

          "mButtonGradientTopFocused":          [0.7576307058334351, 0.7828220129013062, 0.789692223072052, 1.0],
          "mButtonGradientBotFocused":          [0.6495736837387085, 0.671172022819519, 0.6770622730255127, 1.0],
          "mButtonGradientTopUnfocused":        [0.7975060343742371, 0.8240231871604919, 0.8312549591064453, 1.0],
          "mButtonGradientBotUnfocused":        [0.683761715888977, 0.7064968347549438, 0.7126971483230591, 1.0],
          "mButtonGradientTopPushed":           [0.6495736241340637, 0.671172022819519, 0.6770622730255127, 1.0],
          "mButtonGradientBotPushed":           [0.5569282174110413, 0.5754461288452148, 0.5804961919784546, 1.0],

          "mTooltipBackgroundColor":            [0.027450978755950928, 0.21176469326019287, 0.2588234543800354, 0.9019607901573181],
          "mTooltipTextColor":                  [0.7628562450408936, 0.7953678369522095, 0.7991926670074463, 1.0],

          "mWindowFillUnfocused":               [0.8862745761871338, 0.8627451062202454, 0.7921568155288696, 0.9019607901573181],
          "mWindowFillFocused":                 [0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181],
          "mWindowTitleUnfocused":              [0.654053807258606, 0.6819284558296204, 0.6852078437805176, 1.0],
          "mWindowTitleFocused":                [0.7628562450408936, 0.7953678369522095, 0.7991926670074463, 1.0],

          "mWindowHeaderGradientTop":           [0.16616077721118927, 0.3241867423057556, 0.3645337224006653, 0.9019607901573181],
          "mWindowHeaderGradientBot":           [0.027450978755950928, 0.21176469326019287, 0.2588234543800354, 0.9019607901573181],
          "mWindowHeaderSepTop":                [0.28508710861206055, 0.4205746054649353, 0.45516711473464966, 0.9019607901573181],
          "mWindowHeaderSepBot":                [0.0, 0.16862745583057404, 0.21176475286483765, 1.0],

          "mWindowPopup":                       [0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181],
          "mWindowPopupTransparent":            [0.19607843458652496, 0.19607843458652496, 0.19607843458652496, 0.0]
        }
    '''
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

        self.mStandardFontSize                 = 16.0
        self.mButtonFontSize                   = 20.0
        self.mTextBoxFontSize                  = 20.0
        self.mWindowFontSize                   = 18.0
        self.mIconScale                        = 0.7699999809265137

        self.mWindowCornerRadius               = 2
        self.mWindowHeaderHeight               = 30
        self.mWindowDropShadowSize             = 10
        self.mButtonCornerRadius               = 2
        self.mTabBorderWidth                   = 0.75
        self.mTabInnerMargin                   = 5
        self.mTabMinButtonWidth                = 20
        self.mTabMaxButtonWidth                = 160
        self.mTabControlWidth                  = 20
        self.mTabButtonHorizontalPadding       = 10
        self.mTabButtonVerticalPadding         = 2

        self.mDropShadow                       = nanogui.Color(0.0, 0.16862745583057404, 0.21176475286483765, 1.0)
        self.mTransparent                      = nanogui.Color(0.0, 0.0, 0.0, 0.0)
        self.mBorderDark                       = nanogui.Color(0.4627450406551361, 0.5333333015441895, 0.5568627119064331, 0.9019607901573181)
        self.mBorderLight                      = nanogui.Color(0.6431373953819275, 0.6901960968971252, 0.7058823108673096, 0.9019607901573181)
        self.mBorderMedium                     = nanogui.Color(0.564706027507782, 0.6196078658103943, 0.6392157077789307, 0.9019607901573181)
        self.mTextColor                        = nanogui.Color(0.34117648005485535, 0.42745086550712585, 0.4509802758693695, 1.0)
        self.mDisabledTextColor                = nanogui.Color(0.6078431010246277, 0.658823549747467, 0.6745098233222961, 0.9019607901573181)
        self.mTextColorShadow                  = nanogui.Color(0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181)
        self.mIconColor                        = nanogui.Color(0.34117648005485535, 0.42745086550712585, 0.4509802758693695, 1.0)

        self.mButtonGradientTopFocused         = nanogui.Color(0.7576307058334351, 0.7828220129013062, 0.789692223072052, 1.0)
        self.mButtonGradientBotFocused         = nanogui.Color(0.6495736837387085, 0.671172022819519, 0.6770622730255127, 1.0)
        self.mButtonGradientTopUnfocused       = nanogui.Color(0.7975060343742371, 0.8240231871604919, 0.8312549591064453, 1.0)
        self.mButtonGradientBotUnfocused       = nanogui.Color(0.683761715888977, 0.7064968347549438, 0.7126971483230591, 1.0)
        self.mButtonGradientTopPushed          = nanogui.Color(0.6495736241340637, 0.671172022819519, 0.6770622730255127, 1.0)
        self.mButtonGradientBotPushed          = nanogui.Color(0.5569282174110413, 0.5754461288452148, 0.5804961919784546, 1.0)

        self.mTooltipBackgroundColor           = nanogui.Color(0.027450978755950928, 0.21176469326019287, 0.2588234543800354, 0.9019607901573181)
        self.mTooltipTextColor                 = nanogui.Color(0.7628562450408936, 0.7953678369522095, 0.7991926670074463, 1.0)

        # Window-related
        self.mWindowFillUnfocused              = nanogui.Color(0.8862745761871338, 0.8627451062202454, 0.7921568155288696, 0.9019607901573181)
        self.mWindowFillFocused                = nanogui.Color(0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181)
        self.mWindowTitleUnfocused             = nanogui.Color(0.654053807258606, 0.6819284558296204, 0.6852078437805176, 1.0)
        self.mWindowTitleFocused               = nanogui.Color(0.7628562450408936, 0.7953678369522095, 0.7991926670074463, 1.0)

        self.mWindowHeaderGradientTop          = nanogui.Color(0.16616077721118927, 0.3241867423057556, 0.3645337224006653, 0.9019607901573181)
        self.mWindowHeaderGradientBot          = nanogui.Color(0.027450978755950928, 0.21176469326019287, 0.2588234543800354, 0.9019607901573181)
        self.mWindowHeaderSepTop               = nanogui.Color(0.28508710861206055, 0.4205746054649353, 0.45516711473464966, 0.9019607901573181)
        self.mWindowHeaderSepBot               = nanogui.Color(0.0, 0.16862745583057404, 0.21176475286483765, 1.0)

        self.mWindowPopup                      = nanogui.Color(0.9333333373069763, 0.9098039269447327, 0.8352941870689392, 0.9019607901573181)
        self.mWindowPopupTransparent           = nanogui.Color(0.19607843458652496, 0.19607843458652496, 0.19607843458652496, 0.0)
# End CustomTheme #############################################################


class FontawesomeTheme(nanogui.Theme):
    def defaultIconFont(self):
        return "fontawesome"

    def __init__(self, ctx):
        super(FontawesomeTheme, self).__init__(ctx)
        self.mFontAwesomeFont = nanogui.createFontMem(ctx, "fontawesome", "fontawesome.ttf")
        if self.mFontAwesomeFont == -1:
            raise RuntimeError("Could not load the fontawesome font!")

        # The code-point for fontawesome and Entypo are different.  More specifically,
        # fontawesome does not have a set size for all icons, in addition to having a
        # slightly larger code-point.  NanoGUI's default here is 0.77, changing this
        # makes the fontawesome icons *on average* about the same size as Entypo.
        #
        # Run example_custom_icon_font.py and change this value, paying attention to
        # the change in the PopupButton / ComboBox icons, as well as the TextBox spin
        # icons to see the difference.
        #
        # mIconScale is used in Widget::icon_scale() as a global size adjustment to the
        # icons.  See below for individual icon adjustments as well.
        #
        # NOTE: this does not affect labels when using e.g. nanogui::utf8(icon).data(),
        #       set the font size of the label for that.
        self.mIconScale = 0.66

        # Since our dfault icon font is "fontawesome", we *must* override the
        # icon defaults for various widgets!
        self.mCheckBoxIcon             = fontawesome.ICON_SOLID_CHECK
        self.mCheckBoxIconExtraScale   = 1.0
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
