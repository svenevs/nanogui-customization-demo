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
        mSpectralBoldFont = nanogui::createFontMem(ctx, "spectral-bold", "SpectralSC-Regular.ttf");

        if (mSpectralFont == -1 || mSpectralBoldFont == -1)
            throw std::runtime_error("Could not load the `spectral` fonts!");
    }

    /// The ``"sans"`` font.  Override in sub-classes to use a different font-face as the default.  Propagates to children.
    virtual std::string defaultFont() const { return "spectral"; }
    /// The ``"sans-bold"`` font.  Override in sub-classes to use a different font-face for \ref nanogui::Window.
    virtual std::string defaultWindowFont() const { return "spectral-bold"; }

    ~MyTheme() { }

    int mSpiraxFont = -1;
    int mMembraFont = -1;
    int mSpectralFont = -1;
    int mSpectralBoldFont = -1;
};
