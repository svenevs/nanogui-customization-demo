#include <my_theme.h>

#include <nanogui/label.h>
#include <nanogui/layout.h>
#include <nanogui/screen.h>
#include <nanogui/window.h>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen() : nanogui::Screen({400, 400}, "Custom Font") {
        this->setTheme(new MyTheme(mNVGContext));
    }
};


int main(int /*argc*/, const char ** /*argv*/) {
    nanogui::init();

    {
        CustomScreen *screen = new CustomScreen();
        nanogui::Window *window = new nanogui::Window(screen, "");
        window->setSize({300, 300});
        window->setLayout(new nanogui::GroupLayout());
        (new nanogui::Label(window, "First", "spirax"))->setFontSize(66);
        (new nanogui::Label(window, "Second", "spirax"))->setFontSize(66);
        (new nanogui::Label(window, "Third", "spirax"))->setFontSize(66);

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
