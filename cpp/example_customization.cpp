/*******************************************************************************
 * This file is part of an example repository for NanoGUI.  Use of this source *
 * code is governed by a BSD-style license that can be found in the            *
 * LICENSE file:                                                               *
 *                                                                             *
 * https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE   *
 ******************************************************************************/
#include "custom_screen.hpp"

#include <nanogui/nanogui.h>

#include <vector>

int main(void) {
    nanogui::init();

    {
        using namespace nanogui;

        CustomScreen *screen = new CustomScreen({800, 900});

        // manual demonstration
        Window *window = new Window(screen, "Manual Labels");
        window->setLayout(new GroupLayout());

        const std::vector<std::string> pangram = {
            "The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog."
        };
        // add the spirax font
        for (const auto &text : pangram)
            (new Label(window, text, "spirax"))->setFontSize(30);
        // add the membra font
        for (const auto &text : pangram)
            (new Label(window, text, "membra"))->setFontSize(24);

        // make one with the default theme
        window = screen->makeCompareWindow("Default Theme", ThemeChoice::Default);
        window->setPosition({150, 0});

        // make one with the custom theme
        window = screen->makeCompareWindow("Custom Theme", ThemeChoice::Custom);
        window->setPosition({475, 0});

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
