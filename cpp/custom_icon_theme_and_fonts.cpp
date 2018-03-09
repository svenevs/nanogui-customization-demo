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
        window->setLayout(new GridLayout());
        new Label(window, "Entypo+");
        new Label(window, "Awesome");

        // just some similar icons to compare with
        const std::vector<std::pair<int, int>> icons = {
            {        ENTYPO_ICON_INFO_WITH_CIRCLE,    FONTAWESOME_ICON_SOLID_INFO_CIRCLE},
            {                    ENTYPO_ICON_HOME,           FONTAWESOME_ICON_SOLID_HOME},
            {              ENTYPO_ICON_LIGHT_BULB,            FONTAWESOME_ICON_LIGHTBULB},
            {                    ENTYPO_ICON_LINK,           FONTAWESOME_ICON_SOLID_LINK},
            {                     ENTYPO_ICON_EYE,            FONTAWESOME_ICON_SOLID_EYE},
            {           ENTYPO_ICON_EYE_WITH_LINE,      FONTAWESOME_ICON_SOLID_EYE_SLASH},
            {                 ENTYPO_ICON_COMPASS,              FONTAWESOME_ICON_COMPASS},
            {ENTYPO_ICON_CONTROLLER_FAST_BACKWARD,  FONTAWESOME_ICON_SOLID_FAST_BACKWARD},
            { ENTYPO_ICON_CONTROLLER_FAST_FORWARD,   FONTAWESOME_ICON_SOLID_FAST_FORWARD},
            {ENTYPO_ICON_CONTROLLER_JUMP_TO_START,  FONTAWESOME_ICON_SOLID_STEP_BACKWARD},
            {         ENTYPO_ICON_CONTROLLER_NEXT,   FONTAWESOME_ICON_SOLID_STEP_FORWARD},
            {         ENTYPO_ICON_CONTROLLER_PAUS,          FONTAWESOME_ICON_SOLID_PAUSE},
            {         ENTYPO_ICON_CONTROLLER_PLAY,           FONTAWESOME_ICON_SOLID_PLAY},
            {       ENTYPO_ICON_CONTROLLER_RECORD,         FONTAWESOME_ICON_SOLID_CIRCLE},
            {         ENTYPO_ICON_CONTROLLER_STOP,           FONTAWESOME_ICON_SOLID_STOP},
            {                    ENTYPO_ICON_CROP,           FONTAWESOME_ICON_SOLID_CROP},
            {                ENTYPO_ICON_DOWNLOAD,       FONTAWESOME_ICON_SOLID_DOWNLOAD},
            {               ENTYPO_ICON_CLIPBOARD,      FONTAWESOME_ICON_SOLID_CLIPBOARD},
            {                   ENTYPO_ICON_CLOCK,                FONTAWESOME_ICON_CLOCK},
            {               ENTYPO_ICON_THUMBS_UP,      FONTAWESOME_ICON_SOLID_THUMBS_UP},
            {             ENTYPO_ICON_THUMBS_DOWN,    FONTAWESOME_ICON_SOLID_THUMBS_DOWN},
            {             ENTYPO_ICON_PAPER_PLANE,    FONTAWESOME_ICON_SOLID_PAPER_PLANE},
            {                  ENTYPO_ICON_ROCKET,         FONTAWESOME_ICON_SOLID_ROCKET},
            {                     ENTYPO_ICON_KEY,            FONTAWESOME_ICON_SOLID_KEY},
            {                   ENTYPO_ICON_GAUGE, FONTAWESOME_ICON_SOLID_TACHOMETER_ALT}
        };
        for (const auto &pair : icons) {
            // add some vertical spacing (two widgets per row)
            new Label(window, " "); new Label(window, " ");
            // add the entypo icon
            new Label(window, std::string(nanogui::utf8(pair.first).data()), "icons");
            // add the fontawesome icon
            new Label(window, std::string(nanogui::utf8(pair.second).data()), "fontawesome");
        }
        // add some vertical spacing (two widgets per row)
        new Label(window, " "); new Label(window, " ");
        window->setFixedWidth(125);

        // make one with the default theme
        window = makeCompareWindow(screen, "Default Theme", ThemeChoice::Default);
        window->setPosition({150, 0});

        // make one with the custom theme
        window = makeCompareWindow(screen, "Fontawesome Icon Theme", ThemeChoice::Fontawesome);
        window->setPosition({475, 0});

        screen->setVisible(true);
        screen->performLayout();

        nanogui::mainloop();

    }

    nanogui::shutdown();


    return 0;
}
