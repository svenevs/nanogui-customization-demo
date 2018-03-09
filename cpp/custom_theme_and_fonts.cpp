/***************************************************************************************
 * This file is licensed under CC0:                                                    *
 *                                                                                     *
 *      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE      *
 **************************************************************************************/
#include "make_compare_window.hpp" // includes custom_screen and custom_theme

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
        window->setFixedWidth(150);

        auto add_pangram = [window](const std::string &font, int fontSize) {
            std::string pangram = "The quick brown fox jumps over the lazy dog.";
            auto *l = new Label(window, pangram, font, fontSize);
            l->setFixedWidth(110);
        };

        add_pangram("spirax", 33);
        add_pangram("membra", 23);

        // make one with the default theme
        window = makeCompareWindow(screen, "Default Theme", ThemeChoice::Default);
        window->setPosition({150, 0});

        // make one with the custom theme
        window = makeCompareWindow(screen, "Custom Theme", ThemeChoice::Custom);
        window->setPosition({475, 0});

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
