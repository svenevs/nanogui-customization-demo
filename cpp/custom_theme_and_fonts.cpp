/***************************************************************************************
 * This is free and unencumbered software released into the public domain.             *
 *                                                                                     *
 * Anyone is free to copy, modify, publish, use, compile, sell, or                     *
 * distribute this software, either in source code form or as a compiled               *
 * binary, for any purpose, commercial or non-commercial, and by any                   *
 * means.                                                                              *
 *                                                                                     *
 * In jurisdictions that recognize copyright laws, the author or authors               *
 * of this software dedicate any and all copyright interest in the                     *
 * software to the public domain. We make this dedication for the benefit              *
 * of the public at large and to the detriment of our heirs and                        *
 * successors. We intend this dedication to be an overt act of                         *
 * relinquishment in perpetuity of all present and future rights to this               *
 * software under copyright law.                                                       *
 *                                                                                     *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                     *
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                  *
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.              *
 * IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR                   *
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,               *
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR               *
 * OTHER DEALINGS IN THE SOFTWARE.                                                     *
 *                                                                                     *
 * For more information, please refer to <http://unlicense.org>                        *
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
