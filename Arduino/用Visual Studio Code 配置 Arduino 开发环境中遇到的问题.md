最近借助于Visual Studio Code的Arduino插件实现了用VScode来开发Arduino，安装插件以及配置的过程参考网上流传的教程很快就完成了，但是在实际编译的过程中，VScode会出现各种问题，虽然最终Arduino能够顺利的上传并且运行代码，但是提示诸多的Error实在是让强迫症难以忍受，遂花费一下午的时间借助Google整理了各种问题的解决方案，最终成功的消除了全部的Error。

于是我想写下这篇博客来记录这个过程，并且整理问题的解决方案以备以后查阅，也供所有在配置过程中遇到相同问题的人参考。

##  'cannot open source file "xxxx.h" (dependency of "xxxx.h")'

在选择编译之后报错：‘无法打开源文件“xxx.h”（依赖于“xxxx.h”）’，这是说明无法检测到头文件，解决方法是直接找到该文件的位置（可以使用Wox或者Everything之类的软件直接搜索），将路径粘贴在.vscode文件夹下面的c_cpp_properties.json文件的"includePath":[]中，例如我的路径为：

```json
"includePath": [
                "F:\\Arduino\\tools\\**",
                "F:\\Arduino\\hardware\\arduino\\avr\\**",
                "F:\\Arduino\\libraries",
                "F:\\Arduino\\hardware\\tools\\avr\\avr\\include",
                "F:\\Arduino\\libraries\\Servo\\src",
                "F:\\Arduino\\libraries\\Keypad\\src",
                "F:\\Arduino\\libraries\\Adafruit_SSD1306",
                "F:\\Arduino\\libraries\\Adafruit_GFX_Library",
                "F:\\Arduino\\hardware\tools\\avr\\avr\\include\\avr"
            ],
```

这个路径取决于每个人的Arduino安装位置以及libraries文件的储存位置，粘贴完之后重新编译上载，之前的报错就消失了。

## 未定义标识符“Serial”

> 产生这个的原因是头文件索引丢失，intelliSense不能自动找到必要的头文件路径。
>
> Currently，the VSCode Arduino extension leverages the C/C++ for Visual Studio Code for languages service and debugging.You can find the root cause and solutions from these links.
>
> [link]:http://github.com/Microsoft/vscode-arduino/wiki/FQA
>.

解决方法是手动配置头文件，在设置中强制intellisense使用Tag Parser，递归方式检索头文件。打开settings文件，加入

```json
"C_Cpp.intelliSenseEngineFallback":"Disabled",
"C_Cpp.intelliSenseEngine":"Tag Parser",
```

加入之后重新编译上载，报错消失。

## Exit with code = 1

出现这种情况会导致编译上载不成功，出现的可能有

1. 使用中文方式命名文件夹与文件，或者命名中存在空格
2. 代码中存在大小写的误用

解决的办法可以使用“_”下划线来代替“ ”空格，或者转移文件夹，确保路径中不存在中文文件夹。如此操作之后，报错消失。

如果是代码错误，则更正代码中的错误。

## 输出端汉语乱码

输出端汉语乱码的原因是编码方式不同导致的，因为VSCode的Arduino插件本身并不提供编译的IDE，需要调用我们下载的IDE，在1.8.7以后的Arduino IDE会出现编码乱码的情况，可以使用以下方法解决。

#### 更换IDE

因为VSCode要调用Arduino IDE来进行，将Arduino的IDE降级到1.8.7以前的版本就可以解决。


> [历史版本IDE百度云下载地址]:https://pan.baidu.com/s/1xAWW3ABFv7A2aM1wEsZgQQ
>
> 提取码：sal7

#### 改变IDE语言

Arduino IDE默认是系统的语言（我是汉语），如果更改输出的语言为English，那么就不存在输出端汉语乱码的情况。

#### 更改系统的编码格式

进行如下操作，打开Windows设置>时间与语言>语言>相关设置：日期、时间和区域格式设置>其他日期、时间和区域设置>区域：更改日期、时间或数字格式>管理>更改系统区域设置>勾选“Beta版：使用Unicode UTF-8 提供全球语言支持”>确认并且重启电脑

再次打开VSCode进行编译上载，乱码消失。

> 可能是因为三维建模软件对于汉语的支持并不是很好，题主在修改系统的编码格式之后无法启动Solidworks，每次都在加载注册表的时候闪退，不知道是否还有其他的软件存在这种情况，如果出现了，可能是因为改变了系统的编码格式导致的。

### 参考博客

[1]https://www.bilibili.com/read/cv3298341/

[2]https://www.arduino.cn/forum.php?mod=viewthread&tid=94607&highlight=vscode
