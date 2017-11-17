# test repo for user fonts

```
$ git clone --recursive https://github.com/svenevs/nanogui-custom-font-demo.git
$ cd nanogui-custom-font-demo
$ mkdir build
$ cd build
$ cmake ..
$ make -j 4
```

See `src/my_theme.cpp`, toggle comment between `#include <nanogui_resources.{h,cpp}>`.
