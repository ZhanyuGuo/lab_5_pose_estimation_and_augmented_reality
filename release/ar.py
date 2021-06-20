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
        ar_img = img
        # T_cw = la.inv(T)
        # xc = np.matmul(T_cw, self.X_[0])
        # yc = np.matmul(T_cw, self.X_[1])
        # zc = np.matmul(T_cw, self.X_[2])
        # Xc = np.array([xc, yc, 1])
        # U = np.matmul(K, Xc)
        # print(U)
        # U /= zc

        # gst
        # T_cw = la.inv(T)
        # X_C = np.matmul(T_cw, self.X_)
        # X_C = np.mat(X_C).I
        # print(X_C)
        # print(type(X_C))
        # X_C = np.array(X_C)
        #
        # XC_ = np.array([X_C[0][0], X_C[1][0], 1])
        # print(XC_)
        #
        # uX_C = np.matmul(K, XC_)
        # uX_C = np.mat(uX_C).I
        # print(uX_C)
        # uX_C = uX_C / uX_C[2][0]
        # print(uX_C)

        # T_cw = T
        # O_C = np.mat(T_cw) * np.transpose(np.mat(self.origin_))
        # X_C = np.mat(T_cw) * np.transpose(np.mat(self.X_))
        # Y_C = np.mat(T_cw) * np.transpose(np.mat(self.Y_))
        # Z_C = np.mat(T_cw) * np.transpose(np.mat(self.Z_))
        # print(O_C)
        # print(X_C)
        # print(type(X_C))
        # # 1.0
        # O_C = np.array(O_C)
        # X_C = np.array(X_C)
        # Y_C = np.array(Y_C)
        # Z_C = np.array(Z_C)
        #
        # OC_ = np.array([O_C[0][0], O_C[1][0], 1])
        # XC_ = np.array([X_C[0][0], X_C[1][0], 1])
        # YC_ = np.array([Y_C[0][0], Y_C[1][0], 1])
        # ZC_ = np.array([Z_C[0][0], Z_C[1][0], 1])
        # print(OC_)
        # print(XC_)
        # print(YC_)
        # print(ZC_)
        #
        # uO_C = np.mat(K) * np.transpose(np.mat(OC_))
        # uX_C = np.mat(K) * np.transpose(np.mat(XC_))
        # uY_C = np.mat(K) * np.transpose(np.mat(YC_))
        # uZ_C = np.mat(K) * np.transpose(np.mat(ZC_))
        # print(uO_C)
        # print(uX_C)
        # print(uY_C)
        # print(uZ_C)

        # 2.0
        # k = np.mat(np.zeros((3, 4)))
        # k[:, 0:3] = K
        # print(k)
        #
        # uO_C = k * O_C
        # uX_C = k * X_C
        # uY_C = k * Y_C
        # uZ_C = k * Z_C
        # print(uO_C)


        # 3.0
        T_cw = T
        O_P = np.mat(K) * np.mat(T_cw)[0:3, :]
        X_P = np.mat(K) * np.mat(T_cw)[0:3, :]
        Y_P = np.mat(K) * np.mat(T_cw)[0:3, :]
        Z_P = np.mat(K) * np.mat(T_cw)[0:3, :]
        print(O_P)
        print(X_P)
        print(type(X_P))

        uO_C = O_P *np.transpose(np.mat(self.origin_))
        uX_C = X_P *np.transpose(np.mat(self.X_))
        uY_C = Y_P *np.transpose(np.mat(self.Y_))
        uZ_C = Z_P *np.transpose(np.mat(self.Z_))

        print(uO_C)
        print(uX_C)
        print(uY_C)
        print(uZ_C)

        uO_C = uO_C / uO_C[2][0]
        uX_C = uX_C / uX_C[2][0]
        uY_C = uY_C / uY_C[2][0]
        uZ_C = uZ_C / uZ_C[2][0]
        print("\r\n输出像素点坐标：")
        print(uO_C)
        print(uX_C)
        print(uY_C)
        print(uZ_C)

        cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uX_C[0]), int(uX_C[1])), self.red, 4)
        cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uY_C[0]), int(uY_C[1])), self.green, 4)
        cv2.line(ar_img, (int(uO_C[0]), int(uO_C[1])), (int(uZ_C[0]), int(uZ_C[1])), self.blue, 4)
        cv2.imshow('drawline', ar_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # yc = np.matmul(T_cw, self.X_[1])
        # zc = np.matmul(T_cw, self.X_[2])
        # Xc = np.array([xc, yc, 1])
        # U = np.matmul(K, Xc)
        # print(U)
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


def getPixel(T_wc):
    T_cw = la.inv(T_wc)
    O_w = np.mat(np.zeros((4, 1)))
    O_w[3, 0] = 1
    X_w = np.mat(np.zeros((4, 1)))
    X_w[3, 0] = 1
    Y_w = np.mat(np.zeros((4, 1)))
    Z_w = np.mat(np.zeros((4, 1)))
    AR.X_


def main():
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
    T = np.array([[0.96628613, - 0.07172768, - 0.24727769, 0.15288598],
                  [0.05062464, - 0.88873362, 0.45562012, - 0.24048693],
                  [-0.25244457, - 0.45277775, - 0.85513979, 0.43578797],
                  [0., 0., 0., 1.]])
    K = np.array([[9.4880607969563971e+02, 0., 3.1950000000000000e+02],
                  [0., 9.4880607969563971e+02, 2.3950000000000000e+02],
                  [0., 0., 1.]])  # 初始化一个非奇异矩阵(数组)
    # print(T_wc)
    img = cv2.imread('C:/Users/87480/Desktop/test/camera_03.jpg')
    ar.update(img, T, K)


if __name__ == '__main__':
    main()
