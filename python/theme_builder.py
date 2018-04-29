########################################################################################
# This file is licensed under CC0:                                                     #
#                                                                                      #
#      https://github.com/svenevs/nanogui-customization-demo/blob/master/LICENSE       #
########################################################################################

import gc
import nanogui

import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from custom_screen import CustomScreen
from custom_theme import CustomTheme, ThemeChoice
from make_compare_window import makeCompareWindow


class DynamicTheme(nanogui.Theme):
    def __init__(self, screen):
        super(DynamicTheme, self).__init__(screen.nvgContext())
        # stash screen so that theme variable changes can also issue performLayout()
        # which will refresh everything / redraw so the new sizes / colors are used
        self.screen = screen
        # storing references for loading functionality
        self.number_pickers = {}
        self.color_pickers = {}
    ####################################################################################
    # C++ Class Definition                                                             #
    ####################################################################################
    def asCpp(self):
        def col_str(c):
            return "Color({0}f, {1}f, {2}f, {3}f)".format(c.r, c.g, c.b, c.w)

        head = textwrap.dedent('''
            #pragma once

            #include <nanogui/theme.h>

            /*
        ''')
        json_comment = self.asCommentJSON("", "    ")
        tail = textwrap.dedent('''
            */
            class CustomTheme : public nanogui::Theme {{
            public:
                CustomTheme(NVGcontext *ctx) : nanogui::Theme(ctx) {{
                    // TODO: set any icon customizations / load custom fonts if desired

                    mStandardFontSize                 = {mStandardFontSize};
                    mButtonFontSize                   = {mButtonFontSize};
                    mTextBoxFontSize                  = {mTextBoxFontSize};
                    mWindowFontSize                   = {mWindowFontSize};
                    mIconScale                        = {mIconScale};

                    mWindowCornerRadius               = {mWindowCornerRadius};
                    mWindowHeaderHeight               = {mWindowHeaderHeight};
                    mWindowDropShadowSize             = {mWindowDropShadowSize};
                    mButtonCornerRadius               = {mButtonCornerRadius};
                    mTabBorderWidth                   = {mTabBorderWidth};
                    mTabInnerMargin                   = {mTabInnerMargin};
                    mTabMinButtonWidth                = {mTabMinButtonWidth};
                    mTabMaxButtonWidth                = {mTabMaxButtonWidth};
                    mTabControlWidth                  = {mTabControlWidth};
                    mTabButtonHorizontalPadding       = {mTabButtonHorizontalPadding};
                    mTabButtonVerticalPadding         = {mTabButtonVerticalPadding};

                    using nanogui::Color;
                    mDropShadow                       = {mDropShadow};
                    mTransparent                      = {mTransparent};
                    mBorderDark                       = {mBorderDark};
                    mBorderLight                      = {mBorderLight};
                    mBorderMedium                     = {mBorderMedium};
                    mTextColor                        = {mTextColor};
                    mDisabledTextColor                = {mDisabledTextColor};
                    mTextColorShadow                  = {mTextColorShadow};
                    mIconColor                        = {mIconColor};

                    mButtonGradientTopFocused         = {mButtonGradientTopFocused};
                    mButtonGradientBotFocused         = {mButtonGradientBotFocused};
                    mButtonGradientTopUnfocused       = {mButtonGradientTopUnfocused};
                    mButtonGradientBotUnfocused       = {mButtonGradientBotUnfocused};
                    mButtonGradientTopPushed          = {mButtonGradientTopPushed};
                    mButtonGradientBotPushed          = {mButtonGradientBotPushed};

                    mTooltipOpacity                   = {mTooltipOpacity};
                    mTooltipBackgroundColor           = {mTooltipBackgroundColor};
                    mTooltipTextColor                 = {mTooltipTextColor};

                    /* Window-related */
                    mWindowFillUnfocused              = {mWindowFillUnfocused};
                    mWindowFillFocused                = {mWindowFillFocused};
                    mWindowTitleUnfocused             = {mWindowTitleUnfocused};
                    mWindowTitleFocused               = {mWindowTitleFocused};

                    mWindowHeaderGradientTop          = {mWindowHeaderGradientTop};
                    mWindowHeaderGradientBot          = {mWindowHeaderGradientBot};
                    mWindowHeaderSepTop               = {mWindowHeaderSepTop};
                    mWindowHeaderSepBot               = {mWindowHeaderSepBot};

                    mWindowPopup                      = {mWindowPopup};
                    mWindowPopupTransparent           = {mWindowPopupTransparent};
                }}

                virtual ~CustomTheme() {{ /* does nothing */ }}
            }};
        '''.format(
            mStandardFontSize=self.mStandardFontSize,
            mButtonFontSize=self.mButtonFontSize,
            mTextBoxFontSize=self.mTextBoxFontSize,
            mWindowFontSize=self.mWindowFontSize,
            mIconScale=self.mIconScale,

            mWindowCornerRadius=self.mWindowCornerRadius,
            mWindowHeaderHeight=self.mWindowHeaderHeight,
            mWindowDropShadowSize=self.mWindowDropShadowSize,
            mButtonCornerRadius=self.mButtonCornerRadius,
            mTabBorderWidth=self.mTabBorderWidth,
            mTabInnerMargin=self.mTabInnerMargin,
            mTabMinButtonWidth=self.mTabMinButtonWidth,
            mTabMaxButtonWidth=self.mTabMaxButtonWidth,
            mTabControlWidth=self.mTabControlWidth,
            mTabButtonHorizontalPadding=self.mTabButtonHorizontalPadding,
            mTabButtonVerticalPadding=self.mTabButtonVerticalPadding,

            mDropShadow=col_str(self.mDropShadow),
            mTransparent=col_str(self.mTransparent),
            mBorderDark=col_str(self.mBorderDark),
            mBorderLight=col_str(self.mBorderLight),
            mBorderMedium=col_str(self.mBorderMedium),
            mTextColor=col_str(self.mTextColor),
            mDisabledTextColor=col_str(self.mDisabledTextColor),
            mTextColorShadow=col_str(self.mTextColorShadow),
            mIconColor=col_str(self.mIconColor),

            mButtonGradientTopFocused=col_str(self.mButtonGradientTopFocused),
            mButtonGradientBotFocused=col_str(self.mButtonGradientBotFocused),
            mButtonGradientTopUnfocused=col_str(self.mButtonGradientTopUnfocused),
            mButtonGradientBotUnfocused=col_str(self.mButtonGradientBotUnfocused),
            mButtonGradientTopPushed=col_str(self.mButtonGradientTopPushed),
            mButtonGradientBotPushed=col_str(self.mButtonGradientBotPushed),

            mTooltipOpacity=self.mTooltipOpacity,
            mTooltipBackgroundColor=col_str(self.mTooltipBackgroundColor),
            mTooltipTextColor=col_str(self.mTooltipTextColor),

            mWindowFillUnfocused=col_str(self.mWindowFillUnfocused),
            mWindowFillFocused=col_str(self.mWindowFillFocused),
            mWindowTitleUnfocused=col_str(self.mWindowTitleUnfocused),
            mWindowTitleFocused=col_str(self.mWindowTitleFocused),

            mWindowHeaderGradientTop=col_str(self.mWindowHeaderGradientTop),
            mWindowHeaderGradientBot=col_str(self.mWindowHeaderGradientBot),
            mWindowHeaderSepTop=col_str(self.mWindowHeaderSepTop),
            mWindowHeaderSepBot=col_str(self.mWindowHeaderSepBot),

            mWindowPopup=col_str(self.mWindowPopup),
            mWindowPopupTransparent=col_str(self.mWindowPopupTransparent)
        ))
        return "{0}{1}{2}".format(head, json_comment, tail)
    ####################################################################################
    # Python Class Definition                                                          #
    ####################################################################################
    def asPython(self):
        def col_str(c):
            return "nanogui.Color({0}, {1}, {2}, {3})".format(c.r, c.g, c.b, c.w)

        head = textwrap.dedent('''
            import nanogui

            class CustomTheme(nanogui.Theme):
                \'\'\'
        ''')
        json_comment = self.asCommentJSON("    ", "        ")
        tail = textwrap.dedent('''
                \'\'\'

                def __init__(self, ctx):
                    super(CustomTheme, self).__init__(ctx)

                    # TODO: set any icon customizations / load custom fonts if desired

                    self.mStandardFontSize                 = {mStandardFontSize}
                    self.mButtonFontSize                   = {mButtonFontSize}
                    self.mTextBoxFontSize                  = {mTextBoxFontSize}
                    self.mWindowFontSize                   = {mWindowFontSize}
                    self.mIconScale                        = {mIconScale}

                    self.mWindowCornerRadius               = {mWindowCornerRadius}
                    self.mWindowHeaderHeight               = {mWindowHeaderHeight}
                    self.mWindowDropShadowSize             = {mWindowDropShadowSize}
                    self.mButtonCornerRadius               = {mButtonCornerRadius}
                    self.mTabBorderWidth                   = {mTabBorderWidth}
                    self.mTabInnerMargin                   = {mTabInnerMargin}
                    self.mTabMinButtonWidth                = {mTabMinButtonWidth}
                    self.mTabMaxButtonWidth                = {mTabMaxButtonWidth}
                    self.mTabControlWidth                  = {mTabControlWidth}
                    self.mTabButtonHorizontalPadding       = {mTabButtonHorizontalPadding}
                    self.mTabButtonVerticalPadding         = {mTabButtonVerticalPadding}

                    self.mDropShadow                       = {mDropShadow}
                    self.mTransparent                      = {mTransparent}
                    self.mBorderDark                       = {mBorderDark}
                    self.mBorderLight                      = {mBorderLight}
                    self.mBorderMedium                     = {mBorderMedium}
                    self.mTextColor                        = {mTextColor}
                    self.mDisabledTextColor                = {mDisabledTextColor}
                    self.mTextColorShadow                  = {mTextColorShadow}
                    self.mIconColor                        = {mIconColor}

                    self.mButtonGradientTopFocused         = {mButtonGradientTopFocused}
                    self.mButtonGradientBotFocused         = {mButtonGradientBotFocused}
                    self.mButtonGradientTopUnfocused       = {mButtonGradientTopUnfocused}
                    self.mButtonGradientBotUnfocused       = {mButtonGradientBotUnfocused}
                    self.mButtonGradientTopPushed          = {mButtonGradientTopPushed}
                    self.mButtonGradientBotPushed          = {mButtonGradientBotPushed}

                    self.mTooltipOpacity                   = {mTooltipOpacity}
                    self.mTooltipBackgroundColor           = {mTooltipBackgroundColor}
                    self.mTooltipTextColor                 = {mTooltipTextColor}

                    # Window-related
                    self.mWindowFillUnfocused              = {mWindowFillUnfocused}
                    self.mWindowFillFocused                = {mWindowFillFocused}
                    self.mWindowTitleUnfocused             = {mWindowTitleUnfocused}
                    self.mWindowTitleFocused               = {mWindowTitleFocused}

                    self.mWindowHeaderGradientTop          = {mWindowHeaderGradientTop}
                    self.mWindowHeaderGradientBot          = {mWindowHeaderGradientBot}
                    self.mWindowHeaderSepTop               = {mWindowHeaderSepTop}
                    self.mWindowHeaderSepBot               = {mWindowHeaderSepBot}

                    self.mWindowPopup                      = {mWindowPopup}
                    self.mWindowPopupTransparent           = {mWindowPopupTransparent}
            # End CustomTheme ##############################################################

        '''.format(
            mStandardFontSize=self.mStandardFontSize,
            mButtonFontSize=self.mButtonFontSize,
            mTextBoxFontSize=self.mTextBoxFontSize,
            mWindowFontSize=self.mWindowFontSize,
            mIconScale=self.mIconScale,

            mWindowCornerRadius=self.mWindowCornerRadius,
            mWindowHeaderHeight=self.mWindowHeaderHeight,
            mWindowDropShadowSize=self.mWindowDropShadowSize,
            mButtonCornerRadius=self.mButtonCornerRadius,
            mTabBorderWidth=self.mTabBorderWidth,
            mTabInnerMargin=self.mTabInnerMargin,
            mTabMinButtonWidth=self.mTabMinButtonWidth,
            mTabMaxButtonWidth=self.mTabMaxButtonWidth,
            mTabControlWidth=self.mTabControlWidth,
            mTabButtonHorizontalPadding=self.mTabButtonHorizontalPadding,
            mTabButtonVerticalPadding=self.mTabButtonVerticalPadding,

            mDropShadow=col_str(self.mDropShadow),
            mTransparent=col_str(self.mTransparent),
            mBorderDark=col_str(self.mBorderDark),
            mBorderLight=col_str(self.mBorderLight),
            mBorderMedium=col_str(self.mBorderMedium),
            mTextColor=col_str(self.mTextColor),
            mDisabledTextColor=col_str(self.mDisabledTextColor),
            mTextColorShadow=col_str(self.mTextColorShadow),
            mIconColor=col_str(self.mIconColor),

            mButtonGradientTopFocused=col_str(self.mButtonGradientTopFocused),
            mButtonGradientBotFocused=col_str(self.mButtonGradientBotFocused),
            mButtonGradientTopUnfocused=col_str(self.mButtonGradientTopUnfocused),
            mButtonGradientBotUnfocused=col_str(self.mButtonGradientBotUnfocused),
            mButtonGradientTopPushed=col_str(self.mButtonGradientTopPushed),
            mButtonGradientBotPushed=col_str(self.mButtonGradientBotPushed),

            mTooltipOpacity=self.mTooltipOpacity,
            mTooltipBackgroundColor=col_str(self.mTooltipBackgroundColor),
            mTooltipTextColor=col_str(self.mTooltipTextColor),

            mWindowFillUnfocused=col_str(self.mWindowFillUnfocused),
            mWindowFillFocused=col_str(self.mWindowFillFocused),
            mWindowTitleUnfocused=col_str(self.mWindowTitleUnfocused),
            mWindowTitleFocused=col_str(self.mWindowTitleFocused),

            mWindowHeaderGradientTop=col_str(self.mWindowHeaderGradientTop),
            mWindowHeaderGradientBot=col_str(self.mWindowHeaderGradientBot),
            mWindowHeaderSepTop=col_str(self.mWindowHeaderSepTop),
            mWindowHeaderSepBot=col_str(self.mWindowHeaderSepBot),

            mWindowPopup=col_str(self.mWindowPopup),
            mWindowPopupTransparent=col_str(self.mWindowPopupTransparent)
        ))
        return "{0}{1}{2}".format(head, json_comment, tail)
    ####################################################################################
    # JSON specs                                                                       #
    ####################################################################################
    def asCommentJSON(self, indent, json_indent):
        json_comment = "{0}The JSON for this class::\n\n{1}\n\n".format(indent, self.asJSON())
        json_comment = "\n{0}".format(json_indent).join(line for line in json_comment.splitlines())
        json_comment = json_comment.replace("\n{0}\n".format(json_indent), "\n\n")
        return json_comment.rstrip()

    def asJSON(self):
        def col_str(c):
            return "[{0}, {1}, {2}, {3}]".format(c.r, c.g, c.b, c.w)

        return textwrap.dedent('''
            {{
              "mStandardFontSize":                  {mStandardFontSize},
              "mButtonFontSize":                    {mButtonFontSize},
              "mTextBoxFontSize":                   {mTextBoxFontSize},
              "mWindowFontSize":                    {mWindowFontSize},
              "mIconScale":                         {mIconScale},

              "mWindowCornerRadius":                {mWindowCornerRadius},
              "mWindowHeaderHeight":                {mWindowHeaderHeight},
              "mWindowDropShadowSize":              {mWindowDropShadowSize},
              "mButtonCornerRadius":                {mButtonCornerRadius},
              "mTabBorderWidth":                    {mTabBorderWidth},
              "mTabInnerMargin":                    {mTabInnerMargin},
              "mTabMinButtonWidth":                 {mTabMinButtonWidth},
              "mTabMaxButtonWidth":                 {mTabMaxButtonWidth},
              "mTabControlWidth":                   {mTabControlWidth},
              "mTabButtonHorizontalPadding":        {mTabButtonHorizontalPadding},
              "mTabButtonVerticalPadding":          {mTabButtonVerticalPadding},

              "mDropShadow":                        {mDropShadow},
              "mTransparent":                       {mTransparent},
              "mBorderDark":                        {mBorderDark},
              "mBorderLight":                       {mBorderLight},
              "mBorderMedium":                      {mBorderMedium},
              "mTextColor":                         {mTextColor},
              "mDisabledTextColor":                 {mDisabledTextColor},
              "mTextColorShadow":                   {mTextColorShadow},
              "mIconColor":                         {mIconColor},

              "mButtonGradientTopFocused":          {mButtonGradientTopFocused},
              "mButtonGradientBotFocused":          {mButtonGradientBotFocused},
              "mButtonGradientTopUnfocused":        {mButtonGradientTopUnfocused},
              "mButtonGradientBotUnfocused":        {mButtonGradientBotUnfocused},
              "mButtonGradientTopPushed":           {mButtonGradientTopPushed},
              "mButtonGradientBotPushed":           {mButtonGradientBotPushed},

              "mTooltipOpacity":                    {mTooltipOpacity},
              "mTooltipBackgroundColor":            {mTooltipBackgroundColor},
              "mTooltipTextColor":                  {mTooltipTextColor},

              "mWindowFillUnfocused":               {mWindowFillUnfocused},
              "mWindowFillFocused":                 {mWindowFillFocused},
              "mWindowTitleUnfocused":              {mWindowTitleUnfocused},
              "mWindowTitleFocused":                {mWindowTitleFocused},

              "mWindowHeaderGradientTop":           {mWindowHeaderGradientTop},
              "mWindowHeaderGradientBot":           {mWindowHeaderGradientBot},
              "mWindowHeaderSepTop":                {mWindowHeaderSepTop},
              "mWindowHeaderSepBot":                {mWindowHeaderSepBot},

              "mWindowPopup":                       {mWindowPopup},
              "mWindowPopupTransparent":            {mWindowPopupTransparent}
            }}
        '''.format(
            mStandardFontSize=self.mStandardFontSize,
            mButtonFontSize=self.mButtonFontSize,
            mTextBoxFontSize=self.mTextBoxFontSize,
            mWindowFontSize=self.mWindowFontSize,
            mIconScale=self.mIconScale,

            mWindowCornerRadius=self.mWindowCornerRadius,
            mWindowHeaderHeight=self.mWindowHeaderHeight,
            mWindowDropShadowSize=self.mWindowDropShadowSize,
            mButtonCornerRadius=self.mButtonCornerRadius,
            mTabBorderWidth=self.mTabBorderWidth,
            mTabInnerMargin=self.mTabInnerMargin,
            mTabMinButtonWidth=self.mTabMinButtonWidth,
            mTabMaxButtonWidth=self.mTabMaxButtonWidth,
            mTabControlWidth=self.mTabControlWidth,
            mTabButtonHorizontalPadding=self.mTabButtonHorizontalPadding,
            mTabButtonVerticalPadding=self.mTabButtonVerticalPadding,

            mDropShadow=col_str(self.mDropShadow),
            mTransparent=col_str(self.mTransparent),
            mBorderDark=col_str(self.mBorderDark),
            mBorderLight=col_str(self.mBorderLight),
            mBorderMedium=col_str(self.mBorderMedium),
            mTextColor=col_str(self.mTextColor),
            mDisabledTextColor=col_str(self.mDisabledTextColor),
            mTextColorShadow=col_str(self.mTextColorShadow),
            mIconColor=col_str(self.mIconColor),

            mButtonGradientTopFocused=col_str(self.mButtonGradientTopFocused),
            mButtonGradientBotFocused=col_str(self.mButtonGradientBotFocused),
            mButtonGradientTopUnfocused=col_str(self.mButtonGradientTopUnfocused),
            mButtonGradientBotUnfocused=col_str(self.mButtonGradientBotUnfocused),
            mButtonGradientTopPushed=col_str(self.mButtonGradientTopPushed),
            mButtonGradientBotPushed=col_str(self.mButtonGradientBotPushed),

            mTooltipOpacity=self.mTooltipOpacity,
            mTooltipBackgroundColor=col_str(self.mTooltipBackgroundColor),
            mTooltipTextColor=col_str(self.mTooltipTextColor),

            mWindowFillUnfocused=col_str(self.mWindowFillUnfocused),
            mWindowFillFocused=col_str(self.mWindowFillFocused),
            mWindowTitleUnfocused=col_str(self.mWindowTitleUnfocused),
            mWindowTitleFocused=col_str(self.mWindowTitleFocused),

            mWindowHeaderGradientTop=col_str(self.mWindowHeaderGradientTop),
            mWindowHeaderGradientBot=col_str(self.mWindowHeaderGradientBot),
            mWindowHeaderSepTop=col_str(self.mWindowHeaderSepTop),
            mWindowHeaderSepBot=col_str(self.mWindowHeaderSepBot),

            mWindowPopup=col_str(self.mWindowPopup),
            mWindowPopupTransparent=col_str(self.mWindowPopupTransparent)
        )).lstrip()

    # values is a dict from json.load(s)
    def loadFromJSON(self, values):
        sizes = [
            "mStandardFontSize", "mButtonFontSize", "mTextBoxFontSize",
            "mWindowFontSize", "mWindowCornerRadius", #"mIconScale"
            "mWindowHeaderHeight", "mWindowDropShadowSize",
            "mButtonCornerRadius", "mTabBorderWidth", "mTabInnerMargin",
            "mTabMinButtonWidth", "mTabMaxButtonWidth", "mTabControlWidth",
            "mTabButtonHorizontalPadding", "mTabButtonVerticalPadding",
            "mTooltipOpacity"  # not a size, but is a float so do here
        ]
        for s in sizes:
            if s in values:
                val = values[s]
                self.__setattr__(s, val)
                self.number_pickers[s].setValue(val)
            else:
                raise RuntimeError("The key '{0}' was not provided.".format(s))

        colors = [
            "mDropShadow", "mTransparent", "mBorderDark", "mBorderLight",
            "mBorderMedium", "mTextColor", "mDisabledTextColor", "mTextColorShadow",
            "mIconColor", "mButtonGradientTopFocused", "mButtonGradientBotFocused",
            "mButtonGradientTopUnfocused", "mButtonGradientBotUnfocused",
            "mButtonGradientTopPushed", "mButtonGradientBotPushed",
            "mTooltipBackgroundColor", "mTooltipTextColor", "mWindowFillUnfocused",
            "mWindowFillFocused", "mWindowTitleUnfocused", "mWindowTitleFocused",
            "mWindowHeaderGradientTop", "mWindowHeaderGradientBot",
            "mWindowHeaderSepTop", "mWindowHeaderSepBot", "mWindowPopup",
            "mWindowPopupTransparent"
        ]
        for c in colors:
            if c in values:
                r, g, b, a = values[c]
                col = nanogui.Color(r, g, b, a)
                self.__setattr__(c, col)
                self.color_pickers[c].reset(col)
            else:
                raise RuntimeError("The key '{0}' was not provided.".format(s))


