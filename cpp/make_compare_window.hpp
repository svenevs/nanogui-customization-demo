/***************************************************************************************
 * This majority of this code is taken directly from NanoGUI example1.cpp:             *
 *                                                                                     *
 *     https://github.com/wjakob/nanogui/blob/master/src/example1.cpp                  *
 *                                                                                     *
 * Copyright (c) 2017 Wenzel Jakob <wenzel.jakob@epfl.ch>, All rights reserved.        *
 *                                                                                     *
 * Redistribution and use in source and binary forms, with or without                  *
 * modification, are permitted provided that the following conditions are met:         *
 *                                                                                     *
 * 1. Redistributions of source code must retain the above copyright notice, this      *
 *    list of conditions and the following disclaimer.                                 *
 *                                                                                     *
 * 2. Redistributions in binary form must reproduce the above copyright notice,        *
 *    this list of conditions and the following disclaimer in the documentation        *
 *    and/or other materials provided with the distribution.                           *
 *                                                                                     *
 * 3. Neither the name of the copyright holder nor the names of its contributors       *
 *    may be used to endorse or promote products derived from this software            *
 *    without specific prior written permission.                                       *
 *                                                                                     *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND     *
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED       *
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE              *
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE        *
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL          *
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR          *
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER          *
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,       *
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE       *
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                *
 *                                                                                     *
 * You are under no obligation whatsoever to provide any bug fixes, patches, or        *
 * upgrades to the features, functionality or performance of the source code           *
 * ("Enhancements") to anyone; however, if you choose to make your Enhancements        *
 * available either publicly, or directly to the author of this software, without      *
 * imposing a separate written license agreement for such Enhancements, then you       *
 * hereby grant the following license: a non-exclusive, royalty-free perpetual         *
 * license to install, use, modify, prepare derivative works, incorporate into         *
 * other computer software, distribute, and sublicense such enhancements or            *
 * derivative works thereof, in binary and source code form.                           *
 **************************************************************************************/
#pragma once

#include "custom_screen.hpp"

#include <nanogui/nanogui.h>
#include <iostream>

nanogui::Window *makeCompareWindow(CustomScreen *screen, const std::string &title, ThemeChoice themeChoice) {
    using namespace nanogui;
    Window *window = new Window(screen, title);

    /* By setting the theme now *BEFORE* any children are added, this means that
     * all new children created will inherit a reference to this custom theme.
     *
     * When you call setTheme after-the-fact, the same will occur -- calling
     * setTheme on a widget propagates that theme to all children.
     */
    if (themeChoice == ThemeChoice::Custom)
        window->setTheme(screen->mCustomTheme);
    else if (themeChoice == ThemeChoice::Fontawesome)
        window->setTheme(screen->mFontawesomeTheme);

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
        auto imageView = new ImageView(window, screen->mImagesData[0].first.texture());
        imageView->setGridThreshold(20);
        imageView->setPixelInfoThreshold(20);
        // this is the same callback from nanogui src/example1.cpp
        imageView->setPixelInfoCallback(
            [screen, imageView](const Vector2i& index) -> std::pair<std::string, Color> {
                auto &imageData = screen->mImagesData[0].second;
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
            dialogTheme = screen->mCustomTheme;
        else if (themeChoice == ThemeChoice::Fontawesome)
            dialogTheme = screen->mFontawesomeTheme;
        b->setCallback([screen, dialogTheme] {
            auto *dlg = new MessageDialog(
                screen,
                MessageDialog::Type::Information,
                "Title",
                "This is an information message"
            );
            // MessageDialog created with CustomScreen parent, but we want to
            // have the custom theme applied (propagates to children).  When
            // dialogTheme is nullptr, no custom theme is being used
            if (dialogTheme)
                dlg->setTheme(dialogTheme);
            dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
        });
        b = new Button(tools, "Warn");
        b->setCallback([screen, dialogTheme] {
            auto *dlg = new MessageDialog(
                screen,
                MessageDialog::Type::Warning,
                "Title",
                "This is a warning message"
            );
            // MessageDialog created with CustomScreen parent, but we want to
            // have the custom theme applied (propagates to children).  When
            // dialogTheme is nullptr, no custom theme is being used
            if (dialogTheme)
                dlg->setTheme(dialogTheme);
            dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
        });
        b = new Button(tools, "Ask");
        b->setCallback([screen, dialogTheme] {
            auto *dlg = new MessageDialog(
                screen,
                MessageDialog::Type::Question,
                "Title",
                "This is a question message",
                "Yes",
                "No",
                true
            );
            // MessageDialog created with CustomScreen parent, but we want to
            // have the custom theme applied (propagates to children).  When
            // dialogTheme is nullptr, no custom theme is being used
            if (dialogTheme)
                dlg->setTheme(dialogTheme);
            dlg->setCallback([](int result) { std::cout << "Dialog result: " << result << std::endl; });
        });
    }

    // TabWidget used to test TabHeader and others while keeping the size manageable
    new Label(window, "Tab Widget");
    TabWidget* tabWidget = window->add<TabWidget>();

    /* test button and checkbox fonts */ {
        Widget *layer = tabWidget->createTab("Button Like");
        layer->setLayout(new GroupLayout());

        // green color, produces white chevron at start
        auto *cp = new ColorPicker(layer, {0.28573f, 0.56702f, 0.25104f, 1.0f});
        if (themeChoice != ThemeChoice::Default)
            cp->setSide(Popup::Side::Left);
        cp->setFinalCallback([](const Color &c) {
            std::cout << "Color: " << c.transpose() << std::endl;
        });

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

        // regular buttons
        Button *button = new Button(layer, "PushButton");

        // test that non-bold fonts for buttons work (applying to radio buttons)
        std::string radio_font = window->theme()->mDefaultFont;

        button = new Button(layer, "Radio 1 (Hover for Tooltip)");
        button->setFont(radio_font);
        button->setFlags(Button::Flags::RadioButton);
        button->setTooltip("Short tooltip!");

        button = new Button(layer, "Radio 2 (Hover for Tooltip)");
        button->setFont(radio_font);
        button->setFlags(Button::Flags::RadioButton);
        button->setTooltip(
            "This is a much longer tooltip that will get wrapped automatically!"
        );
        button = new Button(layer, "ToggleButton");
        button->setFlags(Button::Flags::ToggleButton);

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
    tabWidget->setCallback([tabWidget, screen, counter] (int index) mutable {
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
            screen->performLayout();
            // Ensure that the newly added header is visible on screen
            tabWidget->ensureTabVisible(index);

        }
    });
    tabWidget->setActiveTab(0);

    return window;
}
