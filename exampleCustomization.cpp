#include "CustomTheme.hpp"
#include "GLTexture.hpp"

#include <nanogui/nanogui.h>

#include <vector>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen(const nanogui::Vector2i &size)
        : nanogui::Screen(size, "Custom Font") {

        /* Important! before you can use the custom fonts, even if you are not
         * setting the theme of a widget directly, you need to instantiate one
         * so that the fonts are actually loaded!
         */
        mCustomTheme = new MyTheme(mNVGContext);

        // load an image for creating the image view in makeCompareWindow
        GLTexture texture;
        auto data = texture.load("./icons/icon1.png");
        mImagesData.emplace_back(std::move(texture), std::move(data));
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

    nanogui::Window *makeCompareWindow(const std::string &title, bool customTheme) {
        using namespace nanogui;
        Window *window = new Window(this, title);

        /* By setting the theme now *BEFORE* any children are added, this means that
         * all new children created will inherit a reference to this custom theme.
         *
         * When you call setTheme after-the-fact, the same will occur -- calling
         * setTheme on a widget propagates that theme to all children.
         */
        if (customTheme)
            window->setTheme(mCustomTheme);

        /* The remainder of the code here is largely irrelevant, the setTheme is the
         * important part.  Everything added below exists as a testing suite to make
         * sure that all widgets that draw fonts are obeying the new theme's default
         * font selections as defined by CustomTheme::defaultFont and
         * CustomTheme::defaultBoldFont overrides (see CustomTheme.hpp).
         */
        window->setLayout(new nanogui::GroupLayout());

        /* test text box fonts */ {
            new Label(window, "Text Boxes");
            Widget *wrapper = new Widget(window);
            GridLayout *grid_layout = new GridLayout();
            grid_layout->setColAlignment({Alignment::Maximum, Alignment::Fill});
            wrapper->setLayout(grid_layout);
            new Label(wrapper, "TextBox : ");
            (new TextBox(wrapper, "Some Text"))->setEditable(true);
            new Label(wrapper, "IntBox : ");
            (new IntBox<int>(wrapper))->setSpinnable(true);
            new Label(wrapper, "FloatBox : ");
            (new FloatBox<float>(wrapper))->setSpinnable(true);
        }

        /* test ImageView fonts (needs callback, scroll up on image to see) */ {
            new Label(window, "Image View");
            // NOTE: there's only ever one image in imagesData!
            auto imageView = new ImageView(window, mImagesData[0].first.texture());
            imageView->setGridThreshold(20);
            imageView->setPixelInfoThreshold(20);
            // this is the same callback from nanogui src/example1.cpp
            imageView->setPixelInfoCallback(
                [this, imageView](const Vector2i& index) -> std::pair<std::string, Color> {
                    auto &imageData = this->mImagesData[0].second;
                    auto &textureSize = imageView->imageSize();
                    std::string stringData;
                    uint16_t channelSum = 0;
                    for (int i = 0; i != 4; ++i) {
                        auto &channelData = imageData[4*index.y()*textureSize.x() + 4*index.x() + i];
                        channelSum += channelData;
                        stringData += (std::to_string(static_cast<int>(channelData)) + "\n");
                    }
                    float intensity = static_cast<float>(255 - (channelSum / 4)) / 255.0f;
                    float colorScale = intensity > 0.5f ? (intensity + 1) / 2 : intensity / 2;
                    Color textColor = Color(colorScale, 1.0f);
                    return { stringData, textColor };
                }
            );
        }

        // TabWidget used to test TabHeader and others while keeping the size manageable
        TabWidget* tabWidget = window->add<TabWidget>();

        /* test button and checkbox fonts */ {
            Widget *layer = tabWidget->createTab("Button Like");
            layer->setLayout(new GroupLayout());

            new Label(layer, "Button Like");
            // regular buttons
            Button *button = new Button(layer, "PushButton");
            button = new Button(layer, "RadioButton 1");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "RadioButton 2");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "ToggleButton");
            button->setFlags(Button::Flags::ToggleButton);

            // popup button
            PopupButton *popupBtn = new PopupButton(layer, "Popup", ENTYPO_ICON_EXPORT);
            Popup *popup = popupBtn->popup();
            // making sure the popup button for the custom theme stays in bounds
            if (customTheme)
                popupBtn->setSide(Popup::Side::Left);
            popup->setLayout(new GroupLayout());
            new Label(popup, "Arbitrary widgets can be placed here");
            new CheckBox(popup, "A check box");
            // popup right
            popupBtn = new PopupButton(popup, "Recursive popup", ENTYPO_ICON_FLASH);
            Popup *popupRight = popupBtn->popup();
            popupRight->setLayout(new GroupLayout());
            new CheckBox(popupRight, "Another check box");
            // popup left
            popupBtn = new PopupButton(popup, "Recursive popup", ENTYPO_ICON_FLASH);
            popupBtn->setSide(Popup::Side::Left);
            Popup *popupLeft = popupBtn->popup();
            popupLeft->setLayout(new GroupLayout());

            // checkbox
            new CheckBox(popupLeft, "Another check box");
            auto *cb = new CheckBox(layer, "A CheckBox");
        }

        /* test the graph widget fonts */ {
            Widget *layer = tabWidget->createTab("Function Graph");
            layer->setLayout(new GroupLayout());

            // Same as nanogui src/example1.cpp
            new Label(layer, "Function Graph Widget");
            Graph *graph = layer->add<Graph>("Some Function");

            graph->setHeader("E = 2.35e-3");
            graph->setFooter("Iteration 89");
            VectorXf &func = graph->values();
            func.resize(100);
            for (int i = 0; i < 100; ++i)
                func[i] = 0.5f * (0.5f * std::sin(i / 10.f) +
                                  0.5f * std::cos(i / 23.f) + 1);
        }

        // Dummy tab used to represent the last tab button.
        tabWidget->createTab("+");

        // A simple counter.
        int counter = 1;
        tabWidget->setCallback([tabWidget, this, counter] (int index) mutable {
            if (index == (tabWidget->tabCount()-1)) {
                // When the "+" tab has been clicked, simply add a new tab.
                std::string tabName = "Dynamic " + std::to_string(counter);
                Widget* layerDyn = tabWidget->createTab(index, tabName);
                layerDyn->setLayout(new GroupLayout());
                layerDyn->add<Label>("Function graph widget", "sans-bold");
                Graph *graphDyn = layerDyn->add<Graph>("Dynamic function");

                graphDyn->setHeader("E = 2.35e-3");
                graphDyn->setFooter("Iteration " + std::to_string(index*counter));
                VectorXf &funcDyn = graphDyn->values();
                funcDyn.resize(100);
                for (int i = 0; i < 100; ++i)
                    funcDyn[i] = 0.5f *
                        std::abs((0.5f * std::sin(i / 10.f + counter) +
                                  0.5f * std::cos(i / 23.f + 1 + counter)));
                ++counter;
                // We must invoke perform layout from the screen instance to keep everything in order.
                // This is essential when creating tabs dynamically.
                performLayout();
                // Ensure that the newly added header is visible on screen
                tabWidget->ensureTabVisible(index);

            }
        });
        tabWidget->setActiveTab(0);

        return window;
    }

protected:
    using imagesDataType = std::vector<std::pair<GLTexture, GLTexture::handleType>>;
    imagesDataType mImagesData;
    MyTheme *mCustomTheme = nullptr;
};

int main(void) {
    nanogui::init();

    {
        using namespace nanogui;

        CustomScreen *screen = new CustomScreen({800, 800});

        // manual demonstration
        Window *window = new Window(screen, "Manual Labels");
        window->setLayout(new GroupLayout());
        Label *label = new Label(window, "First", "spirax");
        label->setFontSize(28);
        label = new Label(window, "Second", "spirax");
        label->setFontSize(28);
        label = new Label(window, "Third", "spirax");
        label->setFontSize(28);
        // add some with the membra font, make sure setFont works too
        label = new Label(window, "First");
        label->setFont("membra");
        label = new Label(window, "Second");
        label->setFont("membra");
        label = new Label(window, "Third");
        label->setFont("membra");

        // make one with the default theme
        window = screen->makeCompareWindow("Default Theme", false);
        window->setPosition({150, 0});

        // make one with the custom theme
        window = screen->makeCompareWindow("Custom Theme", true);
        window->setPosition({475, 0});

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
