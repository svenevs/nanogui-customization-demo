#include <my_theme.h>
#include <iostream>
#include <nanogui/nanogui.h>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen(const nanogui::Vector2i &size) : nanogui::Screen(size, "Custom Font") {
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

nanogui::Window *makeCompareWindow(nanogui::Widget *parent,
                                   const std::string &title,
                                   nanogui::Theme *theme = nullptr) {
    using namespace nanogui;
    Window *window = new Window(parent, title);
    if (theme)
        window->setTheme(theme);
    // classes that use fonts:
    // - Button
    // - CheckBox
    // - Graph
    // - ImageView
    // - Label
    // - Screen ?
    // - TextBox
    // - Window
    window->setLayout(new nanogui::GroupLayout());
    new Label(window, "Group 1");
    new Button(window, "A Button");
    auto *cb = new CheckBox(window, "A CheckBox");

    new Label(window, "Group 2");
    new TextBox(window, "A TextBox");
    Graph *graph = new Graph(window, "Some Function");
    graph->setHeader("E = 2.35e-3");
    graph->setFooter("Iteration 89");
    VectorXf &func = graph->values();
    func.resize(100);
    for (int i = 0; i < 100; ++i)
        func[i] = 0.5f * (0.5f * std::sin(i / 10.f) +
                          0.5f * std::cos(i / 23.f) + 1);

    return window;
}

int main(int /*argc*/, const char ** /*argv*/) {
    nanogui::init();

    {
        using namespace nanogui;

        CustomScreen *screen = new CustomScreen({800, 800});

        // manual demonstration
        Window *window = new Window(screen, "Manual Labels");
        window->setLayout(new GroupLayout());
        (new Label(window, "First", "spirax"))->setFontSize(33);
        (new Label(window, "Second", "spirax"))->setFontSize(33);
        (new Label(window, "Third", "spirax"))->setFontSize(33);
        // add some with the membra font
        new Label(window, "First", "membra");
        new Label(window, "Second", "membra");
        new Label(window, "Third", "membra");

        // make one with the default theme
        window = makeCompareWindow(screen, "Default Theme");
        window->setPosition({125, 0});

        // make one with the custom theme
        window = makeCompareWindow(screen, "Custom Theme", screen->getCustomTheme());
        window->setPosition({360, 0});

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
