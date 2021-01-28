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