def numberPicker(parent, dynamicTheme, name):
    wrapper = nanogui.Widget(parent)
    wrapper.setLayout(nanogui.BoxLayout(nanogui.Orientation.Horizontal))
    nanogui.Label(wrapper, "{0} : ".format(name), "mono", 12).setFixedWidth(160)
    val = dynamicTheme.__getattribute__(name)
    if isinstance(val, float):
        box = nanogui.FloatBox(wrapper)
    else:
        box = nanogui.IntBox(wrapper)
    box.setValue(val)
    box.setSpinnable(True)
    box.setEditable(True)
    box.setDefaultValue(str(val))
    def set_value(v):
        dynamicTheme.__setattr__(name, v)
        dynamicTheme.screen.performLayout()
    box.setCallback(set_value)
    box.setFixedWidth(130)
    box.setFont("mono")

    dynamicTheme.number_pickers[name] = box

    reset = nanogui.Button(wrapper, "", nanogui.entypo.ICON_BACK)
    reset.setTooltip("Reset to NanoGUI Default?")
    def reset_cb():
        box.setValue(val)
        set_value(val)

    reset.setCallback(reset_cb)


class ExplicitColorPicker(nanogui.ColorPicker):
    MARKED_COLOR = None
    ALL_PICKERS = []

    def __init__(self, parent, color, callback):
        super(ExplicitColorPicker, self).__init__(parent, color)
        ExplicitColorPicker.ALL_PICKERS.append(self)
        popup = self.popup()
        self.marked = False

        # really dirty hack to fix the sizes of the buttons created by the parent
        for child in popup.children():
            if isinstance(child, nanogui.Button):
                child.setFixedWidth(180)

        wrapper = nanogui.Widget(popup)
        wrapper.setLayout(nanogui.GridLayout())

        def textColor(label, initValue):
            nanogui.Label(wrapper, label)
            box = nanogui.IntBox(wrapper, int(initValue * 255.0))
            box.setFixedWidth(80)
            box.setFont("mono")
            box.setMinValue(0)
            box.setMaxValue(255)
            box.setSpinnable(True)
            box.setEditable(True)
            return box

        self.redBox = textColor("Red : ", color.r)
        self.greenBox = textColor("Green : ", color.g)
        self.blueBox = textColor("Blue : ", color.b)
        self.alphaBox = textColor("Alpha : ", color.w)

        def red_cb(val):
            r = float(val) / 255.0
            g = float(self.greenBox.value()) / 255.0
            b = float(self.blueBox.value()) / 255.0
            a = float(self.alphaBox.value()) / 255.0
            self.reset(nanogui.Color(r, g, b, a), True)
        self.redBox.setCallback(red_cb)

        def green_cb(val):
            r = float(self.redBox.value()) / 255.0
            g = float(val) / 255.0
            b = float(self.blueBox.value()) / 255.0
            a = float(self.alphaBox.value()) / 255.0
            self.reset(nanogui.Color(r, g, b, a), True)
        self.greenBox.setCallback(green_cb)

        def blue_cb(val):
            r = float(self.redBox.value()) / 255.0
            g = float(self.greenBox.value()) / 255.0
            b = float(val) / 255.0
            a = float(self.alphaBox.value()) / 255.0
            self.reset(nanogui.Color(r, g, b, a), True)
        self.blueBox.setCallback(blue_cb)

        def alpha_cb(val):
            r = float(self.redBox.value()) / 255.0
            g = float(self.greenBox.value()) / 255.0
            b = float(self.blueBox.value()) / 255.0
            a = float(val) / 255.0
            self.reset(nanogui.Color(r, g, b, a), True)
        self.alphaBox.setCallback(alpha_cb)

        b = nanogui.Button(wrapper, "Darken 5%")
        b.setFont("sans")
        def darken_cb():
            curr = self.color()
            r = curr.r - (0.05 * curr.r)
            g = curr.g - (0.05 * curr.g)
            b = curr.b - (0.05 * curr.b)
            next_color = nanogui.Color(r, g, b, curr.w)
            self.master_callback(next_color)
            for child in self.popup().children():
                if isinstance(child, nanogui.Button) and child.caption() == "Pick":
                    child.setBackgroundColor(next_color)
                    child.setTextColor(next_color.contrastingColor())
                elif isinstance(child, nanogui.ColorWheel):
                    child.setColor(next_color)

        b.setCallback(darken_cb)

        b = nanogui.Button(wrapper, "Lighten 5%")
        b.setFont("sans")
        def lighten_cb():
            curr = self.color()
            r = curr.r + (0.05 * (1.0 - curr.r))
            g = curr.g + (0.05 * (1.0 - curr.g))
            b = curr.b + (0.05 * (1.0 - curr.b))
            next_color = nanogui.Color(r, g, b, curr.w)
            self.master_callback(next_color)
            for child in self.popup().children():
                if isinstance(child, nanogui.Button) and child.caption() == "Pick":
                    child.setBackgroundColor(next_color)
                    child.setTextColor(next_color.contrastingColor())
                elif isinstance(child, nanogui.ColorWheel):
                    child.setColor(next_color)

        b.setCallback(lighten_cb)

        self.cb = callback
        self.setCallback(lambda x: self.master_callback(x))
        def final_cb(color):
            if self.marked:
                ExplicitColorPicker.MARKED_COLOR = color
            self.master_callback(color)
        self.setFinalCallback(final_cb)

    def master_callback(self, color):
        self.cb(color)
        self.setBackgroundColor(color)
        self.setTextColor(self.color().contrastingColor())
        self.redBox.setValue(int(color.r * 255.0))
        self.greenBox.setValue(int(color.g * 255.0))
        self.blueBox.setValue(int(color.b * 255.0))
        self.alphaBox.setValue(int(color.w * 255.0))

    def reset(self, color, fromTextBox=False):
        self.master_callback(color)
        # Same as ColorPicker::setColor, only forcibly changes (no check for mPushed)
        fg = color.contrastingColor()
        self.setBackgroundColor(color)
        self.setTextColor(fg)
        for child in self.popup().children():
            if isinstance(child, nanogui.Button):
                change = True
                if fromTextBox and child.caption() == "Reset":
                    change = False
                if change:
                    child.setBackgroundColor(color)
                    child.setTextColor(fg)
            elif isinstance(child, nanogui.ColorWheel):
                # the color wheel
                child.setColor(color)

    def setMarked(self, marked):
        if marked:
            ExplicitColorPicker.MARKED_COLOR = self.color()
            self.marked = True
            self.setCaption("marked")
        else:
            ExplicitColorPicker.MARKED_COLOR = None
            self.marked = False
            self.setCaption("")

    @classmethod
    def mark(cls, picker):
        for p in ExplicitColorPicker.ALL_PICKERS:
            if p != picker:
                p.setMarked(False)
        picker.setMarked(not picker.marked)

    def mouseButtonEvent(self, p, button, down, modifiers):
        if down and button == nanogui.glfw.MOUSE_BUTTON_1:
            if modifiers == nanogui.glfw.MOD_SHIFT:
                ExplicitColorPicker.mark(self)
                return True
            elif modifiers == nanogui.glfw.MOD_CONTROL:
                if ExplicitColorPicker.MARKED_COLOR is not None:
                    self.reset(ExplicitColorPicker.MARKED_COLOR)
                else:
                    print("WTF")
                return True

        return super(ExplicitColorPicker, self).mouseButtonEvent(p, button, down, modifiers)


