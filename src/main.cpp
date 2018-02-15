#include <my_theme.h>
#include <nanogui/nanogui.h>

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>

#include <iostream>
#include <vector>

class GLTexture {
public:
    using handleType = std::unique_ptr<uint8_t[], void(*)(void*)>;
    GLTexture() = default;
    GLTexture(const std::string& textureName)
        : mTextureName(textureName), mTextureId(0) {}

    GLTexture(const std::string& textureName, GLint textureId)
        : mTextureName(textureName), mTextureId(textureId) {}

    GLTexture(const GLTexture& other) = delete;
    GLTexture(GLTexture&& other) noexcept
        : mTextureName(std::move(other.mTextureName)),
        mTextureId(other.mTextureId) {
        other.mTextureId = 0;
    }
    GLTexture& operator=(const GLTexture& other) = delete;
    GLTexture& operator=(GLTexture&& other) noexcept {
        mTextureName = std::move(other.mTextureName);
        std::swap(mTextureId, other.mTextureId);
        return *this;
    }
    ~GLTexture() noexcept {
        if (mTextureId)
            glDeleteTextures(1, &mTextureId);
    }

    GLuint texture() const { return mTextureId; }
    const std::string& textureName() const { return mTextureName; }

    /**
    *  Load a file in memory and create an OpenGL texture.
    *  Returns a handle type (an std::unique_ptr) to the loaded pixels.
    */
    handleType load(const std::string& fileName) {
        if (mTextureId) {
            glDeleteTextures(1, &mTextureId);
            mTextureId = 0;
        }
        int force_channels = 0;
        int w, h, n;
        handleType textureData(stbi_load(fileName.c_str(), &w, &h, &n, force_channels), stbi_image_free);
        if (!textureData)
            throw std::invalid_argument("Could not load texture data from file " + fileName);
        glGenTextures(1, &mTextureId);
        glBindTexture(GL_TEXTURE_2D, mTextureId);
        GLint internalFormat;
        GLint format;
        switch (n) {
            case 1: internalFormat = GL_R8; format = GL_RED; break;
            case 2: internalFormat = GL_RG8; format = GL_RG; break;
            case 3: internalFormat = GL_RGB8; format = GL_RGB; break;
            case 4: internalFormat = GL_RGBA8; format = GL_RGBA; break;
            default: internalFormat = 0; format = 0; break;
        }
        glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, w, h, 0, format, GL_UNSIGNED_BYTE, textureData.get());
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        return textureData;
    }

private:
    std::string mTextureName;
    GLuint mTextureId;
};

class CustomScreen : public nanogui::Screen {
public:
    CustomScreen(const nanogui::Vector2i &size) : nanogui::Screen(size, "Custom Font") {
        // Important! before you can use the custom fonts, even if you are not
        // setting the theme of a widget directly, you need to instantiate one
        // so that the fonts are actually loaded!
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
        if (customTheme)
            window->setTheme(mCustomTheme);
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

        new Label(window, "Image View");
        // NOTE: there's only ever one image in imagesData!  The author is being
        //       lazy and just re-using code from nanogui example1.cpp
        auto imageView = new ImageView(window, mImagesData[0].first.texture());
        imageView->setGridThreshold(20);
        imageView->setPixelInfoThreshold(20);
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

        TabWidget* tabWidget = window->add<TabWidget>();
        Widget *layer = tabWidget->createTab("Button Like");
        layer->setLayout(new GroupLayout());
        {
            new Label(layer, "Button Like");
            Button *button = new Button(layer, "PushButton");
            button = new Button(layer, "RadioButton 1");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "RadioButton 2");
            button->setFlags(Button::Flags::RadioButton);
            button = new Button(layer, "ToggleButton");
            button->setFlags(Button::Flags::ToggleButton);
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
            new CheckBox(popupLeft, "Another check box");
            auto *cb = new CheckBox(layer, "A CheckBox");
        }

        // Use overloaded variadic add to fill the tab widget with Different tabs.

        layer = tabWidget->createTab("Function Graph");
        layer->setLayout(new GroupLayout());
        {
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

int main(int /*argc*/, const char ** /*argv*/) {
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
