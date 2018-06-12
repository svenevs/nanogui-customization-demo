/***************************************************************************************
 * This file is licensed under CC0:                                                    *
 *                                                                                     *
 *      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE      *
 **************************************************************************************/
#pragma once

#include <nanogui/theme.h>
#include <nanogui/entypo.h>
#include <nanogui/resources.h>  // provides nanogui::createFontMem
#include <nanogui/fontawesome.h>// automatically copied for you by NanoGUI


#include <iostream>
#include <nanovg.h>

enum class ThemeChoice {
    Default = 0,///< The default NanoGUI Theme
    Custom,     ///< The 'CustomTheme' class
    Fontawesome ///< The 'FontawesomeTheme' class
};

/*
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
*/
/// Colors loosely inspired by Solarized Light: http://ethanschoonover.com/solarized
class CustomTheme : public nanogui::Theme {
public:
    CustomTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
        // override the default fonts
        mDefaultFont     = "spectral";
        mDefaultBoldFont = "spectral-bold";

        // two additional fonts loaded that are not defaults, but can be used
        // independently e.g. new Label(parent, "label", "spirax")
        mSpiraxFont = nanogui::createFontMem(ctx, "spirax", "Spirax-Regular.ttf");
        mMembraFont = nanogui::createFontMem(ctx, "membra", "membra.ttf");

        // -1 means font could not be loaded
        if (mSpiraxFont == -1 || mMembraFont == -1)
            throw std::runtime_error("Could not load the `spirax` or `membra` fonts!");

        // load the default fonts for this theme
        mSpectralFont     = nanogui::createFontMem(ctx, mDefaultFont.c_str(), "SpectralSC-Regular.ttf");
        mSpectralBoldFont = nanogui::createFontMem(ctx, mDefaultBoldFont.c_str(), "SpectralSC-Bold.ttf");

        if (mSpectralFont == -1 || mSpectralBoldFont == -1)
            throw std::runtime_error("Could not load the `spectral` fonts!");

        // overriding some default icons as demonstration
        // default: ``ENTYPO_ICON_CHECK``
        mCheckBoxIcon = ENTYPO_ICON_CROSS;
        mCheckBoxIconExtraScale = 1.3f;
        // default: ``ENTYPO_ICON_CHEVRON_RIGHT``
        mPopupChevronRightIcon = ENTYPO_ICON_TRIANGLE_RIGHT;
        // default: ``ENTYPO_ICON_CHEVRON_LEFT``
        mPopupChevronLeftIcon = ENTYPO_ICON_TRIANGLE_LEFT;
        mPopupIconExtraScale = 0.8f;
        // default: ``ENTYPO_ICON_ARROW_BOLD_LEFT``
        mTabHeaderLeftIcon = ENTYPO_ICON_ARROW_WITH_CIRCLE_LEFT;
        // default: ``ENTYPO_ICON_ARROW_BOLD_RIGHT``
        mTabHeaderRightIcon = ENTYPO_ICON_ARROW_WITH_CIRCLE_RIGHT;
        // default: ``ENTYPO_ICON_CHEVRON_UP``
        mTextBoxUpIcon = ENTYPO_ICON_TRIANGLE_UP;
        // default: ``ENTYPO_ICON_CHEVRON_DOWN``
        mTextBoxDownIcon = ENTYPO_ICON_TRIANGLE_DOWN;
        mTextBoxIconExtraScale = 0.6f;

        using nanogui::Color;
        mDropShadow                       = Color(0.0f, 0.16862745583057404f, 0.21176475286483765f, 1.0f);
        mTransparent                      = Color(0.0f, 0.0f, 0.0f, 0.0f);
        mBorderDark                       = Color(0.4627450406551361f, 0.5333333015441895f, 0.5568627119064331f, 0.9019607901573181f);
        mBorderLight                      = Color(0.6431373953819275f, 0.6901960968971252f, 0.7058823108673096f, 0.9019607901573181f);
        mBorderMedium                     = Color(0.564706027507782f, 0.6196078658103943f, 0.6392157077789307f, 0.9019607901573181f);
        mTextColor                        = Color(0.34117648005485535f, 0.42745086550712585f, 0.4509802758693695f, 1.0f);
        mDisabledTextColor                = Color(0.6078431010246277f, 0.658823549747467f, 0.6745098233222961f, 0.9019607901573181f);
        mTextColorShadow                  = Color(0.9333333373069763f, 0.9098039269447327f, 0.8352941870689392f, 0.9019607901573181f);
        mIconColor                        = Color(0.34117648005485535f, 0.42745086550712585f, 0.4509802758693695f, 1.0f);

        mButtonGradientTopFocused         = Color(0.7576307058334351f, 0.7828220129013062f, 0.789692223072052f, 1.0f);
        mButtonGradientBotFocused         = Color(0.6495736837387085f, 0.671172022819519f, 0.6770622730255127f, 1.0f);
        mButtonGradientTopUnfocused       = Color(0.7975060343742371f, 0.8240231871604919f, 0.8312549591064453f, 1.0f);
        mButtonGradientBotUnfocused       = Color(0.683761715888977f, 0.7064968347549438f, 0.7126971483230591f, 1.0f);
        mButtonGradientTopPushed          = Color(0.6495736241340637f, 0.671172022819519f, 0.6770622730255127f, 1.0f);
        mButtonGradientBotPushed          = Color(0.5569282174110413f, 0.5754461288452148f, 0.5804961919784546f, 1.0f);

