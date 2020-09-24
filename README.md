# nanogui-customization-demo

[![Build Status Travis](https://travis-ci.org/svenevs/nanogui-customization-demo.svg?branch=master)](https://travis-ci.org/svenevs/nanogui-customization-demo)
[![Build status Appveyor](https://ci.appveyor.com/api/projects/status/5sxk8hvkcq0xgm5x?svg=true)](https://ci.appveyor.com/project/svenevs/nanogui-customization-demo)

# DANGER

This was a failed prototype, follow [mitsuba-renderer/nanogui #57](https://github.com/mitsuba-renderer/nanogui/issues/57) to know when custom theming is implemented.

THIS REPO IS STALE and only works off changes to the old wjakob/nanogui fork. The theme builder will not give you valid class definitions unless you're using the fork I have here, which is also stale!

# What is This?

This repository includes code demonstrating how to customize the [NanoGUI][nanogui]
theme, and embedding custom fonts and icon fonts.

**Overview**

- [Building the Code](#building-the-code)
- [Applications](#applications)
    - [Running the Applications](#running-the-applications)
    - [Custom Theme and Fonts](#custom-theme-and-fonts)
    - [Custom Icon Theme and Fonts](#custom-icon-theme-and-fonts)
    - [Theme Builder](#theme-builder)
    - [Example Fontawesome](#example-fontawesome)
- [License](#license)

# Building the Code

To run the example customizations found in this repository, first clone and build from
source:

```console
$ git clone --recursive https://github.com/svenevs/nanogui-customization-demo.git
$ cd nanogui-customization-demo/
$ mkdir build
$ cd build
```

## Linux / OSX

Generate a `Makefile` and build in parallel (`-j 4` says use four cores, you may also
run `make -j` to use all available cores).

```console
$ cmake ..
$ make -j 4
```

## Windows

Typically you will want to generate a Visual Studio project, making sure to generate a
64 bit project (the default is 32).  Run `cmake -G` to see the available generators, an
example for generating a Visual Studio 2015 64 bit build may look like

```console
$ cmake -G "Visual Studio 14 2015 Win64" ..
```

You can then either launch the visual studio project (`.sln` file), or run

```console
$ cmake --build . --config Release
```

# Applications

## Running the Applications

This repository was originally created to test modifications being made to NanoGUI with
respect to theme and font customization.  When the applications are built in some
``build`` directory, the results will look something like this:

```
build/
    bin/
        example1  example2  example3  example4  example_icons  # From NanoGUI
        custom_theme_and_fonts
        custom_icon_theme_and_fonts
    python/
        ...
        custom_theme_and_fonts.py
        custom_icon_theme_and_fonts.py
        theme_builder.py
    icons/
        icon1.png ...
```

The only reason this needs to be brought up is that the ``icons`` folder is searched for
via a hard-coded path to test the `nanogui::ImageView` widget.  For the C++
applications, run **from the build directory**:

```console
$ ./bin/custom_theme_and_fonts
```

For the Python applications, those files are all copied to the directory where the
NanoGUI python bindings are built.  Without changing `PYTHONPATH` or installing, you
need to run from the same directory as this library in order to `import nanogui`:

```console
$ cd python/
$ python3 theme_builder.py
```

## Custom Theme and Fonts

<p align="center">
  <img alt="custom theme and fonts" src="https://github.com/svenevs/nanogui-customization-demo/blob/master/resources/screens/custom_theme_and_fonts.png" />
</p>

> 👀 See the [documentation on customization](http://nanogui.readthedocs.io/en/latest/usage.html#customization)
> for more information!

The `bin/custom_theme_and_fonts` and `python/custom_theme_and_fonts.py` applications
use the `CustomTheme` class (defined in [`cpp/custom_theme.hpp`](cpp/custom_theme.hpp) /
[`python/custom_theme.py`](python/custom_theme.py)).  It shows how to load additional
font faces, set them as the theme defaults, and customize some of the default icons.

## Custom Icon Theme and Fonts

<p align="center">
  <img alt="custom icon theme and fonts" src="https://github.com/svenevs/nanogui-customization-demo/blob/master/resources/screens/custom_icon_theme_and_fonts.png" />
</p>

> 👀 See the [documentation on customization](http://nanogui.readthedocs.io/en/latest/usage.html#python)
> for more information!

The `bin/custom_icon_theme_and_fonts` and `python/custom_icon_theme_and_fonts.py`
applications use the `FontawesomeTheme` class (defined in
[`cpp/custom_theme.hpp`](cpp/custom_theme.hpp) /
[`python/custom_theme.py`](python/custom_theme.py)).  It shows how to load additional
icon font faces, as well as change the remaining icon related aspects of
`nanogui::Theme`.

## Theme Builder

<p align="center">
  <img alt="theme builder" src="https://github.com/svenevs/nanogui-customization-demo/blob/master/resources/screens/theme_builder_600.gif" />
</p>

From the `build` directory:

```console
$ cd python/
$ python3 theme_builder.py
```

The application helps visualize what colors affect which widgets.  For color
manipulations, use `<shift + left click>` to "mark" a color, and `<ctrl + left click>`
to "paste" the currently marked color.  This can be useful in conjunction with the
"Darken by 5%" and "Lighten by 5%" for differentiating in and out of focus colors.

When you are satisfied with the new colors and sizes, the `C++` and `Python` buttons
will populate your clipboard with a full class definition using the customizations you
have created.  Paste that into a source file to use in your project.

You can also use the `JSON` button to populate the clipboard with data as a temporary
save feature.  If you make changes that you do not like, simply
`Load JSON from Clipboard` to undo those changes.  Each C++ and Python class generated
includes a comment with the full JSON to allow for future tweaks.

**Note**: the theme builder application does not support customization of icons, nor
customization of default fonts.  See the source code for the above two applications for
how to customize default fonts / default icons etc.

## Example Fontawesome

The `bin/example_fontawesome` and `python/example_fontawesome.py` were generated by the
[nanogui-custom-font-generator](https://github.com/svenevs/nanogui-custom-font-generator)
utility.

# License

## Code in this Repository

**See the top of each file for the license**, there are two possible:

1. It was code taken directly from NanoGUI's
   [``example1.cpp``](https://github.com/wjakob/nanogui/blob/master/src/example1.cpp).
   The license at the top is NanoGUI's license.
2. The rest of the code such as ``CMakeLists.txt`` and everything else is CC0.  There's
   nothing special about this code, it came to fruition out of a need for testing.

## Font Awesome 5 Free

The generated [Font Awesome 5 Free][fontawesome] `fontawesome.ttf` font was generated
by using their (graciously hosted) raw SVG images.  So
[their license](resources/fontawesome/LICENSE) indicates that this is governed by
CC-BY-SA 4.0.

**NOTE**: if you want to use the existing generated
[`resources/fontawesome`](resources/fontawesome) utilities in your own repository, you
are more than welcome to _without_ attribution to this repository.  The license
information is already at the top of `fontawesome.h` and `constants_fontawesome.cpp`.
What you will need to do is provide attribution (e.g., in your `README.md`) clarifying
that the generated `fontawesome.ttf` is CC-BY-SA 4.0 as per their license.  It would
also be a good idea to track their `LICENSE` as done here as well.

## Membra Font

The [Membra][membra] font is governed by a
[CC-BY-SA 4.0 license](resources/membra/LICENSE).

## Spectral Font

The [Spectral][spectral] font is governed by the
[SIL Open Font License](resources/spectral/LICENSE).

## Spirax Font

The [Spirax][spirax] font is governed by the
[SIL Open Font License](resources/spirax/LICENSE).


[nanogui]:     https://github.com/wjakob/nanogui
[membra]:      https://www.fontsquirrel.com/fonts/membra
[spectral]:    https://fonts.google.com/specimen/Spectral
[spirax]:      https://fonts.google.com/specimen/Spirax
[fontawesome]: https://fontawesome.com/
