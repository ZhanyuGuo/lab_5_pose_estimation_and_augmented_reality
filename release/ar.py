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
        self.XY_ = np.array([axes_length, axes_length, 0, 1])
        self.XZ_ = np.array([axes_length, 0, axes_length, 1])
        self.YZ_ = np.array([0, axes_length, axes_length, 1])
        self.ZZ_ = np.array([axes_length, axes_length, axes_length, 1])

        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)
        pass

    def update(self, img, T, K, esimator, t1, t2, t3):
        ar_img = img
        if esimator.isEstimate:
            T_cw = la.inv(T)
            P = np.mat(K) * np.mat(T_cw)[0:3, :]
            uO_C = P * np.transpose(np.mat(self.origin_))
            uX_C = P * np.transpose(np.mat(self.X_))
            uY_C = P * np.transpose(np.mat(self.Y_))
            uZ_C = P * np.transpose(np.mat(self.Z_))
            # 正方体
            uXY_C = P * np.transpose(np.mat(self.XY_))
            uXZ_C = P * np.transpose(np.mat(self.XZ_))
            uYZ_C = P * np.transpose(np.mat(self.YZ_))
            uZZ_C = P * np.transpose(np.mat(self.ZZ_))

            uO_C = uO_C / uO_C[2][0]
            uX_C = uX_C / uX_C[2][0]
            uY_C = uY_C / uY_C[2][0]
            uZ_C = uZ_C / uZ_C[2][0]
            # 正方体
            uXY_C = uXY_C / uXY_C[2][0]
            uXZ_C = uXZ_C / uXZ_C[2][0]
            uYZ_C = uYZ_C / uYZ_C[2][0]
            uZZ_C = uZZ_C / uZZ_C[2][0]

            # 坐标系
            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uX_C[0]), int(uX_C[1])), self.red, 4)
            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uY_C[0]), int(uY_C[1])), self.green, 4)
            cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uZ_C[0]), int(uZ_C[1])), self.blue, 4)

            # # 正方体
            # cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uX_C[0]), int(uX_C[1])), self.green, 4)
            # cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uY_C[0]), int(uY_C[1])), self.green, 4)
            # cv2.line(ar_img, (int(uXY_C[0]), int(uXY_C[1])), (int(uX_C[0]), int(uX_C[1])), self.green, 4)
            # cv2.line(ar_img, (int(uXY_C[0]), int(uXY_C[1])), (int(uY_C[0]), int(uY_C[1])), self.green, 4)
            #
            # cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uZ_C[0]), int(uZ_C[1])), self.blue, 4)
            # cv2.line(ar_img, (int(uX_C[0]), int(uX_C[1])), (int(uXZ_C[0]), int(uXZ_C[1])), self.blue, 4)
            # cv2.line(ar_img, (int(uY_C[0]), int(uY_C[1])), (int(uYZ_C[0]), int(uYZ_C[1])), self.blue, 4)
            # cv2.line(ar_img, (int(uXY_C[0]), int(uXY_C[1])), (int(uZZ_C[0]), int(uZZ_C[1])), self.blue, 4)
            #
            # cv2.line(ar_img, (int(uZ_C[0]), int(uZ_C[1])), (int(uXZ_C[0]), int(uXZ_C[1])), self.red, 4)
            # cv2.line(ar_img, (int(uZ_C[0]), int(uZ_C[1])), (int(uYZ_C[0]), int(uYZ_C[1])), self.red, 4)
            # cv2.line(ar_img, (int(uZZ_C[0]), int(uZZ_C[1])), (int(uYZ_C[0]), int(uYZ_C[1])), self.red, 4)
            # cv2.line(ar_img, (int(uZZ_C[0]), int(uZZ_C[1])), (int(uXZ_C[0]), int(uXZ_C[1])), self.red, 4)

            t1 *= 1000
            t2 *= 1000
            t3 *= 1000
            t_cor = t2 - t1
            t_est = t3 - t2
            text_cor = "Match time(ms):    %d" % t_cor
            text_est = "Estimate time(ms): %d" % t_est
            cv2.putText(ar_img, text_cor, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.putText(ar_img, text_est, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

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