def colorPicker(parent, dynamicTheme, name):
    wrapper = nanogui.Widget(parent)
    wrapper.setLayout(nanogui.BoxLayout(nanogui.Orientation.Horizontal))
    nanogui.Label(wrapper, "{0} : ".format(name), "mono", 12).setFixedWidth(160)

    val = dynamicTheme.__getattribute__(name)
    def cp_func(color):
        dynamicTheme.__setattr__(name, color)
        dynamicTheme.screen.performLayout()
    cp = ExplicitColorPicker(wrapper, val, cp_func)
    cp.setFixedWidth(130)

    dynamicTheme.color_pickers[name] = cp

    reset = nanogui.Button(wrapper, "", nanogui.entypo.ICON_BACK)
    reset.setTooltip("Reset to NanoGUI Default?")
    # val is going to change with the color picker since the theme member
    # variable passed here is a reference (?), save the values now and create a
    # new color instance inside the callback
    r = val.r
    g = val.g
    b = val.b
    a = val.w
    def reset_cb():
        cp.reset(nanogui.Color(r, g, b, a))

    reset.setCallback(reset_cb)


def themeWindow(screen, dynamicTheme):
    window = nanogui.Window(screen, "Theme Settings")
    window.setLayout(nanogui.GroupLayout())
    window.setFixedSize((400, 425))

    tabWidget = nanogui.TabWidget(window)
    tabWidget.setFixedSize((400 - 30, 425 - 50))

    ####################################################################################
    # Font Sizes                                                                       #
    ####################################################################################
    layer = tabWidget.createTab("Sizes")
    vscroll = nanogui.VScrollPanel(layer)
    wrapper = nanogui.Widget(vscroll)
    wrapper.setLayout(nanogui.GroupLayout(5, 5, 5, 10))
    vscroll.setFixedSize((400 - 40, 425 - 80))

    wrapper.setLayout(nanogui.GroupLayout(5, 5, 5, 10))
    nanogui.Label(wrapper, "Font Sizes", "sans-bold")

    numberPicker(wrapper, dynamicTheme, "mStandardFontSize")
    numberPicker(wrapper, dynamicTheme, "mButtonFontSize")
    numberPicker(wrapper, dynamicTheme, "mTextBoxFontSize")
    numberPicker(wrapper, dynamicTheme, "mWindowFontSize")
    ####################################################################################
    # Curvature Sizes                                                                  #
    ####################################################################################
    nanogui.Label(wrapper, "Curvature Sizes", "sans-bold")
    numberPicker(wrapper, dynamicTheme, "mWindowCornerRadius")
    numberPicker(wrapper, dynamicTheme, "mWindowHeaderHeight")
    numberPicker(wrapper, dynamicTheme, "mWindowDropShadowSize")
    numberPicker(wrapper, dynamicTheme, "mButtonCornerRadius")
    ####################################################################################
    # TabWidget Sizes                                                                  #
    ####################################################################################
    nanogui.Label(wrapper, "TabWidget Sizes", "sans-bold")
    numberPicker(wrapper, dynamicTheme, "mTabBorderWidth")
    numberPicker(wrapper, dynamicTheme, "mTabInnerMargin")
    numberPicker(wrapper, dynamicTheme, "mTabMinButtonWidth")
    numberPicker(wrapper, dynamicTheme, "mTabMaxButtonWidth")
    numberPicker(wrapper, dynamicTheme, "mTabControlWidth")
    numberPicker(wrapper, dynamicTheme, "mTabButtonHorizontalPadding")
    numberPicker(wrapper, dynamicTheme, "mTabButtonVerticalPadding")
    ####################################################################################
    # Core Colors                                                                      #
    ####################################################################################
    layer = tabWidget.createTab("Colors")
    vscroll = nanogui.VScrollPanel(layer)
    wrapper = nanogui.Widget(vscroll)
    wrapper.setLayout(nanogui.GroupLayout(5, 5, 5, 10))
    vscroll.setFixedSize((400 - 40, 425 - 80))

    nanogui.Label(wrapper, "Help", "sans-bold")
    help_wrapper = nanogui.Widget(wrapper)
    help_wrapper.setLayout(nanogui.GroupLayout(5, 5, 5, 10))
    nanogui.Label(help_wrapper, "<shift + left click> : mark / un-mark color for copy")
    nanogui.Label(help_wrapper, "<ctrl + left click> : paste color (if one is marked)")

    nanogui.Label(wrapper, "Core Colors", "sans-bold")
    colorPicker(wrapper, dynamicTheme, "mDropShadow")
    colorPicker(wrapper, dynamicTheme, "mTransparent")
    colorPicker(wrapper, dynamicTheme, "mBorderDark")
    colorPicker(wrapper, dynamicTheme, "mBorderLight")
    colorPicker(wrapper, dynamicTheme, "mBorderMedium")
    colorPicker(wrapper, dynamicTheme, "mTextColor")
    colorPicker(wrapper, dynamicTheme, "mDisabledTextColor")
    colorPicker(wrapper, dynamicTheme, "mTextColorShadow")
    colorPicker(wrapper, dynamicTheme, "mIconColor")
    ####################################################################################
    # Button Colors                                                                    #
    ####################################################################################
    nanogui.Label(wrapper, "Button Colors", "sans-bold")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientTopFocused")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientBotFocused")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientTopUnfocused")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientBotUnfocused")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientTopPushed")
    colorPicker(wrapper, dynamicTheme, "mButtonGradientBotPushed")
    ####################################################################################
    # Tooltip Colors                                                                   #
    ####################################################################################
    nanogui.Label(wrapper, "Tooltip Colors", "sans-bold")
    numberPicker(wrapper, dynamicTheme, "mTooltipOpacity")
    colorPicker(wrapper, dynamicTheme, "mTooltipBackgroundColor")
    colorPicker(wrapper, dynamicTheme, "mTooltipTextColor")
    ####################################################################################
    # Window Colors                                                                    #
    ####################################################################################
    nanogui.Label(wrapper, "Window Colors", "sans-bold")
    colorPicker(wrapper, dynamicTheme, "mWindowFillUnfocused")
    colorPicker(wrapper, dynamicTheme, "mWindowFillFocused")
    colorPicker(wrapper, dynamicTheme, "mWindowTitleUnfocused")
    colorPicker(wrapper, dynamicTheme, "mWindowTitleFocused")
    colorPicker(wrapper, dynamicTheme, "mWindowHeaderGradientTop")
    colorPicker(wrapper, dynamicTheme, "mWindowHeaderGradientBot")
    colorPicker(wrapper, dynamicTheme, "mWindowHeaderSepTop")
    colorPicker(wrapper, dynamicTheme, "mWindowHeaderSepBot")
    colorPicker(wrapper, dynamicTheme, "mWindowPopup")
    colorPicker(wrapper, dynamicTheme, "mWindowPopupTransparent")

    return window


