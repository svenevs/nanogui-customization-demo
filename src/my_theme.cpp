#include <my_theme.h>
#include <nanovg.h>

///////////////////////////////////
#include <nanogui_resources.h>
// #include <nanogui_resources.cpp>
///////////////////////////////////

MyTheme::MyTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {
    mSpiraxFont = nvgCreateFontMem(ctx, "spirax", spirax_regular_ttf,
                                   spirax_regular_ttf_size, 0);
}