        mTooltipBackgroundColor           = Color(0.027450978755950928f, 0.21176469326019287f, 0.2588234543800354f, 0.9019607901573181f);
        mTooltipTextColor                 = Color(0.7628562450408936f, 0.7953678369522095f, 0.7991926670074463f, 1.0f);

        /* Window-related */
        mWindowFillUnfocused              = Color(0.8862745761871338f, 0.8627451062202454f, 0.7921568155288696f, 0.9019607901573181f);
        mWindowFillFocused                = Color(0.9333333373069763f, 0.9098039269447327f, 0.8352941870689392f, 0.9019607901573181f);
        mWindowTitleUnfocused             = Color(0.654053807258606f, 0.6819284558296204f, 0.6852078437805176f, 1.0f);
        mWindowTitleFocused               = Color(0.7628562450408936f, 0.7953678369522095f, 0.7991926670074463f, 1.0f);

        mWindowHeaderGradientTop          = Color(0.16616077721118927f, 0.3241867423057556f, 0.3645337224006653f, 0.9019607901573181f);
        mWindowHeaderGradientBot          = Color(0.027450978755950928f, 0.21176469326019287f, 0.2588234543800354f, 0.9019607901573181f);
        mWindowHeaderSepTop               = Color(0.28508710861206055f, 0.4205746054649353f, 0.45516711473464966f, 0.9019607901573181f);
        mWindowHeaderSepBot               = Color(0.0f, 0.16862745583057404f, 0.21176475286483765f, 1.0f);

        mWindowPopup                      = Color(0.9333333373069763f, 0.9098039269447327f, 0.8352941870689392f, 0.9019607901573181f);
        mWindowPopupTransparent           = Color(0.19607843458652496f, 0.19607843458652496f, 0.19607843458652496f, 0.0f);
    }

    virtual ~CustomTheme() { /* does nothing */ }


protected:
    int mSpiraxFont = -1;
    int mMembraFont = -1;
    int mSpectralFont = -1;
    int mSpectralBoldFont = -1;
};


class FontawesomeTheme : public nanogui::Theme {
public:
    FontawesomeTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
        // override the default icon font
        mDefaultIconFont = "fontawesome";
        mFontAwesomeFont = nanogui::createFontMem(ctx, mDefaultIconFont.c_str(), "fontawesome.ttf");
        if (mFontAwesomeFont == -1)
            throw std::runtime_error("Could not load the fontawesome font!");

        /* The code-point for fontawesome and Entypo are different.  More specifically,
         * fontawesome does not have a set size for all icons, in addition to having a
         * slightly larger code-point.  NanoGUI's default here is 0.77, changing this
         * makes the fontawesome icons *on average* about the same size as Entypo.
         *
         * Run ./bin/example_custom_icon_font and change this value, paying attention to
         * the change in the PopupButton / ComboBox icons, as well as the TextBox spin
         * icons to see the difference.
         *
         * mIconScale is used in Widget::icon_scale() as a global size adjustment to the
         * icons.  See below for individual icon adjustments as well.
         *
         * NOTE: this does not affect labels when using e.g. nanogui::utf8(icon).data(),
         *       set the font size of the label for that.
         */
        mIconScale = 0.66f;

        // Since our default icon font is "fontawesome", we *must* override the
        // icon defaults for various widgets!
        mCheckBoxIcon             = FONTAWESOME_ICON_SOLID_CHECK;
        mCheckBoxIconExtraScale   = 1.0f;
        mMessageInformationIcon   = FONTAWESOME_ICON_SOLID_INFO_CIRCLE;
        mMessageQuestionIcon      = FONTAWESOME_ICON_SOLID_QUESTION_CIRCLE;
        mMessageWarningIcon       = FONTAWESOME_ICON_SOLID_EXCLAMATION_CIRCLE;
        mMessageAltButtonIcon     = FONTAWESOME_ICON_SOLID_TIMES_CIRCLE;
        mMessagePrimaryButtonIcon = FONTAWESOME_ICON_SOLID_CHECK_CIRCLE;
        mPopupChevronRightIcon    = FONTAWESOME_ICON_SOLID_CHEVRON_CIRCLE_RIGHT;
        mPopupChevronLeftIcon     = FONTAWESOME_ICON_SOLID_CHEVRON_CIRCLE_LEFT;
        mPopupIconExtraScale      = 0.7f;
        mTabHeaderLeftIcon        = FONTAWESOME_ICON_SOLID_ARROW_ALT_CIRCLE_LEFT;
        mTabHeaderRightIcon       = FONTAWESOME_ICON_SOLID_ARROW_ALT_CIRCLE_RIGHT;
        mTextBoxUpIcon            = FONTAWESOME_ICON_SOLID_CHEVRON_UP;
        mTextBoxDownIcon          = FONTAWESOME_ICON_SOLID_CHEVRON_DOWN;
        mTextBoxIconExtraScale    = 0.6f;
    }

    ~FontawesomeTheme() { }

protected:
    int mFontAwesomeFont = -1;
};
