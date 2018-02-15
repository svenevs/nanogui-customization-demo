#include <my_theme.h>
#include <iostream>
#include <nanogui/nanogui.h>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen() : nanogui::Screen({800, 800}, "Custom Font") {
        // Important! before you can use the custom fonts, even if you are not
        // setting the theme of a widget directly, you need to instantiate one
        // so that the fonts are actually loaded!
        mCustomTheme = new MyTheme(mNVGContext);
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

    MyTheme *getCustomTheme() { return mCustomTheme; }

protected:
    MyTheme *mCustomTheme = nullptr;
};

// spliced from nanogui example2
enum test_enum {
    Item1 = 0,
    Item2,
    Item3
};

bool bvar = true;
int ivar = 12345678;
double dvar = 3.1415926;
float fvar = (float)dvar;
std::string strval = "A string";
test_enum enumval = Item2;
nanogui::Color colval(0.5f, 0.5f, 0.7f, 1.f);

int main(int /*argc*/, const char ** /*argv*/) {
    nanogui::init();

    {
        CustomScreen *screen = new CustomScreen();
        nanogui::Window *window = new nanogui::Window(screen, "Manual Labels");
        window->setSize({400, 600});
        window->setLayout(new nanogui::GroupLayout());
        // add some with the spirax font
        (new nanogui::Label(window, "First", "spirax"))->setFontSize(66);
        (new nanogui::Label(window, "Second", "spirax"))->setFontSize(66);
        (new nanogui::Label(window, "Third", "spirax"))->setFontSize(66);
        // add some with the membra font
        (new nanogui::Label(window, "First", "membra"))->setFontSize(44);
        (new nanogui::Label(window, "Second", "membra"))->setFontSize(44);
        (new nanogui::Label(window, "Third", "membra"))->setFontSize(44);

        window = new nanogui::Window(screen, "Full Override");
        window->setTheme(screen->getCustomTheme());
        // screen->addChild(window);
        window->setLayout(new nanogui::GroupLayout());
        new nanogui::Label(window, "Group 1");
        auto *cb = new nanogui::CheckBox(window, "A CheckBox");

        // spliced from nanogui example2
        // bool enabled = true;
        // nanogui::FormHelper *gui = new nanogui::FormHelper(screen);
        // window = gui->addWindow({10, 10}, "Form helper example");
        // gui->addGroup("Basic types");
        // gui->addVariable("bool", bvar);
        // gui->addVariable("string", strval);

        // gui->addGroup("Validating fields");
        // gui->addVariable("int", ivar)->setSpinnable(true);
        // gui->addVariable("float", fvar);
        // gui->addVariable("double", dvar)->setSpinnable(true);

        // gui->addGroup("Complex types");
        // gui->addVariable("Enumeration", enumval, enabled)
        //    ->setItems({"Item 1", "Item 2", "Item 3"});
        // gui->addVariable("Color", colval)
        //    ->setFinalCallback([](const nanogui::Color &c) {
        //          std::cout << "ColorPicker Final Callback: ["
        //                    << c.r() << ", "
        //                    << c.g() << ", "
        //                    << c.b() << ", "
        //                    << c.w() << "]" << std::endl;
        //      });

        // gui->addGroup("Other widgets");
        // gui->addButton("A button", []() { std::cout << "Button pressed." << std::endl; });

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
