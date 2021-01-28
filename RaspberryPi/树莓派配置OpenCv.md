# 树莓派学习笔记-树莓派配置OpenCv

[TOC]

记录树莓派配置OpenCv的过程以及遇到的一些问题。

## 安装OpenCv相关包

```shell
#安装opencv相关工具
sudo apt-get install build-essential cmake git pkg-config
# 安装opencv图像工具包
sudo apt-get install libjpeg8-dev 
sudo apt-get install libtiff5-dev 
sudo apt-get install libjasper-dev 
sudo apt-get install libpng12-dev 
#安装视频I/O包
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#安装gtk2.0和优化函数包
sudo apt-get install libgtk2.0-dev
sudo apt-get install libatlas-base-dev gfortran
```

## 安装OpenCv

### 下载OpenCv源码

```shell
git clone https://github.com/opencv/opencv.git
```

### 安装OpenCv

```shell
#进入目录opencv下
cd opencv
#创建release文件夹
mkdir release
#进入目录release下
cd release
#cmake所有源文件并生成makefile
cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
-D CMAKE_INSTALL_PREFIX=/usr/local ..
#编译
sudo make
#安装
sudo make install
#更新动态链接库
sudo ldconfig
```

1. 在安装OpenCv的过程中，一定要下载OpenCv源码，否咋在编译的过程中会在不同的进度出现不同的报错（大部分是丢失文件）。
2. 编译过程长达数小时，一定要给树莓派充足的供电。

![编译成功](F:\Typora\本地图库\image-20210128220225416.png)

## 用Python的CV2库运行OpenCv

### 用cv2调用摄像头

```python
# -*- coding: utf-8 -*-

import cv2

cap = cv2.VideoCapture(0) # 打开摄像头
print("VideoCapture is opened?", cap.isOpened())

while(True):

    ret, frame = cap.read() # 读取摄像头图像
    cv2.imshow("frame", frame) # 显示图片

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() # 释放摄像头
cv2.destroyAllWindows() # 关闭所有窗口
```

#### 效果

桌面上弹出一个名为frame的窗口，窗口中为摄像头捕捉到的画面。

> 待解决：
>
> 这里似乎只有用远程桌面连接打开树莓派的桌面的时候才能够成功，如果是使用ssh访问，在WindowsTerminal中用命令行运行python程序则报错。

### 用cv2拍摄一段视频

```python
# -*- coding: utf-8 -*-
# 这一行代码解决不能输出中文的问题

import cv2
import time

interval = 0.1           # 捕获图像的间隔，单位：秒
num_frames = 60        # 捕获图像的总帧数
out_fps = 24            # 输出文件的帧率

# VideoCapture(0)表示打开默认的相机
cap = cv2.VideoCapture(0)

# 获取捕获的分辨率
size =(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# 设置要保存视频的编码，分辨率和帧率
video = cv2.VideoWriter(
    "time_lapse.avi", 
    cv2.VideoWriter_fourcc('M','P','4','2'), 
    out_fps, 
    size
)

# 对于一些低画质的摄像头，前面的帧可能不稳定，略过
for i in range(42):
    cap.read()

# 开始捕获，通过read()函数获取捕获的帧
try:
    for i in range(num_frames):
        _, frame = cap.read()
        video.write(frame)

        # 如果希望把每一帧也存成文件，比如制作GIF，则取消下面的注释
        # filename = '{:0>6d}.png'.format(i)
        # cv2.imwrite(filename, frame)

        print('Frame {} is captured.'.format(i))
        time.sleep(interval)
except KeyboardInterrupt:
    # 提前停止捕获
    print('Stopped! {}/{} frames captured!'.format(i, num_frames))

# 释放资源并写入视频文件
video.release()
cap.release()
```

在python的开头记得加上`# -*- coding: utf-8 -*-`这一行代码，可以解决无法显示汉语的问题。

#### 效果

运行python代码后，terminal会开始读秒，当截取完所有的帧数之后，会在桌面上生成命名为“time_lapse.avi”的视频文件。

## 参考文章

1. [树莓派安装Opencv3完整过程](https://blog.csdn.net/kyokozan/article/details/79192646)
2. [Opencv Github主页](https://github.com/opencv/opencv)
3. [模块cv2的用法](https://www.cnblogs.com/shizhengwen/p/8719062.html)