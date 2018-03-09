/***************************************************************************************
 * This file is licensed under CC0:                                                    *
 *                                                                                     *
 *      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE      *
 **************************************************************************************/
#pragma once

#include "custom_theme.hpp"
#include "gl_texture.hpp"

#include <nanogui/screen.h>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen(const nanogui::Vector2i &size)
        : nanogui::Screen(size, "NanoGUI Customization Demo") {

        /* Important! before you can use the custom fonts, even if you are not
         * setting the theme of a widget directly, you need to instantiate one
         * so that the fonts are actually loaded.  Alternatively, load the
         * custom font you want here in the constructor.  You would do this
         * instead if you don't desire to change the default fonts, but just
         * want a specific font face available to set for selected widgets.
         */
        mCustomTheme = new CustomTheme(mNVGContext);
        mFontawesomeTheme = new FontawesomeTheme(mNVGContext);

        // load an image for creating the image view in makeCompareWindow,
        // loadTexture() defined in gl_texture.hpp
        loadTexture("./icons/icon1.png", mImagesData);
    }

    /// Allow <ESCAPE> to close application.
    bool keyboardEvent(int key, int scancode, int action, int modifiers) override {
        if (Screen::keyboardEvent(key, scancode, action, modifiers))
            return true;

        if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
            setVisible(false);
            return true;
        }

        return false;
    }

    // leaving these public so that makeCompareWindow can access them, typically you
    // would want to mark things like this as protected...
    using imagesDataType = std::vector<std::pair<GLTexture, GLTexture::handleType>>;
    imagesDataType mImagesData;
    nanogui::ref<CustomTheme> mCustomTheme = nullptr;
    nanogui::ref<FontawesomeTheme> mFontawesomeTheme = nullptr;
};
