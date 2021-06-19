#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:51
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : estimator.py
# @Software: PyCharm

import cv2
import numpy as np
from my_utils import getRotateMatrix
from numpy import linalg as la


class Estimator(object):
    def __init__(self, K):
        self.K = K
        pass

    def findHomo(self, world_points, image_points):
        h_matrix, mask = cal_homography(world_points, image_points)
        return h_matrix, mask

    def estimate(self, h_matrix, K):
        T = calc_T(h_matrix, K)
        return T

    def pnpEstimate(self, src_pts, dst_pts, camera_matrix, dist_coeffs):
        rvec, tvec = pnp_estimation(src_pts, dst_pts, camera_matrix, dist_coeffs)
        rvec = np.degrees(rvec)
        R = getRotateMatrix(float(rvec[0]), float(rvec[1]), float(rvec[2]))
        # print(R)
        tmp = np.hstack((R, tvec))
        T = np.vstack((tmp, np.array([0, 0, 0, 1])))
        return T

    pass


def pnp_estimation(src_pts, dst_pts, camera_matrix, dist_coeffs):
    retval, rvec, tvec = cv2.solvePnP(src_pts, dst_pts, camera_matrix, dist_coeffs)
    return rvec, tvec


def cal_homography(src_pts, dst_pts):
    h_matrix = None
    mask = None
    if src_pts.any and dst_pts.any:
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return h_matrix, mask
    else:
        return h_matrix, mask


def r3_judge(r1, r2):
    # 确定r3
    r3_1 = np.cross(r1.T, r2.T)
    # print("r3_1:\r\n", r3_1)

    r12 = np.append(r1, r2, axis=1)
    R1 = np.append(r12, r3_1.T, axis=1)
    # print("R1:\r\n", R1)
    # print("R1行列式:", np.linalg.det(R1))

    r3_2 = np.cross(r2.T, r1.T)
    # print("r3_2:\r\n", r3_2)

    r12 = np.append(r1, r2, axis=1)
    R2 = np.append(r12, r3_2.T, axis=1)
    # print("R2:\r\n", R2)
    # print("R2行列式:", np.linalg.det(R2))

    R = np.mat(np.zeros((3, 3)))

    if round(np.linalg.det(R1)) == 1:
        R = R1
    elif round(np.linalg.det(R2)) == 1:
        R = R2

    return R, r12


def cal_lambda(r12, M_):
    # trace(R^T*M) = sigma(rij*mij)
    middle1 = np.array(r12) * np.array(M_)
    # print(middle1)

    # trace(M^T*M) = sigma(mij*mij)
    middle2 = np.array(M_) * np.array(M_)
    # print(middle2)

    nume = middle1.sum()
    # print(nume)
    demo = middle2.sum()
    # print(demo)

    scale = nume / demo
    return scale


def calc_T(H1, k):
    # Homography 输入
    # H1 = np.array([[4.09640840e-01, - 3.05868789e-02, 7.13250044e+01],
    #                [8.21634025e-02, 2.65324620e-01, 3.62846765e+01],
    #                [1.52533011e-04, - 2.16159793e-04, 1.00000000e+00]])
    # H2 = np.array([[4.09271902e-01, - 3.06034520e-02, 7.14371119e+01],
    #                [8.18744756e-02, 2.65426643e-01, 3.62511724e+01],
    #                [1.52130246e-04, - 2.16354490e-04, 1.00000000e+00]])

    # 相机标定K矩阵 输入
    # k = np.array([[9.4880607969563971e+02, 0., 3.1950000000000000e+02],
    #               [0., 9.4880607969563971e+02, 2.3950000000000000e+02],
    #               [0., 0., 1.]])  # 初始化一个非奇异矩阵(数组)
    K_ = np.linalg.inv(k)  # 对应于MATLAB中 inv() 函数

    M = np.mat(K_) * np.mat(H1)

    # print("Homography:\r\n", H1)
    # print("Camera Calibration:\r\n", K_)
    # print("\r\n计算M矩阵")
    # print("M:\r\n", M)

    M_ = M[:, :2]  # 取前两列
    # print("M_:\r\n", M_)

    # 进行SVD奇异值分解
    U, sigma, VT = la.svd(M_)

    # print("\r\n进行SVD奇异值分解")
    # print("U:\r\n", U)
    # print("sigma:\r\n", sigma)
    # print("VT:\r\n", VT)

    # print("\r\n计算R矩阵的前两列")
    U_ = U[:, :2]  # 取前两列
    R_ = np.mat(U_) * np.mat(VT)
    # print("R_*\r\n:", R_)

    r1 = R_[:, 0]
    r2 = R_[:, 1]
    # print("r1:", type(r1), "\r\n", r1)
    # print("r2:", type(r2), "\r\n", r2)

    R, r12 = r3_judge(r1, r2)
    # print("r12:", r12)
    # print("R:", R)

    # print("\r\n计算scale_lambda")
    r12 = np.append(r1, r2, axis=1)
    scale_lambda = cal_lambda(r12, M_)

    # print("scale_lambda:\r\n", scale_lambda)
    result = scale_lambda * M
    # print("lambda*M:\r\n", result)

    # print("\r\n计算转移矩阵T")
    r1_hat = result[:, 0]
    r2_hat = result[:, 1]
    t_hat = result[:, 2]
    R_hat, r12_hat = r3_judge(r1_hat, r2_hat)
    # print("R_hat:\r\n", R_hat)
    # print("t_hat:\r\n", t_hat)

    T = np.mat(np.zeros((4, 4)))
    # T[0:3, 0:3] = R_hat
    T[0:3, 0:3] = R
    T[0:3, -1] = t_hat
    T[3, 3] = 1
    # print("T:\r\n", T)
    return T
