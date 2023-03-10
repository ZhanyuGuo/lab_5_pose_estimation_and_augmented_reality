#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19
# @Author  : Sitong Guo
# @Email   : czgst@tongji.edu.cn
# @File    : calibration.py
# @Software: PyCharm
import glob

import cv2
import numpy as np


def Camera_Cali():
    # 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

    # 获取标定板角点的位置
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点
    images = glob.glob("./Chessboards/*.jpg")
    for fname in images:
        img = cv2.imread(fname)
        cv2.imshow('image_ori', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
        print(ret)
        if ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            # print(corners2)
            if [corners2]:
                img_points.append(corners2)
            else:
                img_points.append(corners)

            cv2.drawChessboardCorners(img, (8, 6), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
            cv2.imshow('img_cali', img)
            cv2.waitKey(2000)
    print('\r\nimage数目:', len(img_points))
    cv2.destroyAllWindows()

    # 标定
    print("\r\n-----------------------------------------------------")
    print("标定相机所得参数:")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    print("ret:", ret)
    print("内参数矩阵 mtx:\r\n", mtx)  # 内参数矩阵
    print("畸变系数 dist:\r\n", dist)  # 畸变系数  distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    print("旋转向量 rvecs:\r\n", rvecs)  # 旋转向量 # 外参数
    print("平移向量 tvecs:\r\n", tvecs)  # 平移向量 # 外参数
    print("-----------------------------------------------------")


def main():
    Camera_Cali()


if __name__ == '__main__':
    main()
