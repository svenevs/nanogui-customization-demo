#pragma once

#include <nanogui/theme.h>
#include <nanogui_resources.h> // provides nanogui::createFontMem
#include <iostream>

class MyTheme : public nanogui::Theme {
public:
    MyTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
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

        // a not-well-thought-out quasi-light scheme.  this was mostly just inverting
        // colors set in nanogui/theme.cpp.  note that for things like
        // `mWindowHeaderGradientTop`, since we are in the derived class if you change
        // `mButtonGradientTopUnfocused`, and still want the window and button to have
        // the same colors, you need to *RESET* it.  there's no requirement to do so
        // of course!
        using nanogui::Color;
        mDropShadow                       = Color(100, 128);
        mTransparent                      = Color(100, 0);
        mBorderDark                       = Color(129, 255);
        mBorderLight                      = Color(192, 255);
        mBorderMedium                     = Color(135, 255);
        mTextColor                        = Color(43, 230);
        mDisabledTextColor                = Color(83, 230);
        mTextColorShadow                  = Color(60, 0);
        mIconColor                        = mTextColor;

        mButtonGradientTopFocused         = Color(148, 255);
        mButtonGradientBotFocused         = Color(164, 255);
        mButtonGradientTopUnfocused       = Color(158, 255);
        mButtonGradientBotUnfocused       = Color(174, 255);
        mButtonGradientTopPushed          = Color(129, 255);
        mButtonGradientBotPushed          = Color(141, 255);

        /* Window-related */
        mWindowFillUnfocused              = Color(143, 230);
        mWindowFillFocused                = Color(145, 230);
        mWindowTitleUnfocused             = Color(83, 230);
        mWindowTitleFocused               = Color(43, 230);

        mWindowHeaderGradientTop          = mButtonGradientTopUnfocused;
        mWindowHeaderGradientBot          = mButtonGradientBotUnfocused;
        mWindowHeaderSepTop               = mBorderLight;
        mWindowHeaderSepBot               = mBorderDark;

        mWindowPopup                      = Color(150, 255);
        mWindowPopupTransparent           = Color(150, 0);
    }

    /// The ``"sans"`` font.  Override in sub-classes to use a different font-face as the default.  Propagates to children.
    virtual std::string defaultFont() const { return "spectral"; }
    /// The ``"sans-bold"`` font.  Override in sub-classes to use a different font-face for \ref nanogui::Window.
    virtual std::string defaultBoldFont() const { return "spectral-bold"; }

    ~MyTheme() { }

    int mSpiraxFont = -1;
    int mMembraFont = -1;
    int mSpectralFont = -1;
    int mSpectralBoldFont = -1;
};
