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

    def update(self, img, T, K, esimator):
        ar_img = img
        if esimator.isEstimate:
            T_cw = la.inv(T)
            O_P = np.mat(K) * np.mat(T_cw)[0:3, :]
            X_P = np.mat(K) * np.mat(T_cw)[0:3, :]
            Y_P = np.mat(K) * np.mat(T_cw)[0:3, :]
            Z_P = np.mat(K) * np.mat(T_cw)[0:3, :]
            uO_C = O_P * np.transpose(np.mat(self.origin_))
            uX_C = X_P * np.transpose(np.mat(self.X_))
            uY_C = Y_P * np.transpose(np.mat(self.Y_))
            uZ_C = Z_P * np.transpose(np.mat(self.Z_))

            uO_C = uO_C / uO_C[2][0]
            uX_C = uX_C / uX_C[2][0]
            uY_C = uY_C / uY_C[2][0]
            uZ_C = uZ_C / uZ_C[2][0]

            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uX_C[0]), int(uX_C[1])), self.red, 4)
            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uY_C[0]), int(uY_C[1])), self.green, 4)
            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uZ_C[0]), int(uZ_C[1])), self.blue, 4)

        cv2.imshow('ar scene', ar_img)


if __name__ == '__main__':
    # ar = AR(25)  # 以mm为单位
    ar = AR(0.025)  # 以m为单位
    # T = np.array([[9.22302300e-01, 1.05540569e-01, - 3.71779041e-01, - 6.43524995e+02],
    #               [1.20225949e-01, 8.35901915e-01, 5.35549913e-01, - 5.26943255e+02],
    #               [3.67293055e-01, - 5.38636405e-01, 7.58265544e-01, 2.46028181e+03],
    #               [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    # T = np.array([[9.22302300e-01, 1.05540569e-01, - 3.71779041e-01, - 6.43524995e-01],
    #               [1.20225949e-01, 8.35901915e-01, 5.35549913e-01, - 5.26943255e-01],
    #               [3.67293055e-01, - 5.38636405e-01, 7.58265544e-01, 2.46028181e+00],
    #               [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    T = np.array([[0.96899591, -0.05974966, -0.23974343, 0.13307025],
                  [0.05289903, -0.89764998, 0.43752281, -0.23316665],
                  [-0.24134753, -0.43664, -0.86665846, 0.42967211],
                  [0., 0., 0., 1.]])

    K = np.array([[9.4880607969563971e+02, 0., 3.1950000000000000e+02],
                  [0., 9.4880607969563971e+02, 2.3950000000000000e+02],
                  [0., 0., 1.]])
    # print(T_wc)
    img = cv2.imread('../images/camera_03.jpg')
    ar.update(img, T, K)
