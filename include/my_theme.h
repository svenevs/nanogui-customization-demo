#pragma once

#include <nanogui/theme.h>

class MyTheme : public nanogui::Theme {
public:
    MyTheme(NVGcontext *ctx);
    ~MyTheme() { }

    int mSpiraxFont;
};
