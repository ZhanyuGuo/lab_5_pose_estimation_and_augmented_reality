#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 10:03
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : ar.py
# @Software: PyCharm
import numpy as np
from numpy import linalg as la
import cv2


class AR(object):
    def __init__(self, axes_length):
        self.axes_length_ = axes_length
        self.origin_ = np.array([0, 0, 0, 1])
        self.X_ = np.array([axes_length, 0, 0, 1])
        self.Y_ = np.array([0, axes_length, 0, 1])
        self.Z_ = np.array([0, 0, axes_length, 1])
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)
        pass

    def update(self, img, T, K):
        # ar_img = img
        # T_cw = la.inv(T)
        # xc = np.matmul(T_cw, self.X_[0])
        # yc = np.matmul(T_cw, self.X_[1])
        # zc = np.matmul(T_cw, self.X_[2])
        # Xc = np.array([xc, yc, 1])
        # U = np.matmul(K, Xc)
        # U /= zc

        # P = np.matmul(K, la.inv(T)[:3, ...])
        # o = np.matmul(P, self.origin_)
        # x = np.matmul(P, self.X_)
        # y = np.matmul(P, self.Y_)
        # z = np.matmul(P, self.Z_)
        # cv2.line(ar_img, (o[0], o[1]), (x[0], x[1]), self.red, 4)
        # cv2.line(ar_img, (o[0], o[1]), (y[0], y[1]), self.green, 4)
        # cv2.line(ar_img, (o[0], o[1]), (z[0], z[1]), self.blue, 4)
        # ar_img = img
        # add_zeros = np.zeros(3)
        # P = np.column_stack((la.inv(H), add_zeros))
        # o = np.matmul(P, self.origin_)
        # x = np.matmul(P, self.X_)
        # y = np.matmul(P, self.Y_)
        # # z = np.matmul(P, self.Z_)
        #
        # cv2.line(ar_img, (int(o[0]), int(o[1])), (int(x[0]), int(x[1])), self.red, 4)
        # cv2.line(ar_img, (int(o[0]), int(o[1])), (int(y[0]), int(y[1])), self.green, 4)
        # cv2.imshow("ar scene", ar_img)
        # cv2.waitKey(0)
        pass

    pass
