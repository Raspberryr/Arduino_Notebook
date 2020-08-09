# Windows Termianl 基于SSH访问树莓派（SSH配置与JSON基本语法）

之前玩树莓派4B都是借助于显示屏利用图形界面来控制，但是因为暑假在家只有一台显示器，平时连接着笔记本电脑，每次想要调试都需要拔插HDMI线，很不方便；平时用SSH访问树莓派都是借助于putty，但是那个界面实在是太丑陋了，最近正巧又发现了Windows Terminal这个软件属实不错，可以集成各种终端，界面现代化，可定制程度高，于是想到能不能借助于SSH访问树莓派呢？

putty可以用SSH访问树莓派，Windows Terminal可以用SSH访问其他Linux系统，理论上应该是可以的。下午借助于Google，加上自己的不断调试，终于成功的用Windows Terminal 访问树莓派，写下这一篇博客来记录自己在这一过程中学到的新知识，以及出现的问题和问题的解决方案，供自己以后查阅以及互联网上的广大朋友们参考。

主要包括两部分的学习SSH配置以及JSON的基本语法规则整理。

> 为了方便记录，本文中操控树莓派使用的Terminal全部使用Windows Terminal完成，如图是连接成功后的界面。

![a7tF91.png](https://s1.ax1x.com/2020/08/09/a7tF91.png)


##  树莓派的SSH配置

树莓派开启ssh的方法有很多，在无桌面系统和有桌面系统的情况下都可以开启：

### 树莓派开启SSH

#### 无桌面系统开启ssh

将TF卡取下，在boot目录下建立文本文档，命名为ssh，去掉txt文件后缀，保存成纯文件格式。

树莓派通电开机之后，会自动打开ssh。这个ssh文件是临时文件，再次取下TF卡打开boot目录的话，文件会自动删除。

#### 有桌面系统开启ssh

1. 左面上左上角点击树莓派LOGO>首选项（Preferences）>Raspberry Pi Configuration>Interfaces>SSH 服务 点击Enable。ssh服务就已经打开。

2. 命令行输入 

   ```linux
   Pi@raspberry:~$ sudo rasp-config
   ```

   在“5 interfacing Options”选项中将“P2 SSH”enabled，Finish之后重启。这种方法也可以打开ssh服务。

### 设置树莓派固定IP

   用SSH登录树莓派有一个问题，因为我的树莓派是用Wlan直接连接上网的，所以每一次关机开机之后都有可能会改变IP地址，这样呼叫起来要每一次都打开Windows Terminal的设置文件修改，比较麻烦，所以这里我修改系统文件使树莓派用固定IP上网。

输入"ifconfig"可以查看树莓派的IP信息。

![a7YMlV.png](https://s1.ax1x.com/2020/08/09/a7YMlV.png)

输入sudo nano /etc/dhcpcd.conf，用vim编辑文件，拖到文件最下方之后在如图所示的地方，将#号去掉,并修改。

```
interface wlan0
static ip_address=192.168.1.107/24
static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.1.1
static domain_name_servers=192.168.0.1 8.8.8.8 fd51:42f8:caae:d92e::1
```

wlan0代表无线上网，ip_adress对应的是ip地址，routers代表网关地址。将ip地址和网关地址修改好，保存之后重启，ip地址就不再改变。

![a7tF91.png](https://s1.ax1x.com/2020/08/09/a7tF91.png)

## Windows Terminal配置

最近发现Windows Terminal这个软件，可以定制外观，集成了多个终端，确实是很不错。设置部分没有图形界面，需要靠修改JSON文件来完成。详细调理的设置规则可以参考官方的文档，已经写的很明白了，这里我只写我用到的部分。

> 官方GitHub连接
>
> [Windows Terminal setting 修改官方说明-Github](https://github.com/microsoft/terminal/blob/master/doc/user-docs/UsingJsonSettings.md)
>
> [Windows Terminal 官方文档-GitHub](https://github.com/microsoft/terminal)

### JSON

> JSON是JavaScript对象表示法（**J**ava**S**cript **O**bject **N**otation）

最近除去玩树莓派，还试着将Arduino的编程搬到了VScode上，于是就需要学习阅读JSON文件，恰巧Windows Terminal的设置是依靠JSON完成的，所以学习JSON可以同时服务于两个地方。这里我们只需呀用到简单的JSON规则即可。

#### json基本语法规则

- 数据在名称/值对中
- 数据由都好分割
- 对象放在大括号里
- 数组放在中括号里

#### setting.json 文件结构

```json
{
    "profiles":
    {
        "defaults":
        {
        },
        "list":
        [
        ]
    },
    "schemes": [
    ],
    "keybindings":
    [

    ]
}
```

可以看到,整个文档是一个对象,包含三个数组,profiles,schemes和keybindings  

其中profiles是环境的配置,这里默认已经加载了Powershell、cmd和Azure Cloudshell。如果你的系统中装有WSL，他也会自动检测到并且添加。除此之外，你还可以自定义终端，比如Git bash和我们今天用到的SSH远程服务器。

schemes可以设置配色方案，供以环境配置过程中调用。

keybindings则可以设置绑定快捷键。

除此之外，在第一层大括号里面可以添加全局属性。

> 具体的详细说明可以参考官方的：[Windows Terminal setting 修改官方说明-Github](https://github.com/microsoft/terminal/blob/master/doc/user-docs/UsingJsonSettings.md)

### SSH配置

```json
{
	"guid": "{99BA5433-DF5F-A898-C8E0-78B8BA55F251}",
    "hidden": false,
    "name": "RaspberryPi",
    "icon" : "F:\\WindowsTerminal\\Raspi-PGB001.webp",
    "commandline":"ssh pi@192.168.1.104 -p 22",
}
```

以我的配置为例：

- guid是全局唯一标识符，一定要是独一无二的，可以直接搜索在线guid生成得到一串数字。
- hidden决定是否隐藏该环境的入口，如果选择Ture，那么在下拉菜单中就找不到这个环境了。
- name是我们配置的环境的名字，这里要连接树莓派，就命名为RaspberryPi。
- icon配置图标，这里我使用的是图标的绝对路径。
- commandline是命令，这里用的是ssh的命令，pi是要访问的用户名，@后面是我分配给他的ip地址，-p表示访问的port ，22是ssh默认的port（如果你用Putty访问树莓派，选择ssh协议的默认端口也是22）

将这一部分添加上之后Ctrl+S，再打开下拉菜单就能够看到RaspberryPi环境已经被我们添加。

#### SSH访问树莓派

如果之前的配置全部都正确，没有填错或者漏掉什么步骤，那么打开环境之后稍等片刻，可以看到terminal跳数如下字样：

> Could not create directory 'C:\\Users\\\345\274\240\345\255\220\350\275\251/.ssh'.
> The authenticity of host '192.168.1.107 (192.168.1.107)' can't be established.
> ECDSA key fingerprint is SHA256:dSwGRWn8+5lTdmUcXLvrSbFxukMGX4hHP/r7clz3+64.
> Are you sure you want to continue connecting (yes/no)?

这里输入“**yes**”之后回车，会让你输入密码，输入树莓派的密码，默认的是raspberry，之后就出现Linux熟悉的命令行了。

## SSH过程中会出现的问题

在树莓派配置SSH的过程中可能会出现各种各样的问题，比如连接超时Connection Timeout和拒绝访问Connection refused。

### Connection Timeout

出现这个问题可能是在配置的过程中输错了什么地方或者是ssh配置没有开启等等，可以先用cmd文件ping一下对应的ip地址然后看一下能否正常连接，如果能够正常连接，那就是在Windows terminal的配置过程中出错，如果无响应，可能是ip地址已经更换或者是ssh没能成功开启。

### Connection refused

出现这个问题可能是三种情况：

1. ssh没有正常运行，可以重复之前的开启ssh的办法将他开启。
2. 端口22在监听。
3. 防火墙不允许port22进行ssh访问，在树莓派上可以用uwf更改防火墙的设置。

出现上述三种情况在网上有很多的解决的文章可以查阅，直接搜索之后按照对应的措施去修改基本上都能够成功解决。

## Windows Terminal的美化

完成配置之后可以根据个人喜好对Windows Terminal进行美化，同样是在JSON文件下进行修改，我是参考[少数派的文章](https://sspai.com/post/59380)进行修改的，对于不同的环境，设置了不同的背景，来区分各个环境，搞完之后看起来还是蛮漂亮的，这样调试起来心情也好。

## 结语

最终成功的在Windows Terminal上面运行了RaspberryPi，这个过程中了解了SSH协议，学习了一些JSON简单的语法，花费了一个下午，感觉收获还是蛮大的。下午一直都ping不到我的ip，找了各种办法无果快要放弃的时候发现原来只是自己的ip一直都打错了，真的是太迷糊了，前几天调试Arduino总是把正负极接反，最近可能是熬夜太多了哈哈哈。