if __name__ == "__main__":
    nanogui.init()
    screen = CustomScreen((800, 700), title="NanoGUI Theme Builder")
    dynamicTheme = DynamicTheme(screen)
    window = themeWindow(screen, dynamicTheme)

    # make one with the custom theme (only so the popups go to the left, which is done
    # when ThemeChoice.Custom is given with makeCompareWindow, setTheme below overwrites)
    window = makeCompareWindow(screen, "Custom Theme", dynamicTheme)
    window.setPosition((405, 0))
    window.setTheme(dynamicTheme)

    nanogui.Label(window, "Copy to / Load from Clipboard", "sans-bold")
    wrapper = nanogui.Widget(window)
    layout = nanogui.AdvancedGridLayout([10, 0, 10, 0], [])
    layout.setColStretch(2, 1)
    wrapper.setLayout(layout)

    layout.appendRow(5) # some spacing
    layout.appendRow(0)
    # save results for C++ header
    b = nanogui.Button(wrapper, "   C++   ")
    b.setCallback(lambda: screen.setClipboardString(dynamicTheme.asCpp()))
    layout.setAnchor(b, nanogui.AdvancedGridLayout.Anchor(1, layout.rowCount()-1, 1, 1))

    # save results for python class
    b = nanogui.Button(wrapper, "Python")
    b.setCallback(lambda: screen.setClipboardString(dynamicTheme.asPython()))
    layout.setAnchor(b, nanogui.AdvancedGridLayout.Anchor(2, layout.rowCount()-1, 1, 1))

    # save results for JSON
    b = nanogui.Button(wrapper, "  JSON  ")
    b.setCallback(lambda: screen.setClipboardString(dynamicTheme.asJSON()))
    layout.setAnchor(b, nanogui.AdvancedGridLayout.Anchor(3, layout.rowCount()-1, 1, 1))

    layout.appendRow(5)
    layout.appendRow(0)
    b = nanogui.Button(wrapper, "Load JSON from Clipboard")
    def load_json():
        clip = screen.getClipboardString()
        try:
            data = json.loads(clip)
            dynamicTheme.loadFromJSON(data)
        except Exception as e:
            nanogui.MessageDialog(
                screen, nanogui.MessageDialog.Type.Warning, "Could not Load JSON",
                "Error parsing JSON from clipboard: {0}".format(e)
            )
    b.setCallback(load_json)
    layout.setAnchor(b, nanogui.AdvancedGridLayout.Anchor(1, layout.rowCount()-1, 3, 1))


    # let it rip
    screen.performLayout()
    screen.drawAll()
    screen.setVisible(True)
    nanogui.mainloop()
    del screen
    gc.collect()
    nanogui.shutdown()
