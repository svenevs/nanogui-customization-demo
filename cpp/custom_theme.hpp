/*******************************************************************************
 * This file is part of an example repository for NanoGUI.  Use of this source *
 * code is governed by a BSD-style license that can be found in the            *
 * LICENSE file:                                                               *
 *                                                                             *
 * https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE   *
 ******************************************************************************/
#pragma once

#include <nanogui/theme.h>
#include <nanogui/entypo.h>
#include <nanogui/resources.h>  // provides nanogui::createFontMem
#include <nanogui/fontawesome.h>// automatically copied for you by NanoGUI

enum class ThemeChoice {
    Default = 0,///< The default NanoGUI Theme
    Custom,     ///< The 'CustomTheme' class
    Fontawesome ///< The 'FontawesomeTheme' class
};

class CustomTheme : public nanogui::Theme {
public:
    /// The ``"spectral"`` font.  Overriding this method is what informs NanoGUI to use it.
    virtual std::string defaultFont() const override { return "spectral"; }

    /// The ``"spectral-bold"`` font.  Overriding this method is what informs NanoGUI to use it.
    virtual std::string defaultBoldFont() const override { return "spectral-bold"; }

    CustomTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
        // two additional fonts loaded that are not defaults, but can be used
        // independently e.g. new Label(parent, "label", "spirax")
        mSpiraxFont = nanogui::createFontMem(ctx, "spirax", "Spirax-Regular.ttf");
        mMembraFont = nanogui::createFontMem(ctx, "membra", "membra.ttf");

        if (mSpiraxFont == -1 || mMembraFont == -1)
            throw std::runtime_error("Could not load the `spirax` or `membra` fonts!");

        // load the default fonts for this theme
        mSpectralFont     = nanogui::createFontMem(ctx, "spectral", "SpectralSC-Regular.ttf");
        mSpectralBoldFont = nanogui::createFontMem(ctx, "spectral-bold", "SpectralSC-Bold.ttf");

        if (mSpectralFont == -1 || mSpectralBoldFont == -1)
            throw std::runtime_error("Could not load the `spectral` fonts!");

        /* a not-well-thought-out quasi-light scheme.  This was mostly just inverting
         * colors set in nanogui/theme.cpp.  note that for things like
         * `mWindowHeaderGradientTop`, since we are in the derived class if you change
         * `mButtonGradientTopUnfocused`, and still want the window and button to have
         * the same colors, you need to *RESET* it.  there's no requirement to do so
         * of course!
         */
        using nanogui::Color;
        mDropShadow                 = Color(100, 128);
        mTransparent                = Color(100, 0);
        mBorderDark                 = Color(111, 255);
        mBorderLight                = Color(202, 255);
        mBorderMedium               = Color(185, 255);
        mTextColor                  = Color(33, 230);
        mDisabledTextColor          = Color(83, 230);
        mTextColorShadow            = Color(53, 0);
        mIconColor                  = mTextColor;

        mButtonGradientTopFocused   = Color(192, 255);
        mButtonGradientBotFocused   = Color(172, 255);
        mButtonGradientTopUnfocused = Color(202, 255);
        mButtonGradientBotUnfocused = Color(182, 255);
        mButtonGradientTopPushed    = Color(161, 255);
        // also affects inactive TabWidget icon, looks best when same as mBorderDark
        mButtonGradientBotPushed    = Color(111, 255);

        /* Window-related */
        mWindowFillUnfocused        = Color(150, 230);
        mWindowFillFocused          = Color(155, 230);
        mWindowTitleUnfocused       = Color(83, 230);
        mWindowTitleFocused         = Color(33, 230);

        mWindowHeaderGradientTop    = mButtonGradientTopUnfocused;
        mWindowHeaderGradientBot    = mButtonGradientBotUnfocused;
        mWindowHeaderSepTop         = mBorderLight;
        mWindowHeaderSepBot         = mBorderDark;

        mWindowPopup                = Color(150, 255);
        mWindowPopupTransparent     = Color(150, 0);

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
    }

    ~CustomTheme() { }

protected:
    int mSpiraxFont = -1;
    int mMembraFont = -1;
    int mSpectralFont = -1;
    int mSpectralBoldFont = -1;
};

class FontawesomeTheme : public nanogui::Theme {
public:
    /// The ``"fontawesome"`` icon font.  Overriding this method is what informs NanoGUI to use it.
    virtual std::string defaultIconFont() const override { return "fontawesome"; }

    FontawesomeTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
        mFontAwesomeFont = nanogui::createFontMem(ctx, "fontawesome", "fontawesome.ttf");
        if (mFontAwesomeFont == -1)
            throw std::runtime_error("Could not load the fontawesome font!");

        // Since our default icon font is "fontawesome", we *must* override the
        // icon defaults for various widgets!
        mCheckBoxIcon             = FONTAWESOME_ICON_SOLID_CHECK;
        mCheckBoxIconExtraScale   = 0.7f;
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
