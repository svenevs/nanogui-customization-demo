#pragma once

#include <nanogui/theme.h>
#include <nanogui_resources.h> // provides nanogui::createFontMem
#include <iostream>

class MyTheme : public nanogui::Theme {
public:
    MyTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
        mSpiraxFont = nanogui::createFontMem(ctx, "spirax", "Spirax-Regular.ttf");
        mMembraFont = nanogui::createFontMem(ctx, "membra", "membra.ttf");

        if (mSpiraxFont == -1 || mMembraFont == -1)
            throw std::runtime_error("Could not load the `spirax` or `membra` fonts!");

        std::cout << "NORMAL: " << mFontNormal << std::endl;

        // by setting these two, you are overriding the nanogui::Theme defaults
        // by using `"sans"` and `"sans-bold"`, you force the roboto fonts out
        mFontNormal = nanogui::createFontMem(ctx, "sans", "SpectralSC-Regular.ttf");
        mFontBold   = nanogui::createFontMem(ctx, "sans-bold", "SpectralSC-Regular.ttf");

        std::cout << "NORMAL: " << mFontNormal << std::endl;

        if (mFontNormal == -1 || mFontBold == -1)
            throw std::runtime_error("Could not load the `spectral` fonts!");
    }

    ~MyTheme() { }

    int mSpiraxFont = -1;
    int mMembraFont = -1;
};
