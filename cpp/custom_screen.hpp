#pragma once

#include "custom_theme.hpp"
#include "gl_texture.hpp"

#include <nanogui/nanogui.h>
#include <iostream>

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen(const nanogui::Vector2i &size)
        : nanogui::Screen(size, "Customization Demo") {

        /* Important! before you can use the custom fonts, even if you are not
         * setting the theme of a widget directly, you need to instantiate one
         * so that the fonts are actually loaded!
         */
        mCustomTheme = new CustomTheme(mNVGContext);
        mFontawesomeTheme = new FontawesomeTheme(mNVGContext);

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

    nanogui::Window *makeCompareWindow(const std::string &title, ThemeChoice themeChoice) {
        using namespace nanogui;
        Window *window = new Window(this, title);

        /* By setting the theme now *BEFORE* any children are added, this means that
         * all new children created will inherit a reference to this custom theme.
         *
         * When you call setTheme after-the-fact, the same will occur -- calling
         * setTheme on a widget propagates that theme to all children.
         */
        if (themeChoice == ThemeChoice::Custom)
            window->setTheme(mCustomTheme);
        else if (themeChoice == ThemeChoice::Fontawesome)
            window->setTheme(mFontawesomeTheme);

        /* The remainder of the code here is largely irrelevant, the setTheme is the
         * important part.  Everything added below exists as a testing suite to make
         * sure that all widgets that draw fonts are obeying the new theme's default
         * font selections as defined by CustomTheme::defaultFont and
         * CustomTheme::defaultBoldFont overrides (see CustomTheme.hpp).
         */
        window->setLayout(new GroupLayout(15, 6, 6));

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
            new Label(window, "Image View (Mouse Over Image and Scroll Up)");
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

        /* Message dialogs */ {
            new Label(window, "Message Dialogues");
            auto *tools = new Widget(window);
            tools->setLayout(new BoxLayout(Orientation::Horizontal,
                                           Alignment::Middle, 0, 6));
            auto *b = new Button(tools, "Info");
            Theme *dialogTheme = nullptr;
            if (themeChoice == ThemeChoice::Custom)
                dialogTheme = mCustomTheme;
            else if (themeChoice == ThemeChoice::Fontawesome)
                dialogTheme = mFontawesomeTheme;
            b->setCallback([this, dialogTheme] {
                auto *dlg = new MessageDialog(
                    this,
                    MessageDialog::Type::Information,
                    "Title",
                    "This is an information message",
                    "OK",
                    "Cancel",
                    false,
                    dialogTheme
                );
                dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
            });
            b = new Button(tools, "Warn");
            b->setCallback([this, dialogTheme] {
                auto *dlg = new MessageDialog(
                    this,
                    MessageDialog::Type::Warning,
                    "Title",
                    "This is a warning message",
                    "OK",
                    "Cancel",
                    false,
                    dialogTheme
                );
                dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
            });
            b = new Button(tools, "Ask");
            b->setCallback([this, dialogTheme] {
                auto *dlg = new MessageDialog(
                    this,
                    MessageDialog::Type::Question,
                    "Title",
                    "This is a question message",
                    "Yes",
                    "No",
                    true,
                    dialogTheme
                );
                dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
            });
        }

        // TabWidget used to test TabHeader and others while keeping the size manageable
        new Label(window, "Tab Widget");
        TabWidget* tabWidget = window->add<TabWidget>();

        /* test button and checkbox fonts */ {
            Widget *layer = tabWidget->createTab("Button Like");
            layer->setLayout(new GroupLayout());

            // regular buttons
            Button *button = new Button(layer, "PushButton");
            button = new Button(layer, "RadioButton 1");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "RadioButton 2");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "ToggleButton");
            button->setFlags(Button::Flags::ToggleButton);

            // combobox
            auto *cb = new ComboBox(
                layer, {"Combo box item 1", "Combo box item 2", "Combo box item 3"}
            );
            if (themeChoice != ThemeChoice::Default)
                cb->setSide(Popup::Side::Left);

            // popup button
            int icon = ENTYPO_ICON_EXPORT;
            if (themeChoice == ThemeChoice::Fontawesome)
                icon = FONTAWESOME_ICON_SOLID_SHARE_SQUARE;
            PopupButton *popupBtn = new PopupButton(layer, "Popup", icon);
            Popup *popup = popupBtn->popup();
            // making sure the popup button for the custom theme stays in bounds
            if (themeChoice == ThemeChoice::Custom || themeChoice == ThemeChoice::Fontawesome)
                popupBtn->setSide(Popup::Side::Left);
            popup->setLayout(new GroupLayout());
            new Label(popup, "Arbitrary widgets can be placed here");
            new CheckBox(popup, "A check box");
            // popup right
            icon = ENTYPO_ICON_FLASH;
            if (themeChoice == ThemeChoice::Fontawesome)
                icon = FONTAWESOME_ICON_SOLID_BOLT;
            popupBtn = new PopupButton(popup, "Recursive popup", icon);
            Popup *popupRight = popupBtn->popup();
            popupRight->setLayout(new GroupLayout());
            new CheckBox(popupRight, "Another check box");
            // popup left
            popupBtn = new PopupButton(popup, "Recursive popup", icon);
            popupBtn->setSide(Popup::Side::Left);
            Popup *popupLeft = popupBtn->popup();
            popupLeft->setLayout(new GroupLayout());
            new CheckBox(popupLeft, "Another check box");

            // checkbox (top level)
            new CheckBox(layer, "A CheckBox");
        }

        /* test the graph widget fonts */ {
            Widget *layer = tabWidget->createTab("Graph");
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
                layerDyn->add<Label>("Function graph widget", "spectrum-bold");
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
    CustomTheme *mCustomTheme = nullptr;
    FontawesomeTheme *mFontawesomeTheme = nullptr;
};